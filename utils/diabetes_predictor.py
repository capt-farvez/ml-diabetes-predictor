import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load and clean diabetes dataset
def load_and_prepare_data():
    df = pd.read_csv('data/diabetes.csv')
    df = df.rename(columns={'DiabetesPedigreeFunction': 'DPF'})
    df_copy = df.copy(deep=True)
    df_copy[['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']] = df_copy[
        ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    ].replace(0, np.nan)

    df_copy['Glucose'].fillna(df_copy['Glucose'].mean(), inplace=True)
    df_copy['BloodPressure'].fillna(df_copy['BloodPressure'].mean(), inplace=True)
    df_copy['SkinThickness'].fillna(df_copy['SkinThickness'].median(), inplace=True)
    df_copy['Insulin'].fillna(df_copy['Insulin'].median(), inplace=True)
    df_copy['BMI'].fillna(df_copy['BMI'].median(), inplace=True)

    return df_copy

# Train and save model
def train_and_save_model():
    df = load_and_prepare_data()
    X = df.drop(columns='Outcome')
    y = df['Outcome']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

    classifier = RandomForestClassifier(n_estimators=20)
    classifier.fit(X_train, y_train)

    with open('models/diabetes-prediction-rfc-model.pkl', 'wb') as file:
        pickle.dump(classifier, file)
    print("Training Successful ✅")

# Predict using saved model
def predict_diabetes(input_data):
    with open('models/diabetes-prediction-rfc-model.pkl', 'rb') as file:
        classifier = pickle.load(file)

    feature_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
                     'Insulin', 'BMI', 'DPF', 'Age']

    input_df = pd.DataFrame([input_data], columns=feature_names)
    prediction = classifier.predict(input_df)
    return prediction[0]

def get_model_accuracy():
    # print("Calculating model accuracy...")
    df = load_and_prepare_data()
    X = df.drop(columns='Outcome')
    y = df['Outcome']

    with open('models/diabetes-prediction-rfc-model.pkl', 'rb') as file:
        classifier = pickle.load(file)

    y_pred = classifier.predict(X)
    accuracy = accuracy_score(y, y_pred)   # returns a float value between 0 and 1
    # Convert accuracy to percentage
    rounded_accuracy = round(accuracy * 100, 2)
    return rounded_accuracy