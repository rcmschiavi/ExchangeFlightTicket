import datetime
import requests
import json
import time
import sheet

date_init = 13
stay_time = 86
menor_valor=30000
data_menor_valor_ida = 0
data_menor_valor_volta = 0

def nome_cidade(acao):
    try:
        cidade = input('Enter your {0} city:'.format(acao))
        url = 'https://www.decolar.com/suggestions?grouped=true&locale=pt_BR&profile=sbox-flights&hint={0}'.format(cidade)
        page = requests.get(url)
        page = page.text
        j = json.loads(page)
        codigo = j['items'][1]['items'][0]['target']['code']
        display = j['items'][1]['items'][0]['display']
        print('Code: {0} City: {1}'.format(codigo,display))
        return codigo,display
    except:
        print('City not found. Try again!')
        return 0

def busca_passagem(date_dep,date_ret,mes_retorno,ano_retorno):
    global menor_valor,data_menor_valor_ida,data_menor_valor_volta,cont,inc_estadia,incr_dias
    url = 'https://www.decolar.com/shop/flights-busquets/api/v1/web/calendar-prices/matrix?adults=1&children=0&infants=0&limit=10&site=BR&channel=site&from={0}&to={1}&departureDate=2018-09-{2}&returnDate={5}-{4}-{3}&groupBy=default&orderBy=total_price_ascending&viewMode=CLUSTER&language=pt_BR&streaming=false&airlineSummary=false&user=01be5064-a932-4505-be50-64a932050539&additionalProduct=NONE&h=baf8b759801e4b6c12a8333d0f72d32a&di=1-0&mustIncludeDates=NA_NA&currency=BRL&breakdownType=TOTAL_FARE_ONLY'.format(city_dep[0],city_arr[0],date_dep,date_ret,mes_retorno,ano_retorno)
    page = requests.get(url)
    page = page.text
    j = json.loads(page)
    print('{0}%'.format(int(cont*100/(inc_estadia*incr_dias))))
    try:
        preco = j['currentPrice']['amount']
        if(preco<=menor_valor):
            menor_valor=preco
            data_menor_valor_ida=date_dep
            data_menor_valor_volta=date_ret
        return preco
    except:
        return -1

city_dep = nome_cidade('Departure')
while(city_dep==0):
    city_dep = nome_cidade('Departure')
city_arr = nome_cidade('Arrival')
while(city_arr==0):
    city_arr = nome_cidade('Arrival')
date_dep_init = 10
cont = 0
inc_estadia = 7
incr_dias = 16
sheet.grava_linha([0,0,0,0,0,0],cont)
print("Loading. Please, wait! Avoid any search on decolar's site while this runs, it may cause some error.")
for j in range (0,inc_estadia):
    time_stay=84
    time_stay+=j
    for i in range (0,incr_dias):
        cont+=1
        date_dep = date_dep_init + i
        data_ida = datetime.date(2018, 9, date_dep)
        data_retorno = data_ida.toordinal() + time_stay
        data_retorno = datetime.date.fromordinal(data_retorno)
        dia_retorno = data_retorno.day
        mes_retorno = data_retorno.month
        ano_retorno = data_retorno.year
        preco = busca_passagem(date_dep_init+i,dia_retorno,mes_retorno,ano_retorno)
        linha=[city_dep[1],city_arr[1],'{0}/{1}/{2}'.format(data_ida.day,data_ida.month,data_ida.year),'{0}/{1}/{2}'.format(data_retorno.day,data_retorno.month,data_retorno.year),preco,time_stay]
        print("Partial amount: R${0} Outbound:{1} Return:{2} Days:{3} ".format(preco,data_ida,data_retorno,time_stay))
        sheet.grava_linha(linha,cont)
        sheet.salvar("{0}-{1}".format(city_dep[0],city_arr[0]))

print("Mission success, open the file {0}-{1}.xls located at the same folder of this program".format(city_dep[0],city_arr[0]))
#Para criar o exe
#pyinstaller --onefile main.py