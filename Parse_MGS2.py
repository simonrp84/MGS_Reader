from os.path import basename
import numpy as np
import glob


def parser(instr):
    '''
    This function extracts some common parameters from the MGS
    datastring.
    Inputs:
        -   instr: Input string from the MGS2.py reader
    Returns:
        -   lenner: Length of input string
        -   prefix:
        -   lenhi:
        -   lenlo:
        -   client:
        -   namtx:
        -   namrx:
        -   stathi:
        -   statlo:
        -   code:
        -   i: Length of header to skip
    '''
    lenner = len(instr)-(7*2)
    i = 0
    prefix = instr[i:i+2]
    i = i+2
    lenhi = instr[i:i+2]
    i = i+2
    lenlo = instr[i:i+2]
    i = i+2
    client = instr[i:i+2]
    i = i+2
    namtx = instr[i:i+2]
    i = i+2
    namrx = instr[i:i+2]
    i = i+2
    stathi = instr[i:i+2]
    i = i+2
    statlo = instr[i:i+2]
    i = i+2
    code = instr[i:i+2]
    i = i+2

    return lenner, prefix, lenhi, lenlo, client,\
        namtx, namrx, stathi, statlo, code, i


# Set some initial values for reading / writing
indir = '/home/eum/Desktop/MGS_DATA/'
outfile = '/home/eum/Desktop/MGS_OUT_DATA.csv'
outfile2 = '/home/eum/Desktop/MGS_OUT_ENERGY.csv'

# Open files for saving
outf = open(outfile, 'w')
outf2 = open(outfile2, 'w')
outf.write('Time,')


# Find input spectra
files = glob.glob(indir + 'SPEC_*.txt')
files.sort()

# Initialise data arrays. dts stores datetime strings, data_arr stores
# the actual spectra, in 1024 bins. first is used to initialise output later
dts = []
data_arr = np.zeros(1024, dtype=np.int16)
first = True

# Loop over files
for f in files:
    inf = open(f, 'r')
    linecount = 0
    # Loop over lines in file
    for line in inf:
        # Reset data arr
        data_arr[:] = 0
        count = 0
        linecount = linecount + 1
        # Remove guff characters and split by comma
        line = line.strip('\t\n\r')
        data = line.split(',')
        # First section is datetime
        dtstr = data[0][11:11+8]
        # Second is the spectra
        data_m = data[1]

        # Parse data and spectra
        retvals = parser(data_m)
        lenner = retvals[0]
        i = retvals[10]
        outf.write(dtstr+',')
        dts.append(dtstr)
        # Loop over all values in the spectra, we convert hex to int
        for i in range(i, lenner, 4):
            val = int(data_m[i:i + 4], 16)
            data_arr[count] = val
            count = count+1
        # Setup the output
        if (first):
            first = False
            out_arr = data_arr
        else:
            out_arr = np.vstack((out_arr, data_arr))

    print('Finished file ' + basename(f) +
          ' with a total of ' + str(linecount) + ' lines.')

outf.write("\n")

out_arr = np.array(out_arr)
shaper = out_arr.shape
totener = np.zeros((shaper[0]))

if (len(shaper) == 1):
    out_arr = out_arr[None,:]

shaper = out_arr.shape

# Loop over data, compute energy and save to file
for i in range(0, shaper[1]):
    energy = 10 + (i * 2.53)
    outf.write(str(energy) + ',')
    for j in range(0, shaper[0]):
        outf.write(str(out_arr[j, i]) + ',')
        totener[j] += energy * out_arr[j, i]
    outf.write('\n')

# Also save the per-acquisition total energy
for j in range(0, shaper[0]):
    gray = totener[j] * 1.602176634e-19
    outf2.write(dts[j] + ',' + str(totener[j]) + ',' + str(gray) + '\n')

outf.close()
outf2.close()
