from dateutil import parser
from collections import Counter, defaultdict

def reader(filename):

    file=open(filename) 
    lines=file.readlines()
    return lines


def get_datetime(log):
    dt = parser.parse(log[1:21])      
    return dt
        
            
def get_file(log):
    if '/'!=log[len(log)-1]:
        if '.' == log[len(log)-4] or '.' == log[len(log)-3]:
            return True
        else:
            return False
    else: 
        return False    
    
def get_url(log): 
    if '?' in log and '://' in log:
        url=log[log.index('://')+3:log.index('?')]
    elif '://' in log and ' ' in log:
        url=log[log.index('://')+3:log.index(' ', log.index('://'))]
    return url

def top_five(logs):    
    
    counter = Counter(logs)  
    for elem, count in counter.most_common(5):
        print(count) 
            

def get_type(log):
    log=log[log.index('"')+1:log.index(' ', log.index('"'))]
    return log

def get_response_time(log):
    return int(log.split()[-1])

def get_withoutwww(log):
    if log[0:4]=='www.':
        return log[4:]
    else:
        return log
        

def parse1(
    ignore_files=False,
    ignore_urls=[],
    start_at=None,
    stop_at=None,
    request_type=None,
    ignore_www=False,
    slow_queries=False
):
    c=Counter()
    lines=reader('log.log')
    res_arr = []
    slow = defaultdict(lambda: [0, 0])

    for line in lines:
        if line[0]=='[' and  line[21]==']':

            typ = get_type(line)
            url = get_url(line)
            file = get_file(url)
            time = get_datetime(line)
            rtime = get_response_time(line)
            
            if ignore_www == True:
                url = get_withoutwww(url)

            if (file == False or ignore_files == False) and\
            (type == request_type or request_type == None) and\
            (start_at == None or time >= start_at) and\
            (stop_at == None or time <= stop_at):

                c[url] += 1
                slow[url][0] += 1
                slow[url][1] += rtime
                
    if slow_queries == True:
        for each in slow:
            res_arr.append(slow[each][1] // slow[each][0])
        res_arr = sorted(res_arr, reverse = True)[:5] 

    else:    
        for elem, count in c.most_common(5):
            res_arr.append(count)   
    
    print(res_arr)
    return res_arr  

if __name__ == '__main__':
    parse1()  
