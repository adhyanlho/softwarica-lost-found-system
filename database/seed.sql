-- Seed script for Softwarica Lost & Found System

USE lost_and_found;

-- Sample Users (Passwords hashed or default for test environment)
INSERT INTO users (username, email, password) VALUES
('john_doe', 'john@softwarica.edu.np', 'scrypt:32768:8:1$test_hash_placeholder_1'),
('sarah_k', 'sarah@softwarica.edu.np', 'scrypt:32768:8:1$test_hash_placeholder_2');

-- Sample Items
INSERT INTO items (title, description, category, status, location, user_id) VALUES
('Black HP Laptop', 'Left in Lab 3 on top of table 4.', 'Electronics', 'lost', 'Lab 3', 1),
('Blue Water Bottle', 'Hydroflask found near the college cafeteria.', 'Accessories', 'found', 'Cafeteria', 2),
('College ID Card', 'Found near the ground floor library entrance.', 'Documents', 'claimed', 'Library', 1);