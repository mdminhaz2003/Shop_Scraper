from tinydb import TinyDB


db = TinyDB('self_ridges_db2.json')
db_data = db.all()
headers = [key for key in db_data[0].keys()]
value = headers.index("Option1 Value")
header_text = ""
for header in headers:
    header_text += f"{header},"
header_text += "\n"
with open("product_info_spotify_format.csv", "w") as file:
    file.write(header_text)
    for single_row_data in db_data:
        single_row_data_list = []
        first_line_data_list = ["" for value in headers]

        for key in single_row_data.keys():
            index = headers.index(key)
            if type(single_row_data[key]) is not list:
                first_line_data_list[index] = single_row_data[key]
            else:
                if len(single_row_data[key]) >= 1:
                    first_line_data_list[index] = single_row_data[key][0]
                else:
                    pass

        single_row_data_list.append(first_line_data_list)
        number_of_line = len(single_row_data["Option1 Value"])

        if number_of_line >= 2:
            value_index = 1
            for line in range(number_of_line - 1):
                secondary_line_data_list = ["" for value in headers]

                handle_index = headers.index("Handle")
                color_index = headers.index("Option1 Value")
                size_index = headers.index("Option2 Value")
                variant_inventory = headers.index("Variant Inventory Policy")
                variant_fulfil = headers.index("Variant Fulfillment Service")
                price_index = headers.index("Variant Price")
                variant_requires = headers.index("Variant Requires Shipping")
                variant_taxable = headers.index("Variant Taxable")
                variant_image = headers.index("Variant Image")
                img_link_index = headers.index("Image Src")
                img_position_index = headers.index("Image Position")
                variant_weight_unit = headers.index("Variant Weight Unit")

                secondary_line_data_list[handle_index] = single_row_data["Handle"][value_index]
                secondary_line_data_list[color_index] = single_row_data["Option1 Value"][value_index]
                secondary_line_data_list[size_index] = single_row_data["Option2 Value"][value_index]
                secondary_line_data_list[variant_inventory] = single_row_data["Variant Inventory Policy"][value_index]
                secondary_line_data_list[variant_fulfil] = single_row_data["Variant Fulfillment Service"][value_index]
                secondary_line_data_list[price_index] = single_row_data["Variant Price"][value_index]
                secondary_line_data_list[variant_requires] = single_row_data["Variant Requires Shipping"][value_index]
                secondary_line_data_list[variant_taxable] = single_row_data["Variant Taxable"][value_index]
                secondary_line_data_list[variant_image] = single_row_data["Variant Image"][value_index]

                secondary_line_data_list[img_link_index] = single_row_data["Image Src"][value_index]
                secondary_line_data_list[img_position_index] = single_row_data["Image Position"][value_index]
                secondary_line_data_list[variant_weight_unit] = single_row_data["Variant Weight Unit"][value_index]
                single_row_data_list.append(secondary_line_data_list)
                value_index += 1
        else:
            pass

        single_line_text = ""
        for line in single_row_data_list:
            for word in line:
                single_line_text += f"{word},"
            single_line_text += "\n"
        file.write(single_line_text)

    file.close()
