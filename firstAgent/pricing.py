"""Pricing + credit catalog.

IMPORTANT: the numbers below are ILLUSTRATIVE PLACEHOLDERS (USD per 1M tokens).
Replace them with your real contract/list prices before trusting any forecast.
"""

# model -> (input_per_1m, output_per_1m, tokenizer_hint)
MODEL_PRICING = {
    "small-model":  {"input": 0.15, "output": 0.60,  "tokenizer": "o200k_base"},
    "medium-model": {"input": 3.00, "output": 15.00, "tokenizer": "o200k_base"},
    "large-model":  {"input": 15.00, "output": 75.00, "tokenizer": "o200k_base"},
}

# For low-code tools billed in credits instead of tokens (e.g. Copilot Studio).
# Map an action type -> credits per execution. PLACEHOLDERS: fill from your licence docs.
CREDIT_RATES = {
    "generative_answer": 2,
    "agent_action": 5,
    "classic_answer": 1,
}
USD_PER_CREDIT = 0.01  # placeholder


def get_price(model: str) -> dict:
    if model not in MODEL_PRICING:
        raise KeyError(f"Unknown model '{model}'. Known: {list(MODEL_PRICING)}")
    return MODEL_PRICING[model]
