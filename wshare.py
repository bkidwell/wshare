import argparse
import subprocess
import re
import pprint
import sys
from wshare_config import config

pp = pprint.PrettyPrinter().pprint

def getConnDict():
    txt = subprocess.getoutput('net use')
    match = re.search(r'--------.*\n([\w\W]*?)The command completed', txt)
    if match is None:
        print("Can't parse 'net use' output.")
        exit
    data = match.group(1).split('\n')
    data = [row for row in data if not re.match('^    ', row)]
    data = [re.split(r' *', row) for row in data]
    result = dict()
    for row in data:
        if len(row) < 2: continue
        if re.match(r'\w:', row[1]):
            result[(row[1] + row[2]).lower()] = {
                'drive_letter': row[1],
                'path': row[2],
                'username': None,
                'password': None,
                'status': row[0],
                'in_conf': False,
            }
        else:
            result[row[1].lower()] = {
                'drive_letter': None,
                'path': row[1],
                'username': None,
                'password': None,
                'status': row[0],
                'in_conf': False,
            }
    return result

def getAll():
    conns = getConnDict()
    for key, value in config.items():
        if value['drive_letter']:
            value['drive_letter'] = value['drive_letter'][0].upper() + ':'
        path = value['path'].replace('/', '\\')
        skey = (value['drive_letter'] + path if value['drive_letter'] else path).lower()
        value['username'] = value['username'].replace('/', '\\')
        if skey in conns:
            conn = conns[skey]
            conn['username'] = value['username']
            conn['password'] = value['password']
            conn['drive_letter'] = conn['drive_letter'] or value['drive_letter']
            conn['in_conf'] = key
        else:
            value['path'] = path
            value['in_conf'] = key
            value['status'] = 'Not connected'
            conns[path.lower()] = value
    conns = [conns[key] for key in sorted(conns.keys())]
    return conns

def printStatus(connList):
    i = 0
    #pp(connList)
    for conn in connList:
        i += 1
        if conn['in_conf']:
            print(str(i) + ' [' + conn['in_conf'] + ']:: ' + (conn['drive_letter'] or '') + ' ' + conn['path'])
        else:
            print(':: ' + (conn['drive_letter'] or '') + ' ' + conn['path'] + ' (not in config)')
        print('        ' + str(conn['status']))

def main(sel):
    conns = getAll()
    if sel is None:
        print('\nNetwork shares:')
        print('')
        printStatus(conns)
        print('')
        num = input('Reconnect which share number or name? (ENTER to quit) ')
        print('')
    else:
        num = sel
    
    if num == '' or num == '0': return False
    
    conn = None
    for value in conns:
        if value['in_conf'] and value['in_conf'] == num:
            conn = value
    
    if conn is None:
        try:
            num = int(num)
            conn = conns[num - 1]
        except:
            print('Bad number or name.')
            if sel: return False
            else: return True

    if sel:
        print('Reconnecting ' + sel + '...')
            
    if conn['drive_letter']:
        subprocess.getoutput('net use ' + conn['drive_letter'] + ' /delete')
    subprocess.getoutput('net use ' + conn['path'] + ' /delete')
    subprocess.call(
        'net use ' +
        (conn['drive_letter'] if conn['drive_letter'] else '') + ' ' +
        conn['path'] + ' ' +
        '/user:' + conn['username'] + ' ' +
        '"' + conn['password'] + '"'
    )
    
    if not sel is None:
        input('Press ENTER to continue.')
        return False
    else:
        return True

parser = argparse.ArgumentParser(description='List Windows File Sharing shares and reconnect bookmarks.')
parser.add_argument(
    'selection', metavar='NAME', type=str, nargs='?',
    help='The name of the bookmark from wshare_config.py to reconnect'
)

args = parser.parse_args()
#pp(args)

while True:
    if not main(args.selection): break
