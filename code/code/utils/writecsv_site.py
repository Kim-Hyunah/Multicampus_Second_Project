import csv
from email import header
from datetime import datetime as dt
comments = []
today = dt.today().strftime('%d-%m-%Y')

def make_csv(list, SEARCH, site):
    header = ['rating','review']
    filename = f'review_{SEARCH}_{site}_{today}.csv'

    with open(filename, 'w', encoding='utf-8', newline='')as f:
        writer = csv.writer(f)
        writer.writerow(header)    # writerow : s 없어야 한줄로 헤더 써짐ㅋㅋㅋㅋㅋ
        writer.writerows(list)
    f.close()

