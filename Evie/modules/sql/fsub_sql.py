# timer added

import threading
import time
from Evie.modules.sql import BASE, SESSION
from sqlalchemy import Boolean, Column, Integer, UnicodeText, String


class FSUB(BASE):
    __tablename__ = "forcesub"

    chat_id = Column(Integer, primary_key=True)
    is_chat = Column(Boolean)
    channel = Column(UnicodeText)

    def __init__(self, chat_id, channel="", is_chat=True):
        self.chat_id = chat_id
        self.channel = channel
        self.is_chat = is_chat

    def __repr__(self):
        return "{}".format(self.chat_id)


FSUB.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()

FSUB_CHATS = {}


def is_chat(chat_id):
    return chat_id in FSUB_CHATS


def check_fsub_status(chat_id):
    try:
        return SESSION.query(FSUB).get(chat_id)
    finally:
        SESSION.close()


def set_fsub(chat_id, channel):
    with INSERTION_LOCK:
        curr = SESSION.query(FSUB).get(chat_id)
        if not curr:
            curr = FSUB(chat_id, channel, True)
        else:
            curr.is_chat = True
            curr.channel = channel
        FSUB_CHATS[chat_id] = channel
        SESSION.add(curr)
        SESSION.commit()


def rm_fsub(chat_id):
    with INSERTION_LOCK:
        curr = SESSION.query(FSUB).get(chat_id)
        if curr:
            if chat_id in FSUB_CHATS:  # sanity check
                del FSUB_CHATS[chat_id]
            SESSION.delete(curr)
            SESSION.commit()
            return True

        SESSION.close()
        return False


def __load_fsub_chats():
    global FSUB_CHATS
    try:
        all_chat = SESSION.query(FSUB).all()
        FSUB_CHATS = {chat.chat_id: chat.channel for chat in all_chat if chat.is_chat}
    finally:
        SESSION.close()


__load_fsub_chats()
