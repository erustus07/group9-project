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
 
# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    delivery_cost = db.Column(db.Float, nullable=False)
    payment_mode = db.Column(db.String(50), nullable=False)
    shop = db.Column(db.String(100), nullable=False)
    query_id = db.Column(db.Integer, db.ForeignKey('query.id'), nullable=False)
    query = db.relationship('Query', backref='products', lazy=True)

    def add_product(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_products_by_query(query_id):
        return Product.query.filter_by(query_id=query_id).all()

    @staticmethod
    def update_product(product_id, **kwargs):
        product = Product.query.get(product_id)
        if product:
            for key, value in kwargs.items():
                setattr(product, key, value)
            db.session.commit()
        return product

    @staticmethod
    def get_product_by_id(product_id):
        return Product.query.get(product_id)


# Query Model
class Query(db.Model):
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


# MarginalBenefitCalculation Model
class MarginalBenefitCalculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    mb_score = db.Column(db.Float, nullable=False)
    cb_score = db.Column(db.Float, nullable=False)
    product = db.relationship('Product', backref='mb_calculations', lazy=True)

    @staticmethod
    def calculate_mb(product_id, mb_score):
        mb_calc = MarginalBenefitCalculation(product_id=product_id, mb_score=mb_score, cb_score=0.0)
        db.session.add(mb_calc)
        db.session.commit()
        return mb_calc

    @staticmethod
    def calculate_cb(product_id, cb_score):
        mb_calc = MarginalBenefitCalculation.query.filter_by(product_id=product_id).first()
        if mb_calc:
            mb_calc.cb_score = cb_score
            db.session.commit()
        return mb_calc

    @staticmethod
    def get_mb_cb_by_product(product_id):
        return MarginalBenefitCalculation.query.filter_by(product_id=product_id).first()