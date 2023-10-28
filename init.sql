BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> ca79b727cd01

CREATE TYPE dogtype AS ENUM ('terrier', 'bulldog', 'dalmatian');

CREATE TABLE dogs (
    pk SERIAL NOT NULL, 
    name VARCHAR(100), 
    kind dogtype, 
    PRIMARY KEY (pk)
);

CREATE INDEX ix_dogs_pk ON dogs (pk);

CREATE TABLE timestamps (
    id SERIAL NOT NULL, 
    timestamp INTEGER, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_timestamps_id ON timestamps (id);

INSERT INTO alembic_version (version_num) VALUES ('ca79b727cd01') RETURNING alembic_version.version_num;
INSERT INTO timestamps (timestamp) VALUES (12), (10);
INSERT INTO dogs (name, kind) VALUES
                                  ('Bob', 'terrier'),
                                  ('Marli', 'bulldog'),
                                  ('Snoopy', 'dalmatian'),
                                  ('Rex', 'dalmatian'),
                                  ('Pongo', 'dalmatian'),
                                  ('Tillman', 'bulldog'),
                                  ('Uga', 'bulldog');

COMMIT;
