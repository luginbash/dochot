from imaplib import IMAP4_SSL
from ruamel.yaml import YAML


def retrieveMail(hostname, password, mailbox=None):
    mailbox = 'INBOX' or None
    with IMAP4_SSL(hostname) as M:
        M.login(username,password)
        M.select(mailbox)
    

if __name__ == '__main__':
    with open('config.yaml','r') as f:
        conf = YAML().load(f)
    
