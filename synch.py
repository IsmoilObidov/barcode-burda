import configparser
import requests
import json

class Synch:

    def __init__(self, application, parent=None):

        self.app = application

        self.app.ui.synch_button.clicked.connect(self.updateDataBaseProduct)
        

    def getDataBaseProduct(self):

        config = configparser.ConfigParser()

        config.read('config/main.ini')

        url = "http://{0}/test1".format(config['main']['domain'])

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        return json.loads(response.json())


    def updateDataBaseProduct(self):

        cur_waherhouse = self.app.con.cursor()

        cur_waherhouse.execute("DELETE FROM barcodes;")

        self.app.con.commit()

        decoded_hand = self.getDataBaseProduct()

        i = 0

        for a in decoded_hand:

            i += 1 

            self.app.ui.status.setValue(i)

            cur_waherhouse.execute("INSERT INTO barcodes( `id_u`, `name`, `model`, `brand`, `size`, `bar_code`, `price`) VALUES ('" + str(a['id_u']) + "', '" + str(
                a['product']) + "', '" + str(a['model']) + "', '" + str(a['brand']) + "', '" + str(a['size']) + "', '" + str(a['bar_code']) + "', '" + str(a['price']) + "');")

            self.app.con.commit()

        self.app.view_message('ok 200', '200')