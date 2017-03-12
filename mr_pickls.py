import win32api
from subprocess import call
import os
import time

print("""             .
            ..';:::;;,..                           ..,;;::;,..
         .',cxkkkkkxdddc'.   ......',,'......    .;codddxko:ooc,..
      .':ldkOO0Okkkxdodddc,;coxkxdldkkdloxxdol;,:ddooddodkkxkOOkdc,.
    .,lxkxxkkkOkOOxxkxdoooox00xodxooxxookxlcx0kllxxoxkxdxkk0OkOkkkdl:..
   .cxdxxkO0kddkOkdxkxdl;..;dx;..:ddddoxo'..ldc'.:llxOkkOkxxOOkkxxdddl'.
  .,dxxkxk0KOoodddooccodl::;,co;';llodoxd::ol::ldddoolcoodxdoxkxxxxxxd:.
  .;xO0OddkOd;;;;,,;;cdkOOkl:lxOxllcodoxOkOkoloxOOkdoo:''';;,;ldxkOkxxl.
  .:xkOkxxxo:;;;;:clllllcldoooodl,':odol::odooodoc::oxdlc::;;;cdkOOkO0o.
  .:ddxxxo:,,,';locodocclxxc;;cxc';lxkdl,'oo;;:oko,,ldkOkl:'''':odxdxOo.
  .cdoooc'.   .;xkdxkxoooOOc..:kdclxOOdcclko'.,d0xc:cldkxo:.   .':cdxxo,
 .,odlcc,.    .:xOxdkOkkooxxoloolookOdxooxddoldxdldOkxxxxxo'     .;looo;.
.'lxkd,..    .:ooddxkO00Odoolloodoxkc'lxoxkkkkkkddOK00Oxlldo,.    .'cxxc,.
.:cc:,.      ,dxdodOOO000OkkxdoodxOd;;:dkddxkkkkxk0K000kllxOl.     ..;cc:'.
.''..       .:xkkdllldkOOkdodocok0KOk0kk0OxdddxxxkO0klcodkOkc.        ..,'.
           .cdxdooolccdxxooooxk0KK00K000000OOxxdoxkkkxdddoddoc'.
           'lxO0kxxkOxoxOxkkkO0000O00O0OO0000OOkkOOkk00kxxkOOk:.
           .'cxOOkxdookOOOxxkkooxkkOOkOOkkoldkkkOOOOxldkOkxkxc.
             .:dkxdoldxxkkddxd:cdllxOOkolxo;lxddxOkdocoO0ko:'.
              .:olododxdxd;;dxllo,.;lc:..ldlxkc,lxooxooolol'
               ..,okxodxkx:.;odooloolcloooodko',ooloddxd;...
                 .okkxodxkd,..cdddolccloodxo:..lxxxoloxx;.
                 .oxlccloxkd;...'coc,.;ll;...'lxxddxkddd,
                 .ll;clllodxxl'.,x00dlkKOl..:dkdoclxkxdd,
                 .:ooddddddxxkxolxK0xokK0dlkkxdlc::coddl'
                  ..;lxxxxxkdc:clxX0dokX0dol:looooddoc,.
                    ..;cododdl' 'xK0xokX0:..;oc:lol:'.
                       .',:ldd; .l0K0O0Kx' .;lll:'..
                         .:xOO:. .:ddddl'. .ll::'
                          .'cl'    .....   .:l,..
                            ..               .
mr_pickls ARP Cache Monitoring Tool Version 1.0
http://www.github.com/gitgiant
___________________________________________________________________________

""")
class arp_cache_entry:

    def __init__(self, ip, mac, status):
        self.ip = ip
        self.mac = mac
        self.status = status

class interface:

    def __init__(self, ip, id):
        self.ip = ip
        #self.list = list[arp_cache_entry]
        self.id = id

# calls arp -a, stores result in text file
def call_arp(target):
    with open(target, "w") as file:
        # calls arp -a, and stores it in file
        call('arp -a', stdout=file)
    file.close()

# parse arp -a output into a list of arp_cache_entry objects
def parse_new_arp_cache(target):

    interfaceList = []
    arpCacheList = []

    with open(target, 'r') as readFile:
        for line in readFile:
            splitLine = line.split()
            #if the line is empty
            if len(splitLine) == 0:
                pass
            # Line starts with interface = interface designator
            elif splitLine[0] == 'Interface:':
                newInterface = interface(splitLine[1], splitLine[3])
                interfaceList.append(newInterface)
            # skip header line
            elif splitLine[0] == 'Internet':
                pass
            # line starts with ip : arp cache entry
            else:
                newArpCache = arp_cache_entry(splitLine[0], splitLine[1], splitLine[2])
                arpCacheList.append(newArpCache)
    readFile.close()
    return arpCacheList

def display_arp_cache(target):

    for line in target:
        print(line.ip.ljust(20) + line.mac)
# get the initial arp cache, store it in arp_cache_old.txt
call_arp("arp_cache_old.txt")

oldArpCacheList = parse_new_arp_cache("arp_cache_old.txt")

# loop forever
while True:
    time.sleep(5)
    # grab new arp cache and parse list
    call_arp("arp_cache_new.txt")
    newArpCacheList = parse_new_arp_cache("arp_cache_new.txt")
    oldArpCacheList = parse_new_arp_cache("arp_cache_old.txt")
    #for each new arp cache entry
    for i in range(0, len(newArpCacheList)):
        #for each old arp cache entry
        for j in range(0, len(oldArpCacheList)):
            # if the two ips match, inspec their mac address'
            if(newArpCacheList[i].ip == oldArpCacheList[j].ip):
                # if the two mac addresses do not match, then ignore and move on
                if(newArpCacheList[i].mac != oldArpCacheList[j].mac):
                    print("New MAC address detected on IP: " + newArpCacheList[i].ip)
                    print("Old MAC address: " + oldArpCacheList[j].mac + "\nNew MAC address: " + newArpCacheList[i].mac)
                    win32api.MessageBox(0, "Old MAC address: " + oldArpCacheList[j].mac + "\nNew MAC address: " + newArpCacheList[i].mac, "New MAC address detected on IP: " + newArpCacheList[i].ip)
                else:
                    print("IP: " + newArpCacheList[i].ip.ljust(20) + "MAC: " + newArpCacheList[i].mac)
    # scanned through for changes, reset old
    time.sleep(5)
    call_arp("arp_cache_old.txt")
    oldArpCacheList = parse_new_arp_cache("arp_cache_old.txt")
    print("______________________________________________")

win32api.MessageBox(0, "GOOD BOY", "title")