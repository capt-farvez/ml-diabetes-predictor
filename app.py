from flask import Flask, render_template, request
from utils.diabetes_predictor import predict_diabetes, train_and_save_model
import os

app = Flask(__name__)


MODEL_PATH = 'models/diabetes-prediction-rfc-model.pkl'

# Only train the model if it doesn't exist
if not os.path.exists(MODEL_PATH):
    train_and_save_model() 

@app.route('/')
def home():
    return render_template('diabetes.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = [float(request.form[key]) for key in [
            'pregnancies', 'glucose', 'bloodpressure', 'skinthickness',
            'insulin', 'bmi', 'dpf', 'age'
        ]]
        result = predict_diabetes(input_data)
        if result == 1:
            return render_template('diabetes.html', prediction_text="Possible Diabetes")
        elif result == 0:
            return render_template('diabetes.html', prediction_text="Not Possible Diabetes")
        else:
            return render_template('diabetes.html', prediction_text="Unknown Result")

    except Exception as e:
        return render_template('diabetes.html', prediction_text=f"Input Error: {e}")

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)