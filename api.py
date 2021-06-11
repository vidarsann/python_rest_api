from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)


class Users(Resource):

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('userId', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('city', required=True)

        args = parser.parse_args()

        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            return {
                'message': f"'{args['userId']}' already exists."
            }, 401
        else:
            new_data = pd.DataFrame({
                'userId': args['userId'],
                'name': args['name'],
                'city': args['city'],
                'locations': [[]]
            })
            
            data = data.append(new_data, ignore_index=True)
            data.to_csv('users.csv', index=False)

            return {'data': data.to_dict()}, 200

    def get(self):
        data = pd.read_csv('users.csv')
        data = data.to_dict()
        return {'data': data}, 200
    
class Locations(Resource):
    pass
    
api.add_resource(Users, '/users')
api.add_resource(Locations, '/locations')

if __name__ == '__main__':
    app.run()