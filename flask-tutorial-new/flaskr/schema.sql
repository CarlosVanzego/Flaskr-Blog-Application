-- Drops the 'user' table if it already exists to avoid errors when recreating it.
DROP TABLE IF EXISTS user;
-- Drops the 'post' table if it already exists to avoid errors when recreating it.
DROP TABLE IF EXISTS post;
-- Creates the 'user' table.
CREATE TABLE user (
  -- The unique identifier for each user; auto-incremented.
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  -- The username of the user; cannot be null.
  username TEXT UNIQUE NOT NULL,
  -- The password of th euser; cannot be null.
  password TEXT NOT NULL
);
-- Creates the 'post' table.
CREATE TABLE post (
  -- The unique identifier for each post; auto-incremented.
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  -- References the ID of the author from the 'user' table; cannot be null
  author_id INTEGER NOT NULL,
  -- Timestamp of when the post was created; defaults to the current timestamp if not provided
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- Title of the post; cannot be null.
  title TEXT NOT NULL,
  -- Body of the post; cannot be null.
  body TEXT NOT NULL,
  -- Foreign key constraint ensuring the 'author_id' corresponds to an existing 'id' in the 'user' table.
  FOREIGN KEY (author_id) REFERENCES user (id)
);
