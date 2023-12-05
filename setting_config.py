# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from sys import platform
import argparse
import re, os, os.path
from random import randint


path = os.path.abspath(os.path.dirname(__file__))


real = True
NETWORK_PATH = '/etc/network/interfaces'
MAC_ETH_PATH = '/etc/network/mac_eth0'
MAC_WLAN_PATH = '/etc/network/mac_wlan0'
WPA_PATH = '/etc/wpa_supplicant/wpa_supplicant.conf'

if platform == "win32":
    # Windows...
    real = False
    NETWORK_PATH = f'{path}/interfaces'

def checkip(your_ip):
    return [0<=int(x)<256 for x in re.split('\.',re.match(r'^\d+\.\d+\.\d+\.\d+$',your_ip).group(0))].count(True)==4




def random_mac(separator_char=':', separator_spacing=2):
    unseparated_mac = ''.join([hex(randint(0, 255))[2:].zfill(2) for _ in range(6)])
    return f'{separator_char}'.join(unseparated_mac[i:i + separator_spacing] for i in range(0, len(unseparated_mac), separator_spacing))

def write_mac(path, mac):
    file = open(path, 'w')
    file.write(mac)
    file.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", choices=['wifi', 'lan', 'setting'], type=str)
    parser.add_argument("-m", "--mode", choices=['none', 'dhcp', 'static'], type=str)
    parser.add_argument("-ssid", "--ssid", type=str)
    parser.add_argument("-pass", "--password", type=str)
    parser.add_argument("-ip", "--ip", type=str)
    parser.add_argument("-nm", "--netmask", type=str)
    parser.add_argument("-g", "--gateway", type=str)
    parser.add_argument("-dns1", "--dns1", type=str)
    parser.add_argument("-dns2", "--dns2", type=str)
    args = parser.parse_args()


    static = False
    getSetting = False
    if args.interface is None:
        print("ERROR: No interface to set, process failed, please use parameter -h to see parameter")
        exit()
    if args.interface == "wifi":
        if args.mode!='none':
            if args.ssid is None or args.password is None:
                print("ERROR: SSID or password is not provided, process failed")
                exit()
            else:
                if args.mode == 'static':
                    static = True
                    #lanjut dibawah

    elif args.interface == "lan":
        if args.mode == 'static':
            static = True
    elif args.interface == 'setting':
        getSetting = True
            #lajut dibawah
    if static:

        if args.ip is None or args.netmask is None or args.gateway is None:
            print("ERROR: parameter for static ip is not provided")
            exit()
        else:

            if not checkip(args.ip):
                print("ERROR: IP wrong format")
                exit()
            if not checkip(args.netmask):
                print("ERROR: netmask wrong format")
                exit()
            if not checkip(args.gateway):
                print("ERROR: gateway wrong format")
                exit()
            if args.dns1:
                if args.dns1 != 'None':
                    if not checkip(args.dns1):
                        print("ERROR: DNS1 wrong format")
                        exit()
            if args.dns2:
                if args.dns2 != 'None':
                    if not checkip(args.dns2):
                        print("ERROR: DNS2 wrong format")
                        exit()
    all = {}
    default = []
    temp = []
    mac_wlan = ''
    mac_eth = ''

    if os.path.exists(MAC_ETH_PATH):
        file = open(MAC_ETH_PATH, 'rt')
        mac = file.read().rstrip('\n')
        if mac:
            mac_eth = mac
        file.close()

    if os.path.exists(MAC_WLAN_PATH):
        file = open(MAC_WLAN_PATH, 'rt')
        mac = file.read().rstrip('\n')
        if mac:
            mac_wlan = mac
        file.close()

    file = open(NETWORK_PATH, "rt")

    group = ""
    for f in file:
        check = f.rstrip("\n")
        if check.strip():
            if (check[0]!="#"):
                if not group.strip():
                    if "wlan0" in check:
                        group="wlan"
                        temp.append(check)
                    elif "eth0" in check:
                        group="eth"
                        temp.append(check)
                    else :
                        default.append(check)
                else:
                    temp.append(check)
        else:
            if group.strip():
                temp.append("")
                all[group] = temp
                group = ""
                temp = []
            #ini kosong brarti ganti line
    if group.strip() and temp:
        temp.append("")
        all[group] = temp
        temp = []

    if default:
        all["default"]=default

    file.close()
    #print(all)

    if getSetting:
        #print(all)
        setting = {}
        temp = {}
        if 'wlan' in all:
            for allset in all['wlan']:
                allset = allset.strip()
                if re.search("iface", allset):
                    res = re.match('iface\ wlan[0-9]*\ inet\ (dhcp|static)', allset)
                    if res:
                        temp['mode'] = res[1]
                elif re.search('wpa-ssid', allset):
                    res = re.match('wpa-ssid\ ([a-zA-Z0-9-._!\"\`\'#%&,:;<>=@{}~\$\(\)\*\+\/\\\?\[\]\^\|]+)', allset)
                    if res:
                        temp['ssid'] = res[1]
                elif re.search('wpa-psk', allset):
                    res = re.match('wpa-psk\ ([a-zA-Z0-9-._!\"\`\'#%&,:;<>=@{}~\$\(\)\*\+\/\\\?\[\]\^\|]+)', allset)
                    if res:
                        temp['pass'] = res[1]
                if 'mode' in temp:
                    if temp['mode'] == 'static':
                        allset = allset.lower()
                        if re.search('address', allset):
                            res = re.match('address\ ([0-9]+.[0-9]+.[0-9]+.[0-9]+)', allset)
                            if res:
                                temp['ip']= res[1]
                        elif re.search('netmask', allset):
                            res = re.match('netmask\ ([0-9]+.[0-9]+.[0-9]+.[0-9]+)', allset)
                            if res:
                                temp['netmask']= res[1]
                        elif re.search('gateway', allset):
                            res = re.match('gateway\ ([0-9]+.[0-9]+.[0-9]+.[0-9]+)', allset)
                            if res:
                                temp['gateway']= res[1]
                        elif re.search('dns-nameservers', allset):
                            res = re.match('dns-nameservers\ ([0-9]+.[0-9]+.[0-9]+.[0-9]+)', allset)
                            if res:
                                if 'dns1' in temp:
                                    temp['dns2'] = res[1]
                                else:
                                    temp['dns1']= res[1]
        else:
            temp['mode']='None'

        setting['wlan'] = temp
        temp = {}
        if 'eth' in all:
            for allset in all['eth']:
                allset = allset.strip()
                if re.search("iface", allset):
                    res = re.match('iface\ eth[0-9]*\ inet\ (dhcp|static)', allset)
                    if res:
                        temp['mode'] = res[1]
                if 'mode' in temp:
                    if temp['mode'] == 'static':
                        allset = allset.lower()
                        if re.search('address', allset):
                            res = re.match('address\ ([0-9]+.[0-9]+.[0-9]+.[0-9]+)', allset)
                            if res:
                                temp['ip']= res[1]
                        elif re.search('netmask', allset):
                            res = re.match('netmask\ ([0-9]+.[0-9]+.[0-9]+.[0-9]+)', allset)
                            if res:
                                temp['netmask']= res[1]
                        elif re.search('gateway', allset):
                            res = re.match('gateway\ ([0-9]+.[0-9]+.[0-9]+.[0-9]+)', allset)
                            if res:
                                temp['gateway']= res[1]
                        elif re.search('dns-nameservers', allset):
                            res = re.match('dns-nameservers\ ([0-9]+.[0-9]+.[0-9]+.[0-9]+)', allset)
                            if res:
                                if 'dns1' in temp:
                                    temp['dns2'] = res[1]
                                else:
                                    temp['dns1']= res[1]
        else:
            temp['mode']='None'
        setting['lan'] = temp
        print(f"RESULT:{setting}")
        exit()
        #klo ambil setting aja ga usah write


    if args.interface == 'lan':
        if args.mode == 'none':
            if 'eth' in all:
                all['eth'] =[]
                mac_eth=''
                os.remove(MAC_ETH_PATH)
        elif args.mode == 'dhcp':
            temp = []
#            temp.append('auto eth0')
            temp.append('allow-hotplug eth0')
            temp.append('iface eth0 inet dhcp')
            if not mac_eth:
                mac_eth = random_mac()
                write_mac(MAC_ETH_PATH, mac_eth)
            temp.append(f'\thwaddress ether {mac_eth}')

             temp.append('if-up ifconfig wlan0 down && ip addr flush dev wlan0')
             temp.append('if-down ip addr flush dev eth0 && rm /var/run/wpa_supplicant/wlan0')
            all['eth'] = temp
            temp = []
        elif args.mode == 'static':
            temp = []
 #           temp.append('auto eth0')
            temp.append('allow-hotplug eth0')
            temp.append('iface eth0 inet static')
            if not mac_eth:
                mac_eth = random_mac()
                write_mac(MAC_ETH_PATH, mac_eth)
            temp.append(f'\thwaddress ether {mac_eth}')
            temp.append(f'\taddress {args.ip}')
            temp.append(f'\tnetmask {args.netmask}')
            temp.append(f'\tgateway {args.gateway}')
            if args.dns1:
                if args.dns1 != "None":
                    temp.append(f'\tdns-nameservers {args.dns1}')
            if args.dns2:
                if args.dns2 != "None":
                    temp.append(f'\tdns-nameservers {args.dns2}')
             temp.append('\tif-up ifconfig wlan0 down && ip addr flush dev wlan0')
             temp.append('\tif-down ip addr flush dev eth0 && rm /var/run/wpa_supplicant/wlan0')

            all['eth'] = temp
            temp = []


    if args.interface == 'wifi':
        if args.mode == 'none':
            if 'wlan' in all:
                all['wlan'] =[]
                mac_wlan = ''
                os.remove(MAC_WLAN_PATH)
        elif args.mode == 'dhcp':
            temp=[]
            temp.append('auto wlan0')
            temp.append('allow-hotplug wlan0')
            temp.append('iface wlan0 inet dhcp')
            if not mac_wlan:
                mac_wlan = random_mac()
                write_mac(MAC_WLAN_PATH, mac_wlan)
            temp.append(f'\thwaddress ether {mac_wlan}')
            temp.append(f'\twpa-ssid {args.ssid}')
            temp.append(f'\twpa-psk {args.password}')
            temp.append(f'\twireless-mode managed')
            temp.append(f'\twireless-power off')

            all['wlan'] = temp
            temp = []

        elif args.mode == 'static':
            temp=[]
            temp.append('auto wlan0')
            temp.append('allow-hotplug wlan0')
            temp.append('iface wlan0 inet static')
            if not mac_wlan:
                mac_wlan = random_mac()
                write_mac(MAC_WLAN_PATH, mac_wlan)
            temp.append(f'\thwaddress ether {mac_wlan}')
            temp.append(f'\twpa-ssid {args.ssid}')
            temp.append(f'\twpa-psk {args.password}')
            temp.append(f'\taddress {args.ip}')
            temp.append(f'\tnetmask {args.netmask}')
            temp.append(f'\tgateway {args.gateway}')
            if args.dns1:
                if args.dns1 != "None":
                    temp.append(f'\tdns-nameservers {args.dns1}')
            if args.dns2:
                if args.dns2 != "None":
                    temp.append(f'\tdns-nameservers {args.dns2}')
            temp.append(f'\twireless-mode managed')
            temp.append(f'\twireless-power off')
#            temp.append(f'\tpre-up rm -f /var/run/wpa_supplicant/wlan0')

            all['wlan'] = temp
            temp = []



    RESULT = NETWORK_PATH
    garis = '-------------------------------------------------------'
    if not real:
        RESULT = "./result"

    file = open(RESULT, "wt")

    for line in all["default"]:
        file.write(f"{line}\n")
    file.write("\n")

    if "wlan" in all:
        for line in all["wlan"]:
            file.write(f"{line}\n")
    file.write("\n")

    if "eth" in all:
        for line in all["eth"]:
            file.write(f"{line}\n")
    file.write("\n")

    file.close()

    print("SUCCESS: config created")
