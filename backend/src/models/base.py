import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.session import make_transient
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

from src.settings import Settings as S


db = SQLAlchemy()
EncryptedString = EncryptedType(db.Unicode, S.AES_SECRET_KEY, AesEngine, 'pkcs5')


class BaseModel(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True)
    # Don't define uuid here - let individual models define it if needed

    @classmethod
    def get_create(cls, *args, **kwargs):
        return cls.get(*args, **kwargs) or cls.create(*args, **kwargs)

    @classmethod
    def get(cls, *args, exception=False, **kwargs):
        result = cls.query.filter_by(*args, **kwargs).first()
        if not result and exception:
            raise Exception('No object matches this query!')
        return result

    @classmethod
    def list(cls, *args, **kwargs):
        return cls.query.filter_by(*args, **kwargs) \
                        .order_by('id') \
                        .all()

    @classmethod
    def create(cls, *args, **kwargs):
        instance = cls(*args, **kwargs)
        # Only generate UUID if the table has uuid column and it's not provided
        instance._try_generate_uuid()
        instance.save()
        return instance

    def _try_generate_uuid(self):
        """Safely try to generate UUID only if uuid column exists."""
        try:
            # Check if uuid column exists in the table
            table_columns = [column.name for column in self.__table__.columns]
            if 'uuid' not in table_columns:
                return
                
            # Only generate if uuid is None
            if hasattr(self, 'uuid') and self.uuid is None:
                self.generate_unique_uuid()
        except Exception:
            # If any error occurs, skip UUID generation silently
            pass

    def generate_unique_uuid(self):
        """Generate unique UUID only if uuid column exists and is not set."""
        try:
            # Double check if uuid column exists
            table_columns = [column.name for column in self.__table__.columns]
            if 'uuid' not in table_columns:
                return
                
            if not hasattr(self, 'uuid') or self.uuid is not None:
                return
                
            potential_uuid = str(uuid.uuid4())
            while self.__class__.get(uuid=potential_uuid):
                potential_uuid = str(uuid.uuid4())
            self.uuid = potential_uuid
        except Exception:
            # If any error occurs, skip UUID generation silently
            pass

    def refresh(self):
        db.session.refresh(self)

    def set(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)

    def clone(self, **fields):
        copy = self.get(id=self.id)
        make_transient(copy)

        copy.set(id=None, **fields)
        copy._try_generate_uuid()

        copy.save()

        return copy

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
