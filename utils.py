import pandas as pd
from models import Expense


def generate_report():
    expenses = Expense.query.all()
    if not expenses:
        return [], []

    df = pd.DataFrame([
        {'Category': e.category, 'Amount': e.amount, 'Date': e.date}
        for e in expenses
    ])

    category_data = (
        df.groupby('Category')['Amount']
        .sum()
        .reset_index()
        .rename(columns={'Amount': 'Total'})
        .to_dict(orient='records')
    )

    df['Month'] = df['Date'].dt.strftime('%B %Y')
    df['SortKey'] = df['Date'].dt.strftime('%Y-%m')
    monthly_data = (
        df.groupby(['Month', 'SortKey'])['Amount']
        .sum()
        .reset_index()
        .rename(columns={'Amount': 'Total'})
        .sort_values('SortKey')
        .drop(columns='SortKey')
        .to_dict(orient='records')
    )

    return category_data, monthly_data
