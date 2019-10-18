import serial
import serial.tools.list_ports


def get_cs(code):
    summer = sum(code)
    while(summer > 256):
        summer = summer-256
    cs = 256 - summer
    code = code + [cs]
    return code


def getserial():
    ser_list = list(serial.tools.list_ports.comports())
    port = ''
    for serp in ser_list:
        nam = serp[0]
        pos = nam.find('/dev/ttyUSB')
        if (pos < 0):
            continue
        if (serp[2][0:34] == 'USB VID:PID=0403:6015 SER=13150179'):
            port = nam
        if (serp[2] == 'MGS 500mm3'):
            port = nam
    if (port == ''):
        print("Error, no device found!")
        for item in ser_list:
            print(item[0],item[1],item[2])
        quit()
    ser = serial.Serial(port=port,
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=0.5)
    ser.close()
    ser.open()
    return ser


def sort_status(outstr, printer=True):
    # Return status
    starter = 0
    if (printer):
        print('STAT',)
        for i in range(starter, starter+9*2, 2):
            print(outstr[i:i+2],)
        print('')

    # ID Unused
    starter = starter + 9 * 2
    if (printer):
        print('IDVA',)
        for i in range(starter, starter+3*2, 2):
            print(outstr[i:i+2],)
        print('')

    # Dose start
    starter = starter + 3 * 2
    dose = outstr[starter:starter+4]

    # Unused
    starter = starter + 4
    if (printer):
        print('UNUS',)
        for i in range(starter, starter+8*2, 2):
            print(outstr[i:i+2],)
        print('')

    # Bat Volt
    starter = starter + 8 * 2
    if (printer):
        print('BATV',)
        for i in range(starter, starter+2*2, 2):
            print(outstr[i:i+2],)
        print('')

    # Dose end
    starter = starter + 2 * 2
    dose = dose + outstr[starter:starter+4]
    if (printer):
        print('DOSE',)
        print(dose)

    # Unused
    starter = starter + 4
    if (printer):
        print('UNUS',)
        for i in range(starter, starter+2*2, 2):
            print(outstr[i:i+2],)
        print('')

    # HiV Voltage
    starter = starter + 2 * 2
    if (printer):
        print('HIVV',)
        for i in range(starter, starter+2*2, 2):
            print(outstr[i:i+2],)
        print('')

    # Count rate
    starter = starter + 2 * 2
    count = outstr[starter:starter+8]
    if (printer):
        print('COUN',)
        print(count)

    # Unused
    starter = starter + 4 * 2
    if (printer):
        print('UNUS',)
        for i in range(starter, starter+7*2, 2):
            print(outstr[i:i+2],)
        print('')

    # Checksum
    starter = starter + 7 * 2
    cs = outstr[starter:starter+2]
    if (printer):
        print('CHSM', cs)

    return dose, count, cs
