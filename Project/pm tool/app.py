from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",port="3307",
        password="",
        database="product_management"
    )
    return conn


@app.route('/')
def home():
    return render_template('layout.html')


@app.route('/categories', methods=['GET', 'POST'])
def categories():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        parent_id = request.form['parent_id'] or None

        cursor.execute(
            "INSERT INTO categories (name, description, parent_id) VALUES (%s, %s, %s)",
            (name, description, parent_id)
        )
        conn.commit()

    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    conn.close()

    return render_template('categories.html', categories=categories)

@app.route('/categories/delete/<int:id>')
def delete_category(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('categories'))

@app.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['category_name']

        cursor.execute(
            "UPDATE categories SET name = %s WHERE id = %s",
            (name, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('categories'))

    cursor.execute("SELECT * FROM categories WHERE id = %s", (id,))
    category = cursor.fetchone()
    conn.close()
    return render_template('edit_category.html', category=category)


@app.route('/products', methods=['GET', 'POST'])
def products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['product_name']
        price = request.form['price']
        description = request.form['description']
        category_id = request.form['category_id']

        cursor.execute(
            "INSERT INTO products (name, category_id, price, description) VALUES (%s, %s, %s, %s)",
            (name, category_id, price, description)
        )
        conn.commit()

    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()
    return render_template('products.html', products=products, categories=categories)

@app.route('/products/delete/<int:id>')
def delete_product(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('products'))

@app.route('/products/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['product_name']
        price = request.form['price']
        description = request.form['description']
        category_id = request.form['category_id']

        cursor.execute(
            "UPDATE products SET name = %s, category_id = %s, price = %s, description = %s WHERE id = %s",
            (name, category_id, price, description, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('products'))

    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()

    cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
    product = cursor.fetchone()
    conn.close()
    return render_template('edit_product.html', product=product, categories=categories)


@app.route('/attributes', methods=['GET', 'POST'])
def attributes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
       
        name = request.form['attribute_name']
        value = request.form['attribute_value']
        product_id = request.form['product_id']
        cursor.execute("SELECT id FROM products WHERE id = %s", (product_id,))
        products= cursor.fetchone()
        cursor.execute(
            "INSERT INTO product_attributes (attribute_name, attribute_value, product_id) VALUES (%s, %s, %s)",
            (name, value, product_id)
        )
        conn.commit()

    cursor.execute("SELECT id, name FROM products")
    products = cursor.fetchall()

    cursor.execute("SELECT * FROM product_attributes")
    attributes = cursor.fetchall()

    conn.close()
    return render_template('attributes.html', attributes=attributes, products=products)

@app.route('/attributes/delete/<int:id>')
def delete_attribute(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM product_attributes WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('attributes'))

@app.route('/attributes/edit/<int:id>', methods=['GET', 'POST'])
def edit_attribute(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['attribute_name']
        value = request.form['attribute_value']


        cursor.execute(
            "UPDATE product_attributes SET attribute_name = %s, attribute_value = %s",
            (name, value)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('attributes'))

    cursor.execute("SELECT id, name FROM products")
    products = cursor.fetchall()

    cursor.execute("SELECT * FROM product_attributes WHERE id = %s", (id,))
    attribute = cursor.fetchone()
    conn.close()
    return render_template('edit_attribute.html', attribute=attribute, products=products)

if __name__ == '__main__':
    app.run(debug=True)
