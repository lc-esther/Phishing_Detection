# 🛡️ Phishing URL Detection using XGBoost + Chrome Extension

This project is a complete phishing detection system using **XGBoost**, a powerful gradient boosting machine learning algorithm, combined with a **Chrome Extension** for real-time URL monitoring and protection. The goal is to identify and block phishing websites before they load, enhancing user safety while browsing the web.

---

## 🚀 Key Features

- 🎯 **High Accuracy Detection** using the XGBoost algorithm.
- 🧠 Uses intelligent feature extraction from URLs (no need for manual blacklists).
- 🔌 **Chrome Extension** integration for real-time detection while browsing.
- 🚫 Displays a **custom warning page** when a phishing URL is detected.
- 🕵️‍♂️ Works dynamically on any URL the user enters in the browser.

---


---

## 🧠 Machine Learning - XGBoost

### ✅ Why XGBoost?
- Handles non-linear relationships well.
- Excellent performance with tabular data.
- Fast and efficient for both training and prediction.
- Provides feature importance, helping understand model decisions.

### 🧪 Model Workflow
1. Preprocessing of URL features (length, symbol count, HTTPS presence, etc.).
2. Training with XGBoost Classifier using labeled phishing & legitimate data.
3. Model saved using `joblib` for real-time use in the extension.

### 📊 Features Used
- Length of URL
- Use of IP address
- Presence of special characters (`@`, `-`, `//`)
- Use of HTTPS
- Count of subdomains and dots
- Suspicious keywords in the domain
- URL shortening and redirection patterns

---

## 🌐 Chrome Extension Integration

- **Real-time URL Capture:** Monitors URLs being accessed by the user.
- **Backend Communication:** Sends the URL to Python backend for ML prediction.
- **Phishing Detection:** If detected, blocks the site and shows a warning.
- **Popup UI:** Optionally shows prediction status to the user.


