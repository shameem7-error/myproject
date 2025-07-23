import pandas as pd
import re
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load dataset
df = pd.read_csv("phishing.csv")

# 🧼 Clean missing values
df.dropna(subset=["url", "class"], inplace=True)  # <-- This line fixes your error

# Handcrafted feature extraction function
def extract_features_from_url(url):
    features = []
    features.append(1 if re.match(r"http[s]?://\d+\.\d+\.\d+\.\d+", url) else 0)  # IP address
    features.append(1 if len(url) >= 75 else 0)  # Long URL
    features.append(1 if any(s in url for s in ["bit.ly", "tinyurl", "goo.gl"]) else 0)  # Shorteners
    features.append(1 if "@" in url else 0)
    features.append(1 if url.count("//") > 1 else 0)
    features.append(1 if "-" in url else 0)
    features.append(1 if url.count(".") > 3 else 0)
    features.append(1 if url.startswith("https://") else 0)
    features.append(1 if ":" in url[8:] else 0)
    features.append(1 if "https" in url.split("/")[2] else 0)

    # Pad to 30 features
    features += [0] * (30 - len(features))
    return features

# Extract features and target
X = df["url"].apply(extract_features_from_url).tolist()
y = df["class"].astype(int)  # Ensure labels are integers

# Split, train, save
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier()
model.fit(X_train, y_train)

joblib.dump(model, "phishing_model_final.pkl")
print("✅ Model trained and saved as phishing_model_final.pkl")

