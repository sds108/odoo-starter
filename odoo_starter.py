import subprocess
import atexit
import os
import time
import argparse

##### Quick perma edits #####

# Skip delimiter selection
skip_delimiter_selection = False
# Skip to load
skip_to_load = False

#############################

# Variables
loaded = False
databases = ""
upgrades = ""
delimiter = "," # Default is the comma

clear_log_process: None
odoo_process: None
tail_process: None

odoo_conf_path = "odoo_starter.odooConf"
odoo_front = "/home/odoo/odoo17-venv/bin/python3 /home/odoo/odoo/odoo-bin -c /etc/odoo.conf"
odoo_tagons = "--log-handler odoo.tools.convert:DEBUG"
odoo_command = ""

config_exists = False

def startup():
  global loaded
  global databases
  global upgrades
  global config_exists
  global skip_to_load

  # Enter to run config
  # 'e' to edit config
  # 'q' to load the current config

  while (True):
    # Clear command line
    print('\033c')

    # Check if config file exists
    config_exists = os.path.isfile(odoo_conf_path)

    if not config_exists:
      loaded = False

    # Loaded variables
    if loaded and config_exists:
      print(f"Loaded databases: {databases}")
      print(f"Loaded upgrades: {upgrades}\n")

    # Skip to loading
    if skip_to_load:
      load_config(False)
      return

    # Get input
    i = input("Press 'Enter' to run config file\nEnter 'q' to load config\nEnter 'e' to edit config\n\nPress Ctrl-C to quit at any point in time\n\n:")

    if i == 'e':
      load_config(True)
    elif i == 'q':
      if config_exists:
        load_config(False)
        loaded = True
      else:
        print("No config file found, please create one first")
        time.sleep(3)
    elif i == '':
      load_config(False)
      return
    else:
      continue

def print_instructions():
  global delimiter

  # Clear command line
  print('\033c')

  print("""=========================================================================
        
  This is the format for entering your database list, and upgrade list

  database_name,database_name,database name with spaces

  module name with spaces,module_name,module_name
  
  In this case, the delimiter is the comma character, but you can
  change it to whatever you want.

  Don't worry about adding Quotes to your names,
  they are added automatically !!!

  Just make sure not to add spaces at the start and end of each name !!!

  It appears the name of each module is the name of its root folder !!!
        
=========================================================================
""")
  
  if delimiter: print(f"Current delimiter: {delimiter}")
  else: print("")

  print("\n")


def load_config(editing: bool):
  global databases
  global upgrades
  global delimiter
  global skip_delimiter_selection

  # Clear command line
  print('\033c')

  if config_exists and not editing:
    config_file = open(odoo_conf_path, 'r')
    # get the databases line
    for line in config_file:
      if not databases:
        databases = line[:-1]
      elif not upgrades:
        upgrades = line
      else:
        break
  else:
    if not skip_delimiter_selection:
      # Choose delimiter
      print_instructions()
      delimiter = input("Enter delimiter\n\n:")

    # Get databases
    print_instructions()
    databases = input("Enter databases\n\n:")
    
    # Get upgrades
    print_instructions()
    upgrades = input("Enter upgrades\n\n:")

    # Delimit databases and add Quotes
    databases_list = databases.split(delimiter)
    databases_list = ['"' + database + '"' for database in databases_list]
    databases = ','.join(databases_list)

    # Delimit upgrades and add Quotes
    upgrades_list = upgrades.split(delimiter)
    upgrades_list = ['"' + upgrade + '"' for upgrade in upgrades_list]
    upgrades = ','.join(upgrades_list)


    print("\nEntered...")
    print("Databases: ",databases)
    print("Upgrades: ",upgrades,"\n")
    print("\nPress Ctrl-C to Cancel\n")

    save_time = 6
    for s in range(save_time):
      print("  Saving in.     ",save_time-s, end='\r')
      time.sleep(0.2)
      print("  Saving in..    ",save_time-s, end='\r')
      time.sleep(0.2)
      print("  Saving in...   ",save_time-s, end='\r')
      time.sleep(0.2)
      print("  Saving in....  ",save_time-s, end='\r')
      time.sleep(0.2)
      print("  Saving in..... ",save_time-s, end='\r')
      time.sleep(0.2)

    config_file = open(odoo_conf_path, 'w')
    config_file.writelines([databases,"\n",upgrades])
    config_file.close()

def construct_command():
  global databases
  global upgrades
  global odoo_command
  global odoo_front
  global odoo_tagons

  if len(databases) > 0 and len(upgrades) > 0:
    odoo_command = odoo_front + " -d " + databases + " -u " + upgrades
  elif len(databases) > 0:
    odoo_command = odoo_front + " -d " + databases
  elif len(upgrades) > 0:
    odoo_command = odoo_front + " -u " + upgrades
  else:
    odoo_command = odoo_front

  # Add tag-ons
  odoo_command += " " + odoo_tagons

def start_processes():
  global clear_log_process
  global odoo_process
  global tail_process

  # Clear command line
  print('\033c')

  # Clear log file
  clear_log_process = subprocess.Popen('> /var/log/odoo/odoo.log',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  clear_log_process.wait()

  # Start Odoo
  odoo_process = subprocess.Popen(odoo_command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

  # Start tailing
  tail_process = subprocess.Popen('tail -f /var/log/odoo/odoo.log',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  for line in iter(tail_process.stdout.readline, b''):
    print(line.decode().strip())

# Handle arguments
def main(q, d):
  global skip_delimiter_selection
  global skip_to_load

  if q:
    skip_to_load = q
  
  if d:
    skip_delimiter_selection = d

# Register a function to be called on exit
def cleanup():
  global clear_log_process
  global odoo_process
  global tail_process

  print("\nCleaning up...")
  if clear_log_process: clear_log_process.kill()
  if odoo_process: odoo_process.kill()
  if tail_process: tail_process.kill()

atexit.register(cleanup)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--q", type=lambda x: (str(x).lower() == 'true'), required=False)
  parser.add_argument("--d", type=lambda x: (str(x).lower() == 'true'), required=False)
  args = parser.parse_args()
  main(args.q, args.d)

# order of operations
startup()
construct_command()
start_processes()