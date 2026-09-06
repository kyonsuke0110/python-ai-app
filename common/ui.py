"""各ページ共通のサイドバー・APIキー管理・生成実行まわりのヘルパー。"""

import os

import streamlit as st
from dotenv import load_dotenv
from google.genai import errors

from common.gemini_client import build_client, stream_text

load_dotenv()

MODEL_OPTIONS = [
    "gemini-flash-latest",
    "gemini-pro-latest",
    "gemini-flash-lite-latest",
]
DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", MODEL_OPTIONS[0])


def setup_page(title: str, icon: str) -> None:
    st.set_page_config(page_title=f"{title} | AIライティングツール", page_icon=icon, layout="wide")
    _render_sidebar()
    st.title(f"{icon} {title}")


def _render_sidebar() -> None:
    with st.sidebar:
        st.header("⚙️ 設定")

        if "api_key" not in st.session_state:
            st.session_state.api_key = os.environ.get("GEMINI_API_KEY", "")
        st.session_state.api_key = st.text_input(
            "Gemini APIキー",
            value=st.session_state.api_key,
            type="password",
            help="環境変数 GEMINI_API_KEY（.env）から自動読込されます。未設定ならここに直接入力してください。",
        )

        if "model" not in st.session_state:
            st.session_state.model = DEFAULT_MODEL if DEFAULT_MODEL in MODEL_OPTIONS else MODEL_OPTIONS[0]
        st.session_state.model = st.selectbox(
            "モデル",
            options=MODEL_OPTIONS,
            index=MODEL_OPTIONS.index(st.session_state.model),
        )

        st.divider()
        st.caption(
            "個人用ツールのためデータベース・認証は使用していません。"
            "APIキーはこのブラウザセッション内でのみ保持され、ディスクには保存されません。"
        )


def get_client_and_model():
    api_key = st.session_state.get("api_key")
    if not api_key:
        st.warning("サイドバーに Gemini APIキーを入力してください。")
        st.stop()
    client = build_client(api_key)
    model = st.session_state.get("model", DEFAULT_MODEL)
    return client, model


def run_generation(system_instruction: str, user_prompt: str, temperature: float = 0.7) -> str | None:
    """生成を実行し、ストリーミング表示した上で最終テキストを返す。失敗時はNone。"""
    client, model = get_client_and_model()
    try:
        with st.spinner("生成中..."):
            return st.write_stream(
                stream_text(client, model, system_instruction, user_prompt, temperature)
            )
    except errors.APIError as e:
        if e.code in (429, 503):
            st.error(
                f"「{model}」に現在アクセスが集中しています。"
                "少し時間をおいて再度お試しいただくか、サイドバーで別のモデル"
                "（例: gemini-flash-lite-latest）に切り替えてください。"
            )
        else:
            st.error(f"Gemini APIの呼び出しでエラーが発生しました: {e.code} {e.status}\n{e.message}")
        return None
