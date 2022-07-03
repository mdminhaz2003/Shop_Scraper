import json
import re
import time
from tinydb import TinyDB
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from tinydb.queries import Query

condition = re.compile(r"(window.__PRELOADED_STATE__ = )")
db = TinyDB("harrods_db2.json")
url_db = TinyDB("harrods_db1.json")
db_data = url_db.all()
todo = Query()
base_url = "https://www.harrods.com"

chrome_options = uc.ChromeOptions()
driver = uc.Chrome(options=chrome_options)
driver.get(base_url)
driver.implicitly_wait(time_to_wait=5)
driver.switch_to.new_window('tab')


def scraper(product_url: str, tab_index: int) -> None:
    try:
        driver.switch_to.window(driver.window_handles[tab_index % 2])
        driver.get(f"{product_url}")
        time.sleep(2)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        script_tags = soup.find_all(name='script')
        data_script_tag = list(
            filter(
                lambda script_tag: re.findall(condition, script_tag.text.strip()), script_tags
            )
        )
        data = {
            "Handle": "",
            "Title": "",
            "Body (HTML)": "",
            "Vendor": "Eslam Hosny M.",
            "Standardized Product Type": "",
            "Custom Product Type": "",
            "Tags": "",
            "Published": "TRUE",
            "ID": product_url,
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
        text = ""

        for tag in data_script_tag:
            text = json.loads(re.sub(condition, "", tag.text.strip()).strip()).get("entities")

        categories_values = text.get("categories").values()
        brands_values = text.get("brands").values()
        products_values = text.get("products").values()

        handle_text = ""
        for value in brands_values:
            handle_text = f'"{value["slug"]}"'
            data["Title"] = f'"{value["name"]}"'

        price_text = ""
        available_sizes = []
        available_colors = []
        images_url = []
        for value in products_values:
            data["Custom Product Type"] = f'"{value["name"]}"'
            data["Google Shopping / AdWords Grouping"] = f'"{value["name"]}"'
            data["Body (HTML)"] = f'"{value["description"]}"'

            price_text = str(value["price"]["includingTaxes"]).replace(",", "")

            for color in value["colors"]:
                if color["tags"][0] == "MainColor":
                    available_colors.append(color["color"]["name"])
                else:
                    pass

            for size in value["sizes"]:
                available_sizes.append(size["name"])

            for img_urls in value["images"]:
                for source_key in img_urls["sources"].keys():
                    images_url.append(img_urls["sources"][source_key])

        tags = ""
        for value in categories_values:
            tags = value["name"] if tags == "" else f'{tags}, {value["name"]}'

        sizes = []
        for size in available_sizes:
            for _ in available_colors:
                sizes.append(size)

        colors = available_colors * len(available_sizes)
        price = [price_text for _ in colors]
        image_position = [str(number) for number in range(1, len(images_url) + 1)]

        max_rows = max(len(colors), len(sizes), len(images_url))
        variant_image = [images_url[0]]
        handle = [handle_text for _ in range(max_rows)]
        variant_inventory_policy = ["deny" for _ in range(max_rows)]
        variant_fulfilment_service = ["manual" for _ in range(max_rows)]
        variant_require_shipping = ["TRUE" for _ in range(max_rows)]
        variant_taxable = ["TRUE" for _ in range(max_rows)]
        variant_weight_unit = ["g" for _ in range(max_rows)]

        if len(colors) == len(sizes) == len(images_url) == len(image_position) == max_row:
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
            if max_rows > len(images_url):
                difference_between = max_rows - len(images_url)
                for _ in range(difference_between):
                    images_url.append("")
                    image_position.append("")
            if max_rows > len(variant_image):
                difference_between = max_rows - len(variant_image)
                for _ in range(difference_between):
                    variant_image.append("")

        data["Handle"] = handle
        data["Tags"] = f'"{tags}"'
        data["Option1 Value"] = colors
        data["Option2 Value"] = sizes
        data["Variant Price"] = price
        data["Variant Inventory Policy"] = variant_inventory_policy
        data["Variant Fulfillment Service"] = variant_fulfilment_service
        data["Image Src"] = images_url
        data["Image Position"] = image_position
        data["Variant Requires Shipping"] = variant_require_shipping
        data["Variant Taxable"] = variant_taxable
        data["Variant Image"] = variant_image
        data["Variant Weight Unit"] = variant_weight_unit

        if not db.contains(todo.ID == str(data['ID'])):
            db.insert(data)
            url_db.remove(todo.url == product_url)
        else:
            url_db.remove(todo.url == product_url)
            pass
        print("complete")
    except Exception as ex:
        print(ex)


for x in db_data:
    try:
        scraper(x['url'], db_data.index(x))
    except Exception as e:
        print(e)


