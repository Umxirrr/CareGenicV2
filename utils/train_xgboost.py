import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb
import pickle

# Load data
X = pd.read_csv('../data/X.csv')
y = pd.read_csv('../data/y.csv').values.ravel()

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Model
model = xgb.XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42, use_label_encoder=False, eval_metric='mlogloss')
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("📊 Classification Report:\n", classification_report(y_test, y_pred))

# Save model
with open('../models/xgboost_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model saved at: models/xgboost_model.pkl")
