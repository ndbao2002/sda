
import pandas as pd
import requests
import time

url = "https://www.immobiliare.it/api-next/city-guide/price-chart/1/"

paths = [
    "/mercato-immobiliare/veneto/venezia/san-marco-rialto/",
    "/mercato-immobiliare/veneto/venezia/san-polo-santa-croce/",
    "/mercato-immobiliare/veneto/venezia/accademia-salute-dorsoduro-san-barnaba-santa-marta/",
    "/mercato-immobiliare/veneto/venezia/santi-giovanni-paolo-san-francesco/",
    "/mercato-immobiliare/veneto/venezia/guglie-san-leonardo-santi-apostoli/",
    "/mercato-immobiliare/veneto/venezia/giudecca/"
    "/mercato-immobiliare/veneto/venezia/lido-di-venezia-malamocco-alberoni/"
    "/mercato-immobiliare/veneto/venezia/cipressina-zelarino-asseggiano/"
    "/mercato-immobiliare/veneto/venezia/mestre-chirignago-marghera-catene/"
    "/mercato-immobiliare/veneto/venezia/carpenedo-favaro-campalto-aeroporto/"
    ,
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/118.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.immobiliare.it/",
    "Accept-Language": "en-US,en;q=0.9"
}

records = []

for path in paths:
    res = requests.get(url, headers=headers, params={"__lang": "en", "path": path})
    data = res.json()
    temp = pd.DataFrame(data, columns=['labels', 'values'])
    temp['timestamp'] = pd.to_datetime(temp['labels'])
    temp['neighborhood'] = path.split('/')[-2]
    records.append(temp)
    time.sleep(2)

df_all = pd.concat(records)
df_all.to_csv("./airbnb_data/immobiliare_venice_price_sell_trends.csv", index=False)