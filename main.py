from processing.tax_statement import create_tax_statement
from processing.commsec_processing import process_commsec_transactions_file


def main() -> None:

    process_commsec_transactions: str = process_commsec_transactions_file()
    print(process_commsec_transactions)

    create_tax_statement_message: str = create_tax_statement()
    print(create_tax_statement_message)

    return


if __name__ == "__main__":
    main()
