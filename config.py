__author__ = 'Usual'

from option import options

class _(object):
    pass

db = _()
xml = None

def updateFromOption():
    print '[+] Update config by options.'

    global xml, db

    db.host = options.host
    db.user = options.user
    db.name = options.database
    db.password = options.password
    db.charset = options.charset

    xml = options.file

updateFromOption()