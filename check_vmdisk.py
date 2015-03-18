#!/usr/bin/python
import sys
import subprocess
import re
import getopt

def main(cliargs):
    vmname = ""
    user = ""
    password = ""
    url = ""

    try:
        opts, args = getopt.getopt(cliargs, "s:u:p:v:")
    except getopt.GetoptError as e:
        print 'check_vmdisk.py -s <vCenter-SDK-url> -u <user> -p <password>  -v <vmname>'
        print "Error: " + e.msg
        sys.exit(3)

    for opt, arg in opts:
        if opt == '-v':
            vmname = arg
        elif opt == '-s':
            url = arg
        elif opt == '-u':
            user = arg
        elif opt == '-p':
            password = arg

    if vmname == '' or user == '' or url == '' or password == '':
        print 'check_vmdisk.py -s <vCenter-SDK-url> -u <user> -p <password>  -v <vmname>'
        print sys.argv
        sys.exit(3)

    vminfo = subprocess.check_output(
        ["/usr/lib/vmware-vcli/apps/vm/guestinfo.pl", "--url", url,
         "--username", user, "--password", password, "--vmname", vmname, "--operation", "display"], stderr=subprocess.PIPE)

    diskinfo = []
    vmsplitlines = vminfo.split("\n")
    for i in vmsplitlines:
        if re.search("Disk\[", i):
            diskinfo.append(i)

    splitlines = diskinfo

    numdisks = len(splitlines) / 3
    diskdict = {}
    for i in xrange(0, numdisks):
        diskdict[str(i)] = {}
    for line in splitlines:
        var = line.replace(':', '').rsplit(' ', 1)
        var[0] = var[0].split('Disk[')
        var[0][0] = var[0][0].strip()
        var[0][1] = var[0][1].replace(']', '')
        var[0][1] = var[0][1].split(' ', 1)
        var[0][1][1] = var[0][1][1].replace(' ', '')
        diskdict[var[0][1][0]].update({var[0][1][1]: var[1]})

    warningthreshold = 25
    criticalthreshold = 10
    exitcode = 0
    finalstatus = "OK"
    returnstring = ""
    for disk in diskdict:
        status = "OK"
        diskdict[disk]['Path'] = diskdict[disk]['Path']
        diskfreepercent = int(round((float(diskdict[disk]['freespace']) / float(diskdict[disk]['Capacity'])) * 100, 0))
        diskfreegb = (((int(diskdict[disk]['freespace'])) / 1024) / 1024) / 1024
        if criticalthreshold < diskfreepercent <= warningthreshold:
            if status != "CRITICAL":
                status = "WARNING"
                if finalstatus == "OK":
                    finalstatus = "WARNING"
                    exitcode = 1
        elif diskfreepercent <= criticalthreshold:
            status = "CRITICAL"
            finalstatus = "CRITICAL"
            exitcode = 2
        returnstring += status + " - " + diskdict[disk]['Path'].rstrip('\\') + " - " + str(diskfreepercent) + "% free (" + str(diskfreegb) + " GB)\n"
    returnstring = returnstring.rsplit("\n", 1)
    print returnstring[0]
    sys.exit(exitcode)

if __name__ == '__main__':
    main(sys.argv[1:])