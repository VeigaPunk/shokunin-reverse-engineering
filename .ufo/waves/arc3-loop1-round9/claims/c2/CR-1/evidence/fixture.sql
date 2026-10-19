PRAGMA journal_mode=DELETE;
CREATE TABLE artifact_catalog (id INTEGER PRIMARY KEY, name TEXT NOT NULL, sha256 TEXT NOT NULL);
INSERT INTO artifact_catalog (id, name, sha256) VALUES (1, 'fixture', '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef');
