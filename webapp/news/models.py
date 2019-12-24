from datetime import datetime
from sqlalchemy.orm import relationship
from webapp.db import db

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.String, nullable=True)

    def comments_count(self):
        return Comment.query.filter(Comment.news_id==self.id).count()

    def __repr__(self):
        return f'<News {self.title} {self.url}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    news_id = db.Column(
        db.Integer,
        db.ForeignKey('news.id', ondelete='CASCADE'),
        index=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        index=True
    )
    news = relationship('News', backref='comments')
    user = relationship('User', backref='comments')

    def __repr__(self):
        return f'<Comment {self.id}>'