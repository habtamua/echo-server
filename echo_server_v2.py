''' Task  to build a simple "echo" server '''
import socket
import sys
import traceback
import os


def server(log_buffer=sys.stderr):
    '''
    Server socket, sends back whatever messages it receives from a client
    :param log_buffer:
    :return:
    '''
    address = ('localhost', 10001)
    # TCP socket with IPv4 Addressing
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Reuse a local socket in TIME_WAIT state,
    # without waiting for its natural timeout to expire
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    # Binding new sock to the address above,& begin to listen for incoming conn
    sock.bind(address)
    sock.listen(1)
    try:
        while True:
            # Wait for a connection
            print('waiting for a connection:›')
            conn, add = sock.accept()
            addr = (conn, add)
            try:
                print('connection from - {0}:{1}'.format(*addr), file=log_buffer)
                # Receive the data in small chunks and retransmit it
                while True:
                    data = conn.recv(16)
                    print('received:› {0}'.format(data.decode('utf8')))
                    if data:
                        recvdata = data.decode('utf8')
                        print(f'sending data back to the client:› {recvdata}')
                        conn.sendall(data)
                    else:
                        print('no data from', addr)
                        break
            except BrokenPipeError as err:
                traceback.print_exc(err)
                sys.exit(1)

            finally:
                # Clean up the connection
                conn.close()

    except KeyboardInterrupt:
        # pass
        print('quitting echo server', file=log_buffer)
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
        sock.close()


if __name__ == '__main__':
    server()
    sys.exit(0)
