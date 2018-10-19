from dateutil import parser
from collections import Counter, defaultdict
import re 



def check_line(log):
    regexp = r'\d{2}\/\w{3}\/\d{4}\s\d{2}\:\d{2}\:\d{2}'
    date=re.findall(regexp,log)
    if len(date)!=0:
        return True
    else:
        return False    





def get_date(log):
    regexp = r'\d{2}\/\w{3}\/\d{4}\s\d{2}\:\d{2}\:\d{2}'
    date = re.findall(regexp,log)
    return date[0]
            

def get_url(log):
    regexp = r'\w{4,5}[://]{3}(.+)\?'
    url = re.findall(regexp,log)
    if len(url)==0:
        regexp = r'\w{4,5}[://]{3}(\S+)'
        url = re.findall(regexp,log)
    return url[0]

def reader(filename):

    file=open(filename) 
    lines=file.readlines()
    return lines

def top_five(logs):    
    
    counter = Counter(logs)  
    for elem, count in counter.most_common(5):
        print(count) 
            


def get_response_time(log):
    return int(log.split()[-1])

def get_withoutwww(log):
    regexp = r'[www.]{4}(\S+)'
    withoutwww = re.findall(regexp,log)
    if len(withoutwww)!=0:
        return withoutwww[0]
    else:
        return log   


def get_type(log):
    regexp = r'\"(\w{3,4})'
    tp=re.findall(regexp,log)
    return tp[0]

def check_file(log):
    regexp = r'\/.+\.\w{2,3}'
    fl=re.findall(regexp,log)
    if len(fl)!=0:
        return True
    else:
        return False 

def get_resptime(log):
    regexp = r' \d{3} (\d{2,6})'
    resptime=re.findall(regexp,log)
    return resptime[0]




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
        if check_line(line)==True:
            date=get_date(line)
            url=get_url(line)
            tp=get_type(line)
            resptime=int(get_resptime(line))
            file=check_file(url)
            print(file)
            if ignore_www == True:
                url = get_withoutwww(url)

            if (file == False or ignore_files == False) and\
            (tp == request_type or request_type == None) and\
            (start_at == None or date >= start_at) and\
            (stop_at == None or date <= stop_at):
                c[url] += 1
                slow[url][0] += 1
                slow[url][1] += resptime
                
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
