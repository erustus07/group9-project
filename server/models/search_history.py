from app import db
from datetime import datetime

class SearchHistory(db.Model):
    __tablename__ = 'search_histories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
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
