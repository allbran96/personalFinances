from scripts.create_income_statement import create_income_statement


def main() -> None:

    output: str = create_income_statement()
    print(output)
    return


if __name__ == "__main__":
    main()
