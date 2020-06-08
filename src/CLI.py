import sys
import os
import requests
from functools import wraps

'''
Function description: Output version information
:param s: Command entered
Usage example: python *.py --version | -V | -v
output:
3.6.5 |Anaconda, Inc.| (default, Mar 29 2018, 13:32:41) [MSC v.1900 64 bit (AMD64)]
'''


def v():
    ret = sys.version
    print(ret)
    return ret


'''
Function description: Output the path of the specified file
:param s: Command entered
Usage example: python *.py PATH 1.txt
output:
E:\lab3\1.txt
'''


def PATH(s):
    path = os.getcwd()
    ret = path + '\\' + s
    print(ret)
    return ret


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


def Help():
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
    return ret


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
    with open(s) as f:
        lines = f.readlines()
        for l in lines:
            print(l, end='')
        return lines


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
    return ret


'''
Function description: Change the input value to hex and save it to the hex.txt
:param s: Command entered 
Usage example: python *.py  10
output:
Write A to hex.txt
'''


def hex(s):
    ret = ""
    HEX = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    num = int(s)
    while num > 15:
        ret = HEX[num % 16] + ret
        num = num // 16
    ret = HEX[num] + ret
    with open('hex.txt', 'a') as f:
        f.write(ret + "\n")
    print(ret)
    return ret


option_command = {}
Coms = []
fun = {'-v': v, '-V': v, '--version': v, 'PATH': PATH, '-h': Help, '-r': read, 'cat': cat, '-hex': hex}
subcommand_name=[]

#Used to decorate a function so that the function serves as a command line interface
def command(f):
    def r(*args, **kwargs):
        global Coms
        Coms = sys.argv[1:]
        return f(*args, **kwargs)
    return r

#Used to decorate a function, the main function is to add options to the command line
def option(func_name, default=None, Help='help'):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            global option_command
            option_command[fun[func_name]] = default
            return func(*args, **kwargs)
        return wrapped_function
    return logging_decorator

#Pass a simple variable value
def argument(func_name, default=None, Help='help'):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            global option_command
            global  Coms
            argu=default
            subcommand_name.append(func_name)
            fun[func_name]=func_name
            option_command[fun[func_name]] = args
            Coms = sys.argv[1:]
            if func_name in Coms:
                index=Coms.index(func_name)
                argu=Coms[index+1]
            func(argu)
        return wrapped_function
    return logging_decorator

def run():
    global  Coms
    while len(Coms) > 0:
        if fun[Coms[0]] not in option_command:
            print('\'' + Coms[0] + '\' is not availiable')
            raise KeyError
            break
        elif fun[Coms[0]] is v:
            v()
            Coms = Coms[1:]
        elif fun[Coms[0]] is Help:
            Help()
            Coms = Coms[1:]
        elif fun[Coms[0]] in subcommand_name:
            break
        elif fun[Coms[0]] is PATH :
            if len(Coms)==1 :
                PATH(option_command[PATH])
                break
            elif Coms[1] in fun:
                PATH(option_command[PATH])
                Coms = Coms[1:]
            else:
                PATH(Coms[1])
                Coms = Coms[2:]
        elif fun[Coms[0]] is read:
            if len(Coms)==1 :
                read(option_command[read])
                break
            elif Coms[1] in fun:
                read(option_command[read])
                Coms = Coms[1:]
            else:
                read(Coms[1])
                Coms = Coms[2:]
        elif fun[Coms[0]] is hex:
            if len(Coms)==1 :
                hex(option_command[hex])
                break
            elif Coms[1] in fun:
                hex(option_command[hex])
                Coms = Coms[1:]
            else:
                hex(Coms[1])
                Coms = Coms[2:]
        elif fun[Coms[0]] is cat:
            if len(Coms)==1 or Coms[1] in fun:
                print('Invalid instruction ')
            else:
                c = []
                Coms.pop(0)
                while Coms[0] in ['n', 'a', 'd']:
                    if Coms[0] is 'a':
                        c.append(Coms[0])
                        Coms.pop(0)
                        c.append(Coms[0])
                        Coms.pop(0)
                        c.append(Coms[0])
                        Coms.pop(0)
                    else:
                        c.append(Coms[0])
                        Coms.pop(0)
                        c.append(Coms[0])
                        Coms.pop(0)
                    if len(Coms) == 0 :
                        break
                cat(c)


if __name__ == '__main__':
    Help()
