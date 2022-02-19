import os
from connector.auth import Auth
from connector.client import Client


username = os.environ['FIBANK_USERNAME']
password = os.environ['FIBANK_PASSWORD']

auth = Auth(username, password)
client = Client(auth)
