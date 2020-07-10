from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:19800506abcD@127.0.0.1'#(替换成自己的用户名，密码和dsn）
db = SQLAlchemy(app)
class testflask(db.Model):  #创建model，对应数据库中的表
    Id_P = db.Column(db.Integer, primary_key=True)
    LastName = db.Column(db.String(255))
    FirstName = db.Column(db.String(255))
    Address = db.Column(db.String(255))
    City = db.Column(db.String(255))

@app.route('/test/list', methods=['GET'])
def get_data():
    myData = testflask.query.all()
    output = []
    for record in myData:
        r_data = {}
        r_data['Id_P'] = record.Id_P
        r_data['FirstName'] = record.FirstName
        r_data['LastName'] = record.LastName
        r_data['Address'] = record.Address
        r_data['City'] = record.City
        output.append(r_data)
    return jsonify({'message': output})

if __name__ == '__main__':
    app.run(debug=True)
