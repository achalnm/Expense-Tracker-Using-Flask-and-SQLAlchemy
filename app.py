import os
from datetime import datetime, timezone
from flask import Flask, request, render_template, redirect, url_for, flash
from models import db, Expense, Budget
import utils

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        category = request.form.get('category', '').strip()
        amount_str = request.form.get('amount', '').strip()
        description = request.form.get('description', '').strip()

        if not category or len(category) > 50:
            flash('Category is required and must be 50 characters or fewer.', 'danger')
            return redirect(url_for('home'))

        try:
            amount = float(amount_str)
        except ValueError:
            flash('Amount must be a valid number.', 'danger')
            return redirect(url_for('home'))

        if amount <= 0:
            flash('Amount must be a positive number.', 'danger')
            return redirect(url_for('home'))

        if len(description) > 200:
            description = description[:200]

        expense = Expense(category=category, amount=amount, description=description)
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('home'))

    category_filter = request.args.get('category', '').strip()
    if category_filter:
        expenses = Expense.query.filter_by(category=category_filter).order_by(Expense.date.desc()).all()
    else:
        expenses = Expense.query.order_by(Expense.date.desc()).all()

    categories = [row[0] for row in db.session.query(Expense.category).distinct().all()]

    now = datetime.now(timezone.utc)
    budget = Budget.query.first()
    monthly_spent = db.session.query(
        db.func.sum(Expense.amount)
    ).filter(
        db.func.strftime('%Y-%m', Expense.date) == now.strftime('%Y-%m')
    ).scalar() or 0.0

    budget_amount = budget.amount if budget else 0.0
    if budget_amount > 0:
        raw_pct = (monthly_spent / budget_amount) * 100
        budget_pct = min(raw_pct, 100)
        if raw_pct >= 100:
            bar_color = 'danger'
        elif raw_pct >= 80:
            bar_color = 'warning'
        else:
            bar_color = 'success'
    else:
        budget_pct = 0
        bar_color = 'success'

    return render_template(
        'home.html',
        expenses=expenses,
        categories=categories,
        category_filter=category_filter,
        budget_amount=budget_amount,
        monthly_spent=monthly_spent,
        budget_pct=budget_pct,
        bar_color=bar_color,
    )


@app.route('/expenses/<int:expense_id>/delete', methods=['POST'])
def delete_expense(expense_id):
    expense = db.get_or_404(Expense, expense_id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/reports')
def reports():
    category_data, monthly_data = utils.generate_report()
    return render_template('reports.html', category_data=category_data, monthly_data=monthly_data)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    budget = Budget.query.first()
    if request.method == 'POST':
        amount_str = request.form.get('budget_amount', '').strip()
        try:
            amount = float(amount_str)
            if amount < 0:
                raise ValueError
        except ValueError:
            flash('Budget amount must be a valid non-negative number.', 'danger')
            return redirect(url_for('settings'))

        if budget is None:
            budget = Budget(amount=amount)
            db.session.add(budget)
        else:
            budget.amount = amount
        db.session.commit()
        flash('Budget updated.', 'success')
        return redirect(url_for('settings'))

    return render_template('settings.html', budget=budget)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
