CREATE TABLE users (
    userid INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    gender CHAR(1),
    password VARCHAR(255),  -- You should consider using a more secure way to store passwords
    user_type VARCHAR(10)
);