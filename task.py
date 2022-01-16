from agencies_list_parser import AgenciesListParser
from excel_writer import ExcelWriter
from detailed_investment_parser import DetailedInvestmentParser
from pdf_validator import PDFValidator


def get_agencies():
    list_parser = AgenciesListParser()
    return list_parser.parse()


def get_detailed_investment(url):
    table_parser = DetailedInvestmentParser(url)
    return table_parser.parse()


def write_to_excel(data_list, data_table):
    excel = ExcelWriter()
    excel.write_column(data_list, 1, "name")
    excel.write_column(data_list, 2, "spending")
    excel.create_new_worksheet("Individual Investments")
    excel.write_table(data_table)
    excel.excel.close_workbook()


def main():
    agencies_list = get_agencies()
    detailed_investment_table = get_detailed_investment(
        agencies_list[23]["link"]
        )
    write_to_excel(agencies_list, detailed_investment_table)
    validator = PDFValidator()
    validator.validate(detailed_investment_table)


if __name__ == "__main__":
    main()
