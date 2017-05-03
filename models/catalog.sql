CREATE TABLE catalog_user (
    username            VARCHAR(30) PRIMARY KEY,
    full_name           VARCHAR(30),
    password            VARCHAR(30),
    signed_up           TIMESTAMP,
    email               VARCHAR(50),
    provider            VARCHAR(25),
    picture             VARCHAR(255)
);

CREATE INDEX user_signed_up          ON catalog_user(signed_up);

CREATE TABLE catalog (
    catalog_id          SERIAL PRIMARY KEY,
    name                VARCHAR(30) NOT NULL,
    description         VARCHAR(300),
    cover_picture       VARCHAR(255),
    owner               VARCHAR(30) REFERENCES catalog_user ON DELETE CASCADE NOT NULL,
    editors             INTEGER[],
    posted              TIMESTAMP
);

CREATE INDEX catalog_name               ON catalog(catalog_id);
CREATE INDEX catalog_cover_picture      ON catalog(cover_picture);
CREATE INDEX catalog_posted             ON catalog(posted);

CREATE TABLE category (
    category_id         SERIAL PRIMARY KEY,
    name                VARCHAR(30) NOT NULL,
    description         VARCHAR(300),
    catalog             INTEGER REFERENCES catalog ON DELETE CASCADE,
    posted              TIMESTAMP
);

CREATE INDEX category_posted             ON category(posted);
    
CREATE TABLE item (
    item_id             SERIAL PRIMARY KEY,
    name                VARCHAR(30),
    description         VARCHAR(300),
    price               MONEY,
    picture             VARCHAR(255),
    owner               VARCHAR(30) REFERENCES catalog_user ON DELETE CASCADE,
    catalog             INTEGER REFERENCES catalog ON DELETE CASCADE,
    category            INTEGER REFERENCES category ON DELETE CASCADE,
    posted              TIMESTAMP  
);

CREATE INDEX item_posted             ON item(posted);