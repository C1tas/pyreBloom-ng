import sys
from pprint import pprint
from os.path import basename, abspath, dirname

sys.setrecursionlimit(2000)
print(dirname(dirname(abspath(__file__))) + '/src/')
new_source = dirname(dirname(abspath(__file__))) + '/src'
sys.path.insert(0, new_source)

pprint(sys.path)


try:
    from pyreBloom.utils._raw_api import load_raw_lib
    tmpa = load_raw_lib("pyreBloom.PyreBloom")
    # print(tmpa)
except Exception as e:
    print(e)
    print("find exception")
    pass
