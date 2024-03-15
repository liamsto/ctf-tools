#!/usr/bin/env python3
import subprocess
from termcolor import colored

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output = result.stdout.strip()
        return output
    except subprocess.CalledProcessError as e:
        return e.output

def print_section_header(title, color='green'):
    print(colored(f"\n{'=' * 80}\n{title}\n{'=' * 80}", color))

# exclude standard users because who cares about these
def list_non_standard_users():
    print_section_header("Non-Standard Users")
    users = run_command("cat /etc/passwd")
    for user in users.split('\n'):
        if not any(standard_user in user for standard_user in ['root', 'daemon', 'bin', 'sys', 'sync', 'games', 'man', 'lp', 'mail', 'news', 'uucp', 'proxy', 'www-data', 'backup', 'list', 'irc', 'gnats', 'nobody', 'systemd-network', 'systemd-resolve', 'syslog', 'messagebus', '_apt', 'lxd', 'uuidd', 'dnsmasq', 'landscape', 'sshd', 'pollinate']):
            print(user.split(":")[0])

# sudo -l output
def check_sudo_permissions():
    print_section_header("Sudo Permissions", 'cyan')
    print(run_command("sudo -l"))

# Listening ports
def list_listening_ports():
    print_section_header("Listening Ports", 'yellow')
    print(run_command("netstat -tuln"))

# Scheduled cron jobs
def list_cron_jobs():
    print_section_header("Cron Jobs", 'magenta')
    print(run_command("crontab -l"))

# Running processes
def list_running_processes():
    print_section_header("Running Processes", 'blue')
    print(run_command("ps aux"))

def list_groups():
    print(run_command("groups"))

def enum_user_home():
    print_section_header("User Home Directories", 'red')
    for(user, home) in run_command("cat /etc/passwd | cut -d: -f1,6").split('\n'):
        print(f"{user}: {home}")

if __name__ == "__main__":
    list_non_standard_users()
    check_sudo_permissions()
    list_listening_ports()
    list_cron_jobs()
    list_running_processes()
    enum_user_home()
    list_groups()
