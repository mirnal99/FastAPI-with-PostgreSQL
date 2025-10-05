from enum import Enum
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Genre(str, Enum):
    fiction = "fiction"
    nonfiction = "nonfiction"
    fantasy = "fantasy"
    mystery = "mystery"
    biography = "biography"
    sci_fi = "sci-fi"
    romance = "romance"
    other = "other"

class Rating(str, Enum):
    one = "1"
    two = "2"
    three = "3"
    four = "4"
    five = "5"

class Mood(str, Enum):
    happy = "happy"
    emotional = "emotional"
    thoughtful = "thoughtful"
    inspired = "inspired"
    bored = "bored"
    confused = "confused"
    relaxed = "relaxed"
    amused = "amused"
    indifferent = "indifferent"
    nostalgic = "nostalgic"
    excited = "excited"
    overwhelmed = "overwhelmed"

class ReadingsBase(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publish_year: Optional[str] = None
    date_read: Optional[date] = None
    tags: Optional[List[str]] = None
    my_rating: Optional[Rating] = None
    mood: Optional[Mood] = None
    notes: Optional[str] = None


class BookCreate(ReadingsBase):
    genre: Optional[Genre] = None
    page_count: Optional[int] = None
    ISBN: Optional[str] = None


class ArticleCreate(ReadingsBase):
    journal: Optional[str] = None
    DOI: Optional[str] = None


class ComicBookCreate(ReadingsBase):
    illustrator: Optional[str] = None
    volume: Optional[int] = None
