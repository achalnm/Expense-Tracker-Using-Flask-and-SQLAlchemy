import math
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

    # Category breakdown with share percentage
    cat = (
        df.groupby('Category')['Amount']
        .sum()
        .reset_index()
        .rename(columns={'Amount': 'Total'})
        .sort_values('Total', ascending=False)
    )
    grand_total = cat['Total'].sum()
    cat['Percent'] = ((cat['Total'] / grand_total) * 100).round(1) if grand_total > 0 else 0.0
    category_data = cat.to_dict(orient='records')

    # Monthly breakdown with change vs previous month
    df['Month'] = df['Date'].dt.strftime('%B %Y')
    df['SortKey'] = df['Date'].dt.strftime('%Y-%m')
    monthly = (
        df.groupby(['Month', 'SortKey'])['Amount']
        .sum()
        .reset_index()
        .rename(columns={'Amount': 'Total'})
        .sort_values('SortKey')
    )
    monthly['VsPrev'] = monthly['Total'].diff()

    monthly_data = []
    for _, row in monthly.iterrows():
        vs = row['VsPrev']
        monthly_data.append({
            'Month': row['Month'],
            'Total': float(row['Total']),
            'VsPrev': None if (isinstance(vs, float) and math.isnan(vs)) else float(vs),
        })

    return category_data, monthly_data
