import datetime
# import les

class LinRef:
    def __init__(self, lr_id, lr_fra, lr_til):
        self.lr_id = lr_id
        self.lr_fra = float(lr_fra)
        self.lr_til = float(lr_til)

class Veglenkesekvens:
    def __init__(self, data):
        self.data = data
        self.veglenkesekvensid = self.data['veglenkesekvensid']

    def veglenker(self):
        for lenkedata in self.data['veglenker']:
            yield Veglenke(lenkedata, self.veglenkesekvensid)

class Veglenke:
    def __init__(self, data, veglenkesekvensid):
        self.data = data
        self.linref = LinRef(veglenkesekvensid, self.data['startposisjon'], self.data['sluttposisjon'])

    def har_gyldig_dato(self, dato = datetime.date.today()):
        if isinstance(dato, str):
            dato = datetime.date.fromisoformat(dato)
        if 'sluttdato' in self.data and self.data['sluttdato'] < dato:
            return False
        else:
            return True

    def kommunenummer(self):
        return self.data['geometri']['kommune']

class Vegobjekt:
    def __init__(self, data):
        self.data = data
        # Gjelder kun for linjeobjekt - hva med punkt?
        self.linrefer = [LinRef(x.veglenkesekvensid, x.startposisjon, x.sluttposisjon) \
                        for x in self.data['lokasjon']['stedfestinger']]

    def har_gyldig_dato(self, dato = datetime.date.today()):
        if isinstance(dato, str):
            dato = datetime.date.fromisoformat(dato)
        if 'sluttdato' in self.data['metadata'] \
           and self.data['metadata']['sluttdato'] < dato:
            return False
        else:
            return True

    def unike_lr_ider():
        return set([x.lr_id for x in self.linrefer])

    def kommuner(self):
        return self.data['lokasjon']['kommuner']
