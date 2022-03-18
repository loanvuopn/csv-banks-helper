import csv
import os
import argparse
from os.path import exists

def check_match_code(list_bank_code, item):
    for i in range(len(list_bank_code)):
        if list_bank_code[i] == item:
            return True
    return False

def main():
    #==== Arguments ====
    parser = argparse.ArgumentParser(description='Perform set value to column banks CSV file.')
    parser.add_argument('-search', metavar='SEARCH', type=str, nargs='+', help='the search column')
    parser.add_argument('-column', metavar='COLUMN', type=str, nargs='+', help='the column name')
    parser.add_argument('-value', metavar='VALUE', type=str, nargs='+', help='the value of column')

    args = parser.parse_args()

    # Root path
    root_path = os.path.abspath(os.curdir)
    # Bank Csv file path
    bank_path = os.path.join(root_path, 'input', 'banks.csv')
    # Search column name
    search = args.search[0]
    # Update list
    search_path = os.path.join(root_path, 'input', 'bank_code.csv')
    # Output file
    output_path = os.path.join(root_path, 'output', 'banks.csv')
    # Header file
    column = args.column[0]
    # Column Value
    value = args.value[0]

    # Validation
    if not exists(bank_path):
        print("File banks.csv was not exist in [input] folder, please check!!!")
        exit()

    if not exists(search_path):
        print("File bank_code.csv was not exist in [input] folder, please check!!!")
        exit()

    # Build list value condition
    with open(search_path) as f:
        bank_code_list = f.readlines()

    for i in range(len(bank_code_list)):
        bank_code_list[i] = bank_code_list[i].strip("\n")

    # Update csv bank file
    csv_result = []
    with open(bank_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                csv_result.append(row)
            else:
                if row[search] != "" and check_match_code(bank_code_list, row[search]):
                    if row[column] == "":
                        row[column] = value
                csv_result.append(row)
            line_count += 1

    # Write final csv file
    fields = ['name', 'name_kana', 'bank_code', 'icon_uri', 'service_type', 'opened_at', 'closed_at', 'order', 'kana_order', 'bank_display_location']
    try:
        with open(output_path, 'w', encoding='utf-8', newline='') as csv_final:
            writer = csv.DictWriter(csv_final, fieldnames = fields)
            writer.writeheader()
            for data in csv_result:
                writer.writerow(data)
    except IOError:
        print("Can not save final file")

if __name__ == "__main__":
    main()