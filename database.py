# coding=utf8
__author__ = 'Usual'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import logging
import MySQLdb

from config import db

conn = None
cur = None

# Create statement
CREATE_NVD = '''
    create table if not exists nvd(
      id int(11) not null auto_increment primary key,
      cve_id varchar(20),
      published_datetime varchar(30),
      last_modified_datetime varchar(30),
      score float,
      access_vector varchar(45),
      access_complexity varchar(45),
      authentication varchar(45),
      confidentiality_impact varchar(45),
      availability_impact varchar(45),
      integrity_impact varchar(45),
      source varchar(45),
      generated_on_datetime varchar(30),
      cwe_id varchar (20),
      summary text(65535)
    );
'''
CREATE_REFERENCE = '''
    create table if not exists reference (
        nvd_id int(11),
        type varchar(45),
        source varchar(45),
        reference varchar(1000),
        url varchar(500)
    );
'''
CREATE_VULNERABLE = '''
    create table if not exists vulnerable (
        nvd_id int(11),
        cpe varchar(255)
    );
'''
CREATE_LOGICAL = '''
    create table if not exists logical_test (
      nvd_id int(11),
      name varchar(255)
    );
'''

# Insert statement.
INSERT_NVD = """
    insert into nvd(
      cve_id, published_datetime, last_modified_datetime,
      score, access_vector, access_complexity, authentication,
      confidentiality_impact, integrity_impact, availability_impact,
      source, generated_on_datetime, cwe_id, summary)
    values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
"""
INSERT_PRODUCT = """
    insert into vulnerable(nvd_id, cpe)
    values(%d, '%s')
"""
INSERT_REFERENCE = """
    insert into reference(nvd_id, type, source, reference, url)
    values(%d, '%s', '%s', '%s', '%s')
"""
INSERT_LOGICAL_TEST = """
    insert into logical_test(nvd_id, name)
    values(%d, '%s')
"""

def createSchema():
    print '[+] Create schema.'
    global conn, cur
    cur.execute(CREATE_NVD)
    cur.execute(CREATE_REFERENCE)
    cur.execute(CREATE_VULNERABLE)
    cur.execute(CREATE_LOGICAL)
    conn.commit()

def connectToDatabase():
    print '[+] Connect to database %s:%s' % (db.host, db.name)
    global conn, cur
    try:
        conn = MySQLdb.connect(host=db.host, user=db.user, passwd=db.password, charset=db.charset, db=db.name, use_unicode=True)
        cur = conn.cursor()
        logging.debug("Connect to host %s with database %s successfully!" % (db.host, db.name))
    except MySQLdb.Error as e:
        print '[-] MySQL error [%d]: %s.' % (e[0], e[1])
        print '[-] If you haven\'t initial databases before, maybe you can run init first.'
        sys.exit()

    # TODO: Complete error reduce.

connectToDatabase()
