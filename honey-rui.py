import socket
import threading
import os
import time
import logging
import logging.handlers
import sys
from datetime import datetime


remote_log = None
sockethostname = socket.gethostname()

def tprint(msg):
    current_time = datetime.now().isoformat()
    fmsg=f"[{current_time}] {msg}"
    print(fmsg,flush=True)

    if remote_log:
        remote_log.info(fmsg)


def start_fake_tcp_server(listen_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', listen_port))
    server_socket.listen(5)
    
    listenmsg=f"{sockethostname} listening on port {listen_port}"
    tprint(listenmsg)

    while True:
        client_socket, addr = server_socket.accept()
        synmsg=f"{sockethostname} listenport {listen_port} received packet from ip {addr[0]} port {addr[1]}"
        tprint(synmsg)

        client_socket.close()


def get_rsyslog_from_env():
    rsyslog_server = os.getenv('RSYSLOG_SERVER')
    rsyslog_port = int(os.getenv('RSYSLOG_PORT',1514))
    if rsyslog_server:
        global remote_log
        remote_log = logging.getLogger("honey-rui")
        remote_log.setLevel(logging.INFO)
        handler = logging.handlers.SysLogHandler(address=(rsyslog_server, rsyslog_port)) #default udp
        remote_log.addHandler(handler)


def get_ports_from_env():
    ports_env = os.getenv('LISTEN_PORTS', '9999')
    ports = []
    for port in ports_env.split(','):
        port = port.strip()
        if port.isdigit():
            ports.append(int(port))

    return ports


def health_report():
    interval_env=int(os.getenv('HEALTH_INTERVAL','86400'))
    while True:
        time.sleep(interval_env)
        healthmsg = f"{sockethostname} service is running"
        tprint(healthmsg)


if __name__ == "__main__":
    get_rsyslog_from_env()
    listen_ports = get_ports_from_env()

    health_thread = threading.Thread(target=health_report)
    health_thread.daemon = True
    health_thread.start()

    listen_threads = []
    for port in listen_ports:
        listen_thread = threading.Thread(target=start_fake_tcp_server, args=(port,))
        listen_thread.daemon = True
        listen_thread.start()
        listen_threads.append(listen_thread)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        tprint("ctrl break, shutting down...")
