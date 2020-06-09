import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

import csv


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', "mysql+pymysql://udemyapi:Udemyapi2020!@localhost/udemyapi")
db = SQLAlchemy(app)
# app.secret_key = 'jose'
api = Api(app)

# jwt = JWT(app, authenticate, identity) #/auth

# /data list all
# /search?date=2020-3-20
# /author


class RecordModel(db.Model):
    __tablename__ = "covid19"
    id = db.Column(db.Integer, primary_key=True)
    notification_date = db.Column(db.Date)
    postcode = db.Column(db.Integer)
    lhd_2010_code = db.Column(db.String(45))
    lhd_2010_name = db.Column(db.String(100))
    lga_code19 = db.Column(db.Integer)
    lga_name19 = db.Column(db.String(100))

    def __init__(self, not_date, postcode, lhd_code, lhd_name, lga_code, lga_name):
        self.notification_date = not_date
        self.postcode = postcode
        self.lhd_2010_code = lhd_code
        self.lhd_2010_name = lhd_name
        self.lga_code19 = lga_code
        self.lga_name19 = lga_name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_record_by_page(cls, page):
        # each page 20 records
        begin = 1 + 20 * (page - 1)
        ends = page * 20
        print(begin)
        print(ends)
        result = cls.query.filter(cls.id >= begin).filter(cls.id <= ends).all()
        report_json = []
        for r in result:
            notification_date = r.notification_date.strftime('%Y-%m-%d')
            single_report = {
                'id': r.id,
                'notification_date': notification_date,
                'postcode': r.postcode,
                'lhd_2010_code': r.lhd_2010_code,
                'lhd_2010_name': r.lhd_2010_name,
                'lga_code19': r.lga_code19,
                'lga_name19': r.lga_name19
            }
            print(single_report)
            report_json.append(single_report)
        return report_json


class RecordsResource(Resource):

    def get(self, page):
        records = RecordModel.find_record_by_page(page)
        return {'records': records}, 201


class SearchResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('postcode',
                        type=int,
                        required=True,
                        help="This field cannot be blank."
                        )

    def get(self):
        data = SearchResource.parser.parse_args()
        result = RecordModel.query.filter(RecordModel.postcode == data['postcode']).all()
        report_json = []
        for r in result:
            notification_date = r.notification_date.strftime('%Y-%m-%d')
            single_report = {
                'id': r.id,
                'notification_date': notification_date,
                'postcode': r.postcode,
                'lhd_2010_code': r.lhd_2010_code,
                'lhd_2010_name': r.lhd_2010_name,
                'lga_code19': r.lga_code19,
                'lga_name19': r.lga_name19
            }
            print(single_report)
            report_json.append(single_report)
        return {'records': report_json}, 201

class AuthorResource(Resource):
    def get(self):
        return{
            'Author': 'Weikun Ye',
            'LinkedIn': 'https://www.linkedin.com/in/weikunye',
            'Github': 'https://github.com/WeikunYe/'
        }

class LoadDataResource(Resource):
    
    def get(self):
        db.creat_all()
        with open('data.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                print(row)
                if row[0] and row[1] and row[2] and row[3] and row[4] and row[5]:
                    covidRecord = Record(row[0], row[1], row[2], row[3], row[4], row[5])
                    covidRecord.save_to_db()
        return{'message': 'success'}, 201

api.add_resource(RecordsResource, '/records/<int:page>')
api.add_resource(SearchResource, '/search')
api.add_resource(AuthorResource, '/author')
api.add_resource(LoadDataResource, '/initial')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
