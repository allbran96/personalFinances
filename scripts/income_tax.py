# script that reads in flat files from artifacts/taxBrackets and works out the tax paid on base salary
import pandas as pd

from config.config import TAX_BRACKETS_DIR

def income_tax(base_salary):
    file_location = f'{TAX_BRACKETS_DIR}/income.csv'
    income_brackets = pd.read_csv(file_location)
    bracket_row = income_brackets[income_brackets['upper_bound'] >= base_salary].index[0]
    cumulative_tax = income_brackets.loc[:bracket_row - 1, 'cumulative_tax'].sum()
    marginal_tax = (base_salary-income_brackets.loc[bracket_row - 1, 'upper_bound'])*(income_brackets.loc[bracket_row, 'marginal_rate'])
    income_tax = cumulative_tax + marginal_tax
    return income_tax

def hecs_tax(base_salary):
    file_location = f'{TAX_BRACKETS_DIR}/hecs.csv'
    hecs_brackets = pd.read_csv(file_location)
    bracket_row = hecs_brackets[hecs_brackets['upper_bound'] >= base_salary].index[0]
    hecs_tax = (base_salary)*(hecs_brackets.loc[bracket_row, 'marginal_rate'])
    return hecs_tax



def medicare_tax(base_salary,levy_rate):
    medicare_tax = base_salary*levy_rate
    return medicare_tax

def payg_tax(base_salary,levy_rate=0.02):
    payg_tax = income_tax(base_salary) + hecs_tax(base_salary) + medicare_tax(base_salary, levy_rate)
    return payg_tax

payg_tax = payg_tax(121000)
print(payg_tax)