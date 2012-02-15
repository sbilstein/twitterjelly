__author__ = 'jonathan'
from optparse import OptionParser
import os
import re

parser = OptionParser()
parser.add_option("-d", "--disable", action="store_true", dest="disable", help="Disable logging. Default behavior.")
parser.add_option("-e", "--enable", action="store_false", dest="disable", help="Enable logging. Use for debugging.")
parser.add_option("-f", "--file", action="store", dest="filename", help="""Optional if you only want to enable/disable
a specific file. Otherwise all js files will be affected.""")
(options, args) = parser.parse_args()

if options.filename:
    filename = options.filename
else:
    filename = None

if type(options.disable).__name__ == 'bool':
    disable = options.disable
else:
    disable = True

pat = r'console\.log\('
replace_str = "// console.log("

if not disable:
    pat = r'(\/+\s*?)+console\.log\('
    replace_str = "console.log("

if not filename:
    files = list(filter(lambda x:os.path.isfile(x) and x[len(x)-3:].lower() == '.js', os.listdir('.')))
else:
    files = [filename]

for filename in files:
    read_original_file = open(filename, 'r')
    original_contents = [line for line in read_original_file.readlines()]
    read_original_file.close()

    configured_file_contents = [re.sub(pat, replace_str, line) for line in original_contents]

    #original_file_backup = open(filename+'.bak','w')
    #for line in original_contents:
    #    original_file_backup.write(line)
    #original_file_backup.close()

    write_original_file = open(filename,'w')
    write_original_file.write(''.join(configured_file_contents))
    write_original_file.close()

    if disable:
        print("disabled logging in",filename)
    else:
        print("enabled logging in",filename)
