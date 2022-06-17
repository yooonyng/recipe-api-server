from flask import Flask
from flask_restful import Api

from resources.recipe import RecipelistResource

app = Flask(__name__)
api = Api(app)

# 경로와 리소스(API 코드)를 연결한다.
api.add_resource(RecipelistResource,'/recipes')


if __name__ == '__main__':
    app.run()
