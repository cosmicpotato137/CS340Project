import sbbst as bst


class asdf:
    def __init__(self, a):
        self.a = a


def getVal(val: asdf):
    return val.a


def cmp_asdf(x: asdf, y: asdf):
    return x.a > y.a


lst = [asdf(1), asdf(2), asdf(1.5)]
q: bst.sbbst = bst.sbbst(lst, fun=cmp_asdf)
q.delete(lst[0])
lst[0].a = 3
q.insert(lst[0])
print(q.getMaxVal().a)
