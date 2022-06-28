from tinydb import TinyDB


db = TinyDB('db2.json')
db_data = db.all()
headers = [key for key in db_data[0].keys()]
value = headers.index("Option1_Value")
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
        number_of_line = len(single_row_data["Option1_Value"])

        if number_of_line >= 2:
            value_index = 1
            for line in range(number_of_line - 1):
                secondary_line_data_list = ["" for value in headers]

                size_index = headers.index("Option1_Value")
                color_index = headers.index("Option2_Value")
                rgb_color = headers.index("Option3_Value")
                product_key = headers.index("Option4_Value")
                color_code = headers.index("Option5_Value")
                price_index = headers.index("Variant_Price")
                img_link_index = headers.index("Original_Image_Src")
                img_position_index = headers.index("Image_Position")

                secondary_line_data_list[size_index] = single_row_data["Option1_Value"][value_index]
                secondary_line_data_list[color_index] = single_row_data["Option2_Value"][value_index]
                secondary_line_data_list[rgb_color] = single_row_data["Option3_Value"][value_index]
                secondary_line_data_list[product_key] = single_row_data["Option4_Value"][value_index]
                secondary_line_data_list[color_code] = single_row_data["Option5_Value"][value_index]
                secondary_line_data_list[price_index] = single_row_data["Variant_Price"]
                secondary_line_data_list[img_link_index] = single_row_data["Original_Image_Src"][value_index]
                secondary_line_data_list[img_position_index] = single_row_data["Image_Position"][value_index]
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
