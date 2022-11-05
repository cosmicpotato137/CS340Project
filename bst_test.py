import sbbst as bst


class asdf:
    def __init__(self, a):
        self.a = a


def getVal(val: asdf):
    return val.a


q = bst.sbbst([asdf(1), asdf(2), asdf(1.5)], getVal=getVal)

print(q)
