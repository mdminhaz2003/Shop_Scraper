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


def scraper(product_url: str, tab_index: int) -> None:
    driver.switch_to.window(driver.window_handles[tab_index % 2])
    driver.get(f"{product_url}")
    time.sleep(2)
    data = {
        "Primary_Key": "",
        "Handle": "",
        "Title": "",
        "Body_HTML": "",
        "Vendor": "",
        "Standardized_Product_Type": "",
        "Custom_Product_Type": "",
        "Tags": "",
        "Published": True,
        "Product_URL": product_url,
        "Option1_Name": "Size",
        "Option1_Value": "",
        "Option2_Name": "Color",
        "Option2_Value": "",
        "Option3_Name": "RGB_Color",
        "Option3_Value": "",
        "Option4_Name": "Product_Key",
        "Option4_Value": "",
        "Option5_Name": "Color_Code",
        "Option5_Value": "",
        "Option6_Name": "",
        "Option6_Value": "",
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
        rgb_color = [color["rgb"] for color in page_info["itemApi"]["colors"]]
        product_key = [color["code10"] for color in page_info["itemApi"]["colors"]]
        color_code = [color["colorCode"] for color in page_info["itemApi"]["colors"]]
        image_format_values = page_info["itemApi"]["imagesFormatValues"]

        image_url = []
        image_position = []
        key = ""
        for code10 in product_key:
            key += code10
            position = 1
            for format_key in image_format_values:
                image_url.append(f"https://www.yoox.com/images/items/{code10[:2]}/{code10}_14{format_key}.jpg")
                image_position.append(str(position))
                position += 1

        max_rows = max(len(colors), len(sizes), len(image_url))

        if len(colors) == max_rows and len(sizes) == max_rows and len(image_url) == max_rows:
            data["Primary_Key"] = key
            data["Option1_Value"] = sizes
            data["Option2_Value"] = colors
            data["Option3_Value"] = rgb_color
            data["Option4_Value"] = product_key
            data["Option5_Value"] = color_code
            data["Original_Image_Src"] = image_url
            data["Image_Position"] = image_position
        else:
            if max_rows > len(colors):
                difference_between = max_rows - len(colors)
                for _ in range(difference_between):
                    colors.append("")
                    rgb_color.append("")
                    product_key.append("")
                    color_code.append("")
            if max_rows > len(sizes):
                difference_between = max_rows - len(sizes)
                for _ in range(difference_between):
                    sizes.append("")
            if max_rows > len(image_url):
                difference_between = max_rows - len(image_url)
                for _ in range(difference_between):
                    image_url.append("")
                    image_position.append("")

            data["Primary_Key"] = key
            data["Option1_Value"] = sizes
            data["Option2_Value"] = colors
            data["Option3_Value"] = rgb_color
            data["Option4_Value"] = product_key
            data["Option5_Value"] = color_code
            data["Original_Image_Src"] = image_url
            data["Image_Position"] = image_position

        if not db.contains(User.Product_Key == str(data['Primary_Key'])):
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


