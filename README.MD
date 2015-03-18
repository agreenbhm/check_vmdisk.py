check_vmdisk.py

by AGreen BHM

License: GPLv2.0

This is a check command for Icinga/Nagios/any other compatible monitoring tool that
reports the free disk space available on VMware vSphere virtual machines.

Returns a listing of all disks in the VM, the percentage of free space, and the size (in GB) available.
Default thresholds are: Warning - <=25%, Critical - <=10%.  Change this to whatever you want.  I will likely add this as a command-line argument in the future.

Dependencies: VMware vSphere Perl SDK (written for v5.5, untested with others)

Usage: check_vmdisk.py -s <vCenter-SDK-url> -u <user> -p <password>  -v <vmname>'

Example: check_vmdisk.py -s https://vCenterServer:443:/sdk/webService -u readonly -p ropassword -v "Sample VM"

Install to a folder containing monitoring plugins.  Create the necessary CheckCommand and CheckService configuration files.
Included are sample CheckCommand, CheckService and Host configuration files.  Make sure to add the appropriate arguments to the service check to be passed to the script.

The user requires read-only access to vCenter.  The vmname is the name of the virtual machine as it appears in vCenter.

To avoid excess output the actual vCenter connection script does not display error messages.  If you have a problem
remove the parameter "stderr=subprocess.PIPE" from the vminfo variable.




