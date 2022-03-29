from seleniumwire import webdriver
import time
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
import threading
import logging

url = "https://masa.finance/validator/"

logger = logging.getLogger()
logger.disabled = True

headless_input = str(input("Запускать браузер в фоновом режиме?(y/n): "))
count_acc = int(input("Введите количество почт: "))
threads = int(input("Колличество потоков: "))
executable_path = str(input("Перетяните chromedriver.exe: "))

useragent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--no-sandbox")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size-minimize_window")

if headless_input in ("y", "Y"):
    options.add_argument("--headless")

proxy_folder = str(input("Перетяните TXT файл с прокси, в формате user:pass@ip:port: "))
mail_folder = str(input("Перетяните TXT файл с почтами: "))

index_proxy = 0
count_error = 0
index_mail = 0


def take_proxy():
    global index_proxy
    with open(proxy_folder) as file:
        lines = file.readlines()
        for line in lines:
            line = lines[index_proxy]
            index_proxy += 1
            return line


def take_mail():
    global index_mail
    with open(mail_folder) as file:
        lines = file.readlines()
        for email in lines:
            email = lines[index_mail]
            index_mail += 1
            return email


def main():
    if index_proxy <= count_acc - 1:
        global count_error
        try:
            proxy_options = {"proxy": {"https": f"http://{take_proxy()}"}}
            options.add_argument(f"user-agent={useragent.random}")
            browser = webdriver.Chrome(
                executable_path=executable_path,
                seleniumwire_options=proxy_options,
                options=options,
            )
            browser.get(url=url)
            time.sleep(3)
            email_input = browser.find_element(
                By.XPATH, '//*[@id="__next"]/div[3]/div[4]/div/div[2]/input'
            )
            email_input.send_keys(take_mail())
            time.sleep(3)
            browser.find_element(
                By.XPATH, "/html/body/div[1]/div[3]/div[4]/div/div[2]/button"
            ).click()
            time.sleep(7)
            print(f"Почта успешно зарегистрирована")
            browser.quit()
            main()
        except:
            count_error += 1
            print(f"Ошибка в процессе: {index_proxy}")
            time.sleep(3)
            browser.quit()
            main()
    else:
        print(f"Конец цикла... Колличество ошибок: {count_error} ")


for _ in range(threads):
    threading.Thread(target=main).start()
