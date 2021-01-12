import getopt
import sys

options, args = getopt.getopt(sys.argv[1:],'ua:', ['user','admin']) 

print(options)
print(args)


