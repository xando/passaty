# import pandas as pd
import csv
import requests

from bs4 import BeautifulSoup


def get_last_page():
    response = requests.get("https://www.otomoto.pl/osobowe/volkswagen/passat/")
    soup = BeautifulSoup(response.text, 'html.parser')
    return int(soup.select('span.page')[-2].text) + 1


def get_page(i):
    response = requests.get("https://www.otomoto.pl/osobowe/volkswagen/passat/?page=%s" % i)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup.select('.offer-title .offer-title__link')
    return map(lambda x:x.attrs['href'],soup.select('.offer-title .offer-title__link'))


def get_details(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')

    przebieg = None
    rok_produkcji = None
    moc = None
    pojemnosc_skokowa = None
    color = None

    for el in soup.select('.offer-params__list .offer-params__item'):
        label = el.select_one('.offer-params__label').text.strip()
        value = el.select_one('.offer-params__value').text.strip()
        if label == "Rok produkcji":
            rok_produkcji = value
        if label == "Przebieg":
            przebieg = value
        if label == "Pojemność skokowa":
            pojemnosc_skokowa = value
        if label == "Moc":
            moc = value
        if label == "Kolor":
            color = value

    return (rok_produkcji, przebieg, pojemnosc_skokowa, moc, color)


with open('passaty.csv', 'w') as csvfile:
    fieldnames = ['year', 'distance', 'engine', 'power', 'color']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    ostania_strona = get_last_page()
    for x in range(1, ostania_strona):

        for link in get_page(x):
            print (x, link)
            results = get_details(link)
            if all(results):
                writer.writerow({
                    'year': int(results[0]),
                    'distance': int(results[1].rstrip(" km").replace(" ", "")),
                    'engine': int(results[2].rstrip(" cm3").replace(" ", "")),
                    'power': int(results[3].rstrip(" KM").replace(" ", "")),
                    'color': results[4]
                })
