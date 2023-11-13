import string
from typing import Dict

import openpyxl
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

TIME_WAIT = 5
TIME_WAIT_CAPTCHA = 60

def parse_table(
    file_name: str, html_content: str, mode_show: int, write: int = 1
) -> None:
    soup = BeautifulSoup(html_content, "html.parser")

    if mode_show == 1:
        table = soup.find("table", class_="table-bordered table-striped table-sm")
    else:
        table = soup.find(
            "table", class_="table-fixed-columns table-bordered table-striped table-sm"
        )

    if table is None:
        print("Нет информации")
        return

    tbody = table.find("tbody")
    trs = tbody.find_all("tr")

    if write:
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        for n, tr in enumerate(trs, start=1):
            for alpha_number, td in enumerate(tr.find_all("td"), start=0):
                sheet[f"{string.ascii_uppercase[alpha_number]}{n}"] = td.text
                print(td.text, end=" ")
            print()
        workbook.save(f"{file_name}.xlsx")
        print("Данные записаны")
    else:
        for n, tr in enumerate(trs, start=1):
            for alpha_number, td in enumerate(tr.find_all("td"), start=0):
                print(td.text, end=" ")
            print()


ua = UserAgent()
user_agent = ua.random
print(user_agent)

options = webdriver.ChromeOptions()
options.add_argument(f"--user-agent={user_agent}")
options.add_argument("--incognito")
# options.add_argument('--proxy-server=94.228.194.18:41890')
driver = webdriver.Chrome(options=options)
url = "http://www.cikrf.ru/"

try:
    driver.get(url)

    wait = WebDriverWait(driver, TIME_WAIT)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "menu_item_li")))
    except TimeoutException:
        wait = WebDriverWait(driver, TIME_WAIT_CAPTCHA)
        print("Решите капчу")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "menu_item_li")))

    menu_items = driver.find_elements(By.CLASS_NAME, "menu_item_li")
    menu_items[2].click()

    wait = WebDriverWait(driver, TIME_WAIT)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "popup_menu_item")))
    except TimeoutException:
        wait = WebDriverWait(driver, TIME_WAIT_CAPTCHA)
        print("Решите капчу")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "popup_menu_item")))

    regions = driver.find_element(By.TAG_NAME, "select").find_elements(
        By.TAG_NAME, "option"
    )
    choices_regions: Dict[int, WebElement] = {}

    for number, region in enumerate(regions[1:], start=1):
        choices_regions.setdefault(number, region)
        print(f"{number}: {region.text}")

    input_selection = int(input("Введите номер территории: "))
    region_site_url = choices_regions[input_selection].get_property("value")

    driver.get(region_site_url)

    wait = WebDriverWait(driver, TIME_WAIT)
    try:
        wait.until(
            EC.presence_of_element_located((By.ID, "horizontal-multilevel-menu"))
        )
    except TimeoutException:
        wait = WebDriverWait(driver, TIME_WAIT_CAPTCHA)
        print("Решите капчу")
        wait.until(
            EC.presence_of_element_located((By.ID, "horizontal-multilevel-menu"))
        )

    menu_items = driver.find_elements(By.TAG_NAME, "li")
    menu_items[1].click()

    wait = WebDriverWait(driver, TIME_WAIT)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "border")))
    except TimeoutException:
        wait = WebDriverWait(driver, TIME_WAIT_CAPTCHA)
        print("Решите капчу")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "border")))

    left_blocks = driver.find_elements(By.CLASS_NAME, "border")
    for block in left_blocks:
        link = block.find_element(By.TAG_NAME, "a")
        if link.text == "Календарь выборов":
            calendar_elections_url = link.get_property("href")
            driver.get(calendar_elections_url)

            wait = WebDriverWait(driver, TIME_WAIT)
            try:
                wait.until(EC.presence_of_element_located((By.ID, "close_filters")))
            except TimeoutException:
                wait = WebDriverWait(driver, TIME_WAIT_CAPTCHA)
                print("Решите капчу")
                wait.until(EC.presence_of_element_located((By.ID, "close_filters")))

            show_filter = driver.find_element(By.ID, "close_filters")
            show_filter.click()

            wait = WebDriverWait(driver, TIME_WAIT)
            try:
                wait.until(EC.presence_of_element_located((By.ID, "start_date")))
            except TimeoutException:
                wait = WebDriverWait(driver, TIME_WAIT_CAPTCHA)
                print("Решите капчу")
                wait.until(EC.presence_of_element_located((By.ID, "start_date")))

            start_date = input("Введите начальную дату: ")
            input_start_date = driver.find_element(By.ID, "start_date")
            input_start_date.clear()
            input_start_date.send_keys(start_date)

            end_date = input("Введите конечную дату: ")
            input_end_date = driver.find_element(By.ID, "end_date")
            input_end_date.clear()
            input_end_date.send_keys(end_date)

            selects = driver.find_elements(By.TAG_NAME, "select")
            label_selects = [
                "Уровень выборов",
                "Вид выборов / Референдумов",
                "Тип выборов",
                "Система выборов",
            ]
            i = 0
            for select in selects:
                choices_option: Dict[int, WebElement] = {}
                options = select.find_elements(By.TAG_NAME, "option")
                print("Чтобы ничего не выбирать нажмите Enter")
                print(label_selects[i])
                for number, option in enumerate(options, start=1):
                    choices_option.setdefault(number, option)
                    print(number, ":", option.text)
                input_option = input("Напишите свой выбор: ")
                if input_option != "":
                    choices_option[int(input_option)].click()
                i += 1

            button_search = driver.find_element(By.ID, "calendar-btn-search")
            button_search.click()

            wait = WebDriverWait(driver, TIME_WAIT)
            try:
                wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "list-group-item"))
                )
            except TimeoutException:
                wait = WebDriverWait(driver, TIME_WAIT_CAPTCHA)
                print("Решите капчу")
                wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "list-group-item"))
                )

            results = driver.find_elements(By.CLASS_NAME, "list-group-item")

            content = BeautifulSoup(driver.page_source, "html.parser")
            list_group_item = content.find_all(class_="list-group-item")

            elections: Dict[int, str] = {}
            number = 1
            print("-" * 100)
            for item in list_group_item:
                child_elements = item.find_all(True)
                if not child_elements:
                    print(item.text)
                    print("-" * 100)
                    continue
                span_element = item.find("span")

                if span_element:
                    print(span_element.text)
                    print("-" * 100)
                child_div = item.find("div")

                if child_div:
                    nested_divs = child_div.find_all("div")

                    if len(nested_divs) == 2:
                        print(
                            number,
                            ": ",
                            nested_divs[0].text or " " * 50,
                            " | ",
                            nested_divs[1].text,
                        )
                        print("-" * 100)
                        link = nested_divs[1].find("a", href=True)["href"]
                        elections.setdefault(number, link)
                number += 1
            input_election = int(input("Введите номер который хотите посмотреть: "))

            driver.get(elections[input_election])

            wait = WebDriverWait(driver, TIME_WAIT)
            try:
                wait.until(
                    EC.presence_of_element_located((By.ID, "election-results-name"))
                )
            except TimeoutException:
                wait = WebDriverWait(driver, TIME_WAIT_CAPTCHA)
                print("Решите капчу")
                wait.until(
                    EC.presence_of_element_located((By.ID, "election-results-name"))
                )

            election_results = driver.find_element(By.ID, "election-results-name")
            election_results.click()

            wait = WebDriverWait(driver, TIME_WAIT)
            try:
                wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".nav-link.active.show")
                    )
                )
            except TimeoutException:
                wait = WebDriverWait(driver, TIME_WAIT_CAPTCHA)
                print("Решите капчу")
                wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".nav-link.active.show")
                    )
                )

            content = BeautifulSoup(driver.page_source, "html.parser")
            all_tbody = content.find_all("tbody")

            links = all_tbody[-1].find_all_next("a", href=True)

            choices: Dict[int, str] = {}
            for number, link in enumerate(links, start=1):
                choices.setdefault(number, link["href"])
                print(number, ": ", link.text)

            choice_input = int(input("Выберите какой вариант будете просматривать: "))

            driver.get(choices[choice_input])

            wait = WebDriverWait(driver, TIME_WAIT)
            try:
                wait.until(EC.presence_of_element_located((By.ID, "jstree_demo_div")))
            except TimeoutException:
                wait = WebDriverWait(driver, TIME_WAIT_CAPTCHA)
                print("Решите капчу")
                wait.until(EC.presence_of_element_located((By.ID, "jstree_demo_div")))

            selected_item = driver.find_element(By.CLASS_NAME, "selected-li")
            choices: Dict[int, WebElement] = {}
            while True:
                try:
                    options = (
                        selected_item.find_element(By.XPATH, "..")
                        .find_element(By.TAG_NAME, "ul")
                        .find_elements(By.TAG_NAME, "li")
                    )
                except NoSuchElementException:
                    options = []
                print("*", selected_item.text)
                print(0, ":", "Записать данные по данному пункту")
                if choices.get(1) is not None:
                    print(1, ":", choices.get(1).text)
                else:
                    print(1, ":")
                for number, option in enumerate(options, start=2):
                    choices.setdefault(
                        number, option.find_elements(By.TAG_NAME, "a")[-1]
                    )
                    print(number, ":", option.text)
                choice = int(input("Выберите пункт: "))
                if choice == 0:
                    name_file = input("Введите название для файла: ")
                    parse_table(name_file, driver.page_source, choice_input)
                else:
                    choices[choice].click()
                    wait = WebDriverWait(driver, TIME_WAIT)
                    try:
                        wait.until(
                            EC.presence_of_element_located((By.ID, "jstree_demo_div"))
                        )
                    except TimeoutException:
                        wait = WebDriverWait(driver, TIME_WAIT_CAPTCHA)
                        print("Решите капчу")
                        wait.until(
                            EC.presence_of_element_located((By.ID, "jstree_demo_div"))
                        )
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    selected_li = (
                        soup.find(class_="selected-li")
                        .find_previous("li")
                        .find_previous("ul")
                        .find_previous("li")
                        .find_all("a", href=True)
                    )
                    selected_item = driver.find_element(By.CLASS_NAME, "selected-li")
                    if selected_li:
                        href = selected_li[0]["href"]
                        previous_selected_item = selected_item.find_element(
                            By.XPATH, "../../.."
                        ).find_element(By.XPATH, f'//a[@href="{href}"]')
                        choices: Dict[int, WebElement] = {1: previous_selected_item}
                    else:
                        choices: Dict[int, WebElement] = {}
except WebDriverException:
    print("Что-то пошло не так...проверьте соединение")
finally:
    driver.delete_all_cookies()
    driver.quit()
