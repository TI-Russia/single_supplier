import requests
import json

DOMAIN = "http://openapi.clearspending.ru"
PATH   = "/restapi/v3/contracts/search/"

def req(reason, n, params=None):
    
    default_params = {
    "singlesupplierreason":reason,
    "page":n,
    "sort":"signDate",
    "fz":"44"
    }

    if params == None:
        params = default_params
    else:
        params.update(default_params)

    try:
        response = requests.get(DOMAIN+PATH, params)
        response_json = response.json()
        return response
    except:
        print(response)