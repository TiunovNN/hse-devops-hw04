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
INSERT INTO timestamps (id, timestamp) VALUES (0, 12), (1, 10);
INSERT INTO dogs (pk, name, kind) VALUES
                                      (0, 'Bob', 'terrier'),
                                      (1, 'Marli', 'bulldog'),
                                      (2, 'Snoopy', 'dalmatian'),
                                      (3, 'Rex', 'dalmatian'),
                                      (4, 'Pongo', 'dalmatian'),
                                      (5, 'Tillman', 'bulldog'),
                                      (6, 'Uga', 'bulldog');

COMMIT;
