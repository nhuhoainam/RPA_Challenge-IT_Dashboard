from RPA.Excel.Files import Files
from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem


class ExcelWriter:
    excel = Files()

    def __init__(self):
        self.excel.create_workbook("output/Agencies.xlsx")
        self.excel.rename_worksheet("Sheet", "Agencies")

    def create_new_worksheet(self, worksheet):
        self.excel.create_worksheet(worksheet)
        self.excel.set_active_worksheet(worksheet)

    def write_column(self, data_list, column, key):
        row_count = 0
        for row in data_list:
            row_count += 1
            self.excel.set_cell_value(row_count, column, row[key])
        self.excel.save_workbook()

    def write_table(self, data_table):
        row_count = 0
        for row in data_table:
            row_count += 1
            col_count = 0
            for col in row:
                col_count += 1
                self.excel.set_cell_value(row_count, col_count, row[col])
        self.excel.save_workbook()
