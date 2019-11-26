
from .__init__ import Base,Session
from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

from app import login



@login.user_loader
def load_user(user_id):
    session = Session()
    return session.query(User).filter_by(id=int(user_id)).first()

class User( UserMixin, Base):
        __tablename__ = 'user'
        __table_args__ = {'extend_existing': True}
        id = Column(Integer, primary_key=True)
        username = Column(String(64) )
        email = Column(String(120))
        password = Column(String(128))
        imagename = Column(String(128))

        def set_password(self, password):
                self.password = generate_password_hash(password)

        def check_password(self, password):
                return check_password_hash(self.password, password)


        #posts = relationship('Post', backref='author', lazy='dynamic')
class Post( Base ):
            __tablename__ = 'post'
            __table_args__ = {'extend_existing': True}
            id = Column(Integer, primary_key=True)
            body = Column(String(140))
            #timestamp = db.Column(db., index=True, default=DateTime.utcnow)
            user_id = Column(Integer, ForeignKey('user.id'))
