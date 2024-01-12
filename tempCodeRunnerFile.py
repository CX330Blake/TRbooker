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

# Search sechedule
url = "https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}
# driver_path = "D:/SourceTree/TRbooker/chromedriver.exe"
departure = input("請輸入出發站: ")
arrival = input("請輸入抵達站: ")
date = input("請輸入日期(yyyy/mm/dd): ")
departure_time = input("24小時制出發時間(hh:mm)(enter跳過): ")
arrival_time = input("24小時制抵達時間(hh:mm)(enter跳過): ")

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

start_station_input = driver.find_element("id", "startStation")
start_station_input.send_keys(departure)  # 替换为实际的出发站名称

end_station_input = driver.find_element("id", "endStation")
end_station_input.send_keys(arrival)  # 替换为实际的抵达站名称

date_input = driver.find_element("id", "rideDate")
date_input.send_keys(date)

submit_button = driver.find_element("css selector", "input[type='submit']")
submit_button.click()

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "itinerary-controls"))
)

response = driver.page_source
soup = BeautifulSoup(response, "html.parser")
table = soup.find("table")

pt_table = pt.PrettyTable()
pt_table.field_names = [
    "出發時間",
    "抵達時間",
    "旅程時間",
    "車種車次",
    "經由",
    "服務設施",
    "狀態",
    "全票票價",
    "優待票票價",
]

train = table.find_all("tr")
print(train)