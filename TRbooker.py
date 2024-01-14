from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import prettytable as pt
import json
import time
from rgbprint import rgbprint, gradient_print, Color
import re
from selenium_recaptcha_solver import RecaptchaSolver
from twocaptcha import TwoCaptcha
import sys

# Search sechedule
url = "https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime"


# 使用者輸入資訊
departure = input(f"{Color.orange}請輸入出發站:{Color.orange} ")
arrival = input(f"{Color.orange}請輸入抵達站:{Color.orange} ")
date = input(f"{Color.orange}請輸入日期(yyyy/mm/dd):{Color.orange} ").replace("/", "")

# 設定web driver
my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument(f"--user-agent={my_user_agent}")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver.get(url)

# 查找元素，並送出request
start_station_input = driver.find_element("id", "startStation")
start_station_input.send_keys(departure)

end_station_input = driver.find_element("id", "endStation")
end_station_input.send_keys(arrival)

# 如果輸入為空，則為當日，反之則為輸入日期
date_input = driver.find_element("id", "rideDate")
if date != "":
    date_input.clear()
    date_input.send_keys(date)

submit_button = driver.find_element("css selector", "input[type='submit']")
submit_button.click()

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "itinerary-controls"))
)
response = driver.page_source
driver.quit()
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
    for char in "[+] Successfully found the schedule...":
        rgbprint(char, color=Color.light_green, end="")
        time.sleep(0.1)
    print()
    gradient_print(
        str(pt_table), start_color=Color.yellow_green, end_color=Color.blue_violet
    )
    print()
    # print(pt_table)
else:
    print("未找到")


# Buy
choice = int(input(f"{Color.orange}請輸入欲購買的列車編號(表格第一行)(輸入99退出不購買): {Color.orange}"))
if choice == 99:
    exit(0)

buy_url = "https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query"
PID = input(f"{Color.orange}請輸入身分證字號:{Color.orange} ")
train_num = int(trains[choice].find_all("td")[0].find("a").text.split(" ")[-1])

# 設定web driver
my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument(f"--user-agent={my_user_agent}")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver.get(buy_url)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
pid_input = driver.find_element("id", "pid")
pid_input.send_keys(PID)

start_station_input = driver.find_element("id", "startStation")
start_station_input.send_keys(departure)

end_station_input = driver.find_element("id", "endStation")
end_station_input.send_keys(arrival)

date_input = driver.find_element("id", "rideDate1")
if date != "":
    date_input.clear()
    date_input.send_keys(date)

train_num_input = driver.find_element("id", "trainNoList1")
train_num_input.send_keys(train_num)

div_container = driver.find_element(By.CSS_SELECTOR, "div.g-recaptcha")
site_key = div_container.get_attribute("data-sitekey")
recaptcha_iframe = driver.find_element(By.TAG_NAME, "iframe")
recaptcha_url = recaptcha_iframe.get_attribute("src")
api_key = "021a2491a1f46203ad05e326c17ce477"
solver = TwoCaptcha(api_key)

while True:
    print("Solving reCAPTCHA")
    result = solver.recaptcha(sitekey=site_key, url=buy_url, version="v2")
    code = result["code"]
    recaptcha_response_element = driver.find_element(By.ID, "g-recaptcha-response")
    driver.execute_script(f'arguments[0].value = "{code}";', recaptcha_response_element)
    submit_btn = driver.find_element("css selector", "input[type='submit']")
    submit_btn.click()
    time.sleep(3)
    if driver.find_element(By.TAG_NAME, "strong").text == "訂票成功！":
        solver.report(result["captchaId"], True)
        break
    else:
        solver.report(result["captchaId"], False)
        print("失敗，再試一次")
        continue

# print(result)
# driver.execute_script(
#     f'document.getElementById("g-recaptcha-response").innerHTML="{result["code"]}";'
# )
# time.sleep(4)
# submit_button = driver.find_element("css selector", "input[type='submit']")
# submit_button.click()
# time.sleep(30)
