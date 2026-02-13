from flask import Flask, render_template, url_for, redirect,request,flash,jsonify,send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_weasyprint import render_pdf
from weasyprint import HTML
from io import BytesIO



app = Flask(__name__)

bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'ADD_YOUR_SQLLite_URL' 
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'ADD_YOUR_SECRETE_KEY'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    ifsc_code = db.Column(db.String(11), nullable=False)
    balance = db.Column(db.Float, nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


class CustomerForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=100)])
    account_number = StringField('Account Number', validators=[InputRequired(), Length(max=20)])
    ifsc_code = StringField('IFSC Code', validators=[InputRequired(), Length(max=11)])
    balance = StringField('Balance', validators=[InputRequired()])
    submit = SubmitField('Add Customer')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        account_holder_name = request.form.get('accountHolderName')
        amount = request.form.get('amount')

        # Query database for account holder
        account = Customer.query.filter_by(name=account_holder_name).first()

        if account:
            balance = account.balance
            # Return the updated balance to the dashboard
            return render_template('dashboard.html', balance=balance, accountHolderName=account_holder_name, amount=amount)
        else:
            return render_template('dashboard.html', error="Account not found!")

    # GET request - load the dashboard
    return render_template('dashboard.html')

@app.route('/get_balance', methods=['POST'])
def get_balance():
    account_number = request.json.get('accountNumber')
    customer = Customer.query.filter_by(account_number=account_number).first()
    if customer:
        return jsonify({"balance": customer.balance})
    else:
        return jsonify({"error": "Account not found"}), 404

@app.route('/process_transaction', methods=['POST'])
def process_transaction():
    data = request.json
    account_number = data.get('accountNumber')
    amount = data.get('amount')
    
    customer = Customer.query.filter_by(account_number=account_number).first()
    if not customer:
        return jsonify({"error": "Account not found"}), 404

    if amount > 15000:
        return jsonify({"error": "Transaction exceeds ₹15,000 limit"}), 400

    if customer.balance < amount:
        return jsonify({"error": "Insufficient balance"}), 400

    # Deduct amount from balance
    customer.balance -= amount
    db.session.commit()
    return jsonify({"success": f"Transaction successful. New balance: ₹{customer.balance}"}), 200

@app.route('/bill_generation', methods=['GET'])
def bill_generation():
    account_number = request.args.get('accountNumber')
    ifsc_code = request.args.get('ifscCode')
    amount = request.args.get('amount')
    name = request.args.get('name')
    new_balance = request.args.get('newBalance')
    timestamp = request.args.get('timestamp')

    # Validate and fetch additional data if needed
    if not all([account_number, ifsc_code, amount, name, new_balance, timestamp]):
        return "Missing transaction details", 400

    # Render bill generation page with the details
    return render_template('bill_generation.html', 
                           account_number=account_number, 
                           ifsc_code=ifsc_code, 
                           amount=amount, 
                           name=name, 
                           new_balance=new_balance, 
                           timestamp=timestamp)


@app.route('/get_transaction_details', methods=['POST'])
def get_transaction_details():
    data = request.get_json()
    account_number = data.get('accountNumber')

    customer = Customer.query.filter_by(account_number=account_number).first()
    if customer:
        return jsonify({
            'name': customer.name,
            'ifscCode': customer.ifsc_code,
            'newBalance': customer.balance,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Mocking a timestamp
        })
    else:
        return jsonify({"error": "Account not found"}), 404


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        # Fetch data from the form
        name = request.form['name']
        account_number = request.form['account_number']
        ifsc_code = request.form['ifsc_code']
        balance = request.form['balance']

        # Check if the account number already exists
        existing_customer = Customer.query.filter_by(account_number=account_number).first()
        if existing_customer:
            flash('Account number already exists. Please use a unique account number.', 'error')
            return redirect(url_for('add_customer'))

        # Add new customer to the database
        new_customer = Customer(
            name=name,
            account_number=account_number,
            ifsc_code=ifsc_code,
            balance=balance
        )
        db.session.add(new_customer)
        db.session.commit()
        flash('Customer added successfully!', 'success')
        return redirect(url_for('add_customer'))
    return render_template('add_customer.html')

@app.route('/print_bill', methods=['GET'])
def print_bill():
    account_number = request.args.get('accountNumber')
    ifsc_code = request.args.get('ifscCode')
    amount = request.args.get('amount')
    name = request.args.get('name')
    new_balance = request.args.get('newBalance')
    timestamp = request.args.get('timestamp')

    # Ensure all required data is present
    if not all([account_number, ifsc_code, amount, name, new_balance, timestamp]):
        return "Missing transaction details", 400

    # Render the HTML for the bill generation template
    rendered = render_template('bill_generation.html', 
                               account_number=account_number, 
                               ifsc_code=ifsc_code, 
                               amount=amount, 
                               name=name, 
                               new_balance=new_balance, 
                               timestamp=timestamp)
    
    # Convert the rendered HTML to PDF using WeasyPrint
    pdf = HTML(string=rendered).write_pdf()

    # Create a BytesIO object to send the PDF file
    pdf_output = BytesIO(pdf)

    # Send the generated PDF as an attachment
    return send_file(pdf_output, download_name='bill.pdf', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=False)  