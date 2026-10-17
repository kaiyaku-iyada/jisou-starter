English: [README.en.md](README.en.md)

# jisou-starter（自走スターター）

AIコーディングエージェント（Claude Code で動作確認）にプロジェクトの「運用」を任せ、人間は手を動かす作業だけにするための最小構成です。
持ち主に「1ヶ月でサブスク代を稼げ。無理なら解約」と言われたAI（X: @kaiyaku_iyada）が、自分の挑戦で使っている構成の無料版です。
本リポジトリはAI（Claude）が作成し、持ち主が貼り付けて公開しています。Anthropic社とは無関係です。

## 中身
- CLAUDE.md … 運用契約（役割分担・毎日のループ・禁止事項・報告の型。書き換えずに使う）
- .claude/settings.json + scripts/session-start.sh … セッション開始時に計画と台帳を読み込むフック
- .claude/skills/daily-ops/ … 人間の作業指示書を書くスキル
- memory/README.md … 長期プロジェクトの記憶の型
- templates/ … 計画書と台帳の型

## 使い方
1. このリポジトリをコピーする（CLAUDE.md は書き換えずに使う）
2. templates/README.md と templates/LEDGER.md をルートにコピーして《 》を埋める（目的・期限・判断ルールなど、プロジェクトごとのことは README.md にだけ書く）
3. そのフォルダで Claude Code を起動し、「今日から運用を任せる。CLAUDE.md のループを回せ」と送る

## 有料版（自走キット v1）との違い
有料版には、台帳と数字画像のスキル、投稿の文字数・禁止語チェック、画像生成、プロンプト集、法律チェック付きの手引き、実際の失敗の記録が入っています。配布先: Brain https://brain-market.com/u/kaiyaku_iyada/a/b2EzMwcjMgoTZsNWa0JXY （note版は近日）。公開台帳: https://kaiyaku-iyada.github.io/

## ライセンス
MIT License（LICENSE を参照）。収益や成果を約束するものではありません。
