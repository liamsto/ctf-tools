#script to enumerate possible docker breakouts

import os
import subprocess

def main():

    #check to see if the docker binary is installed
    if os.path.exists('/usr/bin/docker'):
        print("Docker binary found")
    else:
        print("Docker binary not found")
        exit()
    #check to see if the docker socket is mounted inside the container (usually /var/run/docker.sock)
    if os.path.exists('/var/run/docker.sock'):
        print("Docker socket found")
    else:
        print("Docker socket not found")
        exit()

    #try a privilidged operation to see if --privileged flag is set
    try:
        #try to load a kernel module
        subprocess.check_output(['modprobe', 'dummy']).decode('utf-8')
        print("Privileged operation successful")
    except:
        print("Privileged operation failed")

    #use capsh to check for capabilities
    escape_vectors = ['CAP_SYS_ADMIN', 'CAP_SYS_PTRACE', 'CAP_SYS_MODULE', 'DAC_READ_SEARCH', 'DAC_OVERRIDE', 'CAP_SYS_RAWIO', 'CAP_SYSLOG', 'CAP_NET_RAW', 'CAP_NET_ADMIN']
    capsh_output = subprocess.check_output(['capsh', '--print']).decode('utf-8')
    for vector in escape_vectors:
        if vector in capsh_output:
            print("Possible breakout vector found, user has privilidge: " + vector)

    #check if we can see the PID of the host
    pid = subprocess.check_output(['ps', '-ef']).decode('utf-8')
    print("Host PID: " + pid)
    
    

