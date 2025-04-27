-- Tạo bảng người dùng
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Thêm dữ liệu mẫu vào bảng users
INSERT INTO users (id, name, email) VALUES (1, 'Vo Minh Nhat', 'minhnhat@gmail.com');
INSERT INTO users (id, name, email) VALUES (2, 'Vo Cong Hau', 'conghau@gmail.com');

