import re
import os
import sys
from arg_process import parse_argument

hd = '/home/user/'
try:
    user_path = parse_argument()

    if user_path[0] == '/':
        user_path = user_path[1:]
except:
    sys.exit(0)

if hd in user_path:
    if hd  in '/' + user_path:
        file = '/' + user_path
    else:
        file = user_path
else:
    file = os.path.join(hd ,user_path)

def get_file_lines(file):
    with open(file) as f:
        lines = f.readlines()
    return lines

def catch_libraries(lines):
    edited_lines = []
    pattern = r'import [a-z .A-Z]+'
    for line in lines:
        ans = re.findall(pattern,line)
        if ans:
            edited_lines.append(ans[-1])
 
    libraries = {}
    for line in edited_lines:
        pattern = r'import [a-z.A-Z]*'
        ans = re.findall(pattern,line)[0].split()[-1]
        ref = line.split()[-1]
        libraries[ref] = ans
    return libraries

def check_library(file,libraries):    
    is_present = {lib : False for lib in libraries}
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            for lib in libraries:
                case1 = re.search(r'\b%s\b' %lib,line)
                case2 = re.search(r'\b%s.\b' %lib,line)
                case3 = re.search(r'\b%s\(\b' %lib,line)
                if (case1 or case2 or case3) and 'import' not in line:
                    is_present[lib] = True
                    break
    return is_present

def get_valid_lines(lines,is_present):
    output_file_lines = []
    for line in lines:
        write = True
        for lib,res in is_present.items():
            if not res and lib in line and 'import' in line:
                write = False
                break
        if write:
            output_file_lines.append(line)
    return output_file_lines

def write_file(file,output_file_lines):
    with open(file,'w') as f:
        f.writelines(output_file_lines)

if __name__ == "__main__":
    lines = get_file_lines(file)
    arg1 = catch_libraries(lines)
    arg2 = check_library(file,arg1)
    arg3 = get_valid_lines(lines,arg2)
    write_file(file,arg3)