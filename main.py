from scripts.tax_statement import create_tax_statement
from scripts.commsec_processing import process_commsec_transactions_file
from scripts.inflows import inflows


def main() -> None:

    process_commsec_transactions: str = process_commsec_transactions_file()
    print(process_commsec_transactions)

    create_tax_statement_message: str = create_tax_statement()
    print(create_tax_statement_message)

    inflows_message: str = inflows()
    print(inflows_message)

    return


if __name__ == "__main__":
    main()
