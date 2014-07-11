'''
Created on 2014-7-3

@author: work
'''


def add_if_not_exists(key0,value0,dep_map):
    print 'add dep:'+str(key0)+"->"+str(value0)
    if not key0 in dep_map:
        dep_map[key0] = []
    if(dep_map[key0].count(value0) == 0):
        dep_map[key0].append(value0)