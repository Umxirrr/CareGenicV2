import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle

# Load data
df = pd.read_csv('../data/healthcare_dataset_caregenic_cleaned.csv')

# Get all unique symptoms from both columns
unique_symptoms = pd.unique(df[['symptoms_1', 'symptoms_2']].values.ravel())

# Create binary features for each symptom
for symptom in unique_symptoms:
    df[symptom] = ((df['symptoms_1'] == symptom) | (df['symptoms_2'] == symptom)).astype(int)

# Encode disease labels
le = LabelEncoder()
df['disease_encoded'] = le.fit_transform(df['disease'])

# Save the encoder
with open('../models/label_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)

# Create final dataset
X = df[unique_symptoms]                # One-hot symptom matrix
y = df['disease_encoded']              # Encoded disease labels

# Save them
X.to_csv('../data/X.csv', index=False)
y.to_csv('../data/y.csv', index=False)

print("✅ Preprocessing complete.")
print("🔁 Symptoms encoded:", list(unique_symptoms))
print("🧠 Encoded diseases:", list(le.classes_))
