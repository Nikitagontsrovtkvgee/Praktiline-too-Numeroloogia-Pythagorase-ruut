import email
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Iga numbri omadused
omadused = {
 '1': 'Tahtejõud ja enesekindlus.',
 '2': 'Energia ja tundlikkus.',
 '3': 'Loovus ja eneseväljendusoskus.',
 '4': 'Loogika ja püsivus.',
 '5': 'Intuitsioon ja kohanemisvõime.',
 '6': 'Vastutus ja hoolivus.',
 '7': 'Õnn ja sisemine talent.',
 '8': 'Organisatsioon ja tugevus.',
 '9': 'Intelligentsus ja mälu.',
}

# Kõikide tegevusnumbrite arvutamine
def arvuta_tooarvud(sunnikuupaev):
    paev, kuu, aasta = map(int, sunnikuupaev.split('.'))
    esimene_rida = list(str(paev) + str(kuu) + str(aasta))

    tooarv1 = sum(map(int, list(str(paev) + str(kuu))))
    tooarv2 = sum(map(int, str(aasta)))
    tooarv3 = tooarv1 + tooarv2
    tooarv4 = sum(map(int, str(tooarv3)))
    tooarv5 = tooarv3 - 2 * int(str(paev)[0])
    tooarv6 = sum(map(int, str(abs(tooarv5))))

    teine_rida = list(str(tooarv3) + str(tooarv4) + str(tooarv5) + str(tooarv6))
    koik_numbrid = esimene_rida + teine_rida
    return ''.join(koik_numbrid)



# Loendame, mitu korda iga number esineb
def loenda_numbrid(numbrijada):
    loendur = {str(i): 0 for i in range(1, 10)}
    for number in numbrijada:
        if number in loendur:
            loendur[number] += 1
    return loendur


# Ruudu (3x3) joonistamine sageduste järgi
def loo_ruut(loendur):
    ruut = [
        [loendur['1'] * '1', loendur['4'] * '4', loendur['7'] * '7'],
        [loendur['2'] * '2', loendur['5'] * '5', loendur['8'] * '8'],        
        [loendur['3'] * '3', loendur['6'] * '6', loendur['9'] * '9'],        
    ]
    return ruut



# Tulemuse saatmine e-posti teel
def saada_email(saaja, nimi, kuupaev, ruut, iseloom):
    saatja = 'nikitosgoldboss@gmail.com'
    salasyna = 'sinu_parool'


    sisu = f"Tere, {nimi}!\n\nSünnikuupäev: {kuupaev}\n\nPythagorase ruut:\n"
    for rida in ruut:
        sisu += ' | '.join(rida) + '\n'

    sisu += "\nIseloomustus:\n"
    for nr, kirjeldus in iseloom.items():
        sisu += f"{nr}: {kirjeldus}\n"

    email = MIMEMultipart()
    email['From'] = saatja
    email['To'] = saatja
    email['Subject'] = 'Sinu Pythagorase ruut'
    email.attach(MIMEText(sisu, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(saatja, salasyna)
            server.send_message(email)
        return True
    except Exception as e:
    print("Saatmise viga:", e)
    return False
