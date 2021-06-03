from app import db


class DBAbstract(db.Model):
    __abstract__ = True

    def update_attr(self, attr: dict):
        """動態調整欄位"""
        for key, item in attr.items():
            setattr(self, key, item)
        db.session.add(self)
        db.session.commit()

    @classmethod
    def create(cls, **kwargs):
        """新增"""
        obj = cls(**kwargs)
        db.session.add(obj)
        db.session.commit()
        return obj

    @staticmethod
    def db_session_bind():
        return db.session.bind
