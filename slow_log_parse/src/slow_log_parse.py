import sys
import codecs
import slow_log_parse_line

file_name='slow2.log'
f = codecs.open(file_name,'r',encoding='utf-8')
fo = codecs.open('slow_p.txt','w',encoding='utf-8')
ferror = codecs.open("error.log", 'w',encoding='utf-8')

def process(line_stack, fo, ferror, counts):
    if slow_log_parse_line.output(line_stack, fo, ferror):
        counts['ok'] = counts['ok']+1
    else:
        counts['bad'] = counts['bad']+1

line_stack=[];
counts={'ok':0,'bad':0}
for line in f.readlines():
    if line.find('Time:')>0:
        if len(line_stack)>=4:
            process(line_stack, fo, ferror, counts)
            print str(counts)
        line_stack=[]
    
    if line.find('User@Host')>0:
        if len(line_stack)>=4:
            process(line_stack, fo, ferror, counts)
            print str(counts)
            line_stack = line_stack[0:1]
            
    line_stack.append(line);
        
fo.close()
ferror.close()

