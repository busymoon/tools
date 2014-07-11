import re;
import sys;

lineReg = re.compile(r"(.+')"
                     r"(?P<sp0>[a-z]+)"
                     r"('.+')"
                     r"(?P<sm0>[a-z]+)"
                     r"('.+')"
                     r"(?P<sp1>[a-z]+)"
                     r"('.+')"
                     r"(?P<sm1>[a-z]+)"
                     r"('.+)"
                    )

def match(keySP,keySM,subProj,subMod):
    if(keySP!=subProj):
        return False;
    if((subMod is not None) and keySM!=subMod):
        return False;
    return True;

#find the direct dependent proj or module
def findDep(subProj,subMod,level, depList):
    tmpList = [];
    for (sp,sm,sp0,sm0) in depList:
        if(match(sp,sm,subProj,subMod)):
            if(level==1):
                sm0 = None
            if(tmpList.count((sp0,sm0))==0):
                tmpList.append((sp0,sm0));
        
    return tmpList;

#find the direct or indirect dependent proj or module
def findAllDep(subProj,subMod,level, depList):
    tmp0 = (subProj,subMod,0)
    tmpList = [];
    nodeQueue=[]
    nodeQueue.append(tmp0)

    while len(nodeQueue)>0:
        tmp0 = nodeQueue[0]
        nodeQueue = nodeQueue[1:]
        for (sp,sm,sp0,sm0) in depList:
            if(match(sp,sm,tmp0[0],tmp0[1])):
                if(level==1):
                    sm0 = None
                if len(filter((lambda x:(x[0],x[1])==(sp0,sm0)),tmpList))==0:
                    tmpList.append((sp0,sm0,tmp0[2]+1,tmp0[0],tmp0[1]));
                    nodeQueue.append((sp0,sm0,tmp0[2]+1))
                    
    return tmpList;

#find the direct supported proj or module
def findSupport(subProj,subMod,level, depList):
    tmpList = [];
    for (sp0,sm0,sp,sm) in depList:
        if(match(sp,sm,subProj,subMod)):
            if(level==1):
                sm0 = None
            if(tmpList.count((sp0,sm0))==0):
                tmpList.append((sp0,sm0));
                
    return tmpList;

#find the indirect supported proj or module
def findAllSupport(subProj,subMod,level, depList):
    tmp0 = (subProj,subMod,0)
    tmpList = [];
    nodeQueue=[]
    nodeQueue.append(tmp0)

    while len(nodeQueue)>0:
        tmp0 = nodeQueue[0]
        nodeQueue = nodeQueue[1:]
        for (sp0,sm0,sp,sm) in depList:
            if(match(sp,sm,tmp0[0],tmp0[1])):
                if(level==1):
                    sm0 = None
                if len(filter((lambda x:(x[0],x[1])==(sp0,sm0)),tmpList))==0:
                    tmpList.append((sp0,sm0,tmp0[2]+1,tmp0[0],tmp0[1]));
                    nodeQueue.append((sp0,sm0,tmp0[2]+1))
                    
    return tmpList;

#read the file contents into a tuple
def parseLine(line):
    groupMap = lineReg.search(line);
    if groupMap:
        return (groupMap.group("sp0"),groupMap.group("sm0"),groupMap.group("sp1"),groupMap.group("sm1"))
    print "error:"+line
    return None;

#load the file into memory
def init(filePath):
    f = open(filePath,"r");
    depList=[];
    while True:
        line = f.readline();
        if not line:
            break;
        tmp = parseLine(line)
        if tmp:
            depList.append(tmp)
    f.close();
    return depList;

if __name__ == '__main__':
    if(len(sys.argv)<4):
        print "python findDep.py fileName subProj subMod level relationType\n"
        print "fileName the file containing the relationship\n"
        print "subProj\n"
        print "subMod,- means All mod\n"
        print "level,1 sub proj,2 sub mod\n"
        print "relationType: S=support,D=depends\n"
        sys.exit(0)
    
    depList = init(sys.argv[1])

    subMod=None
    if sys.argv[3]!='-':
        subMod = sys.argv[3]

    if(sys.argv[5]=='D'):
        tmpList = findDep(sys.argv[2],subMod,int(sys.argv[4]),depList)
    elif(sys.argv[5]=='DA'):
        tmpList = findAllDep(sys.argv[2],subMod,int(sys.argv[4]),depList)
    elif(sys.argv[5]=='S'):
        tmpList = findSupport(sys.argv[2],subMod,int(sys.argv[4]),depList)
    elif(sys.argv[5]=='SA'):
        tmpList = findAllSupport(sys.argv[2],subMod,int(sys.argv[4]),depList)
    else:
        print "unknown type:"+sys.argv[5]
        sys.exit(0)

    tmpList.sort()
    line = 0;
    for e in tmpList:
        line = line+1
        print str(line)+" : "+str(e);


            
