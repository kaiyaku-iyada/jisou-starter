#!/usr/bin/env bash
# Claude Code の SessionStart フックから呼ばれる。標準出力がそのままAIの文脈に入る。
# 計画の要点・今日が何日目か・README.md に無い項目・台帳の集計と直近の数字・直近の指示書・記憶の目次を出す。
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/..}" || exit 0
echo "=== 今日: $(date '+%Y-%m-%d %H:%M') ==="

# Day と残り日数（README.md の「開始: YYYY-MM-DD」「期限: YYYY-MM-DD」から計算）
if [ -f README.md ] && command -v python3 >/dev/null 2>&1; then
python3 - <<'PY'
import re, datetime
s = open('README.md', encoding='utf-8').read()
a = re.search(r'開始[:：]\s*(\d{4}-\d{2}-\d{2})', s)
b = re.search(r'期限[:：]\s*(\d{4}-\d{2}-\d{2})', s)
if not (a and b):
    print('=== Day を計算できない: README.md に「開始: YYYY-MM-DD」「期限: YYYY-MM-DD」を書く ===')
else:
    t = datetime.date.today()
    day = (t - datetime.date.fromisoformat(a.group(1))).days + 1
    left = (datetime.date.fromisoformat(b.group(1)) - t).days
    if day < 1:
        print(f'=== 開始前（開始まであと{1 - day}日）===')
    elif left < 0:
        print(f'=== Day {day} ／ 期限を{-left}日過ぎている。台帳を締める ===')
    else:
        print(f'=== Day {day} ／ 残り{left}日（Day = 今日 − 開始日 + 1、残り = 期限日 − 今日）===')
PY
fi

for f in README.md LEDGER.md; do
  [ -f "$f" ] || echo "!!! $f が無い: templates/$f を $f にコピーして《》を埋める"
done
# 未記入の《》
LEFT=$(grep -l '《[^》]' CLAUDE.md README.md LEDGER.md memory/*.md 2>/dev/null | tr '\n' ' ')
if [ -n "$LEFT" ]; then
  echo "!!! 未記入の《》が残っている: $LEFT"
  echo "    README.md から決まるものはAIが埋める。決まらないものだけ ops/dayNN.md の「人間への質問」で1問ずつ聞く（「なぜ」は聞けなければ「未取得」でよい）"
fi
# README.md に要る項目（見出しか「- 項目」で始まる行。型は templates/README.md）。無ければ CLAUDE.md の既定値で進める
if [ -f README.md ]; then
  MISS=""
  while IFS='|' read -r name pat; do
    grep -Eq "^(#+ |[-*] )($pat)" README.md || MISS="$MISS『$name』"
  done <<'EOF'
目標|目標|目的
判定|判定
制約|制約
作り方の方式|作り方の方式
指標の定義|指標の定義
定型行|定型行
話者とAI開示|話者とAI開示
数字画像を作る日|数字画像
判断ルールの単位と定義|単位と定義
EOF
  if [ -n "$MISS" ]; then
    echo "!!! README.md に${MISS}が無い。CLAUDE.md の既定値で進める"
    echo "    CLAUDE.md の「README.md に無いときの既定値」に従い、使った値を README.md に書き足して、LEDGER.md の「決定事項」に1行残す"
  fi
fi

if [ -f README.md ]; then
  echo "--- README.md（冒頭）"; head -12 README.md
  echo "--- README.md（判断ルール）"; awk '/^## 判断ルール/{p=1; next} /^## /{p=0} p && NF' README.md
fi
if [ -f LEDGER.md ]; then
  echo "--- LEDGER.md（集計）"; awk '/^## 集計/{p=1; next} /^## /{p=0} p && /^\|/' LEDGER.md
  echo "--- LEDGER.md（日次の直近5行）"
  awk '/^## 日次/{d=1; next} /^## /{d=0} d && /^\|/{r[++n]=$0} END{for(i=1;i<=n;i++) if(i<=2 || i>n-5) print r[i]}' LEDGER.md
  echo "--- LEDGER.md（決定事項の直近3行）"
  awk '/^## 決定事項/{d=1; next} /^## /{d=0} d && /^\|/{r[++n]=$0} END{for(i=3;i<=n;i++) if(i>n-3) print r[i]}' LEDGER.md
fi
LAST=$(ls ops/day*.md 2>/dev/null | sort | tail -1)
if [ -n "$LAST" ]; then echo "--- 直近の指示書: $LAST"; head -30 "$LAST"; fi
if [ -f memory/MEMORY.md ]; then echo "--- memory/MEMORY.md（記憶の目次。関係するものだけ開く）"; cat memory/MEMORY.md; fi
echo "--- 次にやること: 人間の報告を台帳に記録 → 判断ルールを照らす → 今日の成果物 → ops/dayNN.md → 投稿文と商品文をスクリプトで確認"
