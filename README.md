# 🏦 MyBank Pro – Secure Banking API
Secure Banking API with FastAPI &amp; OAuth

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge&logo=fastapi">
  <img src="https://img.shields.io/badge/Streamlit-Frontend-red?style=for-the-badge&logo=streamlit">
  <img src="https://img.shields.io/badge/Auth-JWT%20%2B%20OAuth-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Database-SQLite-lightgrey?style=for-the-badge">
</p>

🚀 A full-stack banking system built with **FastAPI + Streamlit**, featuring **JWT authentication, Google OAuth, and real-time transaction tracking**.

---

## 🎥 Demo

> 🔗 Add your demo video link here (Loom / YouTube)

Example:

```
https://your-demo-link.com
```

---

## 📸 Screenshots

### 🔐 Login Page

![Login](images/login.png)

### 📝 Signup Page

![Signup](images/signup.png)

### 📊 Dashboard

![Dashboard](images/dashboard.png)

### 💳 Transactions

![Transactions](images/transactions.png)

---

## 🔥 Features

* 🔐 **Authentication**

  * Email & Password login (Argon2 hashing)
  * Google OAuth 2.0 login
  * JWT-based session management

* 💰 **Account Management**

  * Check balance
  * Deposit funds
  * Withdraw funds (with validation)

* 📊 **Dashboard (Streamlit UI)**

  * Modern dark UI
  * Transaction history table
  * Real-time balance updates

* 🧾 **Transaction System**

  * Tracks deposits & withdrawals
  * Timestamped records
  * Visual indicators (🟢 / 🔴)

---

## 🛠️ Tech Stack

### 🔹 Backend

* FastAPI
* SQLite
* JWT (python-jose)
* Authlib (Google OAuth)
* Passlib (Argon2 hashing)

### 🔹 Frontend

* Streamlit
* Pandas

---

## 🔐 Authentication Flow

### 1️⃣ Email/Password Login

* Password hashed using **Argon2**
* Verified securely
* JWT token generated

### 2️⃣ Google OAuth Login

* Redirect to Google
* Fetch user profile
* Auto-register user
* Return JWT token

---

## 🔄 API Endpoints

| Method | Endpoint             | Description         |
| ------ | -------------------- | ------------------- |
| POST   | `/signup`            | Register new user   |
| POST   | `/login`             | Login & get JWT     |
| GET    | `/balance`           | Get account balance |
| POST   | `/deposit`           | Deposit money       |
| POST   | `/withdraw`          | Withdraw money      |
| GET    | `/transactions`      | Transaction history |
| GET    | `/auth/google/login` | Google OAuth login  |

---

## ⚙️ Environment Variables

Create a `.env` file:

```env id="env01"
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REDIRECT_URI=http://localhost:5000/auth/google/callback
```

---

## 🚀 How to Run

```bash id="run01"
git clone https://github.com/YOUR_USERNAME/mybank-pro.git
cd mybank-pro
pip install -r requirements.txt
uvicorn main:app --reload
streamlit run app.py
```

---

## 🔐 Security Highlights

* 🔑 Argon2 password hashing
* 🎟️ JWT authentication
* 🔒 Protected routes
* 🛡️ Secure OAuth integration

---

## 📈 Future Improvements

* PostgreSQL integration
* Docker deployment
* CI/CD pipeline
* Advanced analytics

---

## 👨‍💻 Author

**Harshil Soni**

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
