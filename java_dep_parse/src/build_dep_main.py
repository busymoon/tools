import parse_dep
                
if __name__ == '__main__':
    #path="E:/jdk"
    path="E:/works/space1/ipangu"
    dep_map= {}
    parse_dep.parseDir(path,dep_map)
    
    print "output:\n"
    
    o = open("e:/dep_java3.txt",'w');
    for k in dep_map.keys():
        for v in dep_map[k]:
            o.write(str(k)+" --> "+ str(v)+"\n")
    o.close();
