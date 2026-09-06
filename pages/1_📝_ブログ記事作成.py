import streamlit as st

from common.ui import setup_page, run_generation

setup_page("ブログ記事作成", "📝")

st.write("テーマや条件を入力すると、見出し構成付きのブログ記事の下書きを生成します。")

with st.form("blog_form"):
    topic = st.text_input("記事のテーマ・タイトル案", placeholder="例：初心者向けNISAの始め方")
    audience = st.text_input("想定読者（任意）", placeholder="例：投資未経験の20代社会人")

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox(
            "文体・トーン",
            ["丁寧・解説調", "フレンドリー・親しみやすい", "専門的・硬め", "セールス寄り・訴求力重視"],
        )
    with col2:
        length = st.selectbox("文章量の目安", ["短め（600字程度）", "標準（1200字程度）", "長め（2000字程度）"])

    keywords = st.text_input("含めたいキーワード（任意・カンマ区切り）", placeholder="例：NISA, 積立, 少額投資")
    outline_request = st.text_area(
        "見出し構成の要望（任意）",
        placeholder="例：導入→NISAとは→メリット・デメリット→始め方の手順→まとめ",
        height=80,
    )

    submitted = st.form_submit_button("記事を生成", type="primary", use_container_width=True)

if submitted:
    if not topic.strip():
        st.error("記事のテーマを入力してください。")
    else:
        system_instruction = (
            "あなたはプロのブログライター兼編集者です。"
            "日本語で、読みやすく構成の整ったブログ記事を作成してください。"
            "Markdown形式の見出し（#, ##）を使い、導入・本文（複数の見出しに分割）・まとめの構成にしてください。"
            "誇張した表現や根拠のない断定は避けてください。"
        )
        user_prompt = f"""以下の条件でブログ記事を書いてください。

テーマ: {topic}
想定読者: {audience or '特に指定なし'}
文体・トーン: {tone}
文章量の目安: {length}
含めたいキーワード: {keywords or '指定なし'}
見出し構成の要望: {outline_request or '内容に合わせて自然に構成してください'}
"""
        run_generation(system_instruction, user_prompt)
