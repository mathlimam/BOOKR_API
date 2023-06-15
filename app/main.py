from flask import Flask, request
from flask_restful import Api, Resource
from models import clientes



app = Flask(__name__)
api = Api(app)


class Creation(Resource):
    def get(self):
        pass

    def post(self):
        req = request.get_json()
        clientes.Client.create(req)


        return req


api.add_resource(Creation, '/create')

if __name__ == "__main__":
    app.run(debug=True)
