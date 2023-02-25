import configparser
import requests
import json
import sqlite3


def getDataBaseProduct():

    config = configparser.ConfigParser()

    config.read('./config/main.ini')

    url = "http://{0}/test1".format(config['main']['domain'])

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.json())


def updateDataBaseProduct():

    decoded_hand = getDataBaseProduct()

    conn = sqlite3.connect('burda.db', check_same_thread=False)

    cur_waherhouse = conn.cursor()

    cur_waherhouse.execute(" DELETE FROM barcodes;")

    conn.commit()

    for a in decoded_hand:

        cur_waherhouse.execute("INSERT INTO barcodes( `id_u`, `name`, `model`, `brand`, `size`, `bar_code`, `price`) VALUES ('" + str(a['id_u']) + "', '" + str(a['product']) + "', '" + str(a['model']) + "', '" + str(a['brand']) + "', '" + str(a['size']) + "', '" + str(a['bar_code']) + "', '" + str(a['price']) + "');")

        conn.commit()

updateDataBaseProduct()
