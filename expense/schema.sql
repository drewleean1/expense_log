DROP TABLE IF EXISTS user; 
DROP TABLE IF EXISTS post; 

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL, 
    password TEXT NOT NULL,
    question TEXT NOT NULL 
);

CREATE TABLE expense (
    e_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    user_id INTEGER NOT NULL, 
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    buy_date DATE NOT NULL,
    item TEXT NOT NULL, 
    amount INTEGER NOT NULL, 
    category TEXT NOT NULL, 
    FOREIGN KEY (user_id) REFERENCES user (id)
);