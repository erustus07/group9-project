from app import db

class MarginalBenefitCalculation(db.Model):
    __tablename__ = 'marginal_benefit_calculations'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
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
