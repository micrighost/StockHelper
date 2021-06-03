from app import db
from .db_abstract import DBAbstract
# login manager
from flask_login import UserMixin
from app import login_manager


class Users(DBAbstract, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # relationship
    # users: trade_records = one : many
    trade_records = db.relationship('TradeRecords', backref='users', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def create_trade_record(self, trade_record):
        """創造交易紀錄"""
        self.trade_records.append(trade_record)
        db.session.add(self)
        db.session.commit()


    @login_manager.user_loader
    def user_loader(user_id):
        return Users.query.get(int(user_id))
