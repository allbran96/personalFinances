from processing.create_income_statement import create_income_statement
from processing.commsec_processing import process_commsec_transactions_file


def main() -> None:

    create_income_statement_message: str = create_income_statement()
    print(create_income_statement_message)

    process_commsec_transactions: str = process_commsec_transactions_file()
    print(process_commsec_transactions)

    return


if __name__ == "__main__":
    main()
