
def overlaps(a, b):
    return (a._id == b._id) and \
        ((b.fra > a.fra and b.fra < a.til) or \
         (b.til > a.fra and b.til < a.til))

def equals(a, b):
    return (a._id == b._id) and \
        (a.fra == b.fra) and \
        (a.til == b.til)

def normaliser(a,b,x):
    # a---x-------b => 0.3
    diff_a_b = b - a
    diff_a_x = x - a
    return diff_a_x / diff_a_b

def refs_fra_b_i_a(a, b):
    if a._id != b._id:
        return []
    res=[]
    if b.fra > a.fra and b.fra < a.til:
        res.append(b.fra)
    if b.til > a.fra and b.til < a.til:
        res.append(b.til)
    return res
