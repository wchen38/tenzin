from mongoengine import *
from flask_login import UserMixin
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    print("======> {}".format(user_id))
    return User.objects(pk=user_id).first()


class User(Document, UserMixin):
    email = StringField(required=True)

    def __repr__(self):
        return f"User('{self.email}')"
