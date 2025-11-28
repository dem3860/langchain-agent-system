-- テーブル作成
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    pref VARCHAR(10) -- 都道府県
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    price INTEGER
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER,
    order_date DATE
);

-- データ投入
INSERT INTO users (name, pref) VALUES 
('佐藤', '東京'), ('鈴木', '大阪'), ('高橋', '東京'), ('田中', '北海道');

INSERT INTO products (product_name, price) VALUES 
('ゲーミングPC', 200000), ('モニター', 30000), ('マウス', 5000), ('キーボード', 15000);

INSERT INTO orders (user_id, product_id, quantity, order_date) VALUES 
(1, 1, 1, '2024-01-10'), -- 佐藤: PC
(1, 3, 2, '2024-01-10'), -- 佐藤: マウスx2
(2, 2, 1, '2024-02-05'), -- 鈴木: モニター
(3, 4, 1, '2024-02-15'), -- 高橋: キーボード
(4, 1, 1, '2024-03-01'); -- 田中: PC