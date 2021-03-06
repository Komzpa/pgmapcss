#!/usr/bin/env python3
import sys
import re
import pprint
import pgmapcss.parser
import pgmapcss.compiler
import pgmapcss.version
import argparse
import getpass
import pgmapcss.db
import pgmapcss.eval
import os

parser = argparse.ArgumentParser(description='Compiles a MapCSS style description into PostgreSQL functions and builds an accompanying Mapnik stylesheet.')

parser.add_argument('style_id', type=str, help='''\
  style_id is a required argument. The compiled functions will be prefixed
  by 'style_id', e.g. 'style_id_match()'. Also the resulting mapnik style file
  will be called style_id.mapnik.
''')

parser.add_argument('-d', '--database', dest='database',
    default=getpass.getuser(),
    help='Name of database (default: username)')

parser.add_argument('-u', '--user', dest='user',
    default=getpass.getuser(),
    help='User for database (default: username)')

parser.add_argument('-p', '--password', dest='password',
    default='PASSWORD',
    help='Password for database (default: PASSWORD)')

parser.add_argument('-H', '--host', dest='host',
    default='localhost',
    help='Host for database (default: localhost)')

parser.add_argument('-t', '--template', dest='base_style',
    required=True,
    help='mapcss/mapnik base style for the correct mapnik version, e.g. "mapnik-2.0"')

parser.add_argument('--eval-tests', dest='eval_tests', action='store_const',
    const=True, default=False,
    help='Test all eval functions.')

parser.add_argument('-r', '--database-update', dest='database_update',
    default='auto',
    help='Whether the database should be updated to the current version. Possible values: "re-init": re-initializes the database, need to re-compile all pgmapcss styles, "update": update all database functions, "none": do not update, "auto": if necessary a database functions update will be performed.')

def main():
    print('pgmapcss version %s' % pgmapcss.version.VERSION)
    args = parser.parse_args()

    style_id = args.style_id

    m = re.match('(.*)\.mapcss$', style_id)
    if m:
        style_id = m.group(1)

    file_name = style_id + '.mapcss'

    conn = pgmapcss.db.connect(args)

    if args.database_update == 're-init':
        print('* Re-initializing database')
        pgmapcss.db.db_init(conn)

    db_version = pgmapcss.db.db_version()
    if db_version == None:
        print('* DB functions not installed; installing')
        pgmapcss.db.db_init(conn)
    else:
        db_check = pgmapcss.db.db_version_check()
        if db_check == 1 and args.database_update == 'auto':
            print('* Current DB version: {version} -> updating DB functions'.format(**db_version))
            pgmapcss.db.db_update(conn)

        elif db_check == 2:
            print('* Current DB version: {version}'.format(**db_version))
            print('pgmapcss version too new. Database needs to be re-initialized. Please re-run pgmapcss with parameter "-r re-init". All Mapnik styles need to be re-compiled afterwards.')
            sys.exit(1)

        elif args.database_update == 'update':
            pgmapcss.db.db_update(conn)

        else:
            print('* Current DB version: {version}'.format(**db_version))

    if args.eval_tests:
        pgmapcss.eval.functions().test_all()

    stat = {}

    try:
        pgmapcss.parser.parse_file(stat, filename=file_name, base_style=args.base_style)
    except pgmapcss.parser.ParseError as e:
        print(e)
        sys.exit(1)

    debug = open(style_id + '.output', 'w')

    pp = pprint.PrettyPrinter()

    debug.write("***** Structure of parsed MapCSS style *****\n")
    debug.write(pp.pformat(stat) + '\n')

    style = pgmapcss.compiler.compile_style(style_id, stat)

    #pp.pprint(style)
    for i in style:
        debug.write("\n***** " + i + " *****\n" + style[i])

    pgmapcss.db.install(style_id, style, conn)
    pgmapcss.mapnik.process_mapnik(style_id, args, stat, conn)

    debug.close()
    print('Debug output wrote to ' + style_id + '.output')
