from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Query

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def query(cls) -> Query:
        return db.session.query(cls)

    @classmethod
    def save_all(self, objects):
        """Save list of objects in database"""
        
        with db.session.begin_nested():
            db.session.bulk_save_objects(objects)

        try:
            db.session.commit()
        except:
            db.session.rollback()

    def save(self, commit=True):
        with db.session.begin_nested():
            db.session.add(self)
            db.session.flush()

        if commit:
            try:
                db.session.commit()
            except:
                db.session.rollback()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
