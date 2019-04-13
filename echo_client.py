import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    ''' a client function that can send a message and receive a reply. '''
    server_address = ('localhost', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    sock.connect(server_address)
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)

    message = b'this is the message. It will be repeated'
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)
        sock.sendall(message)

        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print('received "{0}"'.format(message.decode('utf8')), file=log_buffer)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    finally:
        print('closing socket', file=log_buffer)
        sock.close()
    return data


if __name__ == '__main__':
    if len(sys.argv) != 2:
        USAGE = '\nusage: python echo_client.py "this is my message"\n'
        print(USAGE, file=sys.stderr)
        sys.exit(1)

    MSG = sys.argv[1]
    client(MSG)
