from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from rgbprint import rgbprint, Color
import re
from selenium_recaptcha_solver import RecaptchaSolver
from twocaptcha import TwoCaptcha
import prettytable as pt


class TrainTicket:
    def __init__(self):
        self.url = "https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime"
        self.driver = None

    def check_autocomplete(self, station):
        if station == "臺中":
            return "3300"
        elif station == "新竹":
            return "1210"
        return station

    def search_schedule(self, departure, arrival, date=""):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(self.url)

        start_station_input = self.driver.find_element("id", "startStation")
        start_station_input.send_keys(self.check_autocomplete(departure))

        end_station_input = self.driver.find_element("id", "endStation")
        end_station_input.send_keys(self.check_autocomplete(arrival))

        date_input = self.driver.find_element("id", "rideDate")
        if date:
            date_input.clear()
            date_input.send_keys(date)

        submit_button = self.driver.find_element("css selector", "input[type='submit']")
        submit_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "itinerary-controls"))
        )

        response = self.driver.page_source
        self.driver.quit()

        soup = BeautifulSoup(response, "html.parser")
        table = soup.find("table")
        if table:
            pt_table = pt.PrettyTable()
            pt_table.field_names = [
                "編號",
                "車種車次",
                "出發時間",
                "抵達時間",
                "旅程時間",
                "經由",
                "全票票價",
                "優待票票價",
            ]

            trains = table.find_all("tr", class_="trip-column")
            for train in trains[1:]:
                train_data = [trains.index(train)]
                train = train.find_all("td")
                train.pop(9)
                train.pop(8)
                train.pop(5)
                count = 0
                while count < len(train):
                    train_data.append(train[count].text.replace("\n", ""))
                    count += 1
                pt_table.add_row(train_data)

            return str(pt_table)

        return "未找到行程表"

    def buy_ticket(self, departure, arrival, date, choice, PID, quantity):
        buy_url = "https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query"

        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(buy_url)

        pid_is_valid = lambda input_str: re.match(r"^[a-zA-Z]\d{9}$", input_str)

        pid_input = self.driver.find_element("id", "pid")
        pid_input.send_keys(PID)

        start_station_input = self.driver.find_element("id", "startStation")
        start_station_input.send_keys(self.check_autocomplete(departure))

        end_station_input = self.driver.find_element("id", "endStation")
        end_station_input.send_keys(self.check_autocomplete(arrival))

        date_input = self.driver.find_element("id", "rideDate1")
        if date:
            date_input.clear()
            date_input.send_keys(date)

        train_num_input = self.driver.find_element("id", "trainNoList1")
        train_num_input.send_keys(choice)

        quantity_input = self.driver.find_element("id", "normalQty")
        if quantity != "1":
            quantity_input.clear()
            quantity_input.send_keys(quantity)

        while True:
            rgbprint("Solving reCAPTCHA...", color=Color.light_green)
            div_container = self.driver.find_element(By.CSS_SELECTOR, "div.g-recaptcha")
            site_key = div_container.get_attribute("data-sitekey")
            api_key = "021a2491a1f46203ad05e326c17ce477"
            solver = TwoCaptcha(api_key)
            result = solver.recaptcha(sitekey=site_key, url=buy_url, version="v2")
            code = result["code"]
            recaptcha_response_element = self.driver.find_element(
                "id", "g-recaptcha-response"
            )
            self.driver.execute_script(
                f'arguments[0].value = "{code}";', recaptcha_response_element
            )
            submit_btn = self.driver.find_element(
                "css selector", "input[type='submit']"
            )
            submit_btn.click()
            time.sleep(1)
            if self.driver.find_element(By.TAG_NAME, "strong").text == "訂票成功！":
                solver.report(result["captchaId"], True)
                return "[~] 訂票成功！"
            Error = self.driver.find_element(By.ID, "errorDiv")
            if "display: none;" not in Error.get_attribute("style"):
                msg = "[!] " + Error.find_elements(By.TAG_NAME, "p")[-1].text
                solver.report(result["captchaId"], False)
                return msg
            else:
                solver.report(result["captchaId"], False)
                rgbprint("失敗，再試一次", color=Color.red)
                continue


# 示例使用：
if __name__ == "__main__":
    ticket = TrainTicket()
    schedule_result = ticket.search_schedule("臺北", "臺中", "20240114")
    print(schedule_result)
    # 调用购票方法
    buy_result = ticket.buy_ticket("臺北", "臺中", "20240114", 1, "A123456789", "1")
    print(buy_result)
