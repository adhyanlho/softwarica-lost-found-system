# 🔍 Softwarica Lost & Found Portal

An enterprise-grade Web Application built with **Flask**, **MySQL**, and **Bootstrap/CSS** designed to streamline tracking and returning lost items within Softwarica College.

---

## 🚀 Features

- **Authentication System:** Secure registration and login with encrypted password storage.
- **Interactive Dashboard:** Live summary counters, full-text keyword search, and category filtering.
- **Item Reporting & Uploads:** File upload handling with secure filename sanitation for item photos.
- **Reclaim System:** Ownership verification preventing unauthorized status updates.
- **Security Middleware:** Custom HTTP response security headers (`X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection`).
- **Error Handling:** Custom, user-friendly 404 & 500 error pages.
- **Automated Testing:** Dedicated test suite covering core routes, DB connectivity, and edge cases.

---

## 🛠️ Technology Stack

- **Backend:** Python (Flask, Werkzeug)
- **Database:** MySQL
- **Frontend:** HTML5, CSS3, Jinja2 Templates
- **Testing:** Python `unittest` framework

---

## 🔧 Installation & Setup

### 1. Clone & Setup Virtual Environment
```bash
git clone <repository-url>
cd softwarica-lost-found-system
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Variables Configuration
Create a `.env` file in the project root:
```env
FLASK_SECRET_KEY=your_secret_key_here
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=lost_and_found
```

### 3. Database Initialization & Seeding
Import the base schema and seed data into MySQL:
```bash
mysql -u root -p lost_and_found < database/schema.sql
mysql -u root -p lost_and_found < database/seed.sql
```

### 4. Run Application
```bash
python run.py
```
Visit `http://127.0.0.1:5000` in your browser.

---

## 🧪 Running Automated Tests

To execute the complete unit testing suite and verify edge cases:

```bash
python run_tests.py
```