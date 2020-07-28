import datetime
import copy
import nvdbtools.linref
import shapely.wkt

class LinRef:
    def __init__(self, lr_id, lr_fra, lr_til):
        self._id = lr_id
        self.fra = float(lr_fra)
        self.til = float(lr_til)

class Veglenkesekvens:
    def __init__(self, data):
        self.data = data
        self._id = self.data['veglenkesekvensid']
        self.veglenker = {v._id: v for v in self.veglenke_generator()}
        self.noder = sorted(list({x[y] for x in self.veglenker for y in range(2)}))

    def insert_split(ref):
        idx = next(i for i,x in enumerate(self.noder) if x > ref)
        vid = (self.noder[idx-1], self.noder[idx])
        left, right = self.split_veglenke(vid, ref)
        self.veglenker[(vid[0], ref)] = left
        self.veglenker[(ref, vid[1])] = right
        self.noder.insert(idx, ref)

    def split_veglenke(vid, ref):
        orig = self.veglenker.pop(vid)
        split_ref = linref.normaliser(vid[0], vid[1], float(ref))
        left_geom, right_geom = split_geom(orig.geom, split_ref)
        left = copy.deepcopy(orig.data)
        left['sluttposisjon'] = ref
        left['sluttport'] = 'x'
        left['geometri']['wkt'] = left_geom.wkt
        left['geometri']['lengde'] = float(orig['geometri']['lengde']) * split_ref
        right = copy.deepcopy(orig.data)
        right['startposisjon'] = ref
        right['startport'] = 'x'
        right['geometri']['wkt'] = right_geom.wkt
        right['geometri']['lengde'] = float(orig['geometri']['lengde']) * split_ref
        return Veglenke(left), Veglenke(right)

    def veglenke_generator(self):
        for lenkedata in self.data['veglenker']:
            yield Veglenke(lenkedata, self._id)

class Veglenke:
    def __init__(self, data, veglenkesekvensid):
        self.data = data
        self.linref = LinRef(veglenkesekvensid, self.data['startposisjon'], self.data['sluttposisjon'])
        self._id = (self.linref.fra, self.linref.til)
        self.geom = shapely.wkt.loads(self.data['geometri']['wkt'])

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
        self._id = self.data['id']
        # Gjelder kun for linjeobjekt - hva med punkt?
        self.linrefer = [LinRef(x['veglenkesekvensid'], x['startposisjon'], x['sluttposisjon']) \
                        for x in self.data['lokasjon']['stedfestinger']]

    def har_gyldig_dato(self, dato = datetime.date.today()):
        if isinstance(dato, str):
            dato = datetime.date.fromisoformat(dato)
        if 'sluttdato' in self.data['metadata'] \
           and self.data['metadata']['sluttdato'] < dato:
            return False
        else:
            return True

    def unike_lr_ider(self):
        return set([x._id for x in self.linrefer])

    def kommuner(self):
        return self.data['lokasjon']['kommuner']
