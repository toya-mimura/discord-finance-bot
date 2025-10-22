# 📊 Stock Market Daily Report Bot

GitHub ActionsとDiscord Webhookを使用して、主要な市場指標を毎日自動配信するボットです。

## 🎯 機能

以下の市場データを日次で取得し、Discordチャンネルに投稿します：

- 💱 **ドル円** (JPY=X)
- 📈 **日経平均** (^N225)
- 🇺🇸 **S&P500** (^GSPC)
- 📊 **VIX指数** (^VIX) - 恐怖指数

各指標について、以下の情報を表示：
- 現在値
- 前日比の変動額
- 前日比の変動率（%）

## 🏗️ アーキテクチャ

```
GitHub Actions (Cron)
    ↓
Python + yfinance (データ取得)
    ↓
Discord Webhook (配信)
```

### 技術スタック

- **実行環境**: GitHub Actions
- **言語**: Python 3.11
- **データ取得**: yfinance (Yahoo Finance API)
- **配信**: Discord Webhook
- **スケジューリング**: GitHub Actions Cron trigger

## 📁 プロジェクト構成

```
stock-market-bot/
├── .github/
│   └── workflows/
│       └── daily-report.yml    # GitHub Actionsワークフロー
├── src/
│   └── main.py                 # メインスクリプト
├── requirements.txt            # Python依存関係
└── README.md                   # このファイル
```

## 🚀 セットアップ方法

### 1. リポジトリのクローン

```bash
git clone https://github.com/[YOUR_USERNAME]/stock-market-bot.git
cd stock-market-bot
```

### 2. Discord Webhook URLの取得

1. Discordで投稿したいチャンネルの設定を開く
2. 「連携サービス」→「ウェブフック」を選択
3. 「新しいウェブフック」をクリック
4. ウェブフック名を設定（例: "Market Bot"）
5. 「ウェブフックURLをコピー」をクリック

### 3. GitHub Secretsの設定

1. GitHubリポジトリの「Settings」タブを開く
2. 「Secrets and variables」→「Actions」を選択
3. 「New repository secret」をクリック
4. 以下を入力：
   - **Name**: `DISCORD_WEBHOOK_URL`
   - **Secret**: コピーしたWebhook URL
5. 「Add secret」をクリック

### 4. 動作確認

1. リポジトリの「Actions」タブを開く
2. 「Daily Market Report」ワークフローを選択
3. 「Run workflow」ボタンで手動実行
4. Discordチャンネルにメッセージが届くか確認

## ⏰ 実行スケジュール

- **実行タイミング**: 日本時間 平日午前9時（月〜金）
- **Cron式**: `0 0 * * 1-5` (UTC 0:00 = JST 9:00)

### スケジュールのカスタマイズ

`.github/workflows/daily-report.yml`の`cron`を編集：

```yaml
schedule:
  # 毎日午前9時（日本時間）
  - cron: '0 0 * * *'
  
  # 平日の午前9時と午後6時
  - cron: '0 0,9 * * 1-5'
```

## 💻 ローカルでの開発・テスト

### 環境構築

```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化（Windows）
venv\Scripts\activate

# 仮想環境の有効化（Mac/Linux）
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt
```

### ローカル実行

```bash
# 環境変数を設定
export DISCORD_WEBHOOK_URL="your_webhook_url_here"

# スクリプト実行
python src/main.py
```

## 📝 使用しているライブラリ

| ライブラリ | バージョン | 用途 |
|-----------|-----------|------|
| yfinance | 0.2.66 | Yahoo Financeからのデータ取得 |
| requests | 2.31.0 | Discord WebhookへのHTTPリクエスト |
| pytz | 2024.1 | タイムゾーン処理（JST変換） |

## ⚠️ 注意事項

- **データの遅延**: yfinanceのデータはリアルタイムではなく、若干の遅延があります
- **市場休場日**: 休場日はデータが取得できない可能性があります
- **利用制限**: Yahoo Finance APIは個人利用を想定しています
- **GitHub Actions無料枠**: 月2,000分まで（このボットなら十分です）

## 🔮 今後の拡張案

以下の機能追加を検討中：

- [ ] 📊 チャートの自動生成と画像送信
- [ ] 🔔 急激な変動時のアラート機能
- [ ] 📈 週次/月次サマリーレポート
- [ ] 🌐 追加の市場指標（仮想通貨、商品など）
- [ ] 📧 エラー発生時の通知機能
- [ ] 🎨 カスタマイズ可能な表示形式

## 📄 ライセンス

MIT License

## 🙏 謝辞

- データ提供: [Yahoo Finance](https://finance.yahoo.com/)
- Pythonライブラリ: [yfinance](https://github.com/ranaroussi/yfinance)
- 実行環境: [GitHub Actions](https://github.com/features/actions)

---

**作成日**: 2025年10月22日  
**最終更新**: 2025年10月22日
