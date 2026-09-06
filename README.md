# 🖋️ AIライティングツール

ブログ執筆・メール返信・要約など、複数のライティング支援AIをひとつにまとめた個人用アプリです。
Streamlit のマルチページ機能と Gemini API で構築しています。

## 機能

| ページ | 内容 |
| --- | --- |
| 📝 ブログ記事作成 | テーマから見出し付きのブログ記事の下書きを生成 |
| 📧 メール返信作成 | 受信メールと返信の要点から返信文案を作成 |
| 📄 文章要約 | 長文を指定の長さ・形式で要約 |
| ✍️ 校正・リライト | 誤字脱字の修正、トーン・読みやすさの改善 |
| 🔄 トーン変換 | 丁寧・カジュアルなど別の口調に変換 |
| 💡 タイトル・見出し生成 | 記事内容から複数のタイトル案を生成 |
| 🌐 翻訳 | 自然な訳文への翻訳とニュアンス調整 |

## セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # .env に GEMINI_API_KEY を設定
```

APIキーは [Google AI Studio](https://aistudio.google.com/apikey) で取得できます。

## 起動

```bash
source .venv/bin/activate
streamlit run app.py
```

## 設定

| 変数 | 説明 |
| --- | --- |
| `GEMINI_API_KEY` | Gemini APIキー。未設定でもサイドバーから直接入力可能 |
| `GEMINI_MODEL` | 既定モデル（`gemini-flash-latest` など） |

`.env` の値は初期値として読み込まれ、サイドバーで変更した内容がそのブラウザセッション中は優先されます。
APIキーはセッション内にのみ保持され、ディスクには保存されません。

## 構成

```
app.py                 ホーム画面（機能一覧のカードグリッド）
pages/N_絵文字_名前.py    機能ごとのページ。先頭の数字がサイドバーの並び順
common/ui.py           サイドバー・APIキー管理・生成実行の共通処理
common/gemini_client.py google-genai SDK のラッパー（ストリーミング生成）
```

新しい機能を追加する場合は `pages/` に同じ命名規則でファイルを作り、`app.py` の `features` リストに追加してください。

## 備考

個人用の単一ユーザー向けツールのため、認証機能とデータベースは意図的に実装していません。
