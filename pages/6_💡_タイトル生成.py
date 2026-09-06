import streamlit as st

from common.ui import setup_page, run_generation

setup_page("タイトル・見出し生成", "💡")

st.write("記事の内容やテーマから、タイトル・見出しの候補を複数生成します。")

with st.form("title_form"):
    content = st.text_area(
        "記事の内容・テーマ・要約",
        height=200,
        placeholder="記事本文を貼り付けるか、テーマ・要点を箇条書きで入力してください",
    )

    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox(
            "スタイル",
            ["SEOを意識した検索されやすいタイトル", "クリックしたくなるキャッチーなタイトル", "シンプルで分かりやすいタイトル", "問いかけ形式のタイトル"],
        )
    with col2:
        count = st.slider("生成する候補数", min_value=3, max_value=15, value=8)

    max_length = st.number_input("最大文字数の目安（0で指定なし）", min_value=0, max_value=100, value=32, step=1)

    submitted = st.form_submit_button("タイトル案を生成", type="primary", use_container_width=True)

if submitted:
    if not content.strip():
        st.error("記事の内容・テーマを入力してください。")
    else:
        length_note = f"各タイトルは日本語で{max_length}文字程度以内に収めてください。" if max_length else "文字数の制限は特にありません。"
        system_instruction = (
            "あなたは編集者・コピーライターです。与えられた記事内容から、"
            "読者の興味を引くタイトル案を複数考えてください。"
            "誇大広告的な誤解を招く表現は避けてください。"
        )
        user_prompt = f"""以下の記事内容から、タイトル案を{count}個、番号付きの箇条書きで出力してください。

スタイル: {style}
{length_note}

# 記事内容
{content}
"""
        run_generation(system_instruction, user_prompt)
