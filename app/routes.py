import os
import base64

from app import app
from io import BytesIO
from .utils import make_mnist
from skimage import io as skio
from sklearn.externals import joblib
from flask import render_template, request, make_response, jsonify
    
@app.route('/')
def main():
    return render_template('main.html')

dirname = os.path.dirname(__file__)
knn_path = os.path.join(dirname, 'classifiers', 'knn.pkl')
random_forest_path = os.path.join(dirname, 'classifiers', 'random-forest.pkl')
svm_path = os.path.join(dirname, 'classifiers', 'svm.pkl')

models = {
    'knn': joblib.load(knn_path),
    'svm': joblib.load(svm_path),
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