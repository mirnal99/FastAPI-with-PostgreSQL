import json
from fastapi import FastAPI, HTTPException, Query
from database import init_db, close_db
from schemas import BookCreate, ArticleCreate, ComicBookCreate, ReadingsBase

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(lifespan=lifespan)

from fastapi import FastAPI, Query
from typing import Optional
import json
from database import init_db

app = FastAPI()


# Get ALL readings
@app.get("/readings/")
async def get_readings(
    title: Optional[str] = Query(default=None),
    author: Optional[str] = Query(default=None),
    mood: Optional[str] = Query(default=None),
    reading_type: Optional[str] = Query(default=None),
    tag: Optional[str] = Query(default=None)
):
    
    #Get readings with optional filters on title, author, mood, type, and tags:
    pool = await init_db()
    async with pool.acquire() as conn:
        query = 'SELECT * FROM "Readings"'
        params = []
        filters = []

        if title:
            filters.append("title ILIKE $%d" % (len(params)+1))
            params.append(f"%{title}%")
        if author:
            filters.append("author ILIKE $%d" % (len(params)+1))
            params.append(f"%{author}%")
        if mood:
            filters.append("mood = $%d" % (len(params)+1))
            params.append(mood)
        if reading_type:
            filters.append("type = $%d" % (len(params)+1))
            params.append(reading_type)

        if tag:
            filters.append("coalesce(tags, '[]'::jsonb) @> $%d::jsonb" % (len(params)+1))
            params.append(json.dumps([tag]))

        if filters:
            query += " WHERE " + " AND ".join(filters)

        rows = await conn.fetch(query, *params)
        return [dict(row) for row in rows]


@app.get("/readings/{reading_id}")
async def get_reading(reading_id: int):
    pool = await init_db()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            'SELECT * FROM "Readings" WHERE id = $1', reading_id
        )
        if not row:
            raise HTTPException(status_code=404, detail="Reading not found")
        return dict(row)


@app.delete("/readings/{reading_id}")
async def delete_reading(reading_id: int):
    pool = await init_db()
    async with pool.acquire() as conn:
        deleted_id = await conn.fetchval(
            'DELETE FROM "Readings" WHERE id = $1 RETURNING id', reading_id
        )
        if not deleted_id:
            raise HTTPException(status_code=404, detail="Reading not found")
        return {"id": deleted_id, "message": "Reading deleted successfully."}

# ------------------------------
# CRUD for Books
# ------------------------------
@app.get("/books/")
async def get_books(
    genre: str | None = Query(default=None),
    tag: str | None = Query(default=None)
):
    pool = await init_db()
    async with pool.acquire() as conn:
        query = 'SELECT * FROM "Book"'
        params = []
        filters = []

        if genre:
            filters.append("genre = $1")
            params.append(genre)
        if tag:
            filters.append("coalesce(tags, '[]'::jsonb) @> $2::jsonb")
            params.append(json.dumps([tag]))

        if filters:
            query += " WHERE " + " AND ".join(filters)

        rows = await conn.fetch(query, *params)
        return [dict(row) for row in rows]


@app.get("/books/{book_id}")
async def get_book(book_id: int):
    pool = await init_db()
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM "Book" WHERE id = $1;', book_id)
        if not row:
            raise HTTPException(status_code=404, detail="Book not found")
        return dict(row)


@app.post("/books/")
async def create_book(book: BookCreate):
    pool = await init_db()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            INSERT INTO "Book" (
                title, author, publish_year, date_read,
                tags, my_rating, mood, notes, type,
                genre, page_count, ISBN
            ) VALUES ($1, $2, $3, $4, $5::jsonb, $6, $7, $8, $9, $10, $11, $12)
            RETURNING id;
        """,
        book.title,
        book.author,
        book.publish_year,
        book.date_read,
        json.dumps(book.tags or []),
        book.my_rating.value if book.my_rating else None,
        book.mood.value if book.mood else None,
        book.notes,
        "Book",
        book.genre.value,
        book.page_count,
        book.ISBN
        )
        return {"id": row["id"], "message": "Book created successfully."}


@app.put("/books/{book_id}")
async def update_book(book_id: int, book: BookCreate):
    pool = await init_db()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            UPDATE "Book"
            SET title = $1, author = $2, publish_year = $3, date_read = $4,
                tags = $5::jsonb, my_rating = $6, mood = $7, notes = $8,
                genre = $9, page_count = $10, ISBN = $11
            WHERE id = $12
            RETURNING id;
        """,
        book.title,
        book.author,
        book.publish_year,
        book.date_read,
        json.dumps(book.tags or []),
        book.my_rating.value if book.my_rating else None,
        book.mood.value if book.mood else None,
        book.notes,
        book.genre.value,
        book.page_count,
        book.ISBN,
        book_id
        )
        if not row:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"id": book_id, "message": "Book updated successfully."}


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    pool = await init_db()
    async with pool.acquire() as conn:
        row = await conn.fetchrow('DELETE FROM "Book" WHERE id = $1 RETURNING id;', book_id)
        if not row:
            raise HTTPException(status_code=404, detail="Book not found")
        return {"id": row["id"], "message": "Book deleted successfully."}


# ------------------------------
# CRUD for Articles
# ------------------------------
@app.get("/articles/")
async def get_articles():
    pool = await init_db()
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM "Article";')
        return [dict(row) for row in rows]


@app.get("/articles/{article_id}")
async def get_article(article_id: int):
    pool = await init_db()
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM "Article" WHERE id = $1;', article_id)
        if not row:
            raise HTTPException(status_code=404, detail="Article not found")
        return dict(row)


@app.post("/articles/")
async def create_article(article: ArticleCreate):
    pool = await init_db()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            INSERT INTO "Article" (
                title, author, publish_year, date_read,
                tags, my_rating, mood, notes, type,
                journal, DOI
            ) VALUES ($1, $2, $3, $4, $5::jsonb, $6, $7, $8, $9, $10, $11)
            RETURNING id;
        """,
        article.title,
        article.author,
        article.publish_year,
        article.date_read,
        json.dumps(article.tags or []),
        article.my_rating.value if article.my_rating else None,
        article.mood.value if article.mood else None,
        article.notes,
        "Article",
        article.journal,
        article.DOI
        )
        return {"id": row["id"], "message": "Article created successfully."}


@app.put("/articles/{article_id}")
async def update_article(article_id: int, article: ArticleCreate):
    pool = await init_db()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            UPDATE "Article"
            SET title = $1, author = $2, publish_year = $3, date_read = $4,
                tags = $5::jsonb, my_rating = $6, mood = $7, notes = $8,
                journal = $9, DOI = $10
            WHERE id = $11
            RETURNING id;
        """,
        article.title,
        article.author,
        article.publish_year,
        article.date_read,
        json.dumps(article.tags or []),
        article.my_rating.value if article.my_rating else None,
        article.mood.value if article.mood else None,
        article.notes,
        article.journal,
        article.DOI,
        article_id
        )
        if not row:
            raise HTTPException(status_code=404, detail="Article not found")
        return {"id": article_id, "message": "Article updated successfully."}


@app.delete("/articles/{article_id}")
async def delete_article(article_id: int):
    pool = await init_db()
    async with pool.acquire() as conn:
        row = await conn.fetchrow('DELETE FROM "Article" WHERE id = $1 RETURNING id;', article_id)
        if not row:
            raise HTTPException(status_code=404, detail="Article not found")
        return {"id": row["id"], "message": "Article deleted successfully."}


# ------------------------------
# CRUD for ComicBooks
# ------------------------------
@app.get("/comicbooks/")
async def get_comicbooks():
    pool = await init_db()
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM "ComicBook";')
        return [dict(row) for row in rows]


@app.get("/comicbooks/{comic_id}")
async def get_comicbook(comic_id: int):
    pool = await init_db()
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM "ComicBook" WHERE id = $1;', comic_id)
        if not row:
            raise HTTPException(status_code=404, detail="ComicBook not found")
        return dict(row)


@app.post("/comicbooks/")
async def create_comicbook(comic: ComicBookCreate):
    pool = await init_db()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            INSERT INTO "ComicBook" (
                title, author, publish_year, date_read,
                tags, my_rating, mood, notes, type,
                illustrator, volume
            ) VALUES ($1, $2, $3, $4, $5::jsonb, $6, $7, $8, $9, $10, $11)
            RETURNING id;
        """,
        comic.title,
        comic.author,
        comic.publish_year,
        comic.date_read,
        json.dumps(comic.tags or []),
        comic.my_rating.value if comic.my_rating else None,
        comic.mood.value if comic.mood else None,
        comic.notes,
        "ComicBook",
        comic.illustrator,
        comic.volume
        )
        return {"id": row["id"], "message": "ComicBook created successfully."}


@app.put("/comicbooks/{comic_id}")
async def update_comicbook(comic_id: int, comic: ComicBookCreate):
    pool = await init_db()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            UPDATE "ComicBook"
            SET title = $1, author = $2, publish_year = $3, date_read = $4,
                tags = $5::jsonb, my_rating = $6, mood = $7, notes = $8,
                illustrator = $9, volume = $10
            WHERE id = $11
            RETURNING id;
        """,
        comic.title,
        comic.author,
        comic.publish_year,
        comic.date_read,
        json.dumps(comic.tags or []),
        comic.my_rating.value if comic.my_rating else None,
        comic.mood.value if comic.mood else None,
        comic.notes,
        comic.illustrator,
        comic.volume,
        comic_id
        )
        if not row:
            raise HTTPException(status_code=404, detail="ComicBook not found")
        return {"id": comic_id, "message": "ComicBook updated successfully."}


@app.delete("/comicbooks/{comic_id}")
async def delete_comicbook(comic_id: int):
    pool = await init_db()
    async with pool.acquire() as conn:
        row = await conn.fetchrow('DELETE FROM "ComicBook" WHERE id = $1 RETURNING id;', comic_id)
        if not row:
            raise HTTPException(status_code=404, detail="ComicBook not found")
        return {"id": row["id"], "message": "ComicBook deleted successfully."}
