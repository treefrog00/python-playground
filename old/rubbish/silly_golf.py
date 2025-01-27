##########################
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("term")

args = parser.parse_args()
term = args.term


#######################


import datetime;import base36

z = [[2020, 2030],[1,13],[1,32],[25],[60],[60]]

def f(l, *a):
    for x in range(*z[l]):
        if l + 1 == len(z):
            try:
                x = base36.dumps(int(datetime.datetime(*a, x).timestamp()))
                if term in x: print(2024,*a, x)
            except:
                pass
            return
        f(l+1, *a, x)

f(0)



