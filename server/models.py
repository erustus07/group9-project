from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    search_history = db.relationship('SearchHistory', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def create_user(self):
        db.session.add(self)
        db.session.commit()


 # SearchHistory Model
class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    query = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def add_search_history(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_search_history(user_id):
        return SearchHistory.query.filter_by(user_id=user_id).all()

    @staticmethod
    def clear_search_history(user_id):
        SearchHistory.query.filter_by(user_id=user_id).delete()
        db.session.commit()
 
