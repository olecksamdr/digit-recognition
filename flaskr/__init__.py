import os
import base64

from io import BytesIO
from .utils import make_mnist
from skimage import io as skio
from sklearn.externals import joblib
from flask import Flask, render_template, request, make_response, jsonify

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    app.config.from_pyfile('config.py', silent=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def main():
        return render_template('main.html')

    dirname = os.path.dirname(__file__)
    knn_path = os.path.join(dirname, 'classifiers', 'knn.pkl')
    random_forest_path = os.path.join(dirname, 'classifiers', 'random-forest.pkl')
    
    models = {
        'knn': joblib.load(knn_path),
        'random-forest': joblib.load(random_forest_path),
    }
    
    @app.route('/models/<string:model_name>', methods=['POST'])
    def knn_classifier(model_name):
        data = request.get_json(silent=True)['image']
        data = data[22:]

        # select only alpha channel
        img = skio.imread(BytesIO(base64.b64decode(data)))[:,:,3]
        img = make_mnist(img)
        
        if model_name in models:
            number = models[model_name].predict(img.reshape(1, -1))[0]
            return jsonify({ 'number': str(number) })
        else:
            return jsonify({ 'number': "null" })

    return app