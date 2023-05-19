import requests
import http.client
from dotenv import load_dotenv
import os
import json
import warnings
from itertools import chain
from typing import Any, Generator


warnings.simplefilter(action='ignore')

load_dotenv()
conn = http.client.HTTPSConnection("api.vtex.com")
TOKEN = os.getenv('TOKEN')
SECRET_KEY = os.getenv('key')
idloja = os.getenv('IDLOJA')

headers = {
            'Accept': "application/json",
            'Content-Type': "application/json",
            'X-VTEX-API-AppKey': f"{SECRET_KEY}",
            'X-VTEX-API-AppToken': f"{TOKEN}"
            }



def calcula_preco(*args, **kwargs):
    for arg in args:
        
        calc =  (arg.get('CANALVENDA',0)/100) + arg.get('BASE PRICE',0) + arg.get('CUSTOENVIO',0) + arg.get('CNT',0)
        print(calc)
        
     
    conn.request("get", f"/t78536/pricing/prices/{arg.get('SKU ID',None)}/", headers=headers)

    res = conn.getresponse()
    data = res.read()

    products = json.loads(data.decode("utf-8"))
    prices = next(chain(products.get('fixedPrices',None)))
    dict_product_prices = {
        "itemId":products.get('itemId',None),
        "listPrice":float(products.get('listPrice',None)),
        "costPrice":float(products.get('costPrice',None)),
        "markup":products.get('markup',None),
        "basePrice":float(products.get('basePrice',None)),
        "tradePolicyId":prices.get('tradePolicyId',None),
        "value":prices.get('value',None),
        "listPrice":prices.get('listPrice',None),
        "minQuantity":prices.get('minQuantity',None)
        
        }
  
    dict_product_prices['new_price'] = round(float(calc),2)
    
    yield dict_product_prices
   
   

def get_vtex_skus(*args: Any, **kwargs: dict[str, Any]) -> None:
    
    def get_skus() -> Generator[Any, Any, None]:
        url = f"https://t78536.myvtex.com/api/catalog/pvt/product/{kwargs['id']}"

        payload: dict = {}
     
        response = requests.request("GET", url, headers=headers, data=payload)
        
        yield response.json()
        
    def get_inventory_logistics(*args: Any, **kwargs: dict[str, Any]) -> Generator[dict[str, Any], Any, None]:
        cont = len(args)
        i = 0
        while i < cont:
            if isinstance(args[i]['Id'], int):
               
                url = f"https://t78536.myvtex.com/api/logistics/pvt/inventory/skus/{args[i]['Id']}"
                payload: dict = {}
                response = requests.request("GET", url, headers=headers, data=payload)
                inventory = response.json()
             
                try:
                    saldos = [{"warehouseId":saldo.get("warehouseId"),"warehouseName":saldo.get("warehouseName")
                               ,"totalQuantity":saldo.get("totalQuantity"),
                               "hasUnlimitedQuantity":saldo.get("hasUnlimitedQuantity"),"reservedQuantity":saldo.get("reservedQuantity")}
                             for saldo in chain(inventory.get('balance')) if saldo['warehouseName'] == 'estoque - STA MARIA']
                except Exception as e:
                    print(e)

            if len(saldos) >= 1:
                logistics: dict[str, Any] = {
                    "referencia":args[i]['Id'],
                    "LinkId":args[i]['LinkId'],
                    "Name":args[i]['Name'],
                    "BrandId":args[i]['BrandId'],
                    "RefId":args[i]['RefId'],
                    "ListaSaldos":saldos
                }
                yield logistics
            
            i += 1
            
    skus = get_skus()
    produtos = [{"Id":produto["Id"],"LinkId":produto["LinkId"],"Name":produto["Name"]
                    ,"BrandId":produto["BrandId"],"RefId":produto["RefId"]}  for produto in skus]

    produtos_saldos = get_inventory_logistics(*produtos)
    items = next(produtos_saldos)
    print(items)

listas = [{'SKU ID':776,'BASE PRICE':21.00,'CANALVENDA':14,'CUSTOENVIO':0.01,'CNT':2.00},
         {'SKU ID':125,'BASE PRICE':1.99,'CANALVENDA':14,'CUSTOENVIO':0.20,'CNT':2.00},
         {'SKU ID':775,'BASE PRICE':22.00,'CANALVENDA':14,'CUSTOENVIO':1.00,'CNT':2.00}]
for lista in listas:
    if isinstance(lista['SKU ID'], int):  
        jsons = get_vtex_skus(id = lista['SKU ID'])


def update_prices_vtex(new_price, idproduct,policyid):

    def get_product_prices(idproduct):
       
        conn.request("get", f"/t78536/pricing/prices/{idproduct}", headers=headers)

        res = conn.getresponse()
        data = res.read()

        dict_prices = json.loads(data.decode("utf-8"))
        
        prices = {
            "itemId":dict_prices['itemId'],
            "listPrice":dict_prices['listPrice'],
            "costPrice":dict_prices['costPrice'],
            "markup":dict_prices['markup'],
            "basePrice":dict_prices['basePrice'],
            "policyid":policyid,
            "new_price":new_price
            }
        print(prices)
        yield prices
        
    def update_prices(product_prices):
        prices = next(product_prices)

        payload= json.dumps({"markup": 0,"basePrice": prices['basePrice'],"listPrice": prices['listPrice'],
            "fixedPrices": [
                {
                "tradePolicyId": f"{prices['policyid']}",
                "value": prices['new_price'],
                "listPrice": prices['new_price'],
                "minQuantity": 1,
                "dateRange": {
                    "from": "2022-05-21T22:00:00Z",
                    "to": "2023-05-28T22:00:00Z"
                        }
                    }
                ]
            })
        
        conn.request("put", f"/t78536/pricing/prices/{prices['itemId']}", payload, headers)

        res = conn.getresponse()
        data = res.read()
        

    product_prices = get_product_prices(idproduct)
    update_prices(product_prices)
   
#teste com simulação de parametros para atualização
listas = [{'SKU ID':776,'BASE PRICE':21.00,'CANALVENDA':14,'CUSTOENVIO':0.01,'CNT':2.00},
         {'SKU ID':125,'BASE PRICE':1.99,'CANALVENDA':14,'CUSTOENVIO':0.20,'CNT':2.00},
         {'SKU ID':775,'BASE PRICE':22.00,'CANALVENDA':14,'CUSTOENVIO':1.00,'CNT':2.00}]

for lista in listas:
    prices = calcula_preco(lista)
    
    new_prices = next(prices)
  
    if isinstance(new_prices, dict):
        update_prices_vtex(new_prices['new_price'],new_prices['itemId'],1)
