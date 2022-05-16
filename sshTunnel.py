from sshtunnel import SSHTunnelForwarder

server = None

def main():
    global server
    try:
        server = SSHTunnelForwarder(
            "10.10.0.251",
            ssh_username="ruizdev7",
            ssh_password="C9p5au8naa*",
            remote_bind_address=("127.0.0.1", 3306)
        )
        server.start()
        tunnel_port = server.local_bind_port
        print(tunnel_port)
    except Exception as e:
        print("something was wrong: {error}".format(error=e))
        server.stop()
        exit()
        
if __name__ == "__main__":
    main()
    while "c" not in input():
        pass
    server.close()
    