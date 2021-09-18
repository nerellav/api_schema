import pymysql
from app import app
from schema_dao import mysql
from flask import jsonify
from flask import flash, request
import schema_dao
import validator
from validator import FileType

#TODO: need to add authorization
@app.route('/create', methods=['POST'])
def create_schema():
    try:
        _json = request.json

        print (_json)
        _application = _json['application']
        _service = _json['service'] or 'ALL'
        _defn = _json['defn']
        print("validating schema")
        filetype = validator.validateFileType(_defn)

        if filetype in (FileType.JSON, FileType.YAML):
            _type = filetype.name
            print("persisting schema")
            schema_dao.createSchema(_application, _type, _defn, _service)

            res = jsonify('schema created successfully.')
            res.status_code = 200
        else:
            res = jsonify("BAD REQUEST: schema couldn't be persisted as it's neither YAML nor JSON")
            res.status_code = 400
        return res
    except Exception as e:
        print(e)

@app.route('/versions/<app_name>')
def versions(app_name):
    try:
        rows = schema_dao.getVersionsByAppName(app_name)
        res = jsonify(rows)
        res.status_code = 200

        return res
    except Exception as e:
        print(e)

@app.route('/schemas')
def schemas():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM api_schema")
        rows = cursor.fetchall()
        res = jsonify(rows)
        res.status_code = 200

        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/schema/<int:schema_id>', endpoint='schema')
def schema(schema_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM api_schema WHERE id=%s", schema_id)
        row = cursor.fetchone()
        res = jsonify(row)
        res.status_code = 200

        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'There is no record: ' + request.url,
    }
    res = jsonify(message)
    res.status_code = 404

    return res

if __name__ == "__main__":
    app.run()
