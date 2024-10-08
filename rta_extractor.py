import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from RecaptchaSolver import RecaptchaSolver as RecaptchaSolverV2

class RtaExtractor:
    def __init__(self, username, password, nol_id):
        self.RTA_USERNAME = username
        self.RTA_PASSWORD = password
        self.RTA_NOL_CARD = nol_id
        self.LOGIN_URL = "https://www.rta.ae/wps/myportal/rta/ae/home/dashboard?lang=en"
        self.TRANSACTIONS_URL = "https://www.rta.ae/wps/portal/rta/ae/public-transport/nol/view-history?lang=en"
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(60)
        self.ENTER_TAG_NUMBER_CSS = "#nolRefundFrm > div > div > div.swiper-wrapper > div.swiper-slide.swiper-slide-next.rtaOffice.loggedinTabs > label"
        self.TRAVEL_HISTORY_CSS = (
            "#smartStep_2 > div.smart-step__content > div > div > div:nth-child(5)"
        )
        self.form_btn = "button.btn"
    def login(self):
        self.driver.get(self.LOGIN_URL)
        username_box = self.driver.find_element(by=By.NAME, value="username")
        password_box = self.driver.find_element(by=By.NAME, value="password")
        login_btn = self.driver.find_element(by=By.ID, value="btn_login")

        # username_box, password_box
        username_box.send_keys(self.RTA_USERNAME)
        password_box.send_keys(self.RTA_PASSWORD)
        login_btn.click()

    def fill_form(self, retries = 5):
        try:
            self.driver.get(self.TRANSACTIONS_URL)
            time.sleep(0.74)
            type = self.driver.find_element(by=By.CSS_SELECTOR, value=self.ENTER_TAG_NUMBER_CSS)
            self.wait_for_it(type)
            type.click()
            self.driver.find_element(by=By.NAME, value="tagId").send_keys(self.RTA_NOL_CARD)
            print("Solving")
            self.recaptcha_solver_user()
            # self.recaptcha_solver2()
            print("Solved")
            btn = self.driver.find_element(by=By.CSS_SELECTOR, value="button.btn")
            print("Found BTN")
            btn.click()
            print("Clicked BTN")
        except Exception as e:
            if retries > 0:
                print(f"fill_form Error: {e}. Retrying...")
                
                self.fill_form(retries - 1)
            else:
                raise e


    def get_travels(self):
        travel_history = self.driver.find_element(
            by=By.CSS_SELECTOR, value=self.TRAVEL_HISTORY_CSS
        )
        self.wait_for_it(travel_history)
        travel_history.get_attribute("innerHTML")
        travel_history_table = travel_history.find_element(
            by=By.CLASS_NAME, value="ss-table__tbody"
        )
        rows_html = travel_history_table.find_elements(by=By.XPATH, value="*")
        print(f"len:{len(rows_html)}")
        return [RtaExtractor.extract_travel(row=row) for row in rows_html]

    def to_df(travels: list[dict]):
        df = pd.DataFrame(
            travels,
            columns=["nol_tag_id", "date", "time", "event", "station", "amount"],
        )
        return df

    @staticmethod
    def extract_travel(row: webdriver.remote.webelement.WebElement) -> dict:
        def extract(item: webdriver.remote.webelement.WebElement):
            return (
                item.get_attribute("innerHTML")
                .replace("\n", "")
                .replace("\t", "")
                .replace(r"\s{2,}", " ")
                .strip()
            )

        def extract_amount(item: webdriver.remote.webelement.WebElement):
            return (
                item.find_element(by=By.XPATH, value="*")
                .get_attribute("innerHTML")
                .replace("\n", "")
                .replace("\t", "")
                .replace(r"\s{2,}", " ")
                .strip()
            )

        children = row.find_elements(by=By.XPATH, value="*")
        nol_tag_id = extract(children[0])
        date = extract(children[1])
        time = extract(children[2])
        trip = extract(children[3])
        event = trip.split(":")[0].strip()
        station = trip.split(":")[1].strip()
        amount = extract_amount(children[4])
        return {
            "nol_tag_id": nol_tag_id,
            "date": date,
            "time": time,
            # "trip": trip,
            "event": event,
            "station": station,
            "amount": amount,
        }
    
    def recaptcha_solver_user(self):
        input("Solve the recaptcha and press enter")

    def recaptcha_solver2(self):
        recaptchaSolver = RecaptchaSolverV2(self.driver)
        recaptchaSolver.solveCaptcha()
        
    
            
    def wait_for_it(self, element, timeout=20):
        return WebDriverWait(self.driver, timeout).until(
            lambda d : element.is_displayed()
        )