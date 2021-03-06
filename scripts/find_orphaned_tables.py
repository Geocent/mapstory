'''
Find (and delete if told to):
* orphaned geometry tables - those in geometry_columns but with no corresponding
  Layer objects
* Layer objects with no geoserver record or no corresponding table
'''

from geonode.maps.models import Layer
from script_utils import open_db_datastore_connection
import sys

def msg(msg, star=None):
    if star:
        print '*' * star, msg, '*' * star
        print
    else:
        print msg
        print '-' * len(msg)

run = 'run' in sys.argv
if not run:
    msg('DRY RUN ONLY!', star=8)
conn = open_db_datastore_connection()
cur = conn.cursor()
cur.execute("SELECT f_table_name from geometry_columns")

tables = set([r[0] for r in cur.fetchall()])
layer_tables = set()

no_table = set()

for l in Layer.objects.all():
    r = l.resource
    if r is None:
        print l, 'is bunk'
        if run:
            l.delete()
        continue
    r.fetch()
    if r.dom.tag == 'coverage': continue
    table = r.dom.find('nativeName').text
    if table in layer_tables:
        print table, 'is repeat'
    if table not in tables:
        no_table.add(l)
    else:
        tables.remove(table)

msg('Layer objects w/ no table')
if not no_table:
    msg('None', star=2)
for i in sorted(no_table):
    print i
    if run:
        i.delete()

print
msg('Geometry tables with no Layer')
if not tables:
    msg('None', star=2)
for i in sorted(tables):
    print i
    if run:
        cur.execute('DROP TABLE IF EXISTS %s;' % i)
        cur.execute("DELETE FROM geometry_columns WHERE f_table_name='%s'" % i)
        conn.commit()
