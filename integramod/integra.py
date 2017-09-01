import time
from socket import socket, AF_INET, SOCK_STREAM

DELAY = 0.002
MAX_ATTEMPTS = 3


def ihex(byte):
    return str(hex(byte)[2:])


def checksum(command):
    crc = 0x147A;
    for b in command:
        # rotate (crc 1 bit left)
        crc = ((crc << 1) & 0xFFFF) | (crc & 0x8000) >> 15
        crc = crc ^ 0xFFFF
        crc = (crc + (crc >> 8) + b) & 0xFFFF
    return crc;


def send(config, command):
    data = bytearray.fromhex(command)
    c = checksum(bytearray.fromhex(command))
    data.append(c >> 8)
    data.append(c & 0xFF)
    data.replace(b'\xFE', b'\xFE\xF0')

    data = bytearray.fromhex("FEFE") + data + bytearray.fromhex("FE0D")

    failure_counter = 0
    while True:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((config.host, config.port))
        if not sock.send(data): raise Exception("Error Sending message.")
        resp = sock.recv(100)
        sock.close()

        BUSY_MSG = b'\x10\x42\x75\x73\x79\x21\x0D\x0A'
        if (resp[0:8] == BUSY_MSG):
            failure_counter = failure_counter + 1
            if failure_counter < MAX_ATTEMPTS:
                time.sleep(DELAY * failure_counter)
            else:
                break
        else:
            break

    # check message

    if (resp[0:2] != b'\xFE\xFE'):
        for c in resp:
            print("0x%X" % c)
        raise Exception("Wrong header - got %X%X" % (resp[0], resp[1]))
    if (resp[-2:] != b'\xFE\x0D'):
        raise Exception("Wrong footer - got %X%X" % (resp[-2], resp[-1]))

    output = resp[2:-2].replace(b'\xFE\xF0', b'\xFE')
    if output[0:1] == b'\xEF':
        if not output[1:1] in b'\xFF\x00':
            raise Exception("Integra reported an error code %X" % output[1])
    elif output[0] != bytearray.fromhex(command[0:2])[0]:
        raise Exception(
            "Response to a wrong command - got %X expected %X" % (output[0], bytearray.fromhex(command[0:2])[0]))

    c = checksum(bytearray(output[0:-2]))
    if (256 * output[-2:-1][0] + output[-1:][0]) != c:
        raise Exception("Wrong checksum - got %d expected %d" % ((256 * output[-2:-1][0] + output[-1:][0]), c))
    # return only data
    return output[1:-2]


def check_state(config, input_number):
    """
    Checks if given state number (decimal value) is violated
    :param config: Configuration object
    :param input_number: integer
    :return: bool
    """
    if input_number % 8 == 0:
        raise
    r = send(config, "00")
    b = input_number % 8 - 1
    i = int(input_number / 8)
    response = r[i]
    return bool(2 ** b & response)


def get_name(config, input_number):
    """
    Gets name of given number (decimal value)
    :param input_number: integer
    :return: string
    """
    number = str(hex(input_number))[2:]
    if len(number) == 1:
        number = "0" + number
    r = send("EE01" + str(number))
    return r[3:].decode(config.encoding)

#interested_input = 23
#print(get_name(interested_input), check_state(interested_input))