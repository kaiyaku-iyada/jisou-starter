#!/usr/bin/env bash
# セッション開始時に、計画の要点と台帳の末尾を自動で読み込ませる
echo "=== 今日: $(date '+%Y-%m-%d %a %H:%M') ==="
if [ -f README.md ]; then echo "--- README.md（先頭40行）"; head -40 README.md; fi
if [ -f LEDGER.md ]; then echo "--- LEDGER.md（末尾25行）"; tail -25 LEDGER.md; fi
LAST=$(ls ops/day*.md 2>/dev/null | sort | tail -1)
if [ -n "$LAST" ]; then echo "--- 直近の指示書: $LAST"; head -30 "$LAST"; fi
echo "--- 次にやること: 人間の報告を台帳に記録 → 判断ルールを照らす → 今日の成果物 → ops/dayNN.md"
