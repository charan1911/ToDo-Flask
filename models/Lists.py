from Common.db import db

class Lists(db.Model):
    __tablename__ = "lists"
    
    id =db.Column(db.Integer, primary_key=True)
    ListId = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    # user = db.relationship("User", backref="lists")
    
    def __repr__(self):
        return f"<list {self.name} for User {self.user_id}"