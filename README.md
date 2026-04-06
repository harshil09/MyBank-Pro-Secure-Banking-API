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

## 📸 Screenshots

### 🔐 Login Page

<img width="2560" height="1600" alt="login" src="https://github.com/user-attachments/assets/8f94b7aa-a830-439d-a1c0-3cf9951dfa7e" />

### 📝 Signup Page

<img width="2558" height="1387" alt="signup" src="https://github.com/user-attachments/assets/8b9c36cf-14b0-431f-9390-b08e7ecc4028" />

### Google Login

<img width="2559" height="1388" alt="google_login" src="https://github.com/user-attachments/assets/1b662713-2842-4715-90df-8dfddf91be5f" />

### 📊 Dashboard

<img width="2559" height="1387" alt="dashboard" src="https://github.com/user-attachments/assets/297a8666-7881-4cde-bdc9-d262d8c47e8b" />

### 💳 Transactions

<img width="2559" height="1386" alt="transactions" src="https://github.com/user-attachments/assets/cbc59cb8-371f-46d6-b81b-225e02dd4104" />


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
GOOGLE_CLIENT_SECRET=your_secret
GOOGLE_REDIRECT_URI=your_redirect_url
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
## 🌍 Live Demo

- 🎨 Frontend: mybank-pro-secure-banking-api ∙ main ∙ app.py 
- ⚙️ Backend API: https://your-backend-url.onrender.com  

> Try logging in with Google 🚀
---

## 📈 Future Improvements

* PostgreSQL integration
* Docker deployment
* CI/CD pipeline
* Advanced analytics

---

## 👨‍💻 Author

**Harshil Soni**

