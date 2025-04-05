import pandas as pd

def medibank_rebate(base_salary):
    medicare_brackets = pd.read_csv('data/artifacts/taxsBrackets/hecs.csv')
    bracket_row = medicare_brackets[medicare_brackets['upper_bound'] >= base_salary].index[0]
    hecs_tax = (base_salary)*(medicare_brackets.loc[bracket_row, 'marginal_rate'])