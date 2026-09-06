"""Gemini API呼び出しの薄いラッパー。"""

import time

from google import genai
from google.genai import errors, types

_RETRYABLE_CODES = {429, 503}
_MAX_RETRIES = 3
_INITIAL_BACKOFF_SECONDS = 2.0


def build_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)


def stream_text(
    client: genai.Client,
    model: str,
    system_instruction: str,
    user_prompt: str,
    temperature: float = 0.7,
):
    """Gemini からテキストをストリーミングで取得するジェネレータ。

    Streamlit の st.write_stream にそのまま渡せる。
    モデルの一時的な高負荷（429/503）は、まだ何も出力していない場合に限り
    自動的にリトライする。
    """
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=temperature,
    )
    backoff = _INITIAL_BACKOFF_SECONDS
    for attempt in range(_MAX_RETRIES):
        yielded_any = False
        try:
            response = client.models.generate_content_stream(
                model=model,
                contents=user_prompt,
                config=config,
            )
            for chunk in response:
                if chunk.text:
                    yielded_any = True
                    yield chunk.text
            return
        except errors.APIError as e:
            is_last_attempt = attempt == _MAX_RETRIES - 1
            if yielded_any or e.code not in _RETRYABLE_CODES or is_last_attempt:
                raise
            time.sleep(backoff)
            backoff *= 2
