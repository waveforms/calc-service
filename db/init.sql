CREATE DATABASE knights;
use knights;

CREATE TABLE IF NOT EXISTS user (
  id INT AUTO_INCREMENT,
  username VARCHAR(64),
  email VARCHAR(120),
  password_hash VARCHAR(128),
  PRIMARY KEY (id)
) ENGINE=INNODB;

CREATE TABLE post (
  id int(11) AUTO_INCREMENT,
  body text,
  timestamp datetime,
  user_id int(11),
  PRIMARY KEY (id)
) ENGINE=INNODB;
