import streamlit as st

from common.ui import setup_page, run_generation

setup_page("メール返信作成", "📧")

st.write("受信したメールの本文と、返信で伝えたい要点を入力すると、返信文案を作成します。")

with st.form("email_form"):
    original_mail = st.text_area("受信したメール本文", height=200, placeholder="相手から届いたメールをそのまま貼り付けてください")
    intent = st.text_area(
        "返信で伝えたいこと・要点",
        height=120,
        placeholder="例：来週の打ち合わせ日程は火曜14時でOK。資料は前日までに送ると伝えたい。",
    )

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox(
            "トーン",
            ["ビジネス・フォーマル", "丁寧だが柔らかい", "カジュアル・親しい相手向け", "謝罪・お詫びを含む"],
        )
    with col2:
        language = st.selectbox("返信の言語", ["日本語", "英語"])

    submitted = st.form_submit_button("返信文を生成", type="primary", use_container_width=True)

if submitted:
    if not intent.strip():
        st.error("返信で伝えたい要点を入力してください。")
    else:
        system_instruction = (
            "あなたは優秀なビジネスアシスタントです。"
            "与えられた受信メールの文脈と、返信したい要点をもとに、"
            "自然で失礼のない返信メールの本文を作成してください。"
            "件名は変更せず、本文のみを出力してください。挨拶・結びの言葉も適切に含めてください。"
        )
        user_prompt = f"""以下の情報をもとに返信メールを作成してください。

# 受信したメール本文
{original_mail or '（受信メールの提示なし。要点のみから返信を作成してください）'}

# 返信で伝えたい要点
{intent}

# トーン
{tone}

# 言語
{language}
"""
        run_generation(system_instruction, user_prompt)
