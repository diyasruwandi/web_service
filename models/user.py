from . import db
from flask_bcrypt import Bcrypt
import enum


bcrypt = Bcrypt()


class RoleEnum(enum.Enum):
      user = "user"
      admin = "admin"


class User(db.Model):
     __tablename__ = "users"


     id = db.Column(db.Integer, primary_key=True)
     email = db.Column(db.String(255), unique=True, nullable=False)
     password = db.Column(db.String(255), nullable=False)
     role = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.user)


     def set_password(self, plain_password):
         self.password = bcrypt.generate_password_hash(plain_password).decode('utf-8')


     def check_password(self, plain_password):
         return bcrypt.check_password_hash(self.password, plain_password)