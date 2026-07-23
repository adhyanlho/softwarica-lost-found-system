# 📋 Project Technical Documentation & Assessment Summary

## 1. System Architecture
The application follows a modular MVC (Model-View-Controller) structure powered by Flask Blueprints (`auth` and `main`). Database connections are managed via custom dynamic context handlers to ensure clean connection teardowns.

## 2. Security Implementations
- **SQL Injection Prevention:** All SQL statements utilize parameterized queries (`%s` placeholders) via `mysql-connector-python`.
- **Cross-Site Scripting (XSS) Mitigation:** Template rendering strictly leverages Jinja2 auto-escaping.
- **File Upload Security:** Uploaded media assets are sanitized using `secure_filename()` to prevent directory traversal attacks.
- **HTTP Security Headers:** Response middleware injects `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, and `X-XSS-Protection`.

## 3. Testing & Defect Resolution Strategy
Automated unit tests cover happy path routing, database handshakes, unauthorized URL access, and invalid input submissions. Custom 404 and 500 error handlers guarantee graceful fallback behavior across all failure scenarios.


### 4. Entity-Relationship Diagram (ERD)
```
+-----------------------------------+         +-----------------------------------+
|               USERS               |         |               ITEMS               |
+-----------------------------------+         +-----------------------------------+
| PK | id            INT (AI)       |<----+   | PK | id            INT (AI)       |
|    | username      VARCHAR(100)   |     |   |    | title         VARCHAR(100)   |
|    | email         VARCHAR(100)   |     +--| FK | user_id       INT            |
|    | password_hash VARCHAR(255)   | (1:N) |    | description   TEXT           |
|    | created_at    TIMESTAMP      |         |    | category      VARCHAR(50)    |
+-----------------------------------+         |    | status        ENUM           |
                                              |    | location      VARCHAR(255)   |
                                              |    | image_url     VARCHAR(255)   |
                                              |    | created_at    TIMESTAMP      |
                                              +-----------------------------------+
```

### ### Data Flow Diagrams (DFD)

#### Level 0 DFD (Context Diagram)
```text
+--------------------+   Input (Credentials, Item Reports, Search Queries)   +-----------------------------------------+
|                    | ----------------------------------------------------> |                                         |
|  User / Student    |                                                       |  0.0 Softwarica Lost & Found System     |
|                    | <---------------------------------------------------- |                                         |
+--------------------+   Output (Auth Tokens, Search Results, Item Status)   +-----------------------------------------+
```
### Level 1 DFD (Decomposed Processes)
```
                  +-----------------------+
                  |  1.0 Authentication   | <====> [ Data Store: D1 - USERS ]
                  +-----------------------+
                              |
                              v
+------------+    +-----------------------+
|  User /    | -> | 2.0 Item Reporting    | ====> [ Data Store: D2 - ITEMS ]
|  Student   |    +-----------------------+
+------------+                |
      ^                       v
      |           +-----------------------+
      +---------  | 3.0 Search & Filter   | <==== [ Data Store: D2 - ITEMS ]
                  +-----------------------+
                              |
                              v
                  +-----------------------+
                  | 4.0 Status & Reclaim  | ====> [ Data Store: D2 - ITEMS ]
                  +-----------------------+
```
## 🏗️ System Architecture & Diagrams

### 1. Entity-Relationship Diagram (ERD)
The system utilizes a 1-to-Many (1:N) relational database model between `users` and `items`. A registered user can report multiple lost or found items, while each item record is strictly associated with one user.

```
+-----------------------------------+         +-----------------------------------+
|               USERS               |         |               ITEMS               |
+-----------------------------------+         +-----------------------------------+
| PK | id            INT (AI)       |<----+   | PK | id            INT (AI)       |
|    | username      VARCHAR(100)   |     |   |    | title         VARCHAR(100)   |
|    | email         VARCHAR(100)   |     +--| FK | user_id       INT            |
|    | password_hash VARCHAR(255)   | (1:N) |    | description   TEXT           |
|    | created_at    TIMESTAMP      |         |    | category      VARCHAR(50)    |
+-----------------------------------+         |    | status        ENUM           |
                                              |    | location      VARCHAR(255)   |
                                              |    | image_url     VARCHAR(255)   |
                                              |    | created_at    TIMESTAMP      |
                                              +-----------------------------------+
```
### 2. Data Flow Diagrams (DFD)
### Level 0 DFD (Context Diagram)
```
+--------------------+   Input (Credentials, Item Reports, Search Queries)   +-----------------------------------------+
|                    | ----------------------------------------------------> |                                         |
|  User / Student    |                                                       |  0.0 Softwarica Lost & Found System     |
|                    | <---------------------------------------------------- |                                         |
+--------------------+   Output (Auth Tokens, Search Results, Item Status)   +-----------------------------------------+
```
### Level 1 DFD (Decomposed Processes)
```
+-----------------------+
                  |  1.0 Authentication   | <====> [ Data Store: D1 - USERS ]
                  +-----------------------+
                              |
                              v
+------------+    +-----------------------+
|  User /    | -> | 2.0 Item Reporting    | ====> [ Data Store: D2 - ITEMS ]
|  Student   |    +-----------------------+
+------------+                |
      ^                       v
      |           +-----------------------+
      +---------  | 3.0 Search & Filter   | <==== [ Data Store: D2 - ITEMS ]
                  +-----------------------+
                              |
                              v
                  +-----------------------+
                  | 4.0 Status & Reclaim  | ====> [ Data Store: D2 - ITEMS ]
                  +-----------------------+
```
### 3. Model-View-Controller (MVC) Mapping
```
+---------------+---------------------------------------------+---------------------------------------------------------------------------------------------------+
| MVC Component | Files in Project                            | Core Responsibility                                                                               |
+---------------+---------------------------------------------+---------------------------------------------------------------------------------------------------+
| Model         | database/schema.sql                         | Defines data schema, relationship constraints (FOREIGN KEY, UNIQUE), auto-incrementing IDs,       |
|               | database/seed.sql                           | and data persistence.                                                                             |
|               | MySQL (users, items)                        |                                                                                                   |
+---------------+---------------------------------------------+---------------------------------------------------------------------------------------------------+
| View          | templates/*.html                            | Renders the HTML5 user interface styled with Bootstrap 5 and dynamic Jinja2 syntax to present     |
|               | (base.html, dashboard.html,                 | data and capture input forms.                                                                     |
|               | report.html, login.html)                    |                                                                                                   |
+---------------+---------------------------------------------+---------------------------------------------------------------------------------------------------+
| Controller    | app/routes/auth.py                          | Handles HTTP routing (GET/POST), form input validation, Werkzeug password hashing, database       |
|               | app/routes/main.py                          | queries, and view rendering.                                                                      |
|               | run.py                                      |                                                                                                   |
+---------------+---------------------------------------------+---------------------------------------------------------------------------------------------------+
```
### 🧪 Phase 4: Defect Log & Testing Matrix
### 1. Defect Log Matrix
```
+-----------+-----------------+------------------------------------------------------------------------------------+----------+----------+-----------------------------------------------------------------------------------+
| Defect ID | Module          | Issue Description                                                                  | Severity | Status   | Fix Applied                                                                       |
+-----------+-----------------+------------------------------------------------------------------------------------+----------+----------+-----------------------------------------------------------------------------------+
| DEF-001   | Database / Auth | seed.sql contained plain-text passwords, causing login failures with Werkzeug.     | High     | Resolved | Updated seed.sql to generate valid scrypt password hashes matching schema.        |
| DEF-002   | Middleware      | Direct URL navigation to /report without active session threw unhandled 500.     | Medium   | Resolved | Added @login_required decorator to redirect unauthenticated users to /login.       |
| DEF-003   | UI / View       | Missing image file path in item post caused broken img tags on dashboard.          | Low      | Resolved | Added default fallback placeholder image in Jinja2 (item.image_url or default).   |
+-----------+-----------------+------------------------------------------------------------------------------------+----------+----------+-----------------------------------------------------------------------------------+
```
### 2. Functional Test Cases
```
+--------------+-----------------+------------------------------------------------------------+-------------------------------------------------------------+-------------+
| Test Case ID | Feature         | Input / Action                                             | Expected Result                                             | Pass / Fail |
+--------------+-----------------+------------------------------------------------------------+-------------------------------------------------------------+-------------+
| TC-001       | User Login      | Submit valid credentials (admin@softwarica.edu.np)         | Redirects to dashboard with active session banner.          | PASS        |
| TC-002       | User Login      | Submit invalid password                                    | Displays error alert: "Invalid email or password."          | PASS        |
| TC-003       | Item Reporting  | Fill lost item form with title, category, location, submit | Item successfully saved to DB and displayed on dashboard.   | PASS        |
| TC-004       | Search / Filter | Type query into search bar on dashboard                    | Dashboard dynamically filters items matching title/category. | PASS        |
+--------------+-----------------+------------------------------------------------------------+-------------------------------------------------------------+-------------+
```
