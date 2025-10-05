-- run create_tables.py to run this .sql file

DROP TABLE IF EXISTS "Article" CASCADE;
DROP TABLE IF EXISTS "ComicBook" CASCADE;
DROP TABLE IF EXISTS "Book" CASCADE;
DROP TABLE IF EXISTS "Readings" CASCADE;

DROP TYPE IF EXISTS genre_enum;
DROP TYPE IF EXISTS rating_enum;
DROP TYPE IF EXISTS mood_enum;

CREATE TYPE genre_enum AS ENUM (
    'fiction', 'nonfiction', 'fantasy', 'mystery',
    'biography', 'sci-fi', 'romance', 'other'
);

CREATE TYPE rating_enum AS ENUM (
    '1', '2', '3', '4', '5'
);

CREATE TYPE mood_enum AS ENUM (
  'happy', 'emotional', 'thoughtful', 'inspired',
  'bored', 'confused', 'relaxed', 'amused',
  'indifferent', 'nostalgic', 'excited', 'overwhelmed'
);

CREATE FUNCTION avg_rating_by_genre(g genre_enum)
RETURNS NUMERIC AS $$
BEGIN
    RETURN (
        SELECT AVG(my_rating::int) 
        FROM "Book" 
        WHERE genre = g);
END;
$$ LANGUAGE plpgsql;

CREATE TYPE publisher_info AS (
    publisher_name VARCHAR,
    country VARCHAR,
    website VARCHAR
);

CREATE TABLE "Readings" (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    author VARCHAR,
    publisher publisher_info,
    publish_year VARCHAR,
    date_read DATE CHECK (date_read <= CURRENT_DATE),
    tags JSONB,
    my_rating rating_enum,
    mood mood_enum,
    notes VARCHAR,
    type VARCHAR(50) NOT NULL
);

CREATE TABLE "Book" (
    genre genre_enum NOT NULL,
    page_count INTEGER,
    ISBN VARCHAR 
) INHERITS ("Readings");

CREATE TABLE "ComicBook" (
    illustrator VARCHAR,
    volume INTEGER
) INHERITS ("Readings");

CREATE TABLE "Article" (
    journal VARCHAR,
    DOI VARCHAR 
) INHERITS ("Readings");