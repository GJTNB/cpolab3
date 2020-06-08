from CLI import *
import unittest
import sys
import os


class TestMutableList(unittest.TestCase):
    def test_v(self):
        lst = ['-v', '-V', '--version']
        for s in lst:
            ret = v()
            self.assertEqual(ret, sys.version)

    def test_path(self):
        lst = [['PATH', '1.txt'], ['PATH', '2.txt']]
        for s in lst:
            ret = PATH(s[1])
            self.assertEqual(ret, os.getcwd() + '\\' + s[1])

    def test_help(self):
        h = Help()
        self.assertEqual(h, 'usage: [--version | -V |-v ] [-h] [PATH] [-r][cat a|n|d] [-hex]\nsub-commands:\n\t\tcat '
                            'a: add data to the file \n\t\tcat n: create a new file\n\t\tcat d: Download files via http '
                            '\nposition arguments:\n\t\tPATH : Print the absolute path of the file \nnamed '
                            'arguments:\n\t\t--version : Show the current command-line interface version(also -v '
                            '-V)\n\t\t-h: show this help method and exit\n\t\t-r: Read the contents in the file '
                            '\n\t\t-hex: Change the input value to hex and save it to the hex.txt \n')

    def test_read(self):
        lst = ['-r', '1.txt']
        f1 = open('1.txt')
        ret = read(lst[1])
        self.assertEqual(ret, f1.readlines())
        f1.close()

    def test_cat_a(self):
        add_content = 'JG BEAT'
        lst = ['cat', 'a', '1.txt', add_content]
        f1 = open('1.txt')
        original_content = f1.read()
        f1.close()
        cat(lst[1:])
        f2 = open('1.txt')
        new_content = original_content + add_content + '\n'
        self.assertEqual(new_content, f2.read())
        f2.close()

    def test_cat_n(self):
        if (os.path.exists('new.txt')):
            os.remove('new.txt')
        lst = ['cat', 'n', 'new.txt']
        cat(lst[1:])
        flag = os.path.exists('new.txt')
        self.assertEqual(True, flag)

    def test_cat_d(self):
        if (os.path.exists('file.txt')):
            os.remove('file.txt')
        lst = ['cat', 'd', 'http://47.106.110.83/file.tex']
        cat(lst[1:])
        flag = os.path.exists('file.txt')
        self.assertEqual(True, flag)

    def test_hex(self):
        lst = ['hex', 10]
        f = open('hex.txt', 'r+')
        f.truncate()
        hex(lst[1])
        self.assertEqual('a' + '\n', f.read())
        f.close()

        lst = ['hex', 14]
        f = open('hex.txt', 'r+')
        f.truncate()
        hex(lst[1])
        self.assertEqual('e' + '\n', f.read())
        f.close()


if __name__ == '__main__':
    unittest.main()
