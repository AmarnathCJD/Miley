from sqlalchemy import Boolean, Column, Integer, String, UnicodeText
from Evie.modules.sql import BASE, SESSION


class Nightmode(BASE):
    __tablename__ = "sudolist"
    user_id = Column(String(14), primary_key=True)

    def __init__(self, user_id):
        self.user_id = user_id


Nightmode.__table__.create(checkfirst=True)


def addsudo(user_id: str):
    nightmoddy = Nightmode(str(user_id))
    SESSION.add(nightmoddy)
    SESSION.commit()


def rmnightmode(usee_id: str):
    rmnightmoddy = SESSION.query(Nightmode).get(str(user_id))
    if rmnightmoddy:
        SESSION.delete(rmnightmoddy)
        SESSION.commit()


def get_all_user_id():
    stark = SESSION.query(Nightmode).all()
    SESSION.close()
    return stark


def is_nightmode_indb(user_id: str):
    try:
        s__ = SESSION.query(Nightmode).get(str(user_id))
        if s__:
            return str(s__.user_id)
    finally:
        SESSION.close()
