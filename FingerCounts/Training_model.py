# Import libraries
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load data collected from Data_for_training.py
data = pd.read_csv("data/landmarks.csv")
X = data.drop('label', axis=1)
y = data['label']

# Split the dataset into (1) train and (2) test datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train our own finger counter model (More data is better!)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

# Save trained model
joblib.dump(clf, 'finger_classifier.pkl')
print("Model saved as 'finger_classifier.pkl'")
