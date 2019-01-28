# vim: set fileencoding=utf-8 :

#!/usr/bin/env python

#pytach.itach

#:copyright: (c) 2012 by Mark McWilliams.
#:license: MIT, see LICENSE for more details.

import socket
import struct
import sys
import re

class iTach(object):
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = int(port)

    def raw_command(self, command):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((self.ip_address, self.port))

        s.send(command)
        s.send('\r')

        data = ''
        while True:
            data += s.recv(1024)
#            print "data: ", data
            if data.endswith('\r') or data.endswith('\n'):
                s.close()
                return data.rstrip()

def discover():
    p = re.compile((r'AMXB<-UUID=GlobalCache_(?P<UUID>.{12}).+'
        r'Model=iTach(?P<Model>.+?)>.+'
        r'Revision=(?P<Revision>.+?)>.+'
        r'Config-URL=http://(?P<IP>.+?)>.+'
        r'PCB_PN=(?P<PN>.+?)>.+'
        r'Status=(?P<Status>.+?)>'))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 9131))

    group = socket.inet_aton('239.255.250.250')
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        data = s.recv(1024)
        match = p.match(data)
        if match:
            s.close()

            itach = iTach(match.group('IP'))
            itach.uuid = match.group('UUID')
            itach.model = match.group('Model')
            itach.revision = match.group('Revision')
            itach.part_number = match.group('PN')
            itach.status = match.group('Status')
            return itach

if __name__ == '__main__':
    itach = iTach(sys.argv[1], sys.argv[2])
    print(itach.raw_command(sys.argv[3]))
