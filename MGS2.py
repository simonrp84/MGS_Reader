from datetime import datetime
import MGS_Func as MSF
import time

outdir = '/home/eum/Desktop/MGS_DATA/'

time_btwn_acq = 60 * 10

# Produce all the codes
sta_acq = [0xAA, 0x00, 0x0A, 0x00, 0x00, 0xA4, 0x00, 0x00, 0x41]
sta_acq = MSF.get_cs(sta_acq)

sto_acq = [0xAA, 0x00, 0x0A, 0x00, 0x00, 0xA4, 0x00, 0x00, 0x42]
sto_acq = MSF.get_cs(sto_acq)

get_sta = [0xAA, 0x00, 0x0A, 0x00, 0x00, 0x01, 0x00, 0x00, 0x0B]
get_sta = MSF.get_cs(get_sta)

clr_spe = [0xAA, 0x00, 0x0A, 0x00, 0x00, 0x01, 0x00, 0x00, 0x40]
clr_spe = MSF.get_cs(clr_spe)

rea_spe = [0xAA, 0x00, 0x0E, 0x00, 0x00, 0x01, 0x00,
           0x00, 0x45, 0x00, 0x00, 0x04, 0x00]
rea_spe = MSF.get_cs(rea_spe)

print('')

while True:

    dtstr = datetime.utcnow().strftime("%Y%m%d")

    outfile_all = outdir + 'MGS__' + dtstr + '.txt'
    outfile_spec = outdir + 'SPEC_' + dtstr + '.txt'

    f = open(outfile_all, 'a+')
    ser = MSF.getserial()
    ser.write(bytearray(sta_acq))
    outstr = ''
    while True:
        tmp = ser.read().hex()
        if (tmp == ""):
            break
        outstr = outstr + tmp
    print(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
          ' Start Acqstn:          ',
          outstr)
    f.write(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") +
            ' Start Acqstn:           ' + outstr + '\n')

    time.sleep(time_btwn_acq)

    ser = MSF.getserial()
    ser.write(bytearray(rea_spe))
    outstr = ''

    while True:
        tmp = ser.read().hex()
        if (tmp == ""):
            break
        outstr = outstr + tmp
    print(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
          ' Read Spectra:          ',
          outstr)

    f2 = open(outfile_spec, 'a+')
    f.write(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") +
            ' Read Spectra:           ' +
            outstr + '\n')
    f2.write(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") +
             ',' + outstr + '\n')
    f2.close()

    ser = MSF.getserial()
    ser.write(bytearray(clr_spe))
    outstr = ''

    while True:
        tmp = ser.read().hex()
        if (tmp == ""):
            break
        outstr = outstr + tmp
    print(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
          ' Clr Spctr:         ',
          outstr)
    f.write(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") +
            ' Clr Spctr:          ' +
            outstr + '\n')
    f.close()
