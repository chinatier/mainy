CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    surname VARCHAR(50) NOT NULL,
    given_name VARCHAR(50) NOT NULL,
    patronymic VARCHAR(50),
    user_role VARCHAR(50) NOT NULL
);
CREATE TABLE sizes (
    size_id SERIAL PRIMARY KEY,
    size_value NUMERIC(3,1) NOT NULL UNIQUE
);
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL UNIQUE,
    manufacturer VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100) NOT NULL,
    description VARCHAR(200) NOT NULL,
    composition VARCHAR(300) NOT NULL,
    image_path VARCHAR(255),
    unit_price NUMERIC(10,2) NOT NULL,
    UNIQUE (product_name, manufacturer)
);
CREATE TABLE inventory (
    inventory_id SERIAL PRIMARY KEY,
    manufacturer VARCHAR(100) NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    size_value NUMERIC(3,1) NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (product_name, manufacturer)
        REFERENCES products(product_name, manufacturer) ON DELETE RESTRICT,
    FOREIGN KEY (size_value)
        REFERENCES sizes(size_value) ON DELETE RESTRICT
);
CREATE TABLE purchases (
    purchase_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id) ON DELETE RESTRICT,
    purchased_on DATE NOT NULL DEFAULT CURRENT_DATE
);
CREATE TABLE purchase_lines (
    line_id SERIAL PRIMARY KEY,
    purchase_id INTEGER NOT NULL REFERENCES purchases(purchase_id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(product_id) ON DELETE RESTRICT,
    size_id INTEGER NOT NULL REFERENCES sizes(size_id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL
);