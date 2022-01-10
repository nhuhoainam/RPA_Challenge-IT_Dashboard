import datetime
import os

from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem


class DetailedInvestmentParser:
    def __init__(self, page_url):
        self.browser = Selenium()
        self.browser.open_available_browser(page_url)
        self.files = FileSystem()
    # Critical: DO NOT use while loop like this. If the file failed to download then your program will be an infinite loop waiting for it forever. Refer to 
    # https://github.com/kvazarich/IT_Dashboard_RPA_Challenge and use the wait_until_created and with timeout to prevent blocking thread
    def wait_for_download_to_complete(self, file_name):
        while self.files.does_file_not_exist(
                "{}/output/{}.pdf".format(os.getcwd(), file_name)
                ):
            continue

    def open_and_download_pdf(self, page_url):
        self.browser.set_download_directory(
            directory="{}/output".format(os.getcwd()),
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
        self.wait_for_download_to_complete(
            page_url.split('/')[-1]
            )
        # Low: By default browser instances created during task execution are closed at the end of the task.
        # This can be prevented with the auto_close argument when importing the library.
        # Maybe the below line is unneccessary
        self.browser.close_browser()

    def get_individual_investment_list(self):
        # Low: I believe 5 minute timeout is too much for an element to visible. Some where between 20-60 s is more reasonable
        self.browser.wait_until_element_is_visible(
            locator="css:div#investments-table-widget div.pageSelect select",
            timeout=datetime.timedelta(minutes=5)
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
