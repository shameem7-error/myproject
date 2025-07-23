from flask import Flask, render_template, request
import joblib
import re
import os

app = Flask(__name__)
model = joblib.load("phishing_model_final.pkl")

def extract_features_from_url(url):
    features = []
    features.append(1 if re.match(r"http[s]?://\d+\.\d+\.\d+\.\d+", url) else 0)
    features.append(1 if len(url) >= 75 else 0)
    features.append(1 if any(s in url for s in ["bit.ly", "tinyurl", "goo.gl"]) else 0)
    features.append(1 if "@" in url else 0)
    features.append(1 if url.count("//") > 1 else 0)
    features.append(1 if "-" in url else 0)
    features.append(1 if url.count(".") > 3 else 0)
    features.append(1 if url.startswith("https://") else 0)
    features.append(1 if ":" in url[8:] else 0)
    features.append(1 if "https" in url.split("/")[2] else 0)
    features += [0] * (30 - len(features))
    return features

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        url = request.form.get("url", "").strip()

        # ✅ Input validation
        if not url:
            result = "⚠️ Please enter a URL."
        elif not re.match(r"^https?://", url):
            result = "⚠️ Invalid URL format. Make sure it starts with http:// or https://"
        else:
            try:
                features = extract_features_from_url(url)
                prediction = model.predict([features])[0]
                result = "❌ Phishing Site" if prediction == 1 else "✅ Legitimate Site"
            except Exception as e:
                result = f"⚠️ Error during prediction: {str(e)}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)





