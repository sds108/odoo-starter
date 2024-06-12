# odoo-starter
Quick Odoo 17 starter config maker and runner, so that you don't have to waste time editing configurations by text, or resetting any services, and spend more time on fixing your bugs.
The odoo-starter is designed to speed up the process of choosing which databases to load and which modules to upgrade. Basically, a fast way to modify and run the command:
 `/home/odoo/odoo17-venv/bin/python3 /home/odoo/odoo/odoo-bin -c /etc/odoo.conf -d {your_databases} -u {your_upgrades} --log-handler odoo.tools.convert:DEBUG` where you can dynamically change the list of `your_databases` and `your_upgrades`. It then starts the server, and proceeds to run the command `tail -f /var/log/odoo/odoo.log` so you can monitor your log in realtime.

User Guide
---
 - To get started, make sure there aren't any other services running on the port Odoo 17 runs on (typically port:**8069**).
 - To start the odoo-starter, use the command `python3 odoo-starter.py`. Without any flags, the odoo-starter boots up to the startup screen, where you can press `Enter` to load and run the config, enter `e` to overwrite the current config, or `q` to just load the current config without running the server.
 - By entering `e`, you are brought to a screen with formatting instructions, where you choose a delimiter to delimit your databases and your upgrades list. Then you can enter your databases and upgrades list in the following format:
 `database_name,database name with spaces,database_name` and `module path name with spaces,module_path_name`, where in this case the chosen delimiter is the comma character. Please notice there are no spaces at the start or end of each name (unless you intend that), and **No Quotation Marks** are needed, as they are automatically added later.
 - You can press `Ctrl` - `Q` at any point in time to quit the program, and don't worry, all of the background processes are forced to shutdown as well.

 Startup Flags
 ---
  - You can add the flags `--q=True/False` and `--d=True\False` to your odoo-starter command, where the `--q` flag if set to **True** enables a quick start, skipping the startup screen and proceeds to instantly start the server (if the config file exists). The `--d` flag if set to **True** skips the delimiter selection as it can get tedious entering this each time. You can run the odoo-starter with both enabled like so: `python3 odoo-starter.py --q=True --d=True`. You can also modify the default value for each of these settings permanently within the `odoo-starter.py` file by editing the two boolean variables at the top of the file as so:
  >skip_delimiter_selection = False  
  >skip_to_load = False
  - Feel free to modify the rest of the code as you wish as well.

