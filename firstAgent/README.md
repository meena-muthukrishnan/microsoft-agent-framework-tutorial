# Token & Cost Forecaster Agent

Microsoft Agent Framework agent that forecasts tokens/cost per step BEFORE an AI workflow runs.

## Files
- `forecaster/estimator.py`  forecast engine (tested): per-step low/expected/worst, what-if, budget gate, actual-vs-forecast
- `forecaster/pricing.py`    price + credit catalog (PLACEHOLDER numbers, replace with real ones)
- `tools.py`                 5 agent tools
- `main.py`                  agent + Foundry hosting entrypoint
- `sample_flow.json`, `test_engine.py`  demo flow and quick test (`python test_engine.py`)

## Deploy (Foundry hosted agent)
1. Scaffold from Microsoft's basic Agent Framework sample so you get the right manifest/Dockerfile:
   `azd ai agent init -m "https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/01-basic/agent.manifest.yaml"`
2. Copy `main.py`, `tools.py`, `forecaster/`, `requirements.txt` into the generated agent source folder (replace its agent file).
3. Set `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_MODEL_DEPLOYMENT_NAME`.
4. Run locally (serves on http://localhost:8088), then `azd deploy`.
5. Test in the Foundry playground, e.g. paste `sample_flow.json` and ask for a forecast with a 5 cent budget.

Check import names in `main.py` against the sample you scaffolded; the framework is evolving.

