from tinydb import TinyDB
import json
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from tinydb import Query

db = TinyDB("harrods_db1.json")
todo = Query()
base_url = "https://www.harrods.com"

chrome_options = uc.ChromeOptions()
driver = uc.Chrome(options=chrome_options)
driver.get(base_url)
driver.implicitly_wait(time_to_wait=5)
driver.switch_to.new_window('tab')

index = []


def product_info_scraper(link: str, tab_no: int):
    try:
        driver.switch_to.window(driver.window_handles[tab_no % 2])
        time.sleep(1)
        driver.get(f"{link}")
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        page_info = soup.find(name="script", attrs={'type': 'application/ld+json'})
        page_info = json.loads(page_info.text.strip())
        for product in page_info.get("itemListElement"):
            product_url = f'{base_url}{str(product["url"]).replace("/shopping/shopping", "/shopping")}'
            if not db.contains(todo.url == product_url):
                db.insert({"url": product_url})
                print(product_url)
            else:
                pass
    except Exception as exception:
        index.append(tab_no)
        print(exception)


from_page = 1
to_page = 50
page_link = "https://www.harrods.com/en-bd/shopping/beauty?icid=megamenu_shop_beauty_beauty_view-all-beauty"

for x in range(from_page, to_page + 1):
    url = f"{page_link}&pageindex={x}"
    product_info_scraper(url, x)

# driver.close()
print("Finished")
