import openpyxl, json


def main():
    wb = openpyxl.load_workbook('two.xlsx')
    sheet = wb['Number and its square']
    items = sheet['A2':'B6']
    print(items)
    print()
    dict_of_values = dict()
    for row_of_cell_objects in items:
        key = row_of_cell_objects[0].value
        value = row_of_cell_objects[1].value
        dict_of_values[key] = value
    print(dict_of_values)
    print()

    string_of_dict = json.dumps(dict_of_values)
    print(type(string_of_dict))
    print(string_of_dict)

    with open('test_file.json', 'w') as file:
        json.dump(dict_of_values, file)



if __name__ == '__main__':
    main()