import requests

def sendLineNotify():
    # testの箇所はご自身のトークンを取得して入力してください
    lineNotifyToken = "test"
    lineNotifyApi = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {lineNotifyToken}"}
    data = {"message": "行きたい旅行先の方とマッチングしました！"}
    
    response = requests.post(lineNotifyApi, headers=headers, data=data)
    if response.status_code == 200:
        print("LINEに通知が送信されました")
    else:
        print("通知の送信に失敗しました")

# LINE通知を実行:タロイモさんのご指摘通り、compose upすると実行されていた為、コメントアウト
# sendLineNotify()
