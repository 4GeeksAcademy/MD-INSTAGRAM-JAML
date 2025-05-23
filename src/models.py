from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

followers = Table(
    "Followers",
    db.metadata,
    Column("user_from_id", ForeignKey("User.id")),
    Column("user_to_id", ForeignKey("User.id"))
)

class User(db.Model):

    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(30), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    posts: Mapped[List["Post"]] = relationship(back_populates="author")
    comments: Mapped[List["Comment"]] =  relationship(back_populates="author")
    
    
    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "posts": [post.serialize() for post in self.posts]
            # do not serialize the password, its a security breach
        }

class Post(db.Model):

    __tablename__ = "Post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    
    author: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")
    media: Mapped[list["Media"]] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "comments": [comment.serialize() for comment in self.comments],
            "media": [m.serialize() for m in self.media]
        }

class Comment(db.Model):

    __tablename__ = "Comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(240), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("Post.id"))

    post: Mapped["Post"] = relationship(back_populates="comments")
    author: Mapped["User"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "user_id": self.user_id,
            "post_id": self.post_id
        }


class Media(db.Model):

    __tablename__ = "Media"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("Post.id"))
    url: Mapped[str] = mapped_column(String(240), nullable=False)

    post: Mapped["Post"] = relationship(back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "url": self.url
        }