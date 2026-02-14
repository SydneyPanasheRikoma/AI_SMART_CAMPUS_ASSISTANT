-- Sample data for AI Smart Campus Assistant
USE campus_assistant;

-- Insert categories
INSERT INTO categories (category_name, department, description) VALUES
('IT Issues', 'Information Technology', 'Computer labs, network, software issues'),
('Hostel Management', 'Hostel Administration', 'Room allocation, maintenance, food quality'),
('Academics', 'Academic Affairs', 'Course registration, exam queries, faculty issues'),
('Administration', 'General Administration', 'Documentation, certificates, general queries'),
('Library', 'Library Department', 'Book availability, membership, facility issues'),
('Sports & Recreation', 'Sports Department', 'Sports facilities, equipment, events'),
('Other', 'General', 'Miscellaneous complaints');

-- Insert sample admin (password: admin123 - hashed with bcrypt)
-- Note: In production, use proper password hashing
INSERT INTO admins (name, email, password_hash, role, department) VALUES
('Admin User', 'admin@campus.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oVzYKpP7oDuG', 'admin', 'IT'),
('IT Manager', 'it.admin@campus.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oVzYKpP7oDuG', 'admin', 'IT'),
('Hostel Warden', 'hostel.admin@campus.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oVzYKpP7oDuG', 'admin', 'Hostel');

-- Insert sample students (password: student123 - hashed with bcrypt)
INSERT INTO users (name, email, password_hash, phone, department, roll_number) VALUES
('John Doe', 'john.doe@student.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oVzYKpP7oDuG', '1234567890', 'Computer Science', 'CS2021001'),
('Jane Smith', 'jane.smith@student.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oVzYKpP7oDuG', '1234567891', 'Electronics', 'EC2021002'),
('Mike Johnson', 'mike.johnson@student.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oVzYKpP7oDuG', '1234567892', 'Mechanical', 'ME2021003'),
('Sarah Williams', 'sarah.williams@student.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oVzYKpP7oDuG', '1234567893', 'Civil', 'CE2021004'),
('David Brown', 'david.brown@student.edu', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oVzYKpP7oDuG', '1234567894', 'Computer Science', 'CS2021005');

-- Insert sample complaints with different statuses and categories
INSERT INTO complaints (student_id, category, description, priority, status, ai_category, sentiment_score, predicted_resolution_time, submitted_at, assigned_to) VALUES
(1, 'IT Issues', 'Internet connection is very slow in the computer lab. Unable to download required software for assignments.', 'High', 'In Progress', 'IT Issues', -0.3, 24, DATE_SUB(NOW(), INTERVAL 2 DAY), 'IT'),
(2, 'Hostel Management', 'The hot water system in hostel block B is not working for the past 3 days. We need immediate attention.', 'High', 'Pending', 'Hostel Management', -0.5, 12, DATE_SUB(NOW(), INTERVAL 1 DAY), 'Hostel'),
(3, 'Library', 'Required textbooks for the course "Data Structures" are not available in the library. Please add more copies.', 'Medium', 'Resolved', 'Library', 0.0, 48, DATE_SUB(NOW(), INTERVAL 5 DAY), 'Library'),
(4, 'Academics', 'The exam schedule has conflicts. Two exams are scheduled on the same day with only 2 hours gap.', 'High', 'Resolved', 'Academics', -0.2, 72, DATE_SUB(NOW(), INTERVAL 7 DAY), 'Academics'),
(5, 'Sports & Recreation', 'The basketball court lights are not working. Makes it difficult to play in the evening.', 'Medium', 'In Progress', 'Sports & Recreation', -0.1, 36, DATE_SUB(NOW(), INTERVAL 3 DAY), 'Sports'),
(1, 'Administration', 'Waiting for my bonafide certificate for over a week. Need it urgently for scholarship application.', 'High', 'Pending', 'Administration', -0.4, 24, DATE_SUB(NOW(), INTERVAL 1 DAY), 'Admin'),
(3, 'IT Issues', 'Projector in room 301 is not functioning properly. Display is very dim.', 'Low', 'Pending', 'IT Issues', 0.1, 24, NOW(), 'IT'),
(4, 'Hostel Management', 'Mess food quality has deteriorated. Multiple students are facing health issues.', 'High', 'In Progress', 'Hostel Management', -0.6, 12, DATE_SUB(NOW(), INTERVAL 2 DAY), 'Hostel'),
(5, 'Library', 'Library opening hours should be extended during exam period. Current hours are insufficient.', 'Medium', 'Pending', 'Library', 0.0, 48, DATE_SUB(NOW(), INTERVAL 1 DAY), 'Library'),
(2, 'Other', 'Parking space is insufficient. Students are unable to find parking spots.', 'Low', 'Pending', 'Other', -0.1, 168, DATE_SUB(NOW(), INTERVAL 4 DAY), 'Admin');

-- Insert complaint history for tracking status changes
INSERT INTO complaint_history (ticket_id, status, updated_by, updated_at, comments) VALUES
(1, 'Pending', 'System', DATE_SUB(NOW(), INTERVAL 2 DAY), 'Complaint submitted'),
(1, 'In Progress', 'IT Manager', DATE_SUB(NOW(), INTERVAL 1 DAY), 'Assigned to network team for investigation'),
(2, 'Pending', 'System', DATE_SUB(NOW(), INTERVAL 1 DAY), 'Complaint submitted'),
(3, 'Pending', 'System', DATE_SUB(NOW(), INTERVAL 5 DAY), 'Complaint submitted'),
(3, 'In Progress', 'Library Admin', DATE_SUB(NOW(), INTERVAL 4 DAY), 'Books ordered from supplier'),
(3, 'Resolved', 'Library Admin', DATE_SUB(NOW(), INTERVAL 2 DAY), 'New copies added to library'),
(4, 'Pending', 'System', DATE_SUB(NOW(), INTERVAL 7 DAY), 'Complaint submitted'),
(4, 'In Progress', 'Academic Admin', DATE_SUB(NOW(), INTERVAL 6 DAY), 'Reviewing exam schedule'),
(4, 'Resolved', 'Academic Admin', DATE_SUB(NOW(), INTERVAL 5 DAY), 'Exam schedule revised'),
(5, 'Pending', 'System', DATE_SUB(NOW(), INTERVAL 3 DAY), 'Complaint submitted'),
(5, 'In Progress', 'Sports Admin', DATE_SUB(NOW(), INTERVAL 2 DAY), 'Electrician assigned to fix lights');
