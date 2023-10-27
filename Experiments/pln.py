import requests

pln = requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json').json()[32].get('rate')

print(
    str(pln)[:4] # 9.1234 -> 9.12
)
