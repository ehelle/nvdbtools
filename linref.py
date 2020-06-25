
def overlaps(a, b):
    return (a.lr_id == b.lr_id) and \
        ((b.lr_fra <= a.lr_fra and b.lr_fra >= a.lr_til) or \
         (b.lr_til <= a.lr_fra and b.lr_fra >= a.lr_til))

def equals(a, b):
    return (a.lr_id == b.lr_id) and \
        (a.lr_fra == b.lr_fra and \
        (a.lr_til == b.lr_til)
