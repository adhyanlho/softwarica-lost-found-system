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

### ### 2. Data Flow Diagrams (DFD)

#### Level 0 DFD (Context Diagram)
```text
+--------------------+   Input (Credentials, Item Reports, Search Queries)   +-----------------------------------------+
|                    | ----------------------------------------------------> |                                         |
|  User / Student    |                                                       |  0.0 Softwarica Lost & Found System     |
|                    | <---------------------------------------------------- |                                         |
+--------------------+   Output (Auth Tokens, Search Results, Item Status)   +-----------------------------------------+
```
### Level 1 DFD (Decomposed Processes)
```text
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
