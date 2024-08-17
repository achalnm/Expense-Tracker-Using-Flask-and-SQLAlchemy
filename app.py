from flask import Flask, request, render_template, redirect, url_for
from models import db, Expense
import utils

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db.init_app(app)

@app.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    return redirect(url_for('home'))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'reset' in request.form:
            return redirect(url_for('reset'))
        else:
            category = request.form['category']
            amount = float(request.form['amount'])
            description = request.form['description']
            expense = Expense(category=category, amount=amount, description=description)
            db.session.add(expense)
            db.session.commit()
            return redirect(url_for('home'))
    expenses = Expense.query.all()
    return render_template('home.html', expenses=expenses)

@app.route('/reports')
def reports():
    report_data = utils.generate_report()
    return render_template('reports.html', report_data=report_data)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
