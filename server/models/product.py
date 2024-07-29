from app import db

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    delivery_cost = db.Column(db.Float, nullable=False)
    payment_mode = db.Column(db.String(50), nullable=False)
    shop = db.Column(db.String(100), nullable=False)
    query_id = db.Column(db.Integer, db.ForeignKey('queries.id'), nullable=False)
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
