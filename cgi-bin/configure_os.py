__author__ = 'jonathan'
from optparse import OptionParser
import os

environment_shebangs = {}

windows_aliases = ['windows', 'nt']
nix_aliases =  ['posix', 'mac', 'osx', 'ubuntu', 'linux', 'nix']

for windows_alias in windows_aliases:
    environment_shebangs[windows_alias] = 'C:\Python32\python.exe'

for nix_alias in nix_aliases:
    environment_shebangs[nix_alias] = '/usr/bin/env python'

parser = OptionParser()
parser.add_option("-e", "--environment", action="store", dest="environment", help="The environment for which to configure.")
parser.add_option("-f", "--file", action="store", dest="filename", help="The file to configure for the chosen environment.")
(options, args) = parser.parse_args()

environment = options.environment
filename=options.filename

if not environment:
    environment = os.name

if filename and environment:
    if environment in nix_aliases:
        destination_environment = windows_aliases[0]
    else:
        destination_environment = nix_aliases[0]

    read_original_file = open(filename, 'r')
    original_contents = [line.replace(environment_shebangs[environment], environment_shebangs[destination_environment])
                         for line in read_original_file.readlines()]
    read_original_file.close()

    configured_file_contents = [line.replace(environment_shebangs[environment], environment_shebangs[destination_environment])
                                for line in original_contents]

    original_file_backup = open(filename+'.bak','w')
    for line in original_contents:
        original_file_backup.write(line)
    original_file_backup.close()

    write_original_file = open(filename,'w')
    write_original_file.write(''.join(configured_file_contents))
    write_original_file.close()

    print("configured %s to %s"%(filename, destination_environment))

else:
    print("fail!")




