import json
import sys
from pprint import pprint


def aggregate_attrs(fn):
    attrs = set()
    f = open(fn)
    for l in f:
        j = json.loads(l)
        for k, v in j.items():
            if type(v) != dict:
                attrs.add(k)
            else:
                for kk, vv in v.items():
                    attrs.add(k + '__' + kk)
    f.close()
    return sorted(list(attrs))


if __name__ == "__main__":
    a = aggregate_attrs(sys.argv[1])
    for n in a:
        print(n)
