from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Main(Resource):
    def get(self):
        return {'name': 'stockscraper'}

api.add_resource(Main, '/')

if __name__ == '__main__':
    app.run(debug=True)