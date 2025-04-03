from datetime import date
from datetime import datetime
import math as math
import os
from SeqInfo import getSeqList

# ============================= HYPER PARAMETERS =============================

startBat = 0            # When startBat = 3, It goes like 4, 5, 6, 7, ...
method = 'VTM16Enc'    # Name of the executable file
ORIorPRO = True        # True: Codec is not modified. False: Codec is modified, and you have to give additional arguments (-miW, -miH)
config = 'RA16_FS'           # RA, AI, LDP, LDB (LDB, LDB_IBC, LDB_SB, LDB_IBC_SB)
Raw_or_Sq = True        # True: Hexagonal Raw Lenslet, False: Squarred Lenslet
seqIndex = [3,6,8,9,12,14] # Choose the index of the video you want to encode (refer to 'SeqList'.)
numFrame = 33          # How many frames to encode?
numBat = 12              # How many .bat files to create? (When numDivQPset == 2, numBat should not exceed length of seqIndex list.)
genRecon = False        # Generate reconstructed video or not?
inputPath = 'D:\LensletSeq\\'
recPath  = 'D:\LensletSeq_Sq_Rec' 
binPath  = 'Results'
logPath = 'Results'
setLevel = True         # Specify the level value for the sequence, or not? (IF YOU STRICTLY FOLLOW LVC CTC, THEN SET "False"!!!)
valLevel = 6.2          # The maximum list of the reference picture list can vary depending on its value.
qpSetOption = 2     # 0: Use the QP set described in CTC. 1: [22, 27, 32, 37]. 2: [24, 30, 36, 42]. 3: [36, 40, 44, 48]
Allocation  = True      # Thread Allocation. For accurate time complexity measurement, please set it as True.
numDivQPset = 2         # 1->[Q1, Q2, Q3, Q4], 2->[Q1, Q2], [Q3, Q4] WARNING: Use only 1, 2.
StartThread = 0         # When allocating the thread, you can choose from which number to start.
dirDateTime = True     # If True, you create the directory named as the current date and time. Otherwise, you directly run the commands.
standBy     = False     # To precisely measure the time, let the encoder or decoder run after certain amount of time.
standByTime = 1      # How much seconds to wait?


# ======================= Write Main batch file =======================

SeqList = getSeqList(Raw_or_Sq, numFrame, qpSetOption, setLevel, valLevel)
num = max(1, math.ceil(len(seqIndex) / (numBat/numDivQPset)))
SeqChunks = [seqIndex[i:min(i+num,len(seqIndex))] for i in range(0, len(seqIndex), num)]

today = date.today()
d1 = today.strftime("%Y-%m-%d")
time_now = datetime.now()
current_time = time_now.strftime("%H-%M-%S")
dateTime = d1  + '_' + current_time

if dirDateTime == True:
    Path = 'Enc_Script_' + dateTime +'/'
    if os.path.exists(Path) == False:
        os.mkdir(Path)
else:
    Path = ''

for bidx in range(0, numBat, numDivQPset): # When numDivQPset = 2, bidx goes like 0, 2, 4, 6...

    BatChunk = SeqChunks[int(bidx/numDivQPset)]

    myBat = open(Path + f'ENC_main{startBat+bidx+1}.bat','w+')
    myBat.write('ECHO OFF\n')
    if (standBy):
        myBat.write(f'ECHO Standby for {standByTime} seconds...\n')
        myBat.write(f'TIMEOUT /T {standByTime}\n')
    myBat.write(f'SET CFG={config}\n')
    myBat.write('ECHO ###############################################\n\n')

    myBat2 = 0
    if numDivQPset % 2 == 0:
        myBat2 = open(Path + f'ENC_main{startBat+bidx+2}.bat','w+')
        myBat2.write('ECHO OFF\n')
        if (standBy):
            myBat2.write(f'ECHO Standby for {standByTime} seconds...\n')
            myBat2.write(f'TIMEOUT /T {standByTime}\n')
        myBat2.write(f'SET CFG={config}\n')
        myBat2.write('ECHO ###############################################\n\n')

    # REM CALL ENC_sub.bat %CFG% Experimenting 2112 1344 30 300 32 22 32
    for sidx in BatChunk:
        seqC = SeqList[sidx]

        if numDivQPset % 2 == 0:
            newQpSet = [seqC.qpSet[i] for i in [0, 1, 3, 2]]
            seqC.qpSet = newQpSet

        for qidx in range(0, len(seqC.qpSet), numDivQPset):
            myBat.write(f'CALL ENC_sub.bat %CFG% {seqC.seqName} {seqC.wdt} {seqC.hgt} {seqC.isKepGal} ')
            if Raw_or_Sq == True:
                myBat.write(f'{seqC.numFrame} {seqC.intraPeriod} {seqC.qpSet[qidx]}\n')
            elif Raw_or_Sq == False:
                myBat.write(f'{seqC.numFrame} {seqC.intraPeriod} {seqC.qpSet[qidx]} {seqC.sizeSq}\n')
            
            if numDivQPset % 2 == 0:
                myBat2.write(f'CALL ENC_sub.bat %CFG% {seqC.seqName} {seqC.wdt} {seqC.hgt} {seqC.isKepGal} ')
                if Raw_or_Sq == True:
                    myBat2.write(f'{seqC.numFrame} {seqC.intraPeriod} {seqC.qpSet[qidx+1]}\n')
                elif Raw_or_Sq == False:
                    myBat2.write(f'{seqC.numFrame} {seqC.intraPeriod} {seqC.qpSet[qidx+1]} {seqC.sizeSq}\n')

    myBat.close()
    if numDivQPset % 2 == 0:
        myBat2.close()

# ======================= Write sub batch file =======================
myBatEs = open(f'{Path}ENC_sub.bat','w+')
myBatEs.write('ECHO OFF\n\nREM ################################################\n')
myBatEs.write('SET CFG=%1\nSET SEQ_NAME=%2 \nSET WIDTH=%3 \nSET HEIGHT=%4\n')
myBatEs.write('SET IS_KEP_GAL=%5\nSET FRM_NUM=%6\n')
myBatEs.write('if %CFG%==AI (SET INTRA_PERIOD=1) else (if %CFG%==LDB (SET INTRA_PERIOD=-1) else (if %CFG%==LDP (SET INTRA_PERIOD=-1) else (SET INTRA_PERIOD=%7)))\n')
myBatEs.write('SET QP=%8\n')
if Raw_or_Sq == False:
    myBatEs.write('SET SQ=%9\n')
myBatEs.write('REM ################################################\n')

myBatEs.write('REM ##### SET VARIABLE #############################\n')
if Raw_or_Sq == True:
    myBatEs.write('SET IN_NAME=%2_%3x%4_30fps_8bit\nSET OUT_NAME=%1_%2_%3x%4_30fps_QP%8\n')
else:
    myBatEs.write('SET IN_NAME=%2_%3x%4_30fps_8bit_sq%9\nSET OUT_NAME=%1_%2_%3x%4_30fps_QP%8_sq%9\n')
myBatEs.write('SET METHOD=' + method + '\n')
myBatEs.write('REM ################################################\n\n')

myBatEs.write('ECHO ###############################################\n')
myBatEs.write('ECHO Encoding: %METHOD%_%OUT_NAME%\n')
myBatEs.write('ECHO -----------------------------------------------\n\n')

myBatEs.write(f'%METHOD%.exe -c %CFG%.cfg -i %IN_NAME%.yuv -b %METHOD%_%OUT_NAME%.bin ')
if setLevel == True:
    myBatEs.write(f'--Level={valLevel} ')

if genRecon == True:
    myBatEs.write(f'--ReconFile=%METHOD%_%OUT_NAME%.yuv ')
else:
    myBatEs.write('--ReconFile= ')

if ORIorPRO == False:
    myBatEs.write('-KG %IS_KEP_GAL% -miW %SQ%  -miH %SQ% ')

myBatEs.write('-wdt %WIDTH% -hgt %HEIGHT% -fr 30 -f %FRM_NUM% ')
myBatEs.write('-ip %INTRA_PERIOD% -q %QP% ')

myBatEs.write('-dph 1 -v 6 > %METHOD%_%OUT_NAME%.txt\n\n')

myBatEs.write(f'move %METHOD%_%OUT_NAME%.bin {binPath}\n')

if genRecon == True:
    myBatEs.write(f'move %METHOD%_%OUT_NAME%.yuv {recPath}\n')   
myBatEs.write(f'move %METHOD%_%OUT_NAME%.txt {logPath}\n')

myBatEs.write('ECHO -----------------------------------------------\n')
myBatEs.write('ECHO Terminated Encoding...\n')
myBatEs.write('ECHO ###############################################\n')
myBatEs.close()

if os.path.isdir(Path + f'{logPath}/') == False:
    os.mkdir(Path + f'{logPath}/')
if os.path.isdir(Path + f'{binPath}/') == False:
    os.mkdir(Path + f'{binPath}/')

Alloc_Commands = [
    "start /affinity 1   ",
    "start /affinity 10  ",
    "start /affinity 100 ",
    "start /affinity 2   ",
    "start /affinity 20  ",
    "start /affinity 200 ",
    "start /affinity 4   ",
    "start /affinity 40  ",
    "start /affinity 400 ",
    "start /affinity 8   ",
    "start /affinity 80  ",
    "start /affinity 800 ",
]


myBatEs = open(f'{Path}ENC_Alloc.bat','w+')


# Copy sequences from D to C.
for sidx in seqIndex:
    seqC = SeqList[sidx]
    if Raw_or_Sq == True:
        myBatEs.write(f'copy {inputPath}{seqC.seqName}_{seqC.wdt}x{seqC.hgt}_{seqC.frameRate}fps_8bit.yuv %cd%\n')
    elif Raw_or_Sq == False:
        myBatEs.write(f'copy {inputPath}{seqC.seqName}_{seqC.wdt}x{seqC.hgt}_{seqC.frameRate}fps_8bit_sq{seqC.sizeSq}.yuv %cd%\n')
myBatEs.write('\n')

# Thread Allocation
for bidx in range (numBat):
    Command = f'ENC_main{startBat+bidx+1}.bat\n'
    if Allocation == True:
        Command = Alloc_Commands[StartThread + bidx] + Command
    myBatEs.write(Command)
    myBatEs.write("timeout /t 1 /nobreak\n")
    myBatEs.write('\n')
'''
if numDivQPset % 2 == 1: # 1
    for bidx in range (numBat):
        Command = f'ENC_main{startBat+bidx+1}.bat\n'
        if Allocation == True:
            Command = Alloc_Commands[StartThread + bidx] + Command
        myBatEs.write(Command)
        myBatEs.write("timeout /t 1 /nobreak\n")
    myBatEs.write('\n')

elif numDivQPset % 2 == 0: # 2
    for bidx in range (0, numBat, 2):
        Command  = f'ENC_main{startBat+bidx+1}.bat\n'
        Command2 = f'ENC_main{startBat+bidx+2}.bat\n'
        if Allocation == True:
            Command  = Alloc_Commands[StartThread + bidx]     + Command
            Command2 = Alloc_Commands[StartThread + bidx + 1] + Command2
        myBatEs.write(Command)
        myBatEs2.write(Command2)
        myBatEs.write("timeout /t 1 /nobreak\n")
        myBatEs2.write("timeout /t 1 /nobreak\n")
    myBatEs.write('\n')
    myBatEs2.write('\n')

'''

# Delete remaining sequences.
for sidx in seqIndex:
    seqC = SeqList[sidx]
    if Raw_or_Sq == True:
        myBatEs.write(f'del {seqC.seqName}_{seqC.wdt}x{seqC.hgt}_{seqC.frameRate}fps_8bit.yuv\n')
    elif Raw_or_Sq == False:
        myBatEs.write(f'del {seqC.seqName}_{seqC.wdt}x{seqC.hgt}_{seqC.frameRate}fps_8bit_sq{seqC.sizeSq}.yuv\n')

'''
if numDivQPset % 2 == 0:
    for sidx in seqIndex:
        seqC = SeqList[sidx]
        if Raw_or_Sq == True:
            myBatEs2.write(f'del {seqC.seqName}_{seqC.wdt}x{seqC.hgt}_{seqC.frameRate}fps_8bit.yuv\n')
        elif Raw_or_Sq == False:
            myBatEs2.write(f'del {seqC.seqName}_{seqC.wdt}x{seqC.hgt}_{seqC.frameRate}fps_8bit_sq{seqC.sizeSq}.yuv\n')
   ''' 

myBatEs.close()
