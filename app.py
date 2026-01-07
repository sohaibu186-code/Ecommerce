from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import Product
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'solo_store_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/')
def shop_front():
    products = Product.get_all()
    cart = session.get('cart', [])
    cart_count = sum(item['quantity'] for item in cart)
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('shop.html', products=products, cart_count=cart_count, cart=cart, total=total)

@app.route('/add_to_cart/<int:p_id>')
def add_to_cart(p_id):
    if 'cart' not in session: session['cart'] = []
    cart = session['cart']
    product = Product.get_by_id(p_id)
    if product and product.stock > 0:
        found = False
        for item in cart:
            if item['id'] == p_id:
                if item['quantity'] < product.stock:
                    item['quantity'] += 1
                found = True
                break
        if not found:
            cart.append({'id': p_id, 'name': product.name, 'price': product.price, 'quantity': 1})
        session['cart'] = cart
    return redirect(url_for('shop_front'))

@app.route('/process_checkout')
def process_checkout():
    cart = session.get('cart', [])
    if not cart: return redirect(url_for('shop_front'))
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()
    for item in cart:
        cursor.execute("UPDATE Products SET Stock = Stock - ? WHERE ProductID = ?", (item['quantity'], item['id']))
        cursor.execute("INSERT INTO Orders (ProductID, CustomerName, Quantity, TotalAmount, OrderDate) VALUES (?,?,?,?,?)",
                       (item['id'], "Guest", item['quantity'], item['price']*item['quantity'], "2026-01-08"))
    conn.commit()
    conn.close()
    session.pop('cart', None)
    flash("Success")
    return redirect(url_for('shop_front'))

@app.route('/admin')
def admin_panel():
    products = Product.get_all()
    return render_template('admin_products.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    name, price, cat, stock = request.form.get('name'), request.form.get('price'), request.form.get('category'), request.form.get('stock')
    file = request.files.get('image')
    filename = secure_filename(file.filename) if file else "placeholder.jpg"
    if file: file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    Product(name, price, cat, stock, image=filename).save()
    return redirect(url_for('admin_panel'))

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('shop_front'))

if __name__ == '__main__':
    app.run(debug=True)