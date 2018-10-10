
import argparse
import sys


def output(line):
    print(line)


def poisk(line, params): 
    line = line.rstrip('\n')
    
    g = 0    
    for each in params.pattern:
        if each != '?':
            g = 0
            break
        g += 1
    
    if 0 < g <= len(line):
        return True

    if params.ignore_case == True:
        params.pattern=params.pattern.lower()
        line=line.lower()
    if params.pattern.strip('*')=='':
        Z = True
        return Z
    for i in params.pattern.replace('*', ' ').replace('?', ' ').rsplit():
        if i in line[params.pattern.index(i[0]):len(line) - len(params.pattern) + params.pattern.index(i[-1]) + 1] or params.pattern in line:
            if params.invert==False:
                Z = True
            else:
                Z = False
        else:
            if params.invert==False:
                Z = False
            else:
                Z = True    
        
        return Z 

    

    

def grep(lines, params):
    af = max(params.after_context, params.context)
    bef = max(params.before_context, params.context)
    ctr = 0                                
    dic = {}
    last_idx = 0                                   
    afcount = 1

    for idx, line in enumerate(lines, start = 1):
        afcount -= 1  
        line = line.rstrip()
        dic.update({idx: line})     
        if len(dic) > bef + 1:
            dic.pop(idx - bef - 1)  
        if poisk(line,params):      
            for l in dic:
                if l > last_idx:
                    if params.line_number == True:
                        simb = ':'
                        if l != idx:
                            simb = '-'
                        simb = str(l) + simb
                    else:
                        simb = ''
                    ctr += 1
                    if params.count == False:
                        output(simb + dic[l])
            afcount = af + 1
            last_idx = idx
            
        if 0 < afcount <= af:
            if params.line_number == True:
                simb = '-'
                simb = str(idx) + simb
            else:
                simb = ''
            output(simb + dic[idx])
            last_idx += 1 

    if params.count == True:
        output(str(ctr))



def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(), params)

    print()
    print(params)


if __name__ == '__main__':
    main()