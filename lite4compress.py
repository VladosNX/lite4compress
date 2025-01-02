#!/usr/bin/python3
import zlib
import sys
import anderparse
import os

def printhelp():
    print('-f <file>\n-c - compress\n-d - decompress\n-l <loops>')
    sys.exit(0)

parser = anderparse.Parser(sys.argv)
parser.add_arg('file', '-f', xtype=anderparse.T_STRING)
parser.add_arg('compress', '-c', xtype=anderparse.T_BOOL)
parser.add_arg('decompress', '-d', xtype=anderparse.T_BOOL)
parser.add_arg('loops', '-l', xtype=anderparse.T_INT)
try: args = parser.parse()
except anderparse.MissingRequiredArgument as e:
    printhelp()
except anderparse.ArgumentNotFound as e:
    printhelp()
if args['file'] == None or [args['compress'], args['decompress']] == [False, False] or [args['compress'], args['decompress']] == [True, True]:
    printhelp()

if not os.path.exists(args['file']):
    print(f"{args['file']} not found")
    sys.exit(1)

filetype = args['file'].split('.')[len(args['file'].split('.')) - 1]
if not filetype.find('l4c') == -1:
    try:
        args['loops'] = int(filetype.replace('l4c', ''))
    except:
        pass

if args['loops'] == None:
    print(f'No loops specified on filetype or arguments')
    sys.exit(1)

result = open(args['file'], mode='rb').read()
for _ in range(args['loops']):
    if args['compress']:
        result = zlib.compress(result)
    elif args['decompress']:
        result = zlib.decompress(result)
    print(f"Loop {_+1} {'compressed' if args['compress'] else 'decompressed'}")

outname = ''
if args['compress']: outname = f"{args['file']}.l4c{args['loops']}"
elif args['decompress']:
    if not filetype.find('l4c') == -1:
        outname = args['file'].replace(f".{filetype}", '')

of = open(outname, mode='wb+')
of.write(result)
of.close()

print(f"Saved to {outname}")