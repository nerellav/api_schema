import pymysql

from app import app
from flaskext.mysql import MySQL
import keyring

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'b4cdf9d522bef1'
# TODO: Remove plain text password
app.config['MYSQL_DATABASE_PASSWORD'] = 'f536a02f' # keyring.get_password("MYSQL", "DB_PASSWORD")  # 'f536a02f'
app.config['MYSQL_DATABASE_DB'] = 'heroku_06d7bc3ba0de240'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-04.cleardb.com'

mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()


def getRevision(app_name, schema_type, service_name='ALL'):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # if the connection was lost, then it reconnects
    conn.ping(reconnect=True)
    cursor.execute("SELECT coalesce(MAX(REVISION),0)+1 as revision FROM api_schema WHERE type=%s AND application=%s "
                   "AND service=%s ORDER BY revision DESC LIMIT 1", (schema_type, app_name, service_name))
    row = cursor.fetchone()
    return row['revision']

def getVersionsByAppName(app_name):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # if the connection was lost, then it reconnects
    conn.ping(reconnect=True)
    cursor.execute("SELECT application,service,type,revision,defn FROM api_schema WHERE application=%s "
                   "ORDER BY service,revision", app_name)
    rows = cursor.fetchall()
    return rows

def getSchemas():
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    conn.ping(reconnect=True)
    cursor.execute("SELECT * FROM api_schema")
    rows = cursor.fetchall()
    return rows

def getSchemaById(schema_id):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    conn.ping(reconnect=True)
    cursor.execute("SELECT * FROM api_schema where id = %s", (schema_id))
    row = cursor.fetchone()
    return row

def getSchema(app_name, schema_type, service_name=None):
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # if the connection was lost, then it reconnects
    conn.ping(reconnect=True)
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

    # TODO: same revision may come for different records; need to use a sequence instead of this.
    revision = getRevision(app_name, schema_type, service_name)
    print(revision)
    # TODO: Should have application & service in a different table
    data = (app_name, service_name, schema_type, revision, defn)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # if the connection was lost, then it reconnects
    conn.ping(reconnect=True)
    cursor.execute(sqlQuery, data)
    conn.commit()
