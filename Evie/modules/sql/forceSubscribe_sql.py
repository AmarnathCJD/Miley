#By RoseLoverX
import threading
from Evie.modules.sql import BASE, SESSION
from sqlalchemy import Boolean, Column, Integer, UnicodeText, String


class FSUB(BASE):
    __tablename__ = "fsub"

    chat_id = Column(Integer, primary_key=True)
    is_fsub = Column(Boolean)
    channel = Column(UnicodeText)

    def __init__(self, chat_id, channel="", is_fsub=True):
        self.chat_id = chat_id
        self.channel = channel
        self.is_sudo = is_fsub

    def __repr__(self):
        return "{}".format(self.chat_id)


FSUB.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()

F_CHATS = {}
F_CHATSS = {}


def is_fsub(chat_id):
    return chat_id in F_CHATS
    return chat_id in F_CHATSS


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
        F_CHATS[chat_id] = channel
        F_CHATSS[chat_id] = channel
        SESSION.add(curr)
        SESSION.commit()


def rm_fsub(chat_id):
    with INSERTION_LOCK:
        curr = SESSION.query(FSUB).get(chat_id)
        if curr:
            if chat_id in F_CHATS:  # sanity check
                del F_CHAT[chat_id]
                del F_CHATSS[chat_id]
            SESSION.delete(curr)
            SESSION.commit()
            return True

        SESSION.close()
        return False
def get_all_fsub_id():
    stark = SESSION.query(FSUB).all()
    SESSION.close()
    return stark

def __load_f_chats():
    global F_CHATS
    global F_CHATSS
    try:
        all_channel = SESSION.query(FSUB).all()
        F_CHATS = {chat.channel: chat.channel for chat in all_channel if channel.is_chat}
        F_CHATSS = {chat.channel: chat.channel for chat in all_channel if channel.is_chat}
    finally:
        SESSION.close()


__load_f_chats()
