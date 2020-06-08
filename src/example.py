import CLI
import os

@CLI.command
@CLI.option('-v', default=None, Help='vision')
@CLI.option('-h', default=None, Help='help information')
@CLI.option('PATH', default=' ', Help='get the file\'s path')
@CLI.option('-r', default='1.txt', Help='read file')
@CLI.option('-hex', default='0', Help='Change the input value to hex and save it to the hex.txt')
@CLI.option('cat', default=None, Help='This is a subcommand')
@CLI.argument('name',default='',Help='your name')
def hello_world(name):
    print("%s\n" % name)

if __name__ == '__main__':
    hello_world('')
    CLI.run()

