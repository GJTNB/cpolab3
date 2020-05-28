import sys
import os
import requests

'''
Function description: Output version information
:param s: Command entered
Usage example: python *.py --version | -V | -v
output:
3.6.5 |Anaconda, Inc.| (default, Mar 29 2018, 13:32:41) [MSC v.1900 64 bit (AMD64)]
'''
def v(s):
    ret = sys.version
    print(ret)
    return s[1:], ret

'''
Function description: Output the path of the specified file
:param s: Command entered
Usage example: python *.py PATH 1.txt
output:
E:\lab3\1.txt
'''
def PATH(s):
    path = os.getcwd()
    ret = path + '\\' + s[1]
    print(ret)
    return s[2:], ret

'''
Function description: Output help information
:param s: Command entered
Usage example: python *.py -h 
output:
usage: [--version | -V |-v ] [-h] [PATH] [-r][cat a|n|d] [-hex]
sub-commands:
                cat a: add data to the file
                cat n: create a new file
                cat d: download files
position arguments:
                PATH : Print the absolute path of the file
named arguments:
                --version : Show the current command-line interface version(also -v -V)
                -h: show this help method and exit
                -r: Read the contents in the file
                -hex: Change the input value to hex and save it to the hex.txt
'''
def Help(s):
    s.pop(0)
    ret = "usage: [--version | -V |-v ] [-h] [PATH] [-r][cat a|n|d] [-hex]\n"
    ret = ret + "sub-commands:\n"
    ret = ret + "\t\tcat a: add data to the file \n"
    ret = ret + "\t\tcat n: create a new file\n"
    ret = ret + "\t\tcat d: Download files via http \n"
    ret = ret + "position arguments:\n"
    ret = ret + "\t\tPATH : Print the absolute path of the file \n"
    ret = ret + "named arguments:\n"
    ret = ret + "\t\t--version : Show the current command-line interface version(also -v -V)\n"
    ret = ret + "\t\t-h: show this help method and exit\n"
    ret = ret + "\t\t-r: Read the contents in the file \n"
    ret = ret + "\t\t-hex: Change the input value to hex and save it to the hex.txt \n"
    print(ret)
    return s, ret

'''
Function description: Read the contents in the file
:param s: Command entered
Usage example: python *.py -r 1.txt
output:
This is 1.txt
This file is created at 2020/5/28 10:39 in Beijing time.
1234
'''
def read(s):
    with open(s[1]) as f:
        lines = f.readlines()
        for l in lines:
            print(l, end='')
        return s[2:], lines

'''
Function description:          
                        cat a: add data to the file
                        cat n: create a new file
                        cat d: Download files via http
:param s: Command entered
cat a Usage example: python *.py cat a 1.txt 'the text you want to add'
cat n Usage example: python *.py cat n 4.txt
cat d Usage example: python *.py cat d http://47.106.110.83/file.tex
'''
def cat(s):
    s.pop(0)
    ret = []
    while len(s) > 0 and s[0] in ['n', 'a', 'd']:
        if s[0] is 'n':
            s.pop(0)
            f = open(s[0], 'w')
            f.close()
            s.pop(0)
        elif s[0] is 'a':
            s.pop(0)
            with open(s[0], 'a') as f:
                f.write(s[1] + "\n")
            s = s[2:]
        elif s[0] is 'd':
            s.pop(0)
            r = requests.get(s[0])
            with open(os.path.join(os.path.dirname(os.path.abspath("__file__")), "file.txt"), "wb") as f:
                f.write(r.content)
                ret.append(r.content)
            s.pop(0)
    return s, ret

'''
Function description: Change the input value to hex and save it to the hex.txt
:param s: Command entered 
Usage example: python *.py  10
output:
Write A to hex.txt
'''
def hex(s):
    s.pop(0)
    ret =""
    HEX = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    num = int(s[0])
    while num >15:
        ret = HEX[num % 16] + ret
        num = num // 16
    ret = HEX[num] +ret
    with open('hex.txt', 'a') as f:
        f.write(ret + "\n")
    print(ret)
    s.pop(0)
    return s,ret

'''
uses the decorated function as callback.  This will also automatically attach all decorated.
'''
def command(f):
    def r(*args, **kwargs):
        Coms = sys.argv[1:]
        fun = {'-v': v, '-V': v, '--version': v, 'PATH': PATH, '-h': Help, '-r': read, 'cat': cat,'-hex':hex}
        while len(Coms) > 0:
            if Coms[0] not in fun:
                print('\'' + Coms[0] + '\' is not availiable' )
                raise KeyError
                break
            Coms, out = fun[Coms[0]](Coms)

        return f(*args, **kwargs)

    return r


if __name__ == '__main__':
    print(sys.argv[0])
    print(sys.argv[1])
