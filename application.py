import os
import requests

from flask import Flask, render_template, request
from datetime import date, datetime

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/umbrella", methods=["GET"])
def umbrella():
    #API CALL by city ID api.openweathermap.org/data/2.5/forecast?id={city ID}
    res = requests.get("http://api.openweathermap.org/data/2.5/forecast", params={"id":3451328, "appid":"a605057c30faf8f21b4767561ae0f61c"})
    dados=res.json()
    #data inicialization
    i = 0
    media = 0
    valor = 0
    humidade = []
    semana = []
    valoresdias=[]
    #Captura o valor do primeiro dia
    diatempo = datetime.fromtimestamp(dados["list"][0]["dt"])
    dia = diatempo.weekday()
    semana.append(dia)
    #captura os dias da semana e os valores de humdiade de cada dia
    for dado in dados["list"]:
        data = datetime.fromtimestamp(dado["dt"])
        newdia = data.weekday()
        #valida se houve troca de dia
        if dia != newdia:
            valor = valor/media
            i += 1
            media = 1
            humidade.append(valor)
            semana.append(newdia)
            valor = dado["main"]["humidity"]   
            dia = newdia
        #enquanto no mesmo dia soma as humidades para fazer uma media do dia
        else:
            valor += dado["main"]["humidity"]
            media += 1
    valor = valor/media
    humidade.append(valor)

    #dias da semana
    DiasSemanda = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

    #Verifica os dias que possuem mais de 70% de humidade
    var = 0
    chuva = []
    for hum in humidade:
        if hum > 70:
            dia = semana[var]
            chuva.append(DiasSemanda[dia])
            var += 1
        else:
            var += 1

    return render_template("wheather.html",semana=semana, humidade=humidade, chuva=chuva)

