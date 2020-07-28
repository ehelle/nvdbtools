import requests
import json
from nvdbtools.klasser import Veglenkesekvens, Vegobjekt
from ratelimit import limits
import ratelimit
import backoff
import time

config = {# 'base_url': 'https://www.vegvesen.no/nvdb/api/v3/',
    'base_url': 'https://nvdbapiles-v3.test.atlas.vegvesen.no/',
    'X-Client': 'nvdbtools - alfa',
    'User-Agent': 'nvdbtools - alfa'
}

@backoff.on_exception(backoff.expo, ratelimit.exception.RateLimitException, max_time=60)
@limits(10, 1) # max 10 calls per 1 sec
def hent_json(url):
    headers = {'content-type': 'application/json','Accept': 'application/json',
               'X-Client': config['X-Client'], 'User-Agent': config['User-Agent']}
    for i in range(5):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return json.loads(response.text)
        print(url)
        time.sleep(10 + i*30)
    raise ConnectionError(response.status_code)

def veglenkesekvens(sekvens_nr):
    return enkeltelement(Veglenkesekvens, 'vegnett/veglenkesekvenser/', sekvens_nr)

def veglenkesekvenser(params = {}):
    return samling(Veglenkesekvens, 'vegnett/veglenkesekvenser?', params)

def vegobjekt(kat_id, obj_id):
    return enkeltelement(Vegobjekt, 'vegobjekter/{}/'.format(kat_id), obj_id)

def vegobjekter(kat_id, params = {'inkluder': 'alle'}):
    return samling(Vegobjekt, 'vegobjekter/{}?'.format(kat_id), params)

def enkeltelement(klasse, url_del, id):
    data = hent_json(config['base_url'] + url_del + str(id))
    if data:
        return klasse(data)

def samling(klasse, url_del, params):
    param_string = '&'.join(['{}={}'.format(k,params[k]) for k in params])
    data = hent_json(config['base_url'] + url_del + param_string)
    if data:
        for obj in paginator(data):
            yield klasse(obj)

def paginator(data):
    objekter = data['objekter']
    if objekter:
        yield from objekter
        neste_url = data['metadata']['neste']['href']
        neste_side = hent_json(neste_url)
        yield from paginator(neste_side)
