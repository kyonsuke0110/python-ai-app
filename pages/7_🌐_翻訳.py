import streamlit as st

from common.ui import setup_page, run_generation

setup_page("翻訳", "🌐")

st.write("文章を自然な訳文に翻訳します。直訳ではなく、文脈に合った自然な表現を優先します。")

with st.form("translate_form"):
    source_text = st.text_area("翻訳したい文章", height=220)

    col1, col2 = st.columns(2)
    with col1:
        target_lang = st.selectbox(
            "翻訳先の言語",
            ["英語", "日本語", "中国語（簡体字）", "韓国語", "スペイン語", "フランス語", "ドイツ語"],
        )
    with col2:
        register = st.selectbox("文体", ["自然な標準表現", "ビジネス・フォーマル", "カジュアル・口語"])

    submitted = st.form_submit_button("翻訳する", type="primary", use_container_width=True)

if submitted:
    if not source_text.strip():
        st.error("翻訳したい文章を入力してください。")
    else:
        system_instruction = (
            "あなたはプロの翻訳者です。逐語訳ではなく、意味と文脈を保った自然な訳文を作成してください。"
            "訳文のみを出力し、余計な前置きや説明は不要です。"
        )
        user_prompt = f"""以下の文章を{target_lang}に翻訳してください。文体は「{register}」でお願いします。

# 原文
{source_text}
"""
        run_generation(system_instruction, user_prompt)
