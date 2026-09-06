import streamlit as st

from common.ui import setup_page, run_generation

setup_page("校正・リライト", "✍️")

st.write("文章の誤字脱字チェックや、より自然・丁寧・簡潔な表現へのリライトを行います。")

with st.form("proofread_form"):
    source_text = st.text_area("校正・リライトしたい文章", height=250)

    mode = st.selectbox(
        "モード",
        [
            "誤字脱字・文法チェックのみ（最小限の修正）",
            "より自然な日本語にリライト",
            "よりフォーマル・丁寧な表現にリライト",
            "より簡潔にリライト（要点を保って短く）",
        ],
    )
    show_diff_notes = st.checkbox("修正した箇所の説明も付けてほしい", value=True)

    submitted = st.form_submit_button("実行", type="primary", use_container_width=True)

if submitted:
    if not source_text.strip():
        st.error("文章を入力してください。")
    else:
        system_instruction = (
            "あなたはプロの日本語校正者・編集者です。与えられた文章を指定モードに沿って修正してください。"
            "元の文意や意図は変えないでください。"
        )
        note_instruction = (
            "修正後の文章を出力したあと、区切り線を挟んで「## 主な修正点」として"
            "変更箇所を箇条書きで簡潔に説明してください。"
            if show_diff_notes
            else "修正後の文章のみを出力してください。説明は不要です。"
        )
        user_prompt = f"""以下の文章を「{mode}」の方針で修正してください。

{note_instruction}

# 対象の文章
{source_text}
"""
        run_generation(system_instruction, user_prompt)
