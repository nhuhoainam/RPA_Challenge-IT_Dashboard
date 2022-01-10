import datetime
import os

from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem


class DetailedInvestmentParser:
    def __init__(self, page_url):
        self.browser = Selenium()
        self.browser.open_available_browser(page_url)
        self.files = FileSystem()

    def open_and_download_pdf(self, page_url):
        load_dir = "{}/output".format(os.getcwd())
        path_to_file = "{}/{}".format(
            "{}/output".format(os.getcwd()),
            "{}.pdf".format(page_url.split('/')[-1])
            )
        if self.files.does_file_exist(path_to_file):
            self.files.remove_file(path_to_file)
            self.files.wait_until_removed(path_to_file)
        self.browser.set_download_directory(
            directory=load_dir,
            download_pdf=True
            )
        self.browser.open_available_browser(page_url)
        self.browser.wait_until_element_is_visible(
            locator="css:div#business-case-pdf>a",
            timeout=datetime.timedelta(minutes=1)
            )
        self.browser.click_element(
            locator="css:div#business-case-pdf>a"
            )
        self.files.wait_until_created(
            path=path_to_file,
            timeout=60.0*3
            )
        self.browser.close_browser()

    def get_individual_investment_list(self):
        self.browser.wait_until_element_is_visible(
            locator="css:div#investments-table-widget div.pageSelect select",
            timeout=datetime.timedelta(seconds=60)
            )
        self.browser.click_element(
            locator="css:div#investments-table-widget div.pageSelect select"
            )
        self.browser.click_element(
            locator=("css:div#investments-table-widget div.pageSelect "
                     "select option:nth-of-type(4)")
            )
        self.browser.wait_until_element_is_visible(
            locator=("css:table#investments-table-object>"
                     "tbody>tr:nth-of-type(11)"),
            timeout=datetime.timedelta(minutes=5)
            )
        return self.browser.get_webelements(
            locator="css:table#investments-table-object>tbody>tr"
            )

    def get_investment_element(self, investment_element, column_index):
        self.browser.wait_until_element_is_visible(
            locator=[
                investment_element,
                "css:td:nth-of-type({})".format(column_index)
                ]
            )
        return self.browser.get_webelement(
            locator=[
                investment_element,
                "css:td:nth-of-type({})".format(column_index)
                ]
            ).text

    def parse(self):
        self.browser.wait_until_element_is_visible(
            locator="css:div#investments-table-widget",
            timeout=datetime.timedelta(minutes=5)
            )
        data_rows = self.get_individual_investment_list()
        data_list = []
        for row in data_rows:
            investment = {
                "link": '',
                "UII": self.get_investment_element(row, 1),
                "Bureau": self.get_investment_element(row, 2),
                "Investment_Title": self.get_investment_element(row, 3),
                "Total_FY2021_Spending": self.get_investment_element(row, 4),
                "Type": self.get_investment_element(row, 5),
                "CIO_Rating": self.get_investment_element(row, 6),
                "Number_of_Projects": self.get_investment_element(row, 7)
            }
            count_link = self.browser.get_element_count(
                locator=[
                    row,
                    "css:td:nth-of-type(1)>a"
                    ]
                )
            if count_link > 0:
                investment["link"] = self.browser.get_element_attribute(
                    locator=[
                        row,
                        "css:td:nth-of-type(1)>a"
                        ],
                    attribute="href"
                    )
                self.open_and_download_pdf(investment["link"])
            data_list.append(investment)
        return data_list
