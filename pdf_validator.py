import os

from RPA.PDF import PDF


class PDFValidator:
    def __init__(self):
        self.pdf = PDF()

    def get_filepath_from_link(self, url):
        return (
            os.getcwd()
            + '/output/'
            + url.split('/')[-1]
            + ".pdf"
        )

    def list_to_string(self, items):
        str = ""
        for item in items:
            str += item
        return str

    def parse(self, filepath):
        pages = self.pdf.get_text_from_pdf(filepath)
        page_1 = self.list_to_string(list(pages.values())[0])
        investment_name_index = (
            page_1.find("Name of this Investment: ")
            + len("Name of this Investment: ")
            )
        uii_index = page_1.find("2. Unique Investment Identifier (UII): ")
        investment_name = page_1[investment_name_index:uii_index]
        investment_name = investment_name.replace('\n', ' ')
        uii_index += len("2. Unique Investment Identifier (UII): ")
        uii_index_delimiter = page_1.find("Section B")
        uii = page_1[uii_index:uii_index_delimiter]
        return investment_name, uii

    def validate(self, individual_investments):
        for individual_investment in individual_investments:
            if individual_investment["link"]:
                path = self.get_filepath_from_link(
                    individual_investment["link"]
                    )
                investment_name, uii = self.parse(path)
                if uii != individual_investment["UII"]:
                    print("The UII in the PDF file({}) "
                          "does not match the UII on the web({})"
                          "".format(uii, individual_investment["UII"]))
                if (investment_name !=
                        individual_investment["Investment_Title"]):
                    print("The Name of the Investment in the PDF file({}) "
                          "does not match the Investment Title on the web({})"
                          "".format(
                                investment_name,
                                individual_investment["Investment_Title"]
                                ))
