from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import prettytable as pt
import json

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

driver_path = "D:/SourceTree/TRbooker/chromedriver.exe"
driver = webdriver.Chrome(driver_path)
driver.get(url)
start_station_input = driver.find_element("id", "startStation")
start_station_input.send_keys(departure)  # 替换为实际的出发站名称

end_station_input = driver.find_element("id", "endStation")
end_station_input.send_keys(arrival)  # 替换为实际的抵达站名称

date_input = driver.find_element("id", "rideDate")
date_input.send_keys(date)
submit_button = driver.find_element("css selector", "input[type='submit']")
submit_button.click()
driver.implicitly_wait(10)  # 等待10秒
response = driver.page_source
soup = BeautifulSoup(response, "html.parser")

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
