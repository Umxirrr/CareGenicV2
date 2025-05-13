import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('../data/cleaned_data.csv')

X = df.drop(['disease'], axis=1)
y = df['disease']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Save for training
X_train.to_csv('../data/X_train.csv', index=False)
X_test.to_csv('../data/X_test.csv', index=False)
y_train.to_csv('../data/y_train.csv', index=False)
y_test.to_csv('../data/y_test.csv', index=False)

print("Training & test sets saved.")
