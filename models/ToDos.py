from Common.db import db
from datetime import datetime
from uuid import uuid4


class ToDos(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(255), nullable=False)

    list_id = db.Column(db.String(36), db.ForeignKey('lists.ListId'), nullable=False)

    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    edit_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    delete = db.Column(db.Boolean, default=False)
    status = db.Column(db.Boolean, default=False)  # False = Incomplete, True = Done

    user_id = db.Column(db.String(36), nullable=False)  # Optional: if you want user-level tracking

    def save(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "list_id": self.list_id,
            "create_time": self.create_time.isoformat(),
            "edit_time": self.edit_time.isoformat(),
            "delete": self.delete,
            "status": self.status
        }
