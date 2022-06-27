from tinydb import TinyDB
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from tinydb import Query
from webdriver_manager.chrome import ChromeDriverManager

db = TinyDB("db1.json")

Todo = Query()
# db.purge()

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.yoox.com/us/women")
driver.execute_script("window.open('https://www.yoox.com/us/women');")
single_page_products_list_finder = ec.presence_of_all_elements_located(
    (By.CSS_SELECTOR, "div[class='itemData text-center']")
)


def product_info_scraper(link: str, tab_no: int):
    driver.switch_to.window(driver.window_handles[tab_no % 2])
    driver.get(f"{link}")
    time.sleep(3.5)
    single_page_products_list = WebDriverWait(driver=driver, timeout=10).until(method=single_page_products_list_finder)
    for product in single_page_products_list:
        data = {}
        try:
            product_url = product.find_element(by=By.CSS_SELECTOR, value="a[class='itemlink']")
            print(product_url.get_attribute('href'))
            data["url"] = product_url.get_attribute('href')
            if not db.contains(Todo.url == str(data['url'])):
                db.insert(data)
            else:
                pass
        except Exception as e:
            print(e)


from_page = 1
to_page = 2

for x in range(from_page, to_page + 1):
    url = f"https://www.yoox.com/us/women/clothing/shoponline/2#/dept=clothingwomen&gender=D&page={x}&season=X"
    product_info_scraper(url, x)

driver.close()
print("Finished")
