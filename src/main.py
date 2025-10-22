import os
import yfinance as yf
import requests
from datetime import datetime
import pytz

def get_market_data():
    """各市場データを取得"""
    tickers = {
        'ドル円': 'JPY=X',
        '日経平均': '^N225',
        'S&P500': '^GSPC',
        'VIX指数': '^VIX'
    }
    
    data = {}
    for name, symbol in tickers.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='2d')
            
            if len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                previous = hist['Close'].iloc[-2]
                change = current - previous
                change_pct = (change / previous) * 100
                
                data[name] = {
                    'current': current,
                    'change': change,
                    'change_pct': change_pct
                }
            else:
                data[name] = None
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            data[name] = None
    
    return data

def format_message(data):
    """Discord用のメッセージをフォーマット"""
    jst = pytz.timezone('Asia/Tokyo')
    now = datetime.now(jst)
    
    # 埋め込みメッセージの作成
    embed = {
        "title": "📊 本日の市場データ",
        "description": f"{now.strftime('%Y年%m月%d日 %H:%M')} JST",
        "color": 3447003,  # 青色
        "fields": [],
        "footer": {
            "text": "データ提供: Yahoo Finance"
        },
        "timestamp": now.isoformat()
    }
    
    # 各指標のデータを追加
    for name, values in data.items():
        if values:
            arrow = "📈" if values['change'] >= 0 else "📉"
            sign = "+" if values['change'] >= 0 else ""
            
            # ドル円は特別フォーマット
            if name == 'ドル円':
                value_str = f"¥{values['current']:.2f}"
                change_str = f"{sign}{values['change']:.2f}円 ({sign}{values['change_pct']:.2f}%)"
            else:
                value_str = f"{values['current']:,.2f}"
                change_str = f"{sign}{values['change']:.2f} ({sign}{values['change_pct']:.2f}%)"
            
            embed["fields"].append({
                "name": f"{arrow} {name}",
                "value": f"**{value_str}**\n{change_str}",
                "inline": True
            })
        else:
            embed["fields"].append({
                "name": f"⚠️ {name}",
                "value": "データ取得エラー",
                "inline": True
            })
    
    return {"embeds": [embed]}

def send_to_discord(webhook_url, message):
    """DiscordのWebhookにメッセージを送信"""
    try:
        response = requests.post(
            webhook_url,
            json=message,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 204:
            print("✅ メッセージをDiscordに送信しました")
        else:
            print(f"❌ Discord送信エラー: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ 送信中にエラーが発生: {e}")

def main():
    """メイン処理"""
    # 環境変数からWebhook URLを取得
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    if not webhook_url:
        print("❌ DISCORD_WEBHOOK_URL が設定されていません")
        return
    
    print("📊 市場データを取得中...")
    data = get_market_data()
    
    print("💬 メッセージをフォーマット中...")
    message = format_message(data)
    
    print("📤 Discordに送信中...")
    send_to_discord(webhook_url, message)

if __name__ == "__main__":
    main()
