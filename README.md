purpose
===
A simple honeypot program, specify any port number to listen on, when a sniffer tries to connect it will print the connection information, and if a rsyslog server is specified it will also send the information to the rsyslog server.


env for image
===
- RSYSLOG_SERVER : set remote syslog server. we use udp for it
- RSYSLOG_PORT : set port for remote syslog server. default is 1514
- LISTEN_PORTS : set listen port for image. default is 9999
- HEALTH_INTERVAL : default is 86400s (1 day), then echo "service in running"


build image
===
```
docker build -t honey-rui .
```


example
===
```
docker run --rm -p 9999:9999 honey-rui
#use default listen port 9999, listen and print connection information

docker run --rm -e LISTEN_PORTS='8080,8000' -p 8080:8080 -p 8000:8000 honey-rui
#set listen ports to 8080 and 8000, we may add more.

docker run --rm -e LISTEN_PORTS='8080,8000' -e RSYSLOG_SERVER=192.168.122.90 -e RSYSLOG_PORT=1514 -p 8080:8080 -p 8000:8000 honey-rui
#set listen ports to 8080 and 8000. and set IP and port for rsyslog server

docker run --rm -e LISTEN_PORTS='8080,8000' -e RSYSLOG_SERVER=192.168.122.90 -e HEALTH_INTERVAL=10 -p 8080:8080 -p 8000:8000 honey-rui
#set a different health_interval to make sure the service is running
```


sample running log
===
```
[2024-06-23T15:11:17.701094] 39c93dd64944 listening on port 80
[2024-06-23T15:11:17.701957] 39c93dd64944 listening on port 8080
[2024-06-23T15:11:17.702141] 39c93dd64944 listening on port 8000
[2024-06-23T15:11:24.750780] 39c93dd64944 listenport 80 received packet from ip 192.168.122.1 port 39336
[2024-06-23T15:11:27.711134] 39c93dd64944 service is running
[2024-06-23T15:11:37.722307] 39c93dd64944 service is running

```
