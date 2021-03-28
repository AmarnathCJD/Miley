from sqlalchemy import Boolean, Column, Integer, String, UnicodeText
from Evie.modules.sql import BASE, SESSION


class Sudo(BASE):
    __tablename__ = "sudousers"
    iid = Column(String(10), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


Sudo.__table__.create(checkfirst=True)


def addsudo(iid: str):
    nightmoddy = Sudo(str(iid))
    SESSION.add(nightmoddy)
    SESSION.commit()


def rmsudo(iid: str):
    rmnightmoddy = SESSION.query(Sudo).get(str(iid))
    if rmnightmoddy:
        SESSION.delete(rmnightmoddy)
        SESSION.commit()


def get_all_sudo():
    stark = SESSION.query(Sudo).all()
    SESSION.close()
    return stark


def is_sudo(iid: str):
    try:
        s__ = SESSION.query(Sudo).get(str(iid))
        if s__:
            return str(s__.chat_id)
    finally:
        SESSION.close()
