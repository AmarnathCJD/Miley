from Evie import tbot, CMD_HELP, BOT_ID, MONGO_DB_URI
from Evie.events import register


client = MongoClient(MONGO_DB_URI)
db = client["evie"]
tmail = db.tempmail

import string
import random
from hashlib import md5
import requests

class TempMail(object):
    def __init__(
        self, login=None, domain=None, api_domain="privatix-temp-mail-v1.p.rapidapi.com"
    ):
        self.login = login
        self.domain = domain
        self.api_domain = api_domain

    def __repr__(self):
        return u"<TempMail [{0}]>".format(self.get_email_address())

    @property
    def available_domains(self):
        if not hasattr(self, "_available_domains"):
            url = "https://{0}/request/domains/".format(self.api_domain)
            req = requests.request("GET", url, headers=self.headers)
            domains = req.json()
            setattr(self, "_available_domains", domains)
        return self._available_domains

    def set_header(self, host, key):
        self.headers = {"x-rapidapi-host": host, "x-rapidapi-key": key}

    def generate_login(self, min_length=6, max_length=10, digits=True):
        chars = string.ascii_lowercase
        if digits:
            chars += string.digits
        length = random.randint(min_length, max_length)
        return "".join(random.choice(chars) for x in range(length))

    def get_email_address(self):
        if self.login is None:
            self.login = self.generate_login()

        available_domains = self.available_domains
        if self.domain is None:
            self.domain = random.choice(available_domains)
        elif self.domain not in available_domains:
            raise ValueError("Domain not found in available domains!")
        return u"{0}{1}".format(self.login, self.domain)

    def get_hash(self, email):
        return md5(email.encode("utf-8")).hexdigest()

    def get_mailbox(self, email=None, email_hash=None):
        if email is None:
            email = self.get_email_address()
        if email_hash is None:
            email_hash = self.get_hash(email)

        url = "https://{0}/request/mail/id/{1}/".format(self.api_domain, email_hash)
        req = requests.get(url, headers=self.headers)
        return req.json()
    
tm = TempMail()
api_host = "privatix-temp-mail-v1.p.rapidapi.com"
api_key = "cf9e67ea99mshecc7e1ddb8e93d1p1b9e04jsn3f1bb9103c3f"
tm.set_header(api_host, api_key) 

#Soon
