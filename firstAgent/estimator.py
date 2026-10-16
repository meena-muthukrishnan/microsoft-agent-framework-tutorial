"""Core forecasting engine: step graph -> low/expected/worst token + cost range."""
from __future__ import annotations
from dataclasses import dataclass, field
from .pricing import get_price, CREDIT_RATES, USD_PER_CREDIT


def count_tokens(text: str, tokenizer: str = "o200k_base") -> int:
    """Exact-ish count via tiktoken if installed, else ~4 chars/token fallback."""
    try:
        import tiktoken
        return len(tiktoken.get_encoding(tokenizer).encode(text))
    except Exception:
        return max(1, len(text) // 4)


@dataclass
class Step:
    name: str
    model: str = "medium-model"
    prompt: str = ""                  # prompt template text for this step
    expected_output_tokens: int = 300
    max_output_tokens: int = 1000     # worst-case ceiling (the max_tokens setting)
    tool_result_tokens: int = 0       # tokens returned by tools/retrieval into context
    retries: int = 0                  # worst-case extra attempts
    carries_context: bool = True      # does this step see earlier outputs?
    kind: str = "llm"                 # "llm" or a CREDIT_RATES key for credit-billed steps


def _cost(model: str, tin: int, tout: int) -> float:
    p = get_price(model)
    return tin / 1e6 * p["input"] + tout / 1e6 * p["output"]


def forecast_flow(steps: list[Step], system_prompt: str = "", user_input: str = "") -> dict:
    """Forecast each step, with context accumulating across steps."""
    base_ctx = count_tokens(system_prompt) + count_tokens(user_input)
    carried_expected = 0   # outputs + tool results accumulated so far (expected)
    carried_worst = 0
    rows, tot = [], {"low": 0.0, "expected": 0.0, "worst": 0.0}
    tok = {"low": 0, "expected": 0, "worst": 0}

    for s in steps:
        if s.kind != "llm":  # credit-billed step (low-code platforms)
            credits = CREDIT_RATES.get(s.kind, 0)
            usd = credits * USD_PER_CREDIT
            worst_credits = credits * (1 + s.retries)
            rows.append({"step": s.name, "model": s.kind, "credits": credits,
                         "cost_low": usd, "cost_expected": usd,
                         "cost_worst": worst_credits * USD_PER_CREDIT})
            for k, v in (("low", usd), ("expected", usd), ("worst", worst_credits * USD_PER_CREDIT)):
                tot[k] += v
            continue

        own = count_tokens(s.prompt, get_price(s.model)["tokenizer"])
        ctx_e = carried_expected if s.carries_context else 0
        ctx_w = carried_worst if s.carries_context else 0
        in_e = base_ctx + own + ctx_e + s.tool_result_tokens
        in_w = base_ctx + own + ctx_w + s.tool_result_tokens
        out_low = int(s.expected_output_tokens * 0.6)
        out_exp = s.expected_output_tokens
        out_worst = s.max_output_tokens
        attempts_worst = 1 + s.retries

        low = _cost(s.model, in_e, out_low)
        exp = _cost(s.model, in_e, out_exp)
        worst = _cost(s.model, in_w, out_worst) * attempts_worst

        rows.append({"step": s.name, "model": s.model,
                     "input_tokens": in_e,
                     "output_tokens_low": out_low, "output_tokens_expected": out_exp,
                     "output_tokens_worst": out_worst,
                     "cost_low": round(low, 6), "cost_expected": round(exp, 6),
                     "cost_worst": round(worst, 6)})
        tot["low"] += low; tot["expected"] += exp; tot["worst"] += worst
        tok["low"] += in_e + out_low
        tok["expected"] += in_e + out_exp
        tok["worst"] += (in_w + out_worst) * attempts_worst

        # context grows for later steps
        carried_expected += out_exp + s.tool_result_tokens
        carried_worst += out_worst + s.tool_result_tokens

    total_exp = tot["expected"] or 1e-12
    for r in rows:
        r["share_of_expected_cost_pct"] = round(100 * r["cost_expected"] / total_exp, 1)
    top = max(rows, key=lambda r: r["cost_expected"])["step"] if rows else None
    return {
        "steps": rows,
        "total_tokens": tok,
        "total_cost_usd": {k: round(v, 6) for k, v in tot.items()},
        "most_expensive_step": top,
        "note": "Input tokens are counted; output tokens are predicted. Treat as a range.",
    }


def steps_from_dicts(items: list[dict]) -> list[Step]:
    return [Step(**i) for i in items]


def what_if_swap_model(steps: list[Step], step_name: str, new_model: str,
                       system_prompt: str = "", user_input: str = "") -> dict:
    before = forecast_flow(steps, system_prompt, user_input)
    swapped = [Step(**{**s.__dict__, "model": new_model}) if s.name == step_name else s
               for s in steps]
    after = forecast_flow(swapped, system_prompt, user_input)
    b, a = before["total_cost_usd"]["expected"], after["total_cost_usd"]["expected"]
    return {"before_expected_usd": b, "after_expected_usd": a,
            "saving_pct": round(100 * (b - a) / b, 1) if b else 0.0,
            "after": after}


def compare_actual(forecast: dict, actual_tokens: int, actual_cost_usd: float) -> dict:
    exp_t = forecast["total_tokens"]["expected"]
    exp_c = forecast["total_cost_usd"]["expected"]
    return {
        "token_variance_pct": round(100 * (actual_tokens - exp_t) / exp_t, 1) if exp_t else None,
        "cost_variance_pct": round(100 * (actual_cost_usd - exp_c) / exp_c, 1) if exp_c else None,
        "within_forecast_range": actual_cost_usd <= forecast["total_cost_usd"]["worst"],
    }


def check_budget(forecast: dict, budget_usd: float) -> dict:
    t = forecast["total_cost_usd"]
    status = "ok" if t["worst"] <= budget_usd else ("at_risk" if t["expected"] <= budget_usd else "over_budget")
    return {"status": status, "budget_usd": budget_usd, **t,
            "action": {"ok": "Run automatically.",
                       "at_risk": "Expected cost fits but worst case breaches: cap max tokens or require approval.",
                       "over_budget": "Block or require approval; consider a cheaper model or trimming context."}[status]}
