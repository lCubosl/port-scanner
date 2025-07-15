# interface to the Berkeley sockets API
import socket
# work with ipadresses
import ipaddress
# create regex (regular expressions)
import re
import sys

print(r"""
    ___       ___       ___       ___       ___       ___       ___   
   /\  \     /\__\     /\  \     /\  \     /\  \     /\  \     /\  \  
  /  \  \   / /__/_   _\ \  \   /  \  \    \ \  \   /  \  \   /  \  \ 
 /\ \ \__\ /  \/\__\ /\/  \__\ /  \ \__\   /  \__\ /  \ \__\ /  \ \__\
 \ \ \/__/ \/\  /  / \  /\/__/ \/\ \/__/  / /\/__/ \ \ \/__/ \;   /  /
  \  /  /    / /  /   \ \__\      \/__/   \/__/     \ \/__/   | \/__/ 
   \/__/     \/__/     \/__/                         \/__/     \|__|  
""")
print("\n*********************************************************************")
print("\n* Original Credit goes to David Bombal                              *")
print("\n* Edited by SHIFTER                                                 *")
print("\n*********************************************************************")

# regular expression pattern for number of ports to scan
# ex: 10-100
port_range_pattern = re.compile("([0-9]+)-([0-9]+)")

port_min = 0
port_max = 65535

while True:
  # 1. get a valid ip
  while True:
    ip_add_entered = input("\nPlease enter the ip adress that you want to scan: ")
    # except case when the ip adress is not valid the block will repeat until valid one is entered
    try:
      ipaddress.ip_address(ip_add_entered)
      print("You enetered a valid ip adress.")
      break
    except ValueError:
      print("You entered an invalid ip adress.")

  while True:
    # you can scan ports 0-65535. Do not scan all the ports
    print("Please enter the range of ports you want to scan in format <int>-<int> (ex: 0-10)")
    # checks if you input any spaces and removes them 0 - 10 = 0-10
    port_range = input("Enter port range: ").replace(" ","")
    m = port_range_pattern.match(port_range)

    if m:
      port_min, port_max = map(int, m.groups())
      print(f"Searching for open ports in the range: {port_min} - {port_max}")
      break
    else:
      print("bad range format, try again")

  # actual port scanner
  # 2. scan the ports
  open_ports = []
  for port in range(port_min, port_max+1):
    # connect to socket of target machine
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      # longer timeout duration will result in a better result
      # it will allow each port to be tested for a connection for 0.5s
      # scanning ports 0-10 will result in a 10x0.5= 5second wait time (max)
      # if it cannot connect, it will not append the values
      s.settimeout(0.5)
      try:
        if s.connect_ex((ip_add_entered, port)) == 0:
          # only runs when the connection is successfull
          open_ports.append(port)
      except socket.error:
        pass

  # 3. handle result
  if not open_ports:
    print(f"No open ports found on {ip_add_entered}.")

  # we only care about open ports
  for port in open_ports:
    print(f"-> Port {port} is open on {ip_add_entered}.")

  # ask to repeat else exit
  again = input("\nDo you want to search for open ports on another host? [Y/n]: ").strip().lower()
  if again == "n":
    sys.exit(0)