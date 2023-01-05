#!/usr/bin/env python3

from newscaleserial import NewScaleSerial

def setBit7(msg_bytes):
    msg_ba = bytearray(msg_bytes)
    for i in range(len(msg_ba)):
        msg_ba[i] = msg_ba[i] | (1<<7)
    msg_bytes = bytes(msg_ba)
    return msg_bytes


if __name__ == '__main__':

    instances = NewScaleSerial.get_instances()
    print('available controllers (by serial number):')
    for instance in instances:
        print('\t', instance.get_serial_number())
    print('grabbing first available:')
    ser = instances[0]
    print('\tport name = ', ser.get_port_name())
    print('\tserial number = ', ser.get_serial_number())

    print('checking firmware..')
    msg_bytes = b'<01>\r'
    ser.write(setBit7(msg_bytes))
    result = ser.readLine()
    print(result)

