from datetime import datetime
from app.models.db import db

class SongItem(db.Model):
    __tablename__ = 'song_item'

    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    singer = db.Column(db.String(255))
    singer_id = db.Column(db.String(255))
    mark = db.Column(db.String(255))
    label = db.Column(db.String(255))
    src = db.Column(db.String(255))
    index = db.Column(db.Integer)
    lyric = db.Column(db.String(255))
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
    # belong to which list
    list_id = db.Column(db.Integer)

    def __init__(self, song_item):
        self.song_id = song_item['id']
        self.title = song_item['title']
        self.singer = song_item['singer']
        self.singer_id = song_item.get('singer_id')
        self.mark = song_item.get('mark')
        self.label = song_item.get('label')
        self.src = song_item['src']
        self.index = song_item.get('index')
        self.lyric = song_item.get('lyric')
        self.is_deleted = False
        self.list_id = song_item.get('list_id')

    def to_dict(self):
        return {
            'id': self.song_id,
            'title': self.title,
            'singer': self.singer,
            'singer_id': self.singer_id,
            'mark': self.mark,
            'label': self.label,
            'src': self.src,
            'index': self.index,
            'lyric': self.lyric,
            'update_time': self.update_time.isoformat(),
            'is_deleted': self.is_deleted,
            'list_id': self.list_id
        }