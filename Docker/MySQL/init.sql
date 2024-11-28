DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE users (
    uid varchar(255) PRIMARY KEY,
    username varchar(255) UNIQUE NOT NULL,
    email varchar(255) UNIQUE NOT NULL,
    password varchar(255) NOT NULL,
    address varchar(255) NOT NULL,
    greeting varchar(255) NOT NULL,
    icon text(255) NOT NULL
);

CREATE TABLE chat (
    id serial PRIMARY KEY,
    uid varchar(255) REFERENCES users(uid),
    name varchar(255) UNIQUE NOT NULL,
    abstract varchar(255),
    user_ids text  -- チャットへの権限制御：参加ユーザーのIDをカンマ区切りで保存することにより、1対Nではなく、1対1のチャット
);

CREATE TABLE messages (
    id serial PRIMARY KEY,
    uid varchar(255) REFERENCES users(uid),
    cid integer REFERENCES chat(id) ON DELETE CASCADE,
    message text,
    created_at timestamp not null default current_timestamp
);

-- Create friendRequests table
-- CREATE TABLE friendRequests (
--     request_id serial,
--     from_user_id varchar(255) NOT NULL,
--     to_user_id varchar(255) NOT NULL,
--     status enum('pending', 'accepted', 'declined') NOT NULL DEFAULT 'pending',
--     PRIMARY KEY (request_id),
--     FOREIGN KEY (from_user_id) REFERENCES users(u_id) ON DELETE CASCADE,
--     FOREIGN KEY (to_user_id) REFERENCES users(u_id) ON DELETE CASCADE
-- );

-- ユーザデータのサンプル挿入
INSERT INTO users (uid, username, email, password, address, greeting, icon) VALUES
('1', 'アリス', 'alice@example.com', 'password1', '北海道', 'こんにちは、アリスです。', 'chick.png'),
('2', 'タロウ', 'taro@example.com', 'password2', '北海道', 'こんにちは、タロウです。', 'crab.png'),
('3', 'カズマ', 'kazuma@example.com', 'password3', '北海道', 'こんにちは、カズマです。', 'dog.png'),
('4', 'ハナコ', 'hanako@example.com', 'password4', '北海道', 'こんにちは、ハナコです。', 'dolphin.png'),
('5', 'ケンタ', 'kenta@example.com', 'password5', '北海道', 'こんにちは、ケンタです。', 'elephant.png'),
('6', 'サクラ', 'sakura@example.com', 'password6', '北海道', 'こんにちは、サクラです。', 'frog.png'),
('7', 'ユウタ', 'yuta@example.com', 'password7', '北海道', 'こんにちは、ユウタです。', 'giraffe.png'),
('8', 'アヤ', 'aya@example.com', 'password8', '北海道', 'こんにちは、アヤです。', 'gorilla.png'),
('9', 'ナオ', 'nao@example.com', 'password9', '北海道', 'こんにちは、ナオです。', 'hedgehog.png'),
('10', 'リョウ', 'ryo@example.com', 'password10', '北海道', 'こんにちは、リョウです。', 'horse.png'),
('11', 'ユキ', 'yuki@example.com', 'password12', '青森県', 'こんにちは、ユキです。', 'ladybug.png'),
('12', 'ショウ', 'sho@example.com', 'password13', '青森県', 'こんにちは、ショウです。', 'lion.png'),
('13', 'ミキ', 'miki@example.com', 'password14', '青森県', 'こんにちは、ミキです。', 'octopus.png'),
('14', 'リナ', 'rina@example.com', 'password15', '青森県', 'こんにちは、リナです。', 'peacock.png'),
('15', 'ハルカ', 'haruka@example.com', 'password16', '青森県', 'こんにちは、ハルカです。', 'pig.png'),
('16', 'タケシ', 'takeshi@example.com', 'password17', '青森県', 'こんにちは、タケシです。', 'sloth.png'),
('17', 'ユウ', 'yuu@example.com', 'password18', '青森県', 'こんにちは、ユウです。', 'snail.png'),
('18', 'ミズキ', 'mizuki@example.com', 'password19', '青森県', 'こんにちは、ミズキです。', 'squirrel.png'),
('19', 'アキラ', 'akira@example.com', 'password20', '青森県', 'こんにちは、アキラです。', 'turtle.png');

-- チャットルームのサンプル挿入
-- INSERT INTO chat (uid, name, abstract, user_ids) VALUES
-- ('1', 'アリスさんとボブさんのチャットルーム', 'アリスさんとボブさんのチャットルームです', '1,2'),
-- ('1', 'アリスさんとチャーリーさんのチャットルーム', 'アリスさんとチャーリーさんのチャットルーム', '1,3');

-- メッセージのサンプル挿入
-- INSERT INTO messages(id, uid, cid, message)VALUES
-- (1, '1', '1', 'こんにちは、佐藤です。名前教えてください！'),
-- (2, '2', '1', 'こんにちは、鈴木です。');