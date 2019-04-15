
import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    ''' client socket that will send a message and receive a reply,
    :param msg: msg to be sent to server
    :param log_buffer:
    :return: msg received from server
    '''
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 10001)
        print('connecting to:› {} port {}'.format(*server_address))
        sock.connect(server_address)
        recvdata = b''
        try:
            # Send data
            print('sending:› {!r}'.format(msg))
            sock.sendall(msg.encode('utf8'))

            received = 0
            expected = len(msg)

            # Look for the response
            while received < expected:
                data = sock.recv(16)
                recvdata += data
                received += len(data)
                print('received:› {!r}'.format(recvdata))

        except BrokenPipeError as err:
            traceback.print_exc(err)
            sys.exit(1)

        finally:
            print('closing socket')
            sock.close()

        return recvdata.decode('utf8')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
