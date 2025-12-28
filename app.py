import os
import pickle
from flask import Flask, request, render_template, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# load the model
with open('reg_model.pkl', 'rb') as f:
    regmodel = pickle.load(f)

# load scaler if available (scaling.pkl)
scaler = None
if os.path.exists('scaling.pkl'):
    with open('scaling.pkl', 'rb') as f:
        scaler = pickle.load(f)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict_api', methods=['POST'])
def predict_api():
    payload = request.get_json(force=True)
    data = payload.get('data') if isinstance(payload, dict) else payload
    if data is None:
        return jsonify({'error': 'no data provided'}), 400

    # accept dict (feature_name->value) or list of values
    if isinstance(data, dict):
        arr = np.array(list(data.values())).reshape(1, -1)
    elif isinstance(data, (list, tuple)):
        arr = np.array(data).reshape(1, -1)
    else:
        return jsonify({'error': 'unsupported data format'}), 400

    # check expected feature counts from scaler/model if available
    expected = None
    if scaler is not None and hasattr(scaler, 'n_features_in_'):
        expected = int(scaler.n_features_in_)
    if hasattr(regmodel, 'n_features_in_'):
        expected = int(regmodel.n_features_in_) if expected is None else expected

    provided = arr.shape[1]
    if expected is not None and provided != expected:
        return jsonify({
            'error': 'feature_count_mismatch',
            'message': f'Provided {provided} features but model expects {expected}.',
            'provided': provided,
            'expected': expected,
            'received_values': arr.tolist()[0]
        }), 400

    if scaler is not None:
        try:
            arr = scaler.transform(arr)
        except Exception as e:
            return jsonify({'error': 'scaler_transform_failed', 'message': str(e)}), 500

    try:
        output = regmodel.predict(arr)
    except Exception as e:
        return jsonify({'error': 'prediction_failed', 'message': str(e)}), 500

    return jsonify({'prediction': float(output[0])})


if __name__ == '__main__':
    app.run(debug=True)