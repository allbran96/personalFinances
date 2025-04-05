### script that reads in flat files from artifacts/taxBrackets and works out the tax paid on base salary

import numpy as np
import pandas as pd

from config.config import BASE_SALARY, HEALTH_INSURANCE_COST, TAX_BRACKETS_FILE


# calculate amount of tax or subsidy based on income brackets csv
def calculate_tax_bracket_amount(source: str, is_tax: bool, is_cumulative: bool) -> float:

    # read in tax brackets file
    income_brackets = pd.read_csv(TAX_BRACKETS_FILE)
    income_brackets["upper_bound"] = income_brackets["upper_bound"].replace("inf", np.inf).astype(float)

    # only take the parts of the file that are applicable to the current function call and ensure sorted by upper bound
    income_brackets = income_brackets[income_brackets["service"] == source]
    income_brackets.sort_values(by="upper_bound", inplace=True)

    # find dataframe index that salary is in
    bracket_row = income_brackets[income_brackets["upper_bound"] >= BASE_SALARY].index[0]

    # if amount needs to be cumulatively added, like income tax
    if is_cumulative:
        cumulative_amount = 0
        for row in income_brackets.itertuples(index=False):
            if BASE_SALARY > row.upper_bound:
                cumulative_amount += (row.upper_bound - row.lower_bound) * row.rate
            else:
                marginal_amount = (BASE_SALARY - row.lower_bound) * row.rate
                break
        amount = cumulative_amount + marginal_amount

    # else, like hecs and medibank, it is a flat rate
    else:
        if source == "medibank":
            amount = (HEALTH_INSURANCE_COST) * (income_brackets.loc[bracket_row, "rate"])
        elif source == "hecs":
            amount = (BASE_SALARY) * (income_brackets.loc[bracket_row, "rate"])

    # finally, if the value is a tax, report it as a negative
    if is_tax:
        amount *= -1

    # return the amount of the rebate/tax
    return amount
