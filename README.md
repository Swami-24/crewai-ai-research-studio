# AI Research Studio — CrewAI

A Streamlit web app based on the CrewAI notebook. It uses:
- **Senior Research Analyst** agent with Serper web search
- **Content Writer** agent to produce a Markdown blog with source links
- Gemini through CrewAI/LiteLLM
- Streamlit interface with report display and Markdown download

## Run locally

Python 3.10–3.12 is recommended for smoother compatibility with AI packages.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Create `.streamlit/secrets.toml` locally:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
SERPER_API_KEY = "your_serper_api_key"
```

Never commit `secrets.toml` or expose API keys in screenshots, logs, or source code.

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository and upload `app.py`, `requirements.txt`, and `README.md`.
2. Open https://share.streamlit.io/ and deploy the repository.
3. Set the main file path to `app.py`.
4. In the deployed app's **Settings → Secrets**, add:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
SERPER_API_KEY = "your_serper_api_key"
```

5. Save and reboot/redeploy the app.

## Important

- The default model identifier in the app is `gemini/gemini-2.5-flash`. If your Gemini account or CrewAI/LiteLLM version does not support it, change it in the app's Advanced settings to a currently supported model identifier.
- Gemini API and Serper usage may incur charges or have quotas.
- AI outputs and citations must be checked before academic or public use.
