from flask import Flask, render_template, redirect, url_for, flash, request
from pymongo import MongoClient
from flask_pymongo import PyMongo
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = '9b401ce479be403e76d75fa12bb566be'

# MongoDB configuration (update the URI if using MongoDB Atlas or another service)
app.config["MONGO_URI"] = "mongodb://localhost:27017/crochet_creations"
mongo = PyMongo(app)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Gmail SMTP server
app.config['MAIL_PORT'] = 587  # Port for sending emails
app.config['MAIL_USE_TLS'] = True  # Use TLS for security
app.config['MAIL_USE_SSL'] = False  # Disable SSL
app.config['MAIL_USERNAME'] = 'crochetCreationsWork@gmail.com' 
app.config['MAIL_PASSWORD'] = 'jdestztwnxalgjtp' 
app.config['MAIL_DEFAULT_SENDER'] = 'crochetCreationsWork@gmail.com'

# Initialize the mail instance
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect to login if user is not authenticated

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        return User(str(user['_id']))
    return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)

        if mongo.db.users.find_one({"email": email}):
            flash("Email already registered. Please login.", "danger")
            return redirect('/login')

        mongo.db.users.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password
        })
        flash("Registration successful! Please log in.", "success")
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = mongo.db.users.find_one({"email": email})

        if user and check_password_hash(user['password'], password):
            login_user(User(str(user['_id'])))
            flash("Login successful!", "success")
            return redirect('/')

        flash("Invalid email or password.", "danger")
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect('/')

@app.route('/')
def homepage():
    featured_products = mongo.db.products.find({"featured": True})
    return render_template('index.html', featured_products=featured_products, current_user=current_user)

@app.route('/shop')
def shop():
    # Fetch distinct categories from the products collection
    categories = mongo.db.products.distinct('category')
    return render_template('shop.html', categories=categories)

@app.route('/shop/<category_name>')
def category_products(category_name):
    # Fetch products belonging to the selected category
    products = mongo.db.products.find({"category": category_name})
    return render_template('category_products.html', products=products, category_name=category_name)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Print form data to check submission
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        print(f"Received message from {name} ({email}): {message}")  # Debug print
        
        # Create the email message
        msg = Message(
            subject=f"Contact Form Submission from {name}",
            recipients=["your_email@gmail.com"],  # Replace with your email
            body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
        )

        try:
            # Send the email
            mail.send(msg)
            
            # Store contact data in MongoDB (optional)
            contact_message = {
                'name': name,
                'email': email,
                'message': message,
            }
            mongo.db.contact_messages.insert_one(contact_message)
            
            # Flash success message
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            # Flash error message if there's an issue sending the email
            flash(f"An error occurred while sending the message: {e}", "error")
        
        # Redirect after POST to prevent resubmission on refresh
        return redirect('/contact')

    return render_template('contact.html')

@app.route('/product/<product_id>')
def product_detail(product_id):
    # Find the product in the database by product_id (using ObjectId for MongoDB)
    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
    
    return render_template('product_detail.html', product=product)

if __name__ == '__main__':
    app.run(debug=True, port=5000)