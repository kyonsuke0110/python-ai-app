import streamlit as st

from common.ui import setup_page

setup_page("AIライティングツール", "🖋️")

st.write(
    "ブログ執筆・メール返信・要約など、複数のライティング支援AIを"
    "ひとつにまとめた個人用ツールです。左のサイドバーからGemini APIキーを設定し、"
    "使いたい機能のページを開いてください。"
)

st.divider()

features = [
    ("pages/1_📝_ブログ記事作成.py", "📝", "ブログ記事作成", "テーマから見出し付きのブログ記事の下書きを生成します。"),
    ("pages/2_📧_メール返信.py", "📧", "メール返信作成", "受信メールと返信の要点から、返信文案を作成します。"),
    ("pages/3_📄_要約.py", "📄", "文章要約", "長文を指定の長さ・形式で要約します。"),
    ("pages/4_✍️_校正リライト.py", "✍️", "校正・リライト", "誤字脱字の修正や、文章のトーン・読みやすさを改善します。"),
    ("pages/5_🔄_トーン変換.py", "🔄", "トーン変換", "文章を丁寧・カジュアル・フォーマットなど別の口調に変換します。"),
    ("pages/6_💡_タイトル生成.py", "💡", "タイトル・見出し生成", "記事内容から複数のタイトル案・見出し案を生成します。"),
    ("pages/7_🌐_翻訳.py", "🌐", "翻訳", "自然な訳文への翻訳とニュアンス調整を行います。"),
]

cols = st.columns(2)
for i, (page, icon, name, desc) in enumerate(features):
    with cols[i % 2]:
        with st.container(border=True):
            st.subheader(f"{icon} {name}")
            st.caption(desc)
            st.page_link(page, label=f"{name}を開く", icon=icon)

st.divider()
st.caption("個人用ツールのため、ログイン機能やデータベースは実装していません。生成内容はブラウザセッション内にのみ保持されます。")
