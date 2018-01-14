from app import db

class ETF(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(4), index=True, unique=True)
    proportion = db.Column(db.Integer, index=False, unique=False)

    def __repr__(self):
        return '<Ticker {}>'.format(self.ticker)