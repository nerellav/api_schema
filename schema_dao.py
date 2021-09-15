import pymysql

from app import app
from flaskext.mysql import MySQL

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'user_write'
app.config['MYSQL_DATABASE_PASSWORD'] = 'U$erWr1te'
app.config['MYSQL_DATABASE_DB'] = 'schema_rest'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()


def getRevision(app_name, schema_type, service_name='ALL'):

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT coalesce(MAX(REVISION),0)+1 as revision FROM api_schema WHERE type=%s AND application=%s "
                   "AND service=%s ORDER BY revision DESC LIMIT 1", (schema_type, app_name, service_name))
    row = cursor.fetchone()
    return row['revision']

def getVersionsByAppName(app_name):

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT application,service,type,revision,defn FROM api_schema WHERE application=%s "
                   "ORDER BY service,revision", app_name)
    rows = cursor.fetchall()
    return rows

def getSchema(app_name, schema_type, service_name=None):

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if service_name is not None:
        cursor.execute("SELECT defn FROM api_schema WHERE type=%s and application=%s and service=%s order by revision",
                       (schema_type, app_name, service_name))
    else:
        cursor.execute("SELECT defn FROM api_schema WHERE type=%s and application=%s", (schema_type, app_name))
    row = cursor.fetchone()
    return row

def createSchema(app_name, schema_type, defn, service_name='ALL'):
    # insert schema in database
    sqlQuery = "INSERT INTO api_schema(application,service,type,revision,defn) VALUES(%s, %s, %s, %s, %s)"

    revision = getRevision(app_name, schema_type, service_name)
    print(revision)

    data = (app_name, service_name, schema_type, revision, defn)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sqlQuery, data)
    conn.commit()