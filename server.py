import xgboost as xgb
import pickle
from flask import Flask, request, jsonify
import numpy as np
from FeatureExt import FeatureExtraction
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

loaded_model = pickle.load(open('XgClassifierModel.pk1', 'rb'))



@app.route('/process', methods=['POST'])
def process():
    try:
       
        data = request.json

        if 'url' not in data:
            return jsonify({'error': 'Missing "url" key in JSON request'})

        
        url = data['url']

       
        feature_extractor = FeatureExtraction(
            url)
        features = feature_extractor.extract_all_features()

        
        print(features)
        
        loaded_model_prediction = loaded_model.predict([features])
        
        if (loaded_model_prediction == 1):
            print("LEGITIMATE")
        else:
            print("PHISHING")
        
        print(jsonify({'prediction': loaded_model_prediction.tolist()}))
        return jsonify({'prediction': loaded_model_prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
