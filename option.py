__author__ = 'Usual'

from optparse import OptionParser
from optparse import OptionGroup

options = None

def parseOptions():
    """
    Parse options from command line.
    :return options
    """
    global options
    print '[+] Parse options from command line'

    usage = '''%prog -f <filename> [options]

        Python script translate NVD data feeds into MySQL.
        Power by Usual@Asuri <532000663@qq.com>
    '''
    version = 'v1.0'

    parser = OptionParser(usage=usage, version=version)
    parser.add_option('-f', '--file', dest='file', metavar='FILE',
                     help='NVD feed xml file to open with')

    database = OptionGroup(parser, 'Database', 'Specific your own database connection.')
    parser.add_option_group(database)

    database.add_option('-H', dest='host', default='localhost',
                     help='MySQL host default \'%default\'')
    database.add_option('-u', dest='user', default='root',
                     help='MySQL user to log in default \'%default\'')
    database.add_option('-p', dest='password', default='',
                     help='MySQL password to login default \'%default\'')
    database.add_option('-d', dest='database', default='nvd',
                     help='MySQL database default \'%default\'')
    database.add_option('-c', dest='charset', default='utf8',
                      help='MySQL character default \'%default\'')
    database.add_option('--init-database', dest='init',
                      action='store_true', default=False,
                      help='Initial database and create basic tables.')

    (options, _) = parser.parse_args()

    if not options.file:
        parser.error('Missing a mandatory option -f, '
                     'input file name or use -h for more help.')

parseOptions()