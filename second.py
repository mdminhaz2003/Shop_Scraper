import json
import time
from tinydb import TinyDB
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from tinydb.queries import Query
from webdriver_manager.chrome import ChromeDriverManager

db = TinyDB("db2.json")
second_db = TinyDB("db1.json")
db_data = second_db.all()
User = Query()


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.yoox.com/us/women")
driver.execute_script("window.open('https://www.yoox.com/us/women');")


def image_link_creator(code_10: str, key: str) -> str:
    code2 = code_10[:2]
    return f"https://www.yoox.com/images/items/{code2}/{code_10}_14{key}.jpg"


def scraper(product_url: str, tab_index: int) -> None:
    driver.switch_to.window(driver.window_handles[tab_index % 2])
    driver.get(f"{product_url}")
    time.sleep(2)
    data = {
        "Product_Key": "",
        "Handle": "",
        "Title": "",
        "Body_HTML": "",
        "Vendor": "",
        "Standardized_Product_Type": "",
        "Custom_Product_Type": "",
        "Tags": "",
        "Published": True,
        "Product_Images_Downloaded": "",
        "Product_URL": product_url,
        "Option1_Name": "Size",
        "Option1_Value": "",
        "Option2_Name": "Color",
        "Option2_Value": "",
        "Option3_Name": "",
        "Option3_Value": "",
        "Variant_SKU": "",
        "Variant_Grams": "",
        "Variant_Inventory_Tracker": "",
        "Variant_Inventory_Policy": "",
        "Variant_Fulfillment_Service": "",
        "Variant_Price": "",
        "Variant_Compare_At_Price": "",
        "Variant_Requires_Shipping": "",
        "Variant_Taxable": "",
        "Variant_Barcode": "",
        "Original_Image_Src": "",
        "Image_Src": "",
        "Image_Position": "",
        "Image_Alt_Text": "",
        "Gift_Card": "",
        "SEO_Title": "",
        "SEO_Description": "",
        "Google_Shopping__Google_Product_Category": "",
        "Google_Shopping__Gender": "",
        "Google_Shopping__Age_Group": "",
        "Google_Shopping__MPN": "",
        "Google_Shopping__AdWords_Grouping": "",
        "Google_Shopping__AdWords_Labels": "",
        "Google_Shopping__Condition": "",
        "Google_Shopping__Custom_Product": "",
        "Google_Shopping__Custom_Label_0": "",
        "Google_Shopping__Custom_Label_1": "",
        "Google_Shopping__Custom_Label_2": "",
        "Google_Shopping__Custom_Label_3": "",
        "Google_Shopping__Custom_Label_4": "",
        "Variant_Image": "",
        "Variant_Weight_Unit": "",
        "Variant_Tax_Code": "",
        "Cost_per_item": "",
        "Status": ""
    }
    try:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        page_info = soup.find(name='script', attrs={'id': '__NEXT_DATA__', 'type': 'application/json'})
        page_info = json.loads(page_info.text).get("props")["pageProps"]["initialState"]
        data["Handle"] = f"\"{page_info['itemApi']['brand']['name']}\""
        data["Title"] = f"\"{page_info['itemApi']['brand']['name']}\""
        data["Vendor"] = f'\"{page_info["itemApi"]["brand"]["name"]}\"'
        data["Body_HTML"] = f'\"{page_info["itemApi"]["descriptions"]["ItemDescription"]}\"'
        data["Custom_Product_Type"] = f'\"{page_info["itemApi"]["microCategory"]["singleDescription"]}\"'

        tags = ""
        for tag in page_info["breadcrumbs"]:
            tags = tag["title"] if tags == "" else f"{tags}, {tag['title']}"
        data["Tags"] = tags if "," not in tags else f"\"{tags}\""
        price = page_info["itemApi"]["priceFinal"]["transactional"]
        data["Variant_Price"] = f"\"{price['currency']}{price['amount']}\""

        sizes = [size['default']['text'] for size in page_info['itemApi']['sizes']]
        colors = [color["name"] for color in page_info["itemApi"]["colors"]]
        code10 = page_info["itemApi"]["code"]
        data["Product_Key"] = code10
        image_url = [image_link_creator(code10, format_key) for format_key in page_info["itemApi"]["imagesFormatValues"]]
        image_position = [str(value + 1) for value in range(len(image_url))]
        image_download_checker = [str(False) for _ in range(len(image_url))]

        max_rows = max(len(colors), len(sizes), len(image_url))

        if len(colors) == max_rows and len(sizes) == max_rows and len(image_url) == max_rows:
            data["Option1_Value"] = sizes
            data["Option2_Value"] = colors
            data["Original_Image_Src"] = image_url
            data["Image_Position"] = image_position
        else:
            if max_rows > len(colors):
                difference_between = max_rows - len(colors)
                for value in range(difference_between):
                    colors.append("")
            if max_rows > len(sizes):
                difference_between = max_rows - len(sizes)
                for value in range(difference_between):
                    sizes.append("")
            if max_rows > len(image_url):
                difference_between = max_rows - len(image_url)
                for value in range(difference_between):
                    image_url.append("")
                    image_position.append("")
                    image_download_checker.append("")

            data["Option1_Value"] = sizes
            data["Option2_Value"] = colors
            data["Original_Image_Src"] = image_url
            data["Image_Position"] = image_position
            data["Product_Images_Downloaded"] = image_download_checker

        if not db.contains(User.Product_Key == str(data['Product_Key'])):
            db.insert(data)
            second_db.remove(User.url == product_url)
        else:
            second_db.remove(User.url == product_url)
            pass
        print("complete")
        # print("\n\n")
    except Exception:
        pass


for x in db_data:
    try:
        scraper(x['url'], db_data.index(x))
    except Exception as e:
        print(e)


