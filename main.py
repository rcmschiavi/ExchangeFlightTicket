import datetime
import requests
import json
import time

date_init = 13
stay_time = 86
menor_valor=30000
data_menor_valor_ida = 0
data_menor_valor_volta = 0

def nome_cidade(acao):
    try:
        cidade = input('Enter your {0} city:'.format(acao))
        url = 'https://www.decolar.com/suggestions?grouped=true&locale=pt_BR&profile=sbox-flights&hint={0}'.format(cidade)
        print(url)
        page = requests.get(url)
        page = page.text
        j = json.loads(page)
        codigo = j['items'][1]['items'][0]['target']['code']
        display = j['items'][1]['items'][0]['display']
        print('código: {0} cidade: {1}'.format(codigo,display))
        return codigo
    except:
        print('Nome incorreto! Tente digitar mais próximo do que deveria')

def busca_passagem(date_dep,date_ret):
    global menor_valor,data_menor_valor_ida,data_menor_valor_volta
    url = 'https://www.decolar.com/shop/flights-busquets/api/v1/web/calendar-prices/matrix?adults=1&children=0&infants=0&limit=10&site=BR&channel=site&from={0}&to={1}&departureDate=2018-09-{2}&returnDate=2018-12-{3}&groupBy=default&orderBy=total_price_ascending&viewMode=CLUSTER&language=pt_BR&streaming=false&airlineSummary=false&user=01be5064-a932-4505-be50-64a932050539&additionalProduct=NONE&h=baf8b759801e4b6c12a8333d0f72d32a&di=1-0&mustIncludeDates=NA_NA&currency=BRL&breakdownType=TOTAL_FARE_ONLY'.format(city_dep,city_arr,date_dep,date_ret)
    print(url)
    page = requests.get(url)
    page = page.text
    j = json.loads(page)
    try:
        preco = j['currentPrice']['amount']
        print(preco)
        if(preco<=menor_valor):
            menor_valor=preco
            data_menor_valor_ida=date_dep
            data_menor_valor_volta=date_ret
            print(menor_valor)
    except:
        print('Não há vôos entre essas cidades. Tente cidades próximas')

city_dep = nome_cidade('Departure')
city_arr = nome_cidade('Arrival')
print(city_dep)
print(city_arr)
date_dep_init = 12
date_ret = 11
time_stay = 83
for j in range (0,4):
    time_stay+=1
    for i in range (0,8):
        data_retorno = datetime.date(2018, 9, date_dep_init+i).toordinal() + time_stay
        data_retorno = datetime.date.fromordinal(data_retorno)
        data_retorno = data_retorno.day

        print(date_dep_init+i,data_retorno)
        busca_passagem(date_dep_init+i,data_retorno)
        time.sleep(0.5)

print(menor_valor,data_menor_valor_ida,data_menor_valor_volta)
