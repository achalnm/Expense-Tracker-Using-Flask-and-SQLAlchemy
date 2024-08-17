from models import Expense
import pandas as pd

def generate_report():
    expenses = Expense.query.all()
    df = pd.DataFrame([(e.category, e.amount) for e in expenses], columns=['Category', 'Amount'])
    report_data = df.groupby('Category').sum().reset_index().to_dict(orient='records')
    return report_data
