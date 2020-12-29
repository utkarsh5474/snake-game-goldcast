DROP TABLE IF EXISTS user_score;

CREATE TABLE user_score (
    player_name TEXT NOT NULL,
    score INT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);