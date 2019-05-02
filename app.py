import numpy as np
import tensorflow as tf

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask_jsglue import JSGlue

from keras.models import load_model
from optimizer import NormalizedOptimizer

app = Flask(__name__)
jsglue = JSGlue(app)

def setup_model():
	print(' * Loading Keras model...')

	global model
	global graph

	model = load_model('static/model/model.ckpt', custom_objects={'NormalizedOptimizer': NormalizedOptimizer})
	graph = tf.get_default_graph()

	print(' * Model loaded!')
setup_model()

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
	global model
	global graph

	message = request.get_json(force=True)
	encoded = message['encoded']

	with graph.as_default():
		predictions = list(np.argmax(model.predict(np.array([encoded])).squeeze()[1:-1], axis=-1))

	response = {
		'predictions': predictions
	}

	return jsonify(response)