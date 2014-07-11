'''
Created on 2014-7-3

@author: work
'''
import os;
import re;
import utils

pack_pat = re.compile(r"(com.baidu.rigel.ipangu\.)"
                      r"(?P<subProj>[a-z]+)"
                     r"(\.)"
                      r"(?P<mod>[a-z]+)"
                     r"(\.)"
                      )

class_pat = re.compile(r"(.*class\s+)"
                       r"(?P<clz_name>\S+)"
                       r"(\s+implements\s+)"
                       r"(?P<if_names>.+)"
                       r"({)"
                       );

def get_key_lines(java_file):
    f = open(java_file);
    inCmt = False;
    java_contents = [];
    
    while True:
        line = f.readline();

        #print line;
        
        if not line :  break;
        
        if inCmt and line.find("*/"):
            inCmt = False;
            continue;
        
        if inCmt: continue;
        
        if line.find("//")>=0:
            line = line[0:line.find("//")]
            
        if(line.strip().startswith("/*")):
            inCmt = True;
            continue;

        java_contents.append( line )
        
        tmp_line = line
        if line.strip().startswith("public ") :
            while line:
                if line.find('{')>0: break
                line = f.readline()
                tmp_line = tmp_line.strip()+' '+line
                
            java_contents.pop()
            java_contents.append( tmp_line )
            break
        
    return java_contents;
            
    
def connect(java_lines, this_mod, interfaces, dep_map):
    print "start connnect"
    idx = 0;
    while idx < len(java_lines):
        line = java_lines[idx]
        print '..parse..'+line
        idx = idx + 1
        
        if(not line.startswith("import")):
            print 'not a import'
            continue;
        
        tmp = pack_pat.search(line)
        if(not tmp):
            print 'not a valid mod'
            continue;
        
        up_mod = (tmp.group("subProj"), tmp.group("mod"));
        print 'up_mod='+str(up_mod)+",this ="+str(this_mod)
        
        if up_mod == this_mod :
            print 'up == this' 
            continue;
        
        print 'now is ready to add dep:'+line
        for inf in interfaces:
            if line.find(inf.strip()) > 0 :
                utils.add_if_not_exists(up_mod, this_mod, dep_map)
                up_mod = None
                break;
                
        if up_mod:
            utils.add_if_not_exists(this_mod, up_mod, dep_map)
    print '---end connect'
            
def parse_file( java_file, dep_map ):
    if(not java_file.endswith(".java")):
        return;

    print "start "+java_file
    
    java_lines = get_key_lines( java_file )
    
    #get interfaces
    interfaces=[];
    line = java_lines.pop();
    clz_inf = class_pat.search(line)
    if clz_inf:
        clz = clz_inf.group('clz_name');
        infs = clz_inf.group('if_names');
        interfaces = infs.split(",")
        print clz+' '+infs
    
    #extract package define
    this_mod = None
    idx = 0;
    
    while idx<len(java_lines):
        line = java_lines[idx]
        print 'find package:'+line
        idx = idx+1
        if(line.startswith("package")):
            tmp = pack_pat.search(line)
            if(not tmp):
                print 'not a good mod'  
                return;
            this_mod=(tmp.group("subProj"),tmp.group("mod"));
            #print "down mod="+str(downMod)
            if not this_mod in dep_map:
                dep_map[this_mod]=[]
            break;
        
    print '----> this_mod='+str(this_mod)
    
    if(not this_mod):
        print "no mod name in "+java_file
        return;
        
    connect(java_lines, this_mod, interfaces, dep_map)
    
    return

def parseDir( javaDir, dep_map ):    
    for root,_,files in os.walk(javaDir):
        for name in files:
            if name.endswith("test"):continue;
            try:
                file_name = os.path.join(root, name)
                parse_file(file_name,dep_map);
            except:
                raise
                print "error:"+name