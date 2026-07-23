USE lost_and_found;

-- Clear existing data and reset auto-increment counters
DELETE FROM items;
DELETE FROM users;
ALTER TABLE users AUTO_INCREMENT = 1;
ALTER TABLE items AUTO_INCREMENT = 1;

-- Seed Users (Matching column: password_hash)
INSERT INTO users (id, username, email, password_hash) VALUES
(1, 'john_doe', 'john@softwarica.edu.np', 'pbkdf2:sha256:600000$dummyhash123'),
(2, 'jane_smith', 'jane@softwarica.edu.np', 'pbkdf2:sha256:600000$dummyhash456');

-- Seed Items
INSERT INTO items (title, description, category, status, location, user_id, image_url) VALUES
('Black HP Laptop', 'Lost in Block B Room 302 on Tuesday afternoon.', 'Electronics', 'lost', 'Block B Room 302', 1, NULL),
('Silver Water Bottle', 'Found near the cafeteria counter.', 'Personal Belongings', 'found', 'Cafeteria', 2, NULL),
('College Student ID', 'Lost student ID card near the main gate.', 'Documents', 'lost', 'Main Gate', 1, NULL);