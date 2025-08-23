# 🔒 Phishing URL Detector using Machine Learning

This project is a simple yet effective **Phishing URL Detection Web App** built using **Python**, **Flask**, and **Scikit-learn**. It uses machine learning to detect if a given URL is **legitimate** or **phishing** based on patterns, keywords, and URL structure.

---

##  Features

-  Predict if a URL is Phishing or Legitimate
-  Uses a trained ML model (RandomForestClassifier)
-  Feature extraction based on URL structure
-  Web interface using Flask

---

## 📂 Project Structure

 Requirments : 
Flask
scikit-learn
pandas
numpy


---

##  Model Used

**RandomForestClassifier** from `scikit-learn` is used to classify URLs. Features are extracted using basic URL characteristics like:
- Use of IP address
- Use of `https`
- Presence of `@`
- Length of URL
- URL shortening services (e.g., `bit.ly`, `tinyurl`)
- And more...

---

## 🔧 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/phishing-url-detector.git
cd phishing-url-detector
