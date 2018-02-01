from db import db

class Stock(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(45))
    product = db.Column(db.String(45))
    amount = db.Column(db.Integer)
    date = db.Column(db.String(45))
    recby= db.Column(db.String(50))

    def __init__(self, *args, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def json(self):
        return {
            'id': self.id,
            'type': self.type,
            'product': self.product,
            'amount': self.amount,
            'date': self.date,
            'recby': self.recby
        }


    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

        