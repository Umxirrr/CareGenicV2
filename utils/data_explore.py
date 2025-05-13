import pandas as pd

# Load your dataset
df = pd.read_csv('../data/healthcare_dataset_caregenic_cleaned.csv')

# Show dataset info
print("🔍 Dataset Shape:", df.shape)
print("\n🧩 Columns:\n", df.columns.tolist())
print("\n📄 First 5 Rows:\n", df.head())

# Check for missing values
print("\n⚠️ Missing Values:\n", df.isnull().sum())

# Show unique diseases and symptoms
print("\n🦠 Unique Diseases:", df['disease'].nunique())
print("💊 Sample Diseases:", df['disease'].unique()[:10])

print("\n🩺 Sample Symptoms 1:", df['symptoms_1'].unique()[:10])
print("🩺 Sample Symptoms 2:", df['symptoms_2'].unique()[:10])
