__author__ = 'Usual'

import warnings
warnings.filterwarnings("ignore")

from database import createSchema
from option import options
from parse import run

if __name__ == '__main__':
    if options.init:
        createSchema()

    run()

    print
    print 'All done, enjoy your self.'