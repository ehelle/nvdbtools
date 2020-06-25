import requests
import json
from nvdbtools.klasser import Veglenkesekvens, Vegobjekt

config = {# 'base_url': 'https://www.vegvesen.no/nvdb/api/v3/',
    'base_url': 'https://nvdbapiles-v3.test.atlas.vegvesen.no/',
    'X-Client': 'nvdbtools - alfa',
    'User-Agent': 'nvdbtools - alfa'
}

def hent_json(url):
    headers = {'content-type': 'application/json','Accept': 'application/json',
               'X-Client': config['X-Client'], 'User-Agent': config['User-Agent']}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    return data

def veglenkesekvens(sekvens_nr):
    return enkeltelement(Veglenkesekvens, 'vegnett/veglenkesekvenser/', sekvens_nr)

def veglenkesekvenser(params = {'inkluder': 'alle'}):
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
