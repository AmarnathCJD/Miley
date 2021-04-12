from sqlalchemy import Boolean, Column, Integer, String, UnicodeText
from Evie.modules.sql import BASE, SESSION


class Nightmode(BASE):
    __tablename__ = "pin_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


Nightmode.__table__.create(checkfirst=True)


def add_chat(chat_id: str):
    nightmoddy = Nightmode(str(chat_id))
    SESSION.add(nightmoddy)
    SESSION.commit()


def rmchat(chat_id: str):
    rmnightmoddy = SESSION.query(Nightmode).get(str(chat_id))
    if rmnightmoddy:
        SESSION.delete(rmnightmoddy)
        SESSION.commit()

def is_chat(chat_id: str):
    try:
        s__ = SESSION.query(Nightmode).get(str(chat_id))
        if s__:
            return str(s__.chat_id)
    finally:
        SESSION.close()

def get_all_chat_id():
    stark = SESSION.query(Nightmode).all()
    SESSION.close()
    return stark

class Cleaned(BASE):
    __tablename__ = "cleaned"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


Cleaned.__table__.create(checkfirst=True)

def is_pin(chat_id: str):
    try:
        s__ = SESSION.query(Cleaned).get(str(chat_id))
        if s__:
            return str(s__.chat_id)
    finally:
        SESSION.close()

def add_pin(chat_id: str):
    nightmoddy = Cleaned(str(chat_id))
    SESSION.add(nightmoddy)
    SESSION.commit()


def rmpin(chat_id: str):
    rmnightmoddy = SESSION.query(Cleaned).get(str(chat_id))
    if rmnightmoddy:
        SESSION.delete(rmnightmoddy)
        SESSION.commit()


def get_all_id():
    stark = SESSION.query(Cleaned).all()
    SESSION.close()
    return stark

