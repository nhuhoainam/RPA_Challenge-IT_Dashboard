import datetime

from RPA.Browser.Selenium import Selenium


class AgenciesListParser:
    page_url = "https://itdashboard.gov/"

    def __init__(self):
        self.browser = Selenium()
        self.browser.open_available_browser(self.page_url)

    def click_main_button(self):
        self.browser.wait_until_element_is_visible(
            locator='//*[@href="#home-dive-in"]',
            timeout=datetime.timedelta(minutes=5)
            )
        self.browser.click_element(
            locator='//*[@href="#home-dive-in"]'
            )

    def get_agencies_list(self):
        self.browser.wait_until_element_is_visible(
            locator="css:div#agency-tiles-widget>div>div>div>div>div>div"
            )
        return self.browser.get_webelements(
            locator="css:div#agency-tiles-widget>div>div>div>div>div>div"
            )

    def get_agency_name(self, agency_element):
        self.browser.wait_until_element_is_visible(
            locator=[agency_element, "css:span:nth-of-type(1)"]
            )
        return self.browser.get_webelement(
            locator=[agency_element, "css:span:nth-of-type(1)"]
            ).text

    def get_agency_spending(self, agency_element):
        self.browser.wait_until_element_is_visible(
            locator=[agency_element, "css:span:nth-of-type(2)"]
            )
        return self.browser.get_webelement(
            locator=[agency_element, "css:span:nth-of-type(2)"]
            ).text

    def get_agency_link(self, agency_element):
        self.browser.wait_until_element_is_visible(
            locator=[agency_element, "css:a"]
            )
        return self.browser.get_element_attribute(
            locator=[agency_element, "css:a"],
            attribute="href"
            )

    def parse(self):
        self.click_main_button()
        agencies_elements = self.get_agencies_list()
        agencies = []
        for agency_element in agencies_elements:
            agency = {
                "name": self.get_agency_name(agency_element),
                "spending": self.get_agency_spending(agency_element),
                "link": self.get_agency_link(agency_element)
            }
            agencies.append(agency)
        return agencies
