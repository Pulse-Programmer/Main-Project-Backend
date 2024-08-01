# Standard library imports

# Remote library imports
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dine_mate_3hmx_user:ZdJtURJw7t35cd1sdssy6tCcJ39xKNy1@dpg-cq9dlrbv2p9s73ci1380-a.oregon-postgres.render.com/dine_mate_3hmx'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False



CORS(app)



@app.route('/')
def index():
     return "Hello, world!"




if __name__ == "__main__":
    app.run(port=5555, debug=True)