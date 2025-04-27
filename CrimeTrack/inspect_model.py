import pickle
import os

# Path to model.pkl
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'Model', 'model.pkl')

# Load the model
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Inspect model features
if hasattr(model, 'feature_names_in_'):
    print("✅ Model expects these features:\n", model.feature_names_in_)
else:
    print("⚠️ Model does not store feature names.")

if hasattr(model, 'n_features_in_'):
    print("\nℹ️ Number of input features expected:", model.n_features_in_)

print("\n🔍 Model type:", type(model))
