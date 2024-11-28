# 構築や動作に必要なライブラリやモジュールをインポート
from flask import Flask, request, redirect, render_template, session, flash, abort, jsonify, url_for
from datetime import timedelta
import hashlib
import uuid
import re
import os
from models import dbConnect
from notification import sendLineNotify  # notification.py から関数をインポート

# Flask アプリケーションのインスタンスを作成
app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=7)  # セッションの有効期限を7日に変更

# # 新規会員登録ページの表示
# @app.route('/signup')
# def signup():
#     return render_template('registration/signup.html')

# # 新規会員登録の処理、フォームを送信するPOSTの処理を実装
# @app.route('/signup', methods=['POST'])
# def userSignup():
#     username = request.form.get('username')
#     email = request.form.get('email')
#     password1 = request.form.get('password1')
#     password2 = request.form.get('password2')
#     address = request.form.get('address')
#     greeting = request.form.get('greeting')
#     icon = request.form.get('icon')

#     pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

#     if username == '' or email =='' or password1 == '' or password2 == '' or address == '' or greeting == '' or  icon =='':
#         flash('空のフォームがあるようです')
#     elif password1 != password2:
#         flash('二つのパスワードの値が違っています')
#     elif re.match(pattern, email) is None:
#         flash('正しいメールアドレスの形式ではありません')
#     else:
#         uid = uuid.uuid4()
#         # password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
#         password = password1  # local検証の為、一時的にハッシュ化しない
#         DBuser = dbConnect.getUser(email) # メールアドレスを元にユーザー情報を検索する

#         if DBuser != None:
#             flash('既に登録されているようです')
#         else:
#             dbConnect.createUser(uid, username, email, password, address, greeting, icon) # ユーザー情報の追加
#             UserId = str(uid)
#             session['uid'] = UserId
#             return redirect('/')
#     return redirect('/signup')

@app.route('/signup', methods=['GET', 'POST']) # POSTはユーザー情報の登録、GETはiconを取ってくる
def signup():
    if request.method == 'POST':
        # POSTリクエストの処理：新規会員登録
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        address = request.form.get('address')
        greeting = request.form.get('greeting')
        icon = request.form.get('icon')

        pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if username == '' or email =='' or password1 == '' or password2 == '' or address == '' or greeting == '' or icon =='':
            flash('空のフォームがあるようです')
        elif password1 != password2:
            flash('二つのパスワードの値が違っています')
        elif re.match(pattern, email) is None:
            flash('正しいメールアドレスの形式ではありません')
        else:
            uid = uuid.uuid4()
            password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
            # password = password1  # local検証の為、一時的にハッシュ化しない
            DBuser = dbConnect.getUser(email) # メールアドレスを元にユーザー情報を検索する

            if DBuser is not None:
                flash('既に登録されているようです')
            else:
                dbConnect.createUser(uid, username, email, password, address, greeting, icon) # ユーザー情報の追加
                UserId = str(uid)
                session['uid'] = UserId
                return redirect('/')
        return redirect('/signup')
    
    else:
        # GETリクエストの処理：サインアップページの表示
        icon_path = os.path.join(app.static_folder, 'img/icon')
        icons = os.listdir(icon_path)
        return render_template('registration/signup.html', icons=icons)


# ログインページの表示
@app.route('/login')
def login():
    return render_template('registration/login.html')

# ログイン処理、フォームを送信するPOSTの処理を実装
@app.route('/login', methods=['POST'])
def userLogin():
    email = request.form.get('email')
    password = request.form.get('password')

    if email =='' or password == '':
        flash('空のフォームがあるようです')
    else:
        user = dbConnect.getUser(email) # メールアドレスを元にユーザー情報を検索する
        if user is None:
            flash('このユーザーは存在しません')
        else:
            if password != user["password"]:  # ハッシュ化せずに平文で比較
                flash('パスワードが間違っています！')
            # hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            # if hashPassword != user["password"]:
            #     flash('パスワードが間違っています！')
            else:
                session['uid'] = user["uid"]
                return redirect('/')
    return redirect('/login')

# # ①チャットルーム一覧、②＋マッチング、③マッチング依頼一覧画面を表示
# @app.route('/')
# def home():
#     uid = session.get("uid")
#     if uid is None:
#         return redirect('/login')
#     else:
#         channels = dbConnect.getChatAll() # ①②③のすべてのチャットを取得
#         channels = channels[::-1]  # スライスを使ってタプルを逆順にする
#     return render_template('home.html', channels=channels, uid=uid)

@app.route('/')
def home():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        channels = dbConnect.getChatAll()  # ①②③のすべてのチャットを取得
        channels = channels[::-1]  # スライスを使ってタプルを逆順にする
        user = dbConnect.getUserByUid(uid)  # ユーザー情報を取得
    return render_template('home.html', channels=channels, uid=uid, user=user)


# ホーム画面からプロフィール画面にページの遷移
@app.route('/profile')
def profile():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        user = dbConnect.getUserByUid(uid)
        return render_template('profile.html', user=user)

# プロフィール画面からユーザ情報の更新
@app.route('/profile_edit', methods=['GET', 'POST'])
def profile_edit():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')

    if request.method == 'POST': # POSTリクエストの場合、フォームからデータを取得して更新処理を行う
        username = request.form.get('username')
        email = request.form.get('email')
        address = request.form.get('address')
        greeting = request.form.get('greeting')
        icon = request.form.get('icon')

        dbConnect.updateUser(uid, username, email, address, greeting, icon) # データベースを更新
        return redirect('/profile') # 更新後のプロフィール画面ページにリダイレクト
    else:
        user = dbConnect.getUserByUid(uid)  # GETリクエストの場合、ユーザー情報を取得して編集ページを表示

        # アイコン画像のリストを取得
        icon_path = os.path.join(app.static_folder, 'img/icon')
        icons = os.listdir(icon_path)

        return render_template('profile_edit.html', user=user, icons=icons)

# ホーム画面からchat_listページに画面遷移
@app.route('/chat_list')
def chat_list():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')

    channellist = dbConnect.getChatRoom(uid)
    user = dbConnect.getUserByUid(uid)
    chatlist = []
    for channel in channellist: 
        user_numbers = channel["user_ids"].split(",")
        if uid in user_numbers:
            # 自分以外のユーザーを特定
            other_user_id = [u_id for u_id in user_numbers if u_id != uid][0]
            # 相手ユーザーの情報を取得
            other_user = dbConnect.getUserByUid(other_user_id)
            channel["icon"] = url_for('static', filename=f'img/icon/{other_user.get("icon")}')
            chatlist.append(channel)
    return render_template('chat_list.html', chat_rooms=chatlist, user=user)

# チャット画面からGETとPOSTの処理を実装 追加7/28夜に追加
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')

    chat_id = request.args.get('room_id')  # URL パラメータからチャットIDを取得
    user = dbConnect.getUserByUid(uid)
    if chat_id:
        if request.method == 'GET':
            messages = dbConnect.getMessagesByChatRoom(uid, chat_id)  # メッセージの取得
            chat_users = dbConnect.getUsersByChatRoom(chat_id)  # チャットルームに参加しているユーザーの取得
            other_users = [u for u in chat_users if u['uid'] != uid]  # 他のユーザーを取得
            if other_users:
                selected_user = other_users[0]  # 1人目の他のユーザーを選択
            else:
                selected_user = None  # 他のユーザーがいない場合

            return render_template('chat.html', chat_id=chat_id, messages=messages, user=user, selected_user=selected_user)

        if request.method == 'POST':
            message = request.form.get('message')  # メッセージの投稿
            if message:
                dbConnect.createMessage(uid, chat_id, message)
            return redirect(url_for('chat', room_id=chat_id))  # 正しいURLだけを渡す

    else:
        chats = dbConnect.getChatRoomList(uid)  # チャットIDが指定されていない場合、チャットルームの一覧を表示
        return render_template('chat_list.html', chats=chats, user=user)

# マッチング画面からGETとPOSTの処理を実装 7/31に処理を新規追加した
@app.route('/matching', methods=['GET', 'POST'])
def matching():
    uid = session.get("uid")  # uidを定義
    if uid is None:
        return redirect('/login')
    
    user = dbConnect.getUserByUid(uid)
    if request.method == 'POST':
        address = request.json.get('address')
        if address:
            users = dbConnect.getUsersByAddress(address, uid)  # データを取得 (uidを追記)
            # 各ユーザーが辞書であることを確認し、キーを使用してアクセス
            return jsonify([{
                'uid': u.get('uid'),            # ユーザーID
                'name': u.get('username'),      # ユーザー名
                'address': u.get('address'),    # ユーザーの住所
                'greeting': u.get('greeting'),  # 挨拶
                'icon': url_for('static', filename=f'img/icon/{u.get("icon")}')  # フルパスのアイコンURLを生成
            } for u in users])  # ループ内の変数名を`u`に変更
        return jsonify({'error': '住所が指定されていません'}), 400
    else:
        return render_template('matching.html', user=user)

# マッチング画面から派生してPOSTの処理を実装 7/31に処理を新規追加した
# @app.route('/create_chatroom', methods=['POST'])
# def create_chatroom():
#     data = request.get_json()
#     print(f"Received data: {data}")  # デバッグ用ログ

#     name = data.get('name')
#     address = data.get('address')
#     uid = data.get('uid')  # 修正: フロントエンドから送信された uid を取得
    
#     print(f"Received UID: {uid}")  # デバッグ用ログ
#     logged_in_user_id = session.get('uid')

#     if not logged_in_user_id:
#         return jsonify({"message": "ログインしていません"}), 401
#     if not uid:
#         return jsonify({"message": "UID is required"}), 400

#     user_ids = ','.join(map(str, [logged_in_user_id, uid])) # user_ids の生成
#     print(f"Generated user_ids string: {user_ids}")  # デバッグ用ログ
#     abstract = f"Chatroom for {name} at {address}"

#     try:
#         dbConnect.createChatroom(uid=generate_unique_id(), name=name, abstract=abstract, user_ids=user_ids)
#         return jsonify({"message": "チャットルームが作成されました"}), 200
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return jsonify({"message": "チャットルームの作成に失敗しました"}), 500

# ログインユーザー名を取得するAPIエンドポイント
@app.route('/get_logged_in_user', methods=['GET'])
def get_logged_in_user():
    logged_in_user_id = session.get('uid')
    if not logged_in_user_id:
        return jsonify({"message": "ログインしていません"}), 401
    logged_in_username = dbConnect.getUsernameByUid(logged_in_user_id)
    print(f"Logged in username: {logged_in_username}")  # デバッグ用ログ
    if not logged_in_username:
        return jsonify({"message": "ユーザー情報の取得に失敗しました"}), 500
    return jsonify({"username": logged_in_username}), 200

@app.route('/create_chatroom', methods=['POST'])
def create_chatroom():
    data = request.get_json()
    print(f"Received data: {data}")  # デバッグ用ログ

    name = data.get('name')
    address = data.get('address')
    uid = data.get('uid')  # 修正: フロントエンドから送信された uid を取得

    print(f"Received UID: {uid}")  # デバッグ用ログ
    logged_in_user_id = session.get('uid')

    if not logged_in_user_id:
        return jsonify({"message": "ログインしていません"}), 401
    if not uid:
        return jsonify({"message": "UID is required"}), 400

    # ログインユーザーの名前を取得
    logged_in_username = dbConnect.getUsernameByUid(logged_in_user_id)
    selected_username = dbConnect.getUsernameByUid(uid)

    print(f"Logged in username: {logged_in_username}")  # デバッグ用ログ
    print(f"Selected in username: {selected_username}")  # デバッグ用ログ

    if not logged_in_username or not selected_username:
        return jsonify({"message": "ユーザー情報の取得に失敗しました"}), 500

    user_ids = ','.join(map(str, [logged_in_user_id, uid]))  # user_ids の生成
    print(f"Generated user_ids string: {user_ids}")  # デバッグ用ログ
    abstract = f"Chatroom for {selected_username} at {address}"

    try:
        dbConnect.createChatroom(uid=generate_unique_id(), name=name, abstract=abstract, user_ids=user_ids)
        # フロントにログインユーザー名とチャットルーム作成メッセージを送信

        # チャットルームが作成された後に、LINE通知を送信
        sendLineNotify()
        
        return jsonify({
            "message": f"チャットルームが作成されました。",
            "logged_in_username": logged_in_username,
            "selected_username": selected_username
        }), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "チャットルームの作成に失敗しました"}), 500

# 直前の処理で必要な関数を定義
def generate_unique_id():
    return str(uuid.uuid4())

# ログアウトした際の画面遷移としてログイン画面に戻る
@app.route('/logout')
def logout():
    return render_template('registration/login.html')

@app.errorhandler(404)
def show_error404(error):
    return render_template('error/404.html'),404


@app.errorhandler(500)
def show_error500(error):
    return render_template('error/500.html'),500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)