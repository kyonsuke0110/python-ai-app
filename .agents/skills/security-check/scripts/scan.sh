#!/usr/bin/env bash
# 機械的に確認できる項目だけを集めて出力する読み取り専用スクリプト。
# 何も変更せず、何もインストールせず、ネットワークにも出ない（pip-audit が
# 既に入っている場合のみ、その脆弱性DB照会が発生する）。
# 出力はそのまま読んで解釈する前提。判断はスキル本体側で行う。

set -uo pipefail
ROOT="${1:-.}"
cd "$ROOT" || { echo "対象ディレクトリが開けません: $ROOT"; exit 1; }

sec() { printf '\n===== %s =====\n' "$1"; }
none() { echo "  (該当なし)"; }

# .venv / .git / エージェント用ツール類（.agents, .claude）はアプリ本体ではないので除外する。
# ここを除外しないと、スキル自身のスクリプトを検出して結果がノイズだらけになる。
PRUNE=(-name .venv -prune -o -name .git -prune -o -name node_modules -prune -o -name __pycache__ -prune -o -name .agents -prune -o -name .claude -prune -o -name '*-workspace' -prune)
pyfiles() { find . "${PRUNE[@]}" -o -type f -name '*.py' -print; }
textfiles() { find . "${PRUNE[@]}" -o -type f \( -name '*.py' -o -name '*.md' -o -name '*.toml' -o -name '*.json' -o -name '*.yaml' -o -name '*.yml' -o -name '*.txt' -o -name '*.sh' -o -name '*.env*' \) -print; }

echo "対象: $(pwd)"
echo "実行: $(date '+%Y-%m-%d %H:%M:%S')"

sec "1. 秘密情報を含みうるファイルの所在"
for f in .env .env.local .streamlit/secrets.toml secrets.toml; do
  [ -f "$f" ] && echo "  存在: $f (perm $(stat -f '%Sp' "$f" 2>/dev/null || stat -c '%A' "$f" 2>/dev/null))"
done
[ -f .env.example ] && { echo "  存在: .env.example — 中身:"; sed 's/^/      /' .env.example; }

sec "2. .gitignore による除外状況"
if [ -f .gitignore ]; then
  for pat in '.env' 'secrets.toml'; do
    if grep -qF "$pat" .gitignore; then echo "  OK: '$pat' を含む行あり"; else echo "  ★未除外: .gitignore に '$pat' の記載なし"; fi
  done
else
  echo "  ★.gitignore が存在しない"
fi

sec "3. git 管理状況（秘密ファイルが追跡・コミットされていないか）"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "  git リポジトリです"
  tracked=$(git ls-files | grep -E '(^|/)(\.env($|\.)|secrets\.toml$)' || true)
  if [ -n "$tracked" ]; then echo "  ★追跡中の秘密ファイル:"; echo "$tracked" | sed 's/^/      /'; else echo "  OK: .env / secrets.toml は追跡されていない"; fi
  hist=$(git log --all --oneline --name-only -- '.env' '*.env' '**/secrets.toml' 2>/dev/null | head -20 || true)
  if [ -n "$hist" ]; then echo "  ★履歴に登場（過去コミットに残存の可能性）:"; echo "$hist" | sed 's/^/      /'; else echo "  OK: 履歴にも見当たらない"; fi
  echo "  リモート: $(git remote -v | head -2 | tr '\n' ' ' || echo なし)"
else
  echo "  git リポジトリではありません（コミット経由の漏洩リスクは現時点でなし）"
fi

sec "4. コード・ドキュメント中にベタ書きされた鍵らしき文字列"
# Google API キー(AIza...), OpenAI(sk-...), 汎用の代入形
hits=$(textfiles | xargs grep -nE 'AIza[0-9A-Za-z_-]{30,}|sk-[A-Za-z0-9]{20,}|(api[_-]?key|token|secret|password)[[:space:]]*[=:][[:space:]]*["'"'"'][^"'"'"'{}$]{16,}["'"'"']' 2>/dev/null | grep -v '\.env:' || true)
if [ -n "$hits" ]; then echo "$hits" | sed 's/^/  ★/'; else none; fi

sec "5. Streamlit 設定（公開範囲・XSRF・静的配信）"
if [ -f .streamlit/config.toml ]; then sed 's/^/  /' .streamlit/config.toml; else echo "  .streamlit/config.toml なし（すべて既定値）"; fi
echo "  --- 起動コマンドにアドレス指定が埋まっていないか ---"
addr=$(textfiles | xargs grep -nE 'server\.address|0\.0\.0\.0|--server\.port|enableCORS|enableXsrfProtection|enableStaticServing|ngrok|cloudflared' 2>/dev/null || true)
if [ -n "$addr" ]; then echo "$addr" | sed 's/^/  /'; else echo "  (公開方向の設定・記述は見当たらない)"; fi

sec "6. モデル出力・ユーザー入力の危険なレンダリング/実行"
r=$(pyfiles | xargs grep -nE 'unsafe_allow_html[[:space:]]*=[[:space:]]*True|components\.html|\beval\(|\bexec\(|subprocess\.|os\.system|pickle\.loads|yaml\.load\(' 2>/dev/null || true)
if [ -n "$r" ]; then echo "$r" | sed 's/^/  ★/'; else echo "  OK: unsafe_allow_html / eval / exec / subprocess の使用なし"; fi

sec "7. ディスクへの書き出し・ログ出力（「保存しない」の主張と一致するか）"
w=$(pyfiles | xargs grep -nE '\bopen\([^)]*[\"'"'"']([wa]|r\+)|to_csv|to_json|json\.dump\(|logging\.(info|debug|warning|error)|\.write_text\(|\.writelines\(|st\.cache_resource|persist=' 2>/dev/null || true)
if [ -n "$w" ]; then echo "$w" | sed 's/^/  /'; else echo "  OK: ファイル書き込み・ログ出力は見当たらない"; fi

sec "8. 外部から貼り付けたテキストがプロンプトに入る箇所"
echo "  --- 入力ウィジェット ---"
pyfiles | xargs grep -nE 'st\.(text_area|text_input|file_uploader|chat_input)\(' 2>/dev/null | sed 's/^/  /' || none
echo "  --- プロンプト組み立て（f文字列への埋め込み）---"
pyfiles | xargs grep -nE 'user_prompt|system_instruction' 2>/dev/null | grep -E '=|\{' | sed 's/^/  /' | head -40 || none

sec "9. 依存パッケージ"
[ -f requirements.txt ] && { echo "  --- requirements.txt ---"; sed 's/^/    /' requirements.txt; }
unpinned=$(grep -cE '>=|~=|\*|^[a-zA-Z0-9_.-]+$' requirements.txt 2>/dev/null || echo 0)
echo "  バージョン未固定の行数: $unpinned （再現性・供給網リスクの目安）"
PIP=""
for c in ./.venv/bin/pip .venv/bin/pip pip3 pip; do command -v "$c" >/dev/null 2>&1 && { PIP="$c"; break; }; done
if [ -n "$PIP" ]; then
  echo "  --- 実際にインストールされている版 ($PIP) ---"
  "$PIP" list 2>/dev/null | grep -iE 'streamlit|google-genai|dotenv|protobuf|requests|tornado|urllib3|jinja2|pillow' | sed 's/^/    /'
else
  echo "  pip が見つからず、インストール済み版を確認できません"
fi
AUDIT=""
for c in ./.venv/bin/pip-audit .venv/bin/pip-audit pip-audit; do command -v "$c" >/dev/null 2>&1 && { AUDIT="$c"; break; }; done
if [ -n "$AUDIT" ]; then
  echo "  --- pip-audit ---"
  "$AUDIT" 2>&1 | tail -30 | sed 's/^/    /'
else
  echo "  pip-audit 未導入のため既知CVEの自動照合はスキップ（導入するなら: .venv/bin/pip install pip-audit）"
fi

sec "スキャン完了"
echo "★ が付いた行は要確認。ただし最終的な重大度判定はスキル本体の基準で行うこと。"
