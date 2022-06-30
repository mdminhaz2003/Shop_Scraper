import json
import time
import re
from tinydb import TinyDB
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from tinydb.queries import Query
from webdriver_manager.chrome import ChromeDriverManager

condition = re.compile(r"[,'/\\.()^&%$#@!~*|\"]")
db = TinyDB("db2.json")
second_db = TinyDB("db1.json")
db_data = second_db.all()
User = Query()


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.yoox.com/us/women")
driver.execute_script("window.open('https://www.yoox.com/us/women');")


def scraper(product_url: str, tab_index: int) -> None:
    driver.switch_to.window(driver.window_handles[tab_index % 2])
    driver.get(f"{product_url}")
    time.sleep(2)
    data = {
        "Handle": "",
        "Title": "",
        "Body (HTML)": "",
        "Vendor": "",
        "Standardized Product Type": "",
        "Custom Product Type": "",
        "Tags": "",
        "Published": "TRUE",
        "Product URL": product_url,
        "Option1 Name": "Color",
        "Option1 Value": "",
        "Option2 Name": "Size",
        "Option2 Value": "",
        "Option3 Name": "",
        "Option3 Value": "",
        "Variant SKU": "",
        "Variant Grams": "",
        "Variant Inventory Tracker": "",
        "Variant Inventory Qty": "",
        "Variant Inventory Policy": "",
        "Variant Fulfillment Service": "",
        "Variant Price": "",
        "Variant Compare At Price": "",
        "Variant Requires Shipping": "",
        "Variant Taxable": "",
        "Variant Barcode": "",
        "Image Src": "",
        "Image Position": "",
        "Image Alt Text": "",
        "Gift Card": "FALSE",
        "SEO Title": "",
        "SEO Description": "",
        "Google Shopping / Google Product Category": "",
        "Google Shopping / Gender": "",
        "Google Shopping / Age Group": "",
        "Google Shopping / MPN": "",
        "Google Shopping / AdWords Grouping": "",
        "Google Shopping / AdWords Labels": "",
        "Google Shopping / Condition": "",
        "Google Shopping / Custom Product": "FALSE",
        "Google Shopping / Custom Label 0": "",
        "Google Shopping / Custom Label 1": "",
        "Google Shopping / Custom Label 2": "",
        "Google Shopping / Custom Label 3": "",
        "Google Shopping / Custom Label 4": "",
        "Variant Image": "",
        "Variant Weight Unit": "",
        "Variant Tax Code": "",
        "Cost per item": "",
        "Status": "active"
    }
    try:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        page_info = soup.find(name='script', attrs={'id': '__NEXT_DATA__', 'type': 'application/json'})
        page_info = json.loads(page_info.text).get("props")["pageProps"]["initialState"]
        data["Title"] = f"\"{page_info['itemApi']['brand']['name']}\""
        data["Vendor"] = f'\"Eslam Hosny M."'
        data["Body (HTML)"] = f'\"{page_info["itemApi"]["descriptions"]["ItemDescription"]}\"'
        data["Custom Product Type"] = f'\"{page_info["itemApi"]["microCategory"]["singleDescription"]}\"'
        data["Google Shopping / AdWords Grouping"] = f'\"{page_info["itemApi"]["microCategory"]["singleDescription"]}\"'

        route = ""
        tags = ""
        for single_route in page_info["breadcrumbs"]:
            route = single_route["title"] if route == "" else f"{route} > {single_route['title']}"
            tags = single_route["title"] if tags == "" else f"{tags}, {single_route['title']}"
        # data["Standardized Product Type"] = f"\"{route}\""
        # data["Google Shopping / Google Product Category"] = f"\"{route}\""
        data["Tags"] = f"\"{tags}\""

        price_number = str(page_info["itemApi"]["priceFinal"]["transactional"]["amount"]).replace(",", "")

        available_sizes = [size['default']['text'] for size in page_info['itemApi']['sizes']]
        available_colors = [color["name"] for color in page_info["itemApi"]["colors"]]
        available_product_key = [color["code10"] for color in page_info["itemApi"]["colors"]]

        sizes = []
        handle_str = re.sub(pattern=condition, repl="", string=data["Title"].strip().lower())
        handle_str = handle_str.strip().replace(" ", "-")

        for size in available_sizes:
            for _ in range(len(available_colors)):
                sizes.append(size)

        colors = available_colors * len(available_sizes)
        price = [price_number for _ in colors]
        image_format_values = page_info["itemApi"]["imagesFormatValues"]

        image_url = []
        variant_image = []
        for code10 in available_product_key:
            for format_key in image_format_values:
                if image_format_values.index(format_key) == 0:
                    variant_image.append(f"https://cdn.yoox.biz//images/items/{code10[:2]}/{code10}_14{format_key}.jpg")
                else:
                    pass
                image_url.append(f"https://cdn.yoox.biz//images/items/{code10[:2]}/{code10}_14{format_key}.jpg")

        image_position = [str(number) for number in range(1, len(image_url) + 1)]

        max_rows = max(len(colors), len(sizes), len(image_url))

        handle = []
        variant_inventory_policy = []
        variant_fulfilment_service = []
        variant_require_shipping = []
        variant_taxable = []
        variant_weight_unit = []
        for _ in range(max_rows):
            handle.append(handle_str)
            variant_inventory_policy.append("deny")
            variant_fulfilment_service.append("manual")
            variant_require_shipping.append("TRUE")
            variant_taxable.append("TRUE")
            variant_weight_unit.append("g")

        if len(colors) == max_rows and len(sizes) == max_rows and len(image_url) == max_rows and len(variant_image) == max_rows:
            pass
        else:
            if max_rows > len(colors):
                difference_between = max_rows - len(colors)
                for _ in range(difference_between):
                    colors.append("")
                    price.append("")
            if max_rows > len(sizes):
                difference_between = max_rows - len(sizes)
                for _ in range(difference_between):
                    sizes.append("")
            if max_rows > len(image_url):
                difference_between = max_rows - len(image_url)
                for _ in range(difference_between):
                    image_url.append("")
                    image_position.append("")
            if max_rows > len(variant_image):
                difference_between = max_rows - len(variant_image)
                for _ in range(difference_between):
                    variant_image.append("")

        data["Handle"] = handle
        data["Option1 Value"] = colors
        data["Option2 Value"] = sizes
        data["Variant Price"] = price
        data["Variant Inventory Policy"] = variant_inventory_policy
        data["Variant Fulfillment Service"] = variant_fulfilment_service
        data["Image Src"] = image_url
        data["Image Position"] = image_position
        data["Variant Requires Shipping"] = variant_require_shipping
        data["Variant Taxable"] = variant_taxable
        data["Variant Image"] = variant_image
        data["Variant Weight Unit"] = variant_weight_unit

        if not db.contains(User.Product_Key == str(data['Product URL'])):
            db.insert(data)
            second_db.remove(User.url == product_url)
        else:
            second_db.remove(User.url == product_url)
            pass
        print("complete")
        # print("\n\n")
    except Exception as ex:
        print(ex)


for x in db_data:
    try:
        scraper(x['url'], db_data.index(x))
    except Exception as e:
        print(e)

