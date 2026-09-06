# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal (single-user, no auth/DB) AI writing tool built with Streamlit and the Gemini API. It bundles several writing assistants (blog drafting, email replies, summarization, proofreading/rewriting, tone conversion, title generation, translation) as pages of one Streamlit multipage app.

## Commands

Setup (first time / new environment):
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then set GEMINI_API_KEY inside
```

Run the app:
```bash
source .venv/bin/activate
streamlit run app.py
```

There is no lint or test suite configured in this repo.

## Architecture

- `app.py` — Home page. Calls `setup_page()` and renders a card grid linking to each page via `st.page_link`.
- `pages/N_<emoji>_<name>.py` — One file per feature. Streamlit's native multipage routing uses the filename's leading number for sidebar ordering, so new features should follow the existing `N_emoji_name.py` pattern to slot into the nav correctly.
- `common/ui.py` — Shared logic every page uses instead of duplicating boilerplate:
  - `setup_page(title, icon)`: sets page config and renders the sidebar (API key input + model selectbox), backed by `st.session_state["api_key"]` / `st.session_state["model"]` so settings persist across page navigation within a browser session but are never written to disk.
  - `get_client_and_model()`: builds a `genai.Client` from the session API key, or calls `st.stop()` if none is set.
  - `run_generation(system_instruction, user_prompt, temperature=0.7)`: the single entry point pages use to call Gemini — streams the response into the page via `st.write_stream` and returns the final text.
- `common/gemini_client.py` — Thin wrapper around the `google-genai` SDK (`stream_text`) that turns a `generate_content_stream` call into a plain text generator consumable by `st.write_stream`.

### Adding a new feature page

Each page follows the same shape: `setup_page(...)` → a `st.form` collecting inputs → on submit, build a `system_instruction` (role/constraints for Gemini) and a `user_prompt` (the actual task filled in with form values) → `run_generation(system_instruction, user_prompt)`. Follow this pattern rather than introducing a different structure, and add the new page to the `features` list in `app.py` so it appears on the home screen.

### Configuration

- `GEMINI_API_KEY` and `GEMINI_MODEL` are read from `.env` (via `python-dotenv`) as defaults, but can be overridden per-session from the sidebar — the sidebar value always wins once set. Available models are the hardcoded `MODEL_OPTIONS` list in `common/ui.py`.
- No database, no authentication — this is intentional for a personal single-user tool; do not add either without being asked.
