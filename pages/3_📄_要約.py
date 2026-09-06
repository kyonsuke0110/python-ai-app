import streamlit as st

from common.ui import setup_page, run_generation

setup_page("文章要約", "📄")

st.write("長い文章を貼り付けると、指定した長さ・形式で要約します。")

with st.form("summary_form"):
    source_text = st.text_area("要約したい文章", height=280, placeholder="ここに要約したい文章を貼り付けてください")

    col1, col2 = st.columns(2)
    with col1:
        length = st.selectbox("要約の長さ", ["一言（1文）", "短く（3〜4行）", "詳しく（段落でしっかり）"])
    with col2:
        style = st.selectbox("形式", ["箇条書き", "文章（段落）"])

    focus = st.text_input("特に重視したい観点（任意）", placeholder="例：結論と数値データを優先してまとめて")

    submitted = st.form_submit_button("要約する", type="primary", use_container_width=True)

if submitted:
    if not source_text.strip():
        st.error("要約したい文章を入力してください。")
    else:
        system_instruction = (
            "あなたは優秀な編集者です。与えられた文章の要点を正確に保ちながら、"
            "指定された長さと形式で日本語の要約を作成してください。"
            "元の文章にない情報を追加したり、事実を歪めたりしないでください。"
        )
        user_prompt = f"""以下の文章を要約してください。

# 要約対象の文章
{source_text}

# 要約の長さ
{length}

# 形式
{style}

# 重視したい観点
{focus or '指定なし。全体としてバランスよく'}
"""
        run_generation(system_instruction, user_prompt)
