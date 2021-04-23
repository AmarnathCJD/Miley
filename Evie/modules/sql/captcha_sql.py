import threading
from Evie.modules.sql import BASE, SESSION
from sqlalchemy import Boolean, Column, Integer, String, UnicodeText

class Captcha(BASE):
    __tablename__ = "ct"
    chat_id = Column(String(14), primary_key=True)
    mode = Column(UnicodeText)
    time = Column(Integer)
    style = Column(UnicodeText)
    
    def __init__(self, chat_id, mode, style, time):
        self.chat_id = chat_id
        self.mode = mode
        self.time = time
        self.style = style
        
        
Captcha.__table__.create(checkfirst=True)

C_LOCK = threading.RLock()
CAPTCHA_CHAT = {}

def set_captcha(chat_id, style):
 with C_LOCK:
  global CAPTCHA_CHAT
  captcha = Captcha(
            chat_id,
            "on",
            0,
            style,
  )
  SESSION.add(captcha)
  SESSION.commit()
  CAPTCHA_CHAT = {
    "chat_id": chat_id,
    "mode": "on",
    "time": 0,
    "style": style,
  }
  return captcha
  
