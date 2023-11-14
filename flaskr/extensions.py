from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def find_by_id(cls, identifier):
        return cls.query.get(identifier)

    @classmethod
    def simple_filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs)

    def save(self):
        db.session.add(self)
        db.session.commit()
