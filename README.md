sudo apt-get install python-crontab
echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list
wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install rabbitmq-server
sudo pip-install pika

To setup as a service:

follow this sysvinit tutorial: https://blog.frd.mn/how-to-set-up-proper-startstop-services-ubuntu-debian-mac-windows/
use "lawn" instead of example