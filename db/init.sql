CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL,
    image_url VARCHAR(500)
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    message VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    review_text TEXT NOT NULL,
    sentiment_score VARCHAR(20) DEFAULT 'NEUTRAL'
);

-- Seed some data with Indian prices and images
INSERT INTO products (name, price, image_url) VALUES 
('Laptop', 82499.00, 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400'),
('Smartphone', 41249.00, 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400'),
('Headphones', 6599.00, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400');
