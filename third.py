from tinydb import TinyDB


db = TinyDB('db2.json')
db_data = db.all()
headers = [key for key in db_data[0].keys()]

header_text = ""
for header in headers:
    header_text = header if header_text == "" else f"{header_text},{header}"
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

                size_index = headers.index("Option1_Value") - 1
                color_index = headers.index("Option2_Value") - 1
                price_index = headers.index("Variant_Price") - 1
                img_link_index = headers.index("Original_Image_Src") - 1
                img_position_index = headers.index("Image_Position") - 1

                secondary_line_data_list[size_index] = single_row_data["Option1_Value"][value_index]
                secondary_line_data_list[color_index] = single_row_data["Option2_Value"][value_index]
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
                single_line_text += word if single_line_text == "" else f",{word}"
            single_line_text += "\n"
        file.write(single_line_text)

    file.close()
