from tkinter import *
import requests
import json
import datetime


def proximohorario():
    global horaInicial
    global dataInicial
    global primeiroDia

    horaInicial = str(int(horaInicial) + 3)
    if horaInicial == '24':
        horaInicial = '00'
        data = datetime.date(int(dataInicial[6:]), int(dataInicial[3:5]), int(dataInicial[0:2]))
        data = data + datetime.timedelta(days=1)
        dataInicial = data.strftime('%d/%m/%Y')

    if len(horaInicial) == 1:
        horaInicial = '0'+horaInicial

    if dataInicial != primeiroDia:
        primeiroDia = dataInicial
        return False
    else:
        return True


root = Tk()
root.title('Weather App (results from www.7timer.info)')
root.iconbitmap('./weather.ico')
root.geometry("1235x715")

horaInicial = ''
dataInicial = ''
primeiroDia = ''

opcoes = ['-', 'Sorocaba', 'São Paulo', 'Poá', 'Suzano', 'Londres, UK', 'Munique, GE']

clicado = StringVar()
clicado.set(opcoes[0])


# locationLookup function
def locationLookup():
    global horaInicial
    global dataInicial
    global primeiroDia
    global opcoes

    opclong = ['-', '-47.485', '-46.64', '-46.344', '-46.309', '-0.128', '11.582']
    opclati = ['-', '-23.471', '-23.556', '-23.52', '-23.538', '51.507', '48.135']

    escolhido = clicado.get()
    print(escolhido)
    if escolhido == opcoes[0]:
        lon = longitude.get()
        lat = latitude.get()
    else:
        lon = opclong[opcoes.index(escolhido)]
        lat = opclati[opcoes.index(escolhido)]
        longitude.delete(0, END)
        latitude.delete(0, END)
        longitude.insert(0, lon)
        latitude.insert(0, lat)

    velocVento = [
        '(calmo)',
        '(leve)',
        '(moderado)',
        '(fresco)',
        '(forte)',
        '(ventania)',
        '(tempestade)',
        '(furacão)'
    ]

    climas = {
        'clearday': 'Limpo',
        'pcloudyday': 'Parcialmente Nublado',
        'mcloudyday': 'Nublado',
        'cloudyday': 'Muito Nublado',
        'humidday': 'Nevoeiro',
        'lightrainday': 'Chuva Leve ou Garoa',
        'oshowerday': 'Chuvas Ocasionais',
        'ishowerday': 'Chuvas Isoladas',
        'lightsnowday': 'Neve Leve ou Ocasional',
        'rainday': 'Chuva',
        'snowday': 'Neve',
        'rainsnowday': 'Chuva e Neve',
        'tsday': 'Possível Tempestade',
        'tsrainday': 'Tempestade',
        'clearnight': 'Limpo',
        'pcloudynight': 'Parcialmente Nublado',
        'mcloudynight': 'Nublado',
        'cloudynight': 'Muito Nublado',
        'humidnight': 'Nevoeiro',
        'lightrainnight': 'Chuva Leve ou Garoa',
        'oshowernight': 'Chuvas Ocasionais',
        'ishowernight': 'Chuvas Isoladas',
        'lightsnownight': 'Neve Leve ou Ocasional',
        'rainnight': 'Chuva',
        'snownight': 'Neve',
        'rainsnownight': 'Chuva e Neve',
        'tsnight': 'Possível Tempestade',
        'tsrainnight': 'Tempestade'
    }
    # na página:
    # http://www.7timer.info/index.php?product=civil&lang=en&lon=-47.4851488&lat=-23.470905
    # arquivo json:
    # http://www.7timer.info/bin/api.pl?lon=-47.485&lat=-23.471&product=civil&output=json

    # Sorocaba = lon=-47.485&lat=-23.471
    # São Paulo = lon=-46.64&lat=-23.556
    # Poá = lon=-46.344&lat=-23.52
    # Suzano = lon=-46.309&lat=-23.538

    # Londres, UK = lon=-0.128&lat=51.507
    # Munique, GE = lon=11.582&lat=48.135

    quadro = list()

    try:
        url = "http://www.7timer.info/bin/api.pl?lon="+lon+"&lat="+lat+"&product=civil&output=json"
        print(url)
        api_request = requests.get(url)
        api = json.loads(api_request.content)

        horaInicial = api['init'][-2:]
        dataInicial = api['init'][6:8]+"/"+api['init'][4:6]+"/"+api['init'][0:4]

        SerieDeDados = api['dataseries']

        primeiroDia = dataInicial

        linha = list()
        quadro = list()

        for serie in SerieDeDados:
            if serie['weather'][-3:] == 'day':
                DiaNoite = 'D'
            else:
                DiaNoite = 'N'

            mensagem = dataInicial + " " + horaInicial + " h\n"
            mensagem = mensagem + str(serie['temp2m']) + " °C  Umid: "
            mensagem = mensagem + serie['rh2m'] + "\nVento: "
            mensagem = mensagem + serie['wind10m']['direction'] + " "
            mensagem = mensagem + velocVento[serie['wind10m']['speed']-1] + "\n"
            mensagem = mensagem + climas[serie['weather']]
            mensagem = mensagem + "_" + DiaNoite

            if proximohorario():
                linha.append(mensagem)
            else:
                linha.append(mensagem)
                quadro.append(linha)
                linha = list()

        if len(linha) > 0:
            quadro.append(linha)

    except Exception as e:
        api = "Error..."

    if api != "Error...":
        nLin = -1
        for reg in quadro:
            nLin += 1
            nCol = 0
            if len(reg) < 8 and nLin == 0:
                nCol = (8-len(reg))

            for prev in reg:
                if '_D' in prev:
                    corFundo = "yellow"
                    corLetra = "black"
                else:
                    corFundo = "blue"
                    corLetra = "white"
                myButton = Button(root, text=prev, width=20, background=corFundo, foreground=corLetra, justify='center')
                myButton.grid(row=nLin+1, column=nCol, padx=2, pady=2)
                nCol += 1
    else:
        print(api)


cidadeLabel = Label(root, text='Cidades:')
longLabel = Label(root, text='Longitude:')
latiLabel = Label(root, text='Latitude:')
cidade = OptionMenu(root, clicado, *opcoes)
longitude = Entry(root)
latitude = Entry(root)
botao = Button(root, text='Selecionar', command=locationLookup)

cidadeLabel.grid(row=0, column=0, pady=8)
cidade.grid(row=0, column=1)
longLabel.grid(row=0, column=2)
longitude.grid(row=0, column=3)
latiLabel.grid(row=0, column=4)
latitude.grid(row=0, column=5)
botao.grid(row=0, column=6)

root.mainloop()

'''
wind speed:
1	Below 0.3m/s (calm)
2	0.3-3.4m/s (light)
3	3.4-8.0m/s (moderate)
4	8.0-10.8m/s (fresh)
5	10.8-17.2m/s (strong)
6	17.2-24.5m/s (gale)
7	24.5-32.6m/s (storm)
8	Over 32.6m/s (hurricane)

1	Abaixo de 0.3m/s (calmo)
2	0.3-3.4m/s (leve)
3	3.4-8.0m/s (moderado)
4	8.0-10.8m/s (fresco)
5	10.8-17.2m/s (forte)
6	17.2-24.5m/s (ventania)
7	24.5-32.6m/s (tempestade)
8	Over 32.6m/s (furacão)

weather: 

Meaning	                    Technical Definition

Clear	                    clearday, clearnight         - Total cloud cover less than 20%
Partly Cloudy	            pcloudyday, pcloudynight     - Total cloud cover between 20%-60%
Cloudy	                    mcloudyday, mcloudynight     - Total cloud cover between 60%-80%
Very Cloudy	                cloudyday, cloudynight       - Total cloud cover over over 80%
Foggy	                    humidday, humidnight         - Relative humidity over 90% with total cloud cover less than 60%
Light rain or showers	    lightrainday, lightrainnight - Precipitation rate less than 4mm/hr with cloud cover more than 80%
Occasional showers	        oshowerday, oshowernight     - Precipitation rate less than 4mm/hr with cloud cover between 60%-80%
Isolated showers	        ishowerday, ishowernight     - Precipitation rate less than 4mm/hr less than 60%
Light or occasional snow	lightsnowday, lightsnownight - Precipitation rate less than 4mm/hr
Rain	                    rainday, rainnight           - Precipitation rate over 4mm/hr
Snow	                    snowday, snownight           - Precipitation rate over 4mm/hr
Mixed	                    rainsnowday, rainsnownight   - Precipitation type to be ice pellets or freezing rain
Thunderstorm possible	    tsday, tsnight               - Lifted Index less than -5 with precipitation rate below 4mm/hr
Thunderstorm	            tsrainday, tsrainnight       - Lifted Index less than -5 with precipitation rate over 4mm/hr
Windy	                    Sustained wind speed over 10.8m/s (force 6 or above)

Limpo	                    clearday, clearnight         - Total cloud cover less than 20%
Parcialmente Nublado        pcloudyday, pcloudynight     - Total cloud cover between 20%-60%
Nublado                     mcloudyday, mcloudynight     - Total cloud cover between 60%-80%
Muito Nublado               cloudyday, cloudynight       - Total cloud cover over over 80%
Nevoeiro                    humidday, humidnight         - Relative humidity over 90% with total cloud cover less than 60%
Chuva Leve ou Garoa  	    lightrainday, lightrainnight - Precipitation rate less than 4mm/hr with cloud cover more than 80%
Chuvas Ocasionais 	        oshowerday, oshowernight     - Precipitation rate less than 4mm/hr with cloud cover between 60%-80%
Chuvas Isoladas 	        ishowerday, ishowernight     - Precipitation rate less than 4mm/hr less than 60%
Neve Leve ou Ocasional  	lightsnowday, lightsnownight - Precipitation rate less than 4mm/hr
Chuva                       rainday, rainnight           - Precipitation rate over 4mm/hr
Neve	                    snowday, snownight           - Precipitation rate over 4mm/hr
Chuva e Neve                rainsnowday, rainsnownight   - Precipitation type to be ice pellets or freezing rain
Possível Tempestade  	    tsday, tsnight               - Lifted Index less than -5 with precipitation rate below 4mm/hr
Tempestade  	            tsrainday, tsrainnight       - Lifted Index less than -5 with precipitation rate over 4mm/hr
Vendaval                    Sustained wind speed over 10.8m/s (force 6 or above)
 
'dataseries': 
    [
    {'timepoint': 3, 'cloudcover': 1, 'lifted_index': 2, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 18, 'rh2m': '65%', 'wind10m': {'direction': 'W', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 6, 'cloudcover': 1, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 15, 'rh2m': '71%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 9, 'cloudcover': 1, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 14, 'rh2m': '73%', 'wind10m': {'direction': 'S', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 12, 'cloudcover': 1, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 13, 'rh2m': '77%', 'wind10m': {'direction': 'S', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 15, 'cloudcover': 1, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 13, 'rh2m': '89%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 18, 'cloudcover': 1, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 17, 'rh2m': '78%', 'wind10m': {'direction': 'SE', 'speed': 3}, 'weather': 'clearday'}, 
    {'timepoint': 21, 'cloudcover': 2, 'lifted_index': 2, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 21, 'rh2m': '56%', 'wind10m': {'direction': 'SE', 'speed': 3}, 'weather': 'clearday'}, 
    {'timepoint': 24, 'cloudcover': 3, 'lifted_index': 2, 'prec_type': 'rain', 'prec_amount': 1, 'temp2m': 20, 'rh2m': '61%', 'wind10m': {'direction': 'SE', 'speed': 3}, 'weather': 'ishowerday'}, 
    {'timepoint': 27, 'cloudcover': 7, 'lifted_index': 2, 'prec_type': 'rain', 'prec_amount': 0, 'temp2m': 15, 'rh2m': '83%', 'wind10m': {'direction': 'SE', 'speed': 3}, 'weather': 'oshowernight'}, 
    {'timepoint': 30, 'cloudcover': 6, 'lifted_index': 6, 'prec_type': 'rain', 'prec_amount': 0, 'temp2m': 15, 'rh2m': '86%', 'wind10m': {'direction': 'SE', 'speed': 3}, 'weather': 'oshowernight'}, 
    {'timepoint': 33, 'cloudcover': 7, 'lifted_index': 2, 'prec_type': 'rain', 'prec_amount': 0, 'temp2m': 15, 'rh2m': '77%', 'wind10m': {'direction': 'SE', 'speed': 3}, 'weather': 'oshowernight'}, 
    {'timepoint': 36, 'cloudcover': 7, 'lifted_index': 6, 'prec_type': 'rain', 'prec_amount': 0, 'temp2m': 13, 'rh2m': '90%', 'wind10m': {'direction': 'SE', 'speed': 3}, 'weather': 'oshowernight'}, 
    {'timepoint': 39, 'cloudcover': 3, 'lifted_index': 6, 'prec_type': 'rain', 'prec_amount': 0, 'temp2m': 13, 'rh2m': '86%', 'wind10m': {'direction': 'SE', 'speed': 3}, 'weather': 'ishowernight'}, 
    {'timepoint': 42, 'cloudcover': 2, 'lifted_index': 6, 'prec_type': 'rain', 'prec_amount': 0, 'temp2m': 16, 'rh2m': '73%', 'wind10m': {'direction': 'SE', 'speed': 3}, 'weather': 'ishowerday'}, 
    {'timepoint': 45, 'cloudcover': 2, 'lifted_index': 2, 'prec_type': 'rain', 'prec_amount': 0, 'temp2m': 22, 'rh2m': '52%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'ishowerday'}, 
    {'timepoint': 48, 'cloudcover': 4, 'lifted_index': 2, 'prec_type': 'rain', 'prec_amount': 0, 'temp2m': 23, 'rh2m': '48%', 'wind10m': {'direction': 'E', 'speed': 2}, 'weather': 'ishowerday'}, 
    {'timepoint': 51, 'cloudcover': 3, 'lifted_index': 2, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 15, 'rh2m': '78%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'pcloudynight'}, 
    {'timepoint': 54, 'cloudcover': 2, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 13, 'rh2m': '88%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 57, 'cloudcover': 2, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 12, 'rh2m': '88%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 60, 'cloudcover': 2, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 11, 'rh2m': '95%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'humidnight'}, 
    {'timepoint': 63, 'cloudcover': 1, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 11, 'rh2m': '91%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'humidnight'}, 
    {'timepoint': 66, 'cloudcover': 1, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 15, 'rh2m': '78%', 'wind10m': {'direction': 'E', 'speed': 2}, 'weather': 'clearday'}, 
    {'timepoint': 69, 'cloudcover': 1, 'lifted_index': 2, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 21, 'rh2m': '60%', 'wind10m': {'direction': 'NW', 'speed': 2}, 'weather': 'clearday'}, 
    {'timepoint': 72, 'cloudcover': 1, 'lifted_index': 2, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 23, 'rh2m': '45%', 'wind10m': {'direction': 'W', 'speed': 2}, 'weather': 'clearday'}, 
    {'timepoint': 75, 'cloudcover': 1, 'lifted_index': 2, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 17, 'rh2m': '65%', 'wind10m': {'direction': 'S', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 78, 'cloudcover': 1, 'lifted_index': 2, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 14, 'rh2m': '70%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 81, 'cloudcover': 1, 'lifted_index': 2, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 13, 'rh2m': '84%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 84, 'cloudcover': 1, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 12, 'rh2m': '80%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 87, 'cloudcover': 1, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 11, 'rh2m': '93%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'humidnight'}, 
    {'timepoint': 90, 'cloudcover': 1, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 16, 'rh2m': '77%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearday'}, 
    {'timepoint': 93, 'cloudcover': 1, 'lifted_index': 2, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 21, 'rh2m': '60%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearday'}, 
    {'timepoint': 96, 'cloudcover': 2, 'lifted_index': 2, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 22, 'rh2m': '52%', 'wind10m': {'direction': 'SE', 'speed': 3}, 'weather': 'clearday'}, 
    {'timepoint': 99, 'cloudcover': 9, 'lifted_index': 6, 'prec_type': 'rain', 'prec_amount': 0, 'temp2m': 15, 'rh2m': '73%', 'wind10m': {'direction': 'SE', 'speed': 3}, 'weather': 'lightrainnight'}, 
    {'timepoint': 102, 'cloudcover': 5, 'lifted_index': 6, 'prec_type': 'rain', 'prec_amount': 0, 'temp2m': 13, 'rh2m': '88%', 'wind10m': {'direction': 'SE', 'speed': 3}, 'weather': 'ishowernight'}, 
    {'timepoint': 105, 'cloudcover': 1, 'lifted_index': 10, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 12, 'rh2m': '90%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 108, 'cloudcover': 1, 'lifted_index': 10, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 11, 'rh2m': '87%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 111, 'cloudcover': 3, 'lifted_index': 10, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 11, 'rh2m': '85%', 'wind10m': {'direction': 'SE', 'speed': 3}, 'weather': 'pcloudynight'}, 
    {'timepoint': 114, 'cloudcover': 6, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 16, 'rh2m': '70%', 'wind10m': {'direction': 'SE', 'speed': 3}, 'weather': 'mcloudyday'}, 
    {'timepoint': 117, 'cloudcover': 9, 'lifted_index': 6, 'prec_type': 'rain', 'prec_amount': 0, 'temp2m': 20, 'rh2m': '58%', 'wind10m': {'direction': 'E', 'speed': 3}, 'weather': 'lightrainday'}, 
    {'timepoint': 120, 'cloudcover': 9, 'lifted_index': 2, 'prec_type': 'rain', 'prec_amount': 0, 'temp2m': 21, 'rh2m': '53%', 'wind10m': {'direction': 'E', 'speed': 3}, 'weather': 'lightrainday'}, 
    {'timepoint': 123, 'cloudcover': 6, 'lifted_index': 6, 'prec_type': 'rain', 'prec_amount': 0, 'temp2m': 14, 'rh2m': '77%', 'wind10m': {'direction': 'SE', 'speed': 3}, 'weather': 'oshowernight'}, 
    {'timepoint': 126, 'cloudcover': 4, 'lifted_index': 6, 'prec_type': 'rain', 'prec_amount': 0, 'temp2m': 12, 'rh2m': '85%', 'wind10m': {'direction': 'SE', 'speed': 3}, 'weather': 'ishowernight'}, 
    {'timepoint': 129, 'cloudcover': 3, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 12, 'rh2m': '88%', 'wind10m': {'direction': 'SE', 'speed': 3}, 'weather': 'pcloudynight'}, 
    {'timepoint': 132, 'cloudcover': 3, 'lifted_index': 10, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 11, 'rh2m': '89%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'pcloudynight'}, 
    {'timepoint': 135, 'cloudcover': 4, 'lifted_index': 10, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 10, 'rh2m': '88%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'pcloudynight'}, 
    {'timepoint': 138, 'cloudcover': 3, 'lifted_index': 10, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 14, 'rh2m': '75%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'pcloudyday'}, 
    {'timepoint': 141, 'cloudcover': 1, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 21, 'rh2m': '52%', 'wind10m': {'direction': 'E', 'speed': 2}, 'weather': 'clearday'}, 
    {'timepoint': 144, 'cloudcover': 1, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 22, 'rh2m': '46%', 'wind10m': {'direction': 'N', 'speed': 2}, 'weather': 'clearday'}, 
    {'timepoint': 147, 'cloudcover': 2, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 15, 'rh2m': '73%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 150, 'cloudcover': 2, 'lifted_index': 10, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 12, 'rh2m': '85%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 153, 'cloudcover': 1, 'lifted_index': 10, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 11, 'rh2m': '86%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 156, 'cloudcover': 1, 'lifted_index': 15, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 11, 'rh2m': '89%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 159, 'cloudcover': 1, 'lifted_index': 15, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 11, 'rh2m': '88%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 162, 'cloudcover': 1, 'lifted_index': 10, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 15, 'rh2m': '71%', 'wind10m': {'direction': 'E', 'speed': 2}, 'weather': 'clearday'}, 
    {'timepoint': 165, 'cloudcover': 1, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 21, 'rh2m': '54%', 'wind10m': {'direction': 'NW', 'speed': 2}, 'weather': 'clearday'}, 
    {'timepoint': 168, 'cloudcover': 1, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 22, 'rh2m': '47%', 'wind10m': {'direction': 'NW', 'speed': 2}, 'weather': 'clearday'}, 
    {'timepoint': 171, 'cloudcover': 1, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 17, 'rh2m': '61%', 'wind10m': {'direction': 'S', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 174, 'cloudcover': 1, 'lifted_index': 10, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 14, 'rh2m': '68%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 177, 'cloudcover': 1, 'lifted_index': 10, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 13, 'rh2m': '72%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 180, 'cloudcover': 1, 'lifted_index': 10, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 13, 'rh2m': '79%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 183, 'cloudcover': 1, 'lifted_index': 10, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 12, 'rh2m': '85%', 'wind10m': {'direction': 'SE', 'speed': 2}, 'weather': 'clearnight'}, 
    {'timepoint': 186, 'cloudcover': 1, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 16, 'rh2m': '67%', 'wind10m': {'direction': 'E', 'speed': 2}, 'weather': 'clearday'}, 
    {'timepoint': 189, 'cloudcover': 1, 'lifted_index': 2, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 22, 'rh2m': '46%', 'wind10m': {'direction': 'NW', 'speed': 2}, 'weather': 'clearday'}, 
    {'timepoint': 192, 'cloudcover': 1, 'lifted_index': 6, 'prec_type': 'none', 'prec_amount': 0, 'temp2m': 24, 'rh2m': '38%', 'wind10m': {'direction': 'W', 'speed': 2}, 'weather': 'clearday'}
    ]
}
'''