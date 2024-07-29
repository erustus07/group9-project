from app import db
from datetime import datetime

class Query(db.Model):
    __tablename__ = 'queries'
    
    id = db.Column(db.Integer, primary_key=True)
    search_term = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def create_query(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_query_by_id(query_id):
        return Query.query.get(query_id)

    @staticmethod
    def get_all_queries():
        return Query.query.all()
