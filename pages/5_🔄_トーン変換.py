import streamlit as st

from common.ui import setup_page, run_generation

setup_page("トーン変換", "🔄")

st.write("文章はそのままに、口調・トーンだけを変換します。SNS投稿の言い換えなどにも使えます。")

with st.form("tone_form"):
    source_text = st.text_area("変換したい文章", height=220)

    target_tone = st.selectbox(
        "変換先のトーン",
        [
            "フォーマル・ビジネス調",
            "カジュアル・友人向け",
            "丁寧語（ですます調）",
            "フレンドリー・親しみやすい",
            "自信のある・力強い",
            "共感的・柔らかい",
            "簡潔・端的",
        ],
    )
    extra_note = st.text_input("追加の指示（任意）", placeholder="例：絵文字は使わないで")

    submitted = st.form_submit_button("変換する", type="primary", use_container_width=True)

if submitted:
    if not source_text.strip():
        st.error("文章を入力してください。")
    else:
        system_instruction = (
            "あなたは文章のトーン調整を専門とするライターです。"
            "元の文章が伝えたい内容・情報は変えずに、指定されたトーンだけを変えて書き直してください。"
        )
        user_prompt = f"""以下の文章を「{target_tone}」のトーンに変換してください。

追加の指示: {extra_note or 'なし'}

# 対象の文章
{source_text}
"""
        run_generation(system_instruction, user_prompt)
