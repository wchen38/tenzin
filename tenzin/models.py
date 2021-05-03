from mongoengine import *
from flask_login import UserMixin
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


class User(Document, UserMixin):
    user_id = StringField()
    email = StringField(required=True)

    def __repr__(self):
        return f"User('{self.email}')"


class Portfolio(Document):
    user = ReferenceField(User)
    appt = DictField()
    latest_trade_id_map = DictField()

    def __repr__(self):
        return f"Portfolio('{self.user.email}')"
