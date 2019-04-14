import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    ''' client socket that will send a message and receive a reply,
    :param msg: msg to be sent to server
    :param log_buffer:
    :return: msg received from server
    '''
    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP) as sock:
        sock.connect(server_address)
        print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)
        # Send data
        # message = b'this is the message. It will be repeated'
        recvdata = b''
        try:
            print('sending "{0}"'.format(msg), file=log_buffer)
            sock.sendall(msg.encode('utf8'))
            # Look for the response
            amount_received = 0
            amount_expected = len(msg)
            while amount_received < amount_expected:
                data = sock.recv(16)
                recvdata += data
                amount_received += len(recvdata)
                print('received "{0}"'.format(recvdata.decode('utf8')), file=log_buffer)
        except BrokenPipeError as err:
            traceback.print_exc(err)
            sys.exit(1)
        finally:
            print('closing socket', file=log_buffer)
            # sock.close()
        # return msg
        return recvdata.decode('utf8')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
