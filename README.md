ASSUMPTIONS
-----------
python 2.7 is installed

```bash
pi@raspberrypi:~/LawnCronPi $ python --version
  > Python 2.7.9
```

INSTALL DEPENDENCIES
--------------------

```bash
# Too much output for these next three
sudo apt-get update
sudo apt-get install rabbitmq-server
sudo apt-get install python-crontab

# Download pip
pi@raspberrypi:~/ $ wget https://bootstrap.pypa.io/get-pip.py
  > --2017-04-23 16:18:47--  https://bootstrap.pypa.io/get-pip.py
  > Resolving bootstrap.pypa.io (bootstrap.pypa.io)... 151.101.68.175
  > Connecting to bootstrap.pypa.io (bootstrap.pypa.io)|151.101.68.175|:443... connected.
  > HTTP request sent, awaiting response... 200 OK
  > Length: 1595408 (1.5M) [text/x-python]
  > Saving to: ‘get-pip.py’
  >
  > get-pip.py                100%[====================================>]   1.52M   492KB/s   in 3.2s
  >
  > 2017-04-23 16:18:50 (492 KB/s) - ‘get-pip.py’ saved [1595408/1595408]

# Install pip
pi@raspberrypi:~/ $ sudo python get-pip.py
  > Collecting pip
  >   Downloading pip-9.0.1-py2.py3-none-any.whl (1.3MB)
  >     100% |████████████████████████████████| 1.3MB 100kB/s
  > Installing collected packages: pip
  >   Found existing installation: pip 1.5.6
  >     Uninstalling pip-1.5.6:
  >       Successfully uninstalled pip-1.5.6
  > Successfully installed pip-9.0.1

# Install pika
pi@raspberrypi:~/ $ sudo pip install pika
  > Collecting pika
  >   Downloading pika-0.10.0-py2.py3-none-any.whl (92kB)
  >     100% |████████████████████████████████| 102kB 708kB/s
  > Installing collected packages: pika
  > Successfully installed pika-0.10.0

# Install python-rpi.gpio
pi@raspberrypi:~/LawnCronPi $ sudo apt-get install python-rpi.gpio
  > Reading package lists... Done
  > Building dependency tree
  > Reading state information... Done
  > The following packages will be upgraded:
  >   python-rpi.gpio
  > 1 upgraded, 0 newly installed, 0 to remove and 299 not upgraded.
  > Need to get 23.5 kB of archives.
  > After this operation, 6,144 B of additional disk space will be used.
  > Get:1 http://archive.raspberrypi.org/debian/ jessie/main python-rpi.gpio armhf 0.6.3~jessie-1 [23.5 kB]
  > Fetched 23.5 kB in 0s (50.6 kB/s)
  > (Reading database ... 133338 files and directories currently installed.)
  > Preparing to unpack .../python-rpi.gpio_0.6.3~jessie-1_armhf.deb ...
  > Unpacking python-rpi.gpio (0.6.3~jessie-1) over (0.6.1-1) ...
  > Setting up python-rpi.gpio (0.6.3~jessie-1) ...
```

INSTALL LAWN CRON
-------------

```bash
    pi@raspberrypi:~ $ ~
    pi@raspberrypi:~ $ git clone https://github.com/zmiller91/LawnCronPi.git
      > Cloning into 'LawnCronPi'...
      > remote: Counting objects: 28, done.
      > remote: Compressing objects: 100% (22/22), done.
      > remote: Total 28 (delta 8), reused 25 (delta 5), pack-reused 0
      > Unpacking objects: 100% (28/28), done.
      > Checking connectivity... done.
```

CONFIGURE LAWN CRON
---------------------------

Bare minimum configuration to get running:

```bash
# Create the cron file
pi@raspberrypi:~/LawnCronPi $ sudo touch /etc/cron.d/lawn

# Move to LawnCronPi directory
pi@raspberrypi:~ $ cd ~/LawnCronPi/

# Update the python configuration
pi@raspberrypi:~/LawnCronPi $ nano configuration.py

# Rabbit MQ Configuration
id = "rpi_id" # RPi ID generated at lawncron.com/rpi
rmq_host = "lawncron.com"

# Cron configuration
python = "/usr/bin/python" # Absolute path of python executable -- the output of `which python`
driver = "/home/pi/LawnCronPi/valve_driver.py" # Absolute path of valve driver
```

From here you should be able to execute lawn_cron.py and start recieving messages from lawncron.com.

```bash
pi@raspberrypi:~/LawnCronPi $ sudo python lawn_cron.py
  >  [*] Waiting for messages. To exit press CTRL+C
```

Create a schedule at lawncron.com/schedules and it will be added to your /etc/cron.d/lawn

```bash
pi@raspberrypi:~/LawnCronPi $ sudo python lawn_cron.py
  >  [*] Waiting for messages. To exit press CTRL+C
  > Adding schedule 11 in zone 2 for 1200 minutes starting at 18:45 on MON, WED, THU

pi@raspberrypi:~/LawnCronPi $ cat /etc/cron.d/lawn
  > 45 18 * * MON,WED,THU root /usr/bin/python /home/pi/LawnCronPi/valve_driver.py 2 1200 # 11
```

Everything is setup and fully integrated with lawncron.com. It's recommended to setup lawn cron as a service, but it's
entirely optional.

CREATE LAWN SERVICE
-------------------

```bash
# Configure the service
pi@raspberrypi:~/LawnCronPi $ vi lawn

# Make any changes if necessary
APPDIR="/home/pi/LawnCronPi" # Change to root directory of LawnCronPi -- the output of `pwd`
APPBIN="/usr/bin/python" # Absolute path of python executable -- the output of `which python`
APPARGS="lawn_cron.py" # No need to change, but it's the lawn cron service

# Install the service
pi@raspberrypi:~/LawnCronPi $ sudo mv lawn /etc/init.d/
pi@raspberrypi:~/LawnCronPi $ sudo chmod +x /etc/init.d/lawn
pi@raspberrypi:~/LawnCronPi $ sudo update-rc.d lawn defaults
pi@raspberrypi:~/LawnCronPi $ sudo systemctl daemon-reload

# Run the service
pi@raspberrypi:~/LawnCronPi $ sudo service lawn start
pi@raspberrypi:~/LawnCronPi $ ps -ef |grep lawn
  > root     25654     1  3 16:58 ?        00:00:00 /usr/bin/python lawn_cron.py
  > pi       25772  2183  0 16:58 pts/1    00:00:00 grep --color=auto lawn
```