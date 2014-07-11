import re
import sys

pat_time = re.compile(r"(Time:\s*)"
                 r"(?P<date>(\d)+)"
                 r"(\s+)"
                 r"(?P<time>(\d|:)+)"
                 );

pat_user = re.compile(r"(User@Host:\s*)"
                 r"(?P<user>(\S)+\])"
                 r"(.*\[)"
                 r"(?P<host>(\S)+)"
                 r"(])"
                );

pat_count = re.compile(r"(Query_time:\s*)"
                 r"(?P<cost>(\d+\.\d+))"
                 r"(\s*Lock_time:\s*)"
                 r"(?P<lock>(\d+\.\d+))"
                 r"(\s*Rows_sent:\s*)"
                 r"(?P<rows_sent>(\d+))"
                 r"(\s*Rows_exam.*:\s*)"
                 r"(?P<rows_exam>(\d+))"
                 r"((\s*.*)?)"
                );
pat_sql = re.compile(r"(?P<sql>(commit|rollback|select|update|delete|insert)\s*(.|\s){0,800})"
                     r"(.*;)",re.VERBOSE
                     );


def output( lines, fo, ferror ):
    big_line=""

    record = {}

    m_time = None
    m_user = None
    m_count = None
    m_sql = None
    
    for line in lines:
        big_line = big_line + line
        if not m_time:
            m_time = pat_time.search( line )
        if not m_user:
            m_user = pat_user.search( line )
        if not m_count:
            m_count = pat_count.search( line )
        if not m_sql:
            m_sql = pat_sql.search( line +';')
        
    if not (m_time and m_user and m_count and m_sql ) :
        ferror.write(big_line)
        print 'match results:'+str((m_time is None,m_user is None,m_count is None,m_sql is None))
        return False
        
    row=[];
    row.append( m_time.group("date"));
    row.append( m_time.group("time"));
    row.append( m_user.group("user"));
    row.append( m_user.group("host"));
    row.append( m_count.group("cost"));
    row.append( m_count.group("lock"));
    row.append( m_count.group("rows_sent"));
    row.append( m_count.group("rows_exam"));
    row.append( m_sql.group("sql"));

    tmp = row.pop()
    tmp = tmp.replace('\r','')
    tmp = tmp.replace('\t',' ')
    tmp = tmp.replace('\n',' ').strip()

    row.append(tmp)

    for cell in row:
        fo.write(cell+"\t")
    fo.write("\n")
    
    return True
