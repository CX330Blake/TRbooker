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

# Search sechedule
url = "https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}
# 使用者輸入資訊
departure = input(f"{Color.orange}請輸入出發站:{Color.orange} ")
arrival = input(f"{Color.orange}請輸入抵達站:{Color.orange} ")
date = input(f"{Color.orange}請輸入日期(yyyy/mm/dd):{Color.orange} ").replace("/", "")


# 設定web driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver.get(url)

# 查找元素，並送出request
start_station_input = driver.find_element("id", "startStation")
start_station_input.send_keys(departure)

end_station_input = driver.find_element("id", "endStation")
end_station_input.send_keys(arrival)

date_input = driver.find_element("id", "rideDate")
date_input.clear()
date_input.clear()
date_input.send_keys(date)

submit_button = driver.find_element("css selector", "input[type='submit']")
submit_button.click()

element = WebDriverWait(driver, 10).until(
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
    for char in "[+] Succesfully found the schedule...":
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


# data = {
#     "startStation": departure,  # 替换为实际的出发站
#     "endStation": arrival,  # 替换为实际的抵达站
#     "rideDate": date,  # 替换为实际的日期
#     "startTime": departure_time,  # 替换为实际的出发时间
#     "endTime": arrival_time,  # 替换为实际的抵达时间
#     "transfer": "",  # 替换为实际的转乘条件，比如 'NORMAL'
#     "trainTypeList": "",  # 替换为实际的车种条件，比如 'ALL'
#     "queryClassification": "",  # 替换为实际的查询方式，比如 'NORMAL'
# }
