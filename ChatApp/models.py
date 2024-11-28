import pymysql
import json
from util.DB import DB
from flask import abort

class dbConnect:
    # ユーザー情報の追加
    def createUser(uid, username, email, password, address, greeting, icon):
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()  # カーソルを作成
            sql = "INSERT INTO users (uid, username, email, password, address, greeting, icon) VALUES (%s, %s, %s, %s, %s, %s, %s);"  # SQLクエリを定義 # iconカラムも追加する
            cur.execute(sql, (uid, username, email, password, address, greeting, icon))  # クエリを実行
            conn.commit()  # トランザクションをコミット
        except Exception as e:
            print(str(e) + 'が発生しています')  # エラーメッセージを出力
            abort(500)  # HTTP 500エラーを返す
        finally:
            cur.close()  # カーソルを閉じる

    # メールアドレスを指定してユーザー情報を取得
    def getUser(email):
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()  # カーソルを作成
            sql = "SELECT * FROM users WHERE email=%s;"  # SQLクエリを定義
            cur.execute(sql, (email))  # クエリを実行
            user = cur.fetchone()  # 結果を取得
            return user  # ユーザー情報を返す
        except Exception as e:
            print(e + 'が発生しています')  # エラーメッセージを出力
            abort(500)  # HTTP 500エラーを返す
        finally:
            cur.close()  # カーソルを閉じる

    # uidを指定してprofile.htmlに表示する
    def getUserByUid(uid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()  # カーソルを作成
            sql = "SELECT * FROM users WHERE uid=%s;"
            cur.execute(sql, (uid,))
            user = cur.fetchone()
            return user
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    # ユーザー情報の更新
    def updateUser(uid, username, email, address, greeting, icon):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "UPDATE users SET username=%s, email=%s, address=%s, greeting=%s, icon=%s WHERE uid=%s;"
            cur.execute(sql, (username, email, address, greeting, icon, uid))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しました')
            abort(500)
        finally:
            cur.close()

    # ①チャットルーム一覧、②＋マッチング、③マッチング依頼一覧画面を表示
    def getChatAll():
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()  # カーソルを作成
            sql = "SELECT * FROM chat;"  # SQLクエリを定義
            cur.execute(sql)  # クエリを実行
            chats = cur.fetchall()  # 結果を全て取得
            return chats  # チャット情報を返す
        except Exception as e:
            print(e + 'が発生しています')  # エラーメッセージを出力
            abort(500)  # HTTP 500エラーを返す
        finally:
            cur.close()  # カーソルを閉じる

    # uidを軸にchatテーブルから情報を検索して取得
    def getChatRoom(uid):
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()  # カーソルを作成
            sql = "SELECT * FROM chat;"
            cur.execute(sql)  # クエリを実行
            chat_rooms = cur.fetchall()  # 結果を取得
            return chat_rooms  # チャットルームの一覧を返す
        except Exception as e:
            print(str(e) + 'が発生しました')  # エラーメッセージを出力
            abort(500)  # HTTP 500エラーを返す
        finally:
            cur.close()  # カーソルを閉じる

    # チャットルーム一覧を取得するメソッド
    def getChatRoomList(uid):
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()  # カーソルを作成
            # sql = "SELECT * FROM chat WHERE FIND_IN_SET(%s, user_ids,);"
            sql = "SELECT * FROM chat WHERE user_ids;"
            cur.execute(sql)  # クエリを実行
            chat_rooms = cur.fetchall()  # 結果を取得
            return chat_rooms  # チャットルームの一覧を返す
        except Exception as e:
            print(str(e) + 'が発生しました')  # エラーメッセージを出力
            abort(500)  # HTTP 500エラーを返す
        finally:
            cur.close()  # カーソルを閉じる

    # uidに紐づくメッセージを取得する処理
    def getMessageAll(cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * from messages WHERE cid = %s;"
            cur.execute(sql, (cid))
            messages = cur.fetchall()
            return messages
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    # uidに紐づくメッセージを作成する処理
    def createMessage(uid, cid, message):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO messages(uid, cid, message) VALUES(%s, %s, %s)"
            cur.execute(sql, (uid, cid, message))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    # メッセージとユーザー情報を結合してアイコン情報も取得する処理
    def getMessagesByChatRoom(uid, chat_id):
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()
            sql = "SELECT m.id, m.uid, m.cid, m.message, m.created_at, u.icon FROM messages m JOIN users u ON m.uid = u.uid WHERE m.cid = %s ORDER BY m.created_at;"
            params = (chat_id,)  # パラメータはタプル形式
            cur.execute(sql, params)  # クエリを実行
            messages = cur.fetchall()  # 結果を全て取得
            return messages  # メッセージ一覧を返す
        
        except Exception as e:
            print(f"エラー: {str(e)}")  # エラーメッセージを出力
            abort(500)  # HTTP 500エラーを返す
        
        finally:
            cur.close()  # カーソルを閉じる
            conn.close()  # データベース接続を閉じる

    # 都道府県でユーザーを検索する
    def getUsersByAddress(address, uid): # 自分自身を除外するためにuid引数を追加
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()  # カーソルを作成
            sql = "SELECT * FROM users WHERE address = %s AND uid != %s;"  # SQLクエリを定義 # ここで本人のuidだけ!=で除外
            cur.execute(sql, (address, uid))  # クエリを実行 # uidを追記
            users = cur.fetchall()  # 結果を全て取得
            return users  # ユーザー情報を返す
        except Exception as e:
            print(str(e) + 'が発生しています')  # エラーメッセージを出力
            abort(500)  # HTTP 500エラーを返す
        finally:
            cur.close()  # カーソルを閉じる
            conn.close()  # データベース接続を閉じる

    # マッチング成功後に1対1のチャットルームを作成する
    def createChatroom(uid, name, abstract, user_ids):
        try:
            conn = DB.getConnection()  # データベース接続を取得
            cur = conn.cursor()  # カーソルを作成
            sql = "INSERT INTO chat (uid, name, abstract, user_ids) VALUES (%s, %s, %s, %s);"
            cur.execute(sql, (uid, name, abstract, user_ids))
            conn.commit()  # トランザクションをコミット
        except Exception as e:
            print(f"エラーが発生しました: {str(e)}")
            abort(500)  
        finally:
            cur.close()  
            conn.close()

    # uidに基づいてユーザー名を取得する
    def getUsernameByUid(uid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT username FROM users WHERE uid=%s;"
            cur.execute(sql, (uid,))
            user = cur.fetchone()
            return user['username'] if user else None
        except Exception as e:
            print(f"エラーが発生しました: {str(e)}")
            abort(500)
        finally:
            cur.close()
            conn.close()

    def getUsersByChatRoom(chat_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT user_ids FROM chat WHERE id=%s;" # チャットルームの user_ids を取得
            cur.execute(sql, (chat_id,))
            result = cur.fetchone()
            if not result:
                return []  # チャットIDが存在しない場合、空のリストを返す

            user_ids = result['user_ids']
            # user_ids をカンマで分割
            user_ids_list = user_ids.split(',')
            
            # 各ユーザーを取得
            placeholders = ','.join(['%s'] * len(user_ids_list))
            sql = f"SELECT * FROM users WHERE uid IN ({placeholders});"
            cur.execute(sql, user_ids_list)
            users = cur.fetchall()
            return users
        except Exception as e:
            print(f"エラーが発生しました: {str(e)}")
            abort(500)
        finally:
            cur.close()
            conn.close()