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
    address = ('127.0.0.1', 10000)
    # TCP socket with IPv4 Addressing
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP) as sock:
        # Reuse a local socket in TIME_WAIT state,
        # without waiting for its natural timeout to expire
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        print("making a server on {0}:{1}".format(*address), file=log_buffer)

        # Binding new sock to the address above, and
        # begin to listen for incoming connection
        sock.bind(address)
        sock.listen(1)

        try:
            # the outer loop controls the creation of new connection sockets. The
            # server will handle each incoming connection one at a time.
            while True:
                print('waiting for a new connection', file=log_buffer)
                conn, add = sock.accept()
                addr = (conn, add)
                with conn:
                    recvdata = b''
                    try:
                        print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                        while True:
                            data = conn.recv(16)
                            print('Current received data:> {0}'.format(data.decode('utf8')))
                            recvdata += data
                            print('Total received data:> "{0}"'.format(recvdata.decode('utf8')))
                            print("len of received data: {0}".format(len(recvdata)))
                            if len(data) < 16:
                                print(log_buffer, "sending data")
                                conn.sendall(recvdata)
                                print('sent all received data: "{0}"'.format(recvdata.decode('utf8')))
                                break
                        # conn.close()
                        print('no data from', add)

                    except BrokenPipeError as err:
                        traceback.print_exc(err)
                        sys.exit(1)
                    finally:
                        print('echo complete, client conn closed', file=log_buffer)
                        # Clean up the connections
                        # conn.close()

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
