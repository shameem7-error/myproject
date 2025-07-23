import pandas as pd
import re
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

df = pd.read_csv("phishing.csv")

df.dropna(subset=["url", "class"], inplace=True)

def extract_features_from_url(url):
    features = []
    try:
        features.append(1 if re.match(r"http[s]?://\d+\.\d+\.\d+\.\d+", url) else 0)  
        features.append(1 if len(url) >= 75 else 0)  
        features.append(1 if any(s in url for s in ["bit.ly", "tinyurl", "goo.gl"]) else 0) 
        features.append(1 if "@" in url else 0)
        features.append(1 if url.count("//") > 1 else 0)
        features.append(1 if "-" in url else 0)
        features.append(1 if url.count(".") > 3 else 0)
        features.append(1 if url.startswith("https://") else 0)
        features.append(1 if ":" in url[8:] else 0)

        parts = url.split("/")
        if len(parts) > 2:
            features.append(1 if "https" in parts[2] else 0)
        else:
            features.append(0)

    except Exception as e:
        print("Feature extraction error for URL:", url, "\nError:", e)
        features = [0] * 10

    
    features += [0] * (30 - len(features))
    return features


X = df["url"].apply(extract_features_from_url).tolist()
y = df["class"].astype(int)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


joblib.dump(model, "phishing_model_final.pkl")
print("✅ Model trained and saved as phishing_model_final.pkl")


