import json
import requests
import xlsxwriter
import argparse

markets = ['jita', 'perimeter', 'universe', 'amarr', "dodixie", "hek", "rens"]

parser = argparse.ArgumentParser(prog="EVEGetPrice")
parser.add_argument('-m', '--market', dest='market', default='jita', help="Market name")
parser.add_argument('-n', '--name', dest='name', default='Example', help="Name File")

args = parser.parse_args()

headers = {
    'User-Agent': 'A friend asked to take this information',
    'From': 'alex.sidorof@ya.ru'
}


def get_type_ids():
    print("Запрос всех id у https://esi.evetech.net/latest/markets/prices/")
    return [{"type_id": x['type_id']} for x in requests.get("https://esi.evetech.net/latest/markets/prices/",
                                                            headers=headers).json()]


def get_json(market_name):
    print("Пошли брать данные")
    return requests.post(F"https://evepraisal.com/appraisal/structured.json",
                         headers=headers,
                         data=json.dumps({
                             "market_name": market_name,
                             "items": get_type_ids()})).json()


def create_xlsx_file(market_name):
    workbook = xlsxwriter.Workbook(F"{args.name}.xlsx")
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    index = 0
    items = get_json(market_name)["appraisal"]["items"]
    for item in items:
        if item['prices']['sell']['min'] != 0:
            index += 1
            print(index,
                  "/",
                  len(items),
                  '=>',
                  item['typeName'],
                  '|',
                  market_name,
                  '|',
                  item['prices']['sell']['min'])

            worksheet.write(row, col, str(item['typeName']))
            worksheet.write(row, col + 1, market_name)
            worksheet.write(row, col + 2, item['prices']['sell']['min'])
            row += 1

    workbook.close()


if __name__ == '__main__':
    if args.market in ['jita', 'perimeter', 'universe', 'amarr', "dodixie", "hek", "rens"]:
        create_xlsx_file(market_name=args.market)
    else:
        print(F'Not found {args.market} in market')
        print(F'List, markets:', ', '.join(map(str, markets)))