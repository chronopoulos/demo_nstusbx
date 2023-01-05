from serial.tools.list_ports import comports as list_comports
from serial import Serial
from sys import platform as PLATFORM

#if PLATFORM == 'win32':
if True:
    from usbxpress import USBXpressLib, USBXpressDevice

VID_NEWSCALE = 0x10c4
PID_NEWSCALE = 0xea61


class NewScaleSerial():

    """
    Cross-platform abstraction layer for New Scale USB Serial devices
    Usage:
        instances = NewScaleSerial.get_instances()
        -> [newScaleSerial1, newScaleSerial2]
        for instance in instances:
            print('serial number = ', instance.get_serial_number())
    """

    def __init__(self, serial_number, pyserial_device=None, usbxpress_device=None):
        self.sn = serial_number
        if pyserial_device:
            self.t = 'pyserial'
            self.io = pyserial_device
        elif usbxpress_device:
            self.t = 'usbxpress'
            usbxpress_device.open()
            self.io = usbxpress_device
        self.set_timeout(1)
        self.set_baudrate(250000)

    @classmethod
    def get_instances(cls):
        instances = []
        if PLATFORM == 'linux':
            for comport in list_comports():
                if (comport.vid == VID_NEWSCALE):
                    if (comport.pid == PID_NEWSCALE):
                        hwid = comport.hwid
                        serial_number = hwid.split()[2].split('=')[1]
                        instances.append(cls(serial_number,
                                        pyserial_device=Serial(comport.device)))    # does this work?
        elif PLATFORM== 'win32':
            n = USBXpressLib().get_num_devices()
            for i in range(n):
                device = USBXpressDevice(i)
                if (int(device.get_vid(), 16) == VID_NEWSCALE):
                    if (int(device.get_pid(), 16) == PID_NEWSCALE):
                        serial_number = device.get_serial_number()
                        instances.append(cls(serial_number, usbxpress_device=device))   # does this work?
        return instances

    def get_port_name(self):
        if self.t == 'pyserial':
            return self.io.port
        elif self.t == 'usbxpress':
            return 'USBXpress Device'

    def get_serial_number(self):
        return self.sn

    def set_baudrate(self, baudrate):
        if self.t == 'pyserial':
            self.io.baudrate = baudrate
        elif self.t == 'usbxpress':
            self.io.set_baud_rate(baudrate)

    def set_timeout(self, timeout):
        if self.t == 'pyserial':
            self.io.timeout = timeout
        elif self.t == 'usbxpress':
            timeout_ms = int(timeout*1000)
            self.io.set_timeouts(timeout_ms, timeout_ms)

    def write(self, data):
        if self.t == 'pyserial':
            self.io.write(data)
        elif self.t == 'usbxpress':
            self.io.write(data) # branching unnecessary?

    def readLine(self):
        if self.t == 'pyserial':
            data = self.io.read_until(b'\r').decode('utf8')
        elif self.t == 'usbxpress':
            # homebrew read until
            while True:
                print('reading ', debug)
                c = self.io.read(1).decode()
                data += c   # do we include the terminator?
                if (c == '\r'): break
        return data

