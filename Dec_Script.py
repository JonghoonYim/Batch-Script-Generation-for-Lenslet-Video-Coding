from datetime import date
from datetime import datetime
import math as math
import os
from SeqInfo import getSeqList

# ============================= HYPER PARAMETERS =============================
startBat = 0            # When startBat = 3, It goes like 4, 5, 6, 7, ...
method_e = 'VTM11Enc'  # Name of the executable file
method_d = 'VTM11Dec'  # Name of the executable file
config = 'RA'           # RA, AI, LDP, LDB
Raw_or_Sq = False        # True: Hexagonal Raw Lenslet, False: Squarred Lenslet
seqIndex = [9, 11, 14] # Choose the index of the video you want to decode (refer to 'SeqList'.)
numFrame = 300          # How many frames to encode? (For decoder implementation, not necessary, but to bring SeqList, we need it.)
numBat = 3              # How many .bat files to create?
binPath  = 'bin/'
printDecLog = False
logPath = 'Log_Dec'
decPath  = 'D:\LensletSeq_Sq_Dec'
setLevel = True        # Specify the level value for the sequence, or not? (IF YOU STRICTLY FOLLOW LVC CTC, THEN SET "False"!!!) (To bring SeqList, we need it.)
valLevel = 6.2          # The maximum list of the reference picture list can vary depending on its value. (To bring SeqList, we need it.)
qpSetOption = 2     # 0: Use the QP set described in CTC. 1: [22, 27, 32, 37]. 2: [24, 30, 36, 42]. 3: [36, 40, 44, 48]
Allocation  = True      # Thread Allocation. For accurate time complexity measurement, please set it as True.
StartThread = 0         # When allocating the thread, you can choose from which number to start.
dirDateTime = True     # If True, you create the directory named as the current date and time. Otherwise, you directly run the commands.
standBy     = False     # To precisely measure the time, let the encoder or decoder run after certain amount of time.
standByTime = 1        # How much seconds to wait?

# ======================= Write Main batch file =======================
SeqList = getSeqList(Raw_or_Sq, numFrame, qpSetOption, setLevel, valLevel)
numBat = min(len(seqIndex), numBat)
num = max(1, math.ceil(len(seqIndex)/numBat))
SeqChunks = [seqIndex[i:min(i+num,len(seqIndex))] for i in range(0, len(seqIndex), num)]

today = date.today()
d1 = today.strftime("%Y-%m-%d")
time_now = datetime.now()
current_time = time_now.strftime("%H-%M-%S")
dateTime = d1  + '_' + current_time

if dirDateTime == True:
    Path = 'Dec_Script_' + dateTime + '/'
    if os.path.exists(Path) == False:
        os.mkdir(Path)
else: 
    Path = ''

for bidx in range(numBat):

    BatChunk = SeqChunks[bidx]

    myBat = open(Path + f'DEC_main{bidx+1}.bat','w+')
    myBat.write('ECHO OFF\n')
    if standBy:
        myBat.write('ECHO Standby for 10 seconds...\n')
        myBat.write(f'TIMEOUT /T {standByTime}\n')
    myBat.write(f'SET CFG={config}\n')
    myBat.write('ECHO ###############################################\n')
    myBat.write('ECHO Decoding Videos...\n')
    myBat.write('ECHO ###############################################\n\n')

    for sidx in BatChunk:
        seqC = SeqList[sidx]
        for qidx in range(len(seqC.qpSet)):
            myBat.write(f'CALL DEC_sub.bat %CFG% {seqC.seqName} {seqC.wdt} {seqC.hgt} {seqC.frameRate} ')
            myBat.write(f'{seqC.numFrame} {seqC.intraPeriod} {seqC.qpSet[qidx]} {seqC.sizeSq}\n')
        myBat.write('\n')

    myBat.close()  

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

    # Thread Allocation
    myBatDs = open(f'{Path}DEC_Alloc.bat','w+')
    for bidx in range (numBat):
        Command = f'DEC_main{startBat+bidx+1}.bat\n'
        if Allocation == True:
            Command = Alloc_Commands[StartThread + bidx] + Command
        myBatDs.write(Command)
        myBatDs.write("timeout /t 1 /nobreak\n")
        myBatDs.write('\n')
    myBatDs.close()

# ======================= Write sub batch file =======================
myBatDs = open(f'{Path}DEC_sub.bat','w+')
myBatDs.write('ECHO OFF\n\nREM ################################################\n')
myBatDs.write('SET CFG=%1\nSET SEQ_NAME=%2\nSET WIDTH=%3\nSET HEIGHT=%4\n')
myBatDs.write('SET FRM_RATE=%5\nSET FRM_NUM=%6\n')
# myBatDs.write('if %CFG%==AI (SET INTRA_PERIOD=1) else (SET INTRA_PERIOD=%7)\n')
myBatDs.write('SET QP=%8\nSET SQ=%9\n')
myBatDs.write('REM ################################################\n')

myBatDs.write('REM ##### SET VARIABLE #############################\n')
if Raw_or_Sq == True:
    myBatDs.write('SET OUT_NAME=%CFG%_%SEQ_NAME%_%WIDTH%x%HEIGHT%_%FRM_RATE%fps_QP%QP%\n')
else:
    myBatDs.write('SET OUT_NAME=%CFG%_%SEQ_NAME%_%WIDTH%x%HEIGHT%_%FRM_RATE%fps_QP%QP%_sq%SQ%\n')
myBatDs.write('SET METHOD_D=' + method_d + '\n')
myBatDs.write('SET METHOD_E=' + method_e + '\n')
myBatDs.write('REM ################################################\n\n')

myBatDs.write('ECHO ###############################################\n')
myBatDs.write('ECHO Decoding: %METHOD_E%_%OUT_NAME%\n')
myBatDs.write('ECHO -----------------------------------------------\n\n')

myBatDs.write(f'%METHOD_D%.exe -b {binPath}%METHOD_E%_%OUT_NAME%.bin ')

myBatDs.write(f'-o %METHOD_D%_%OUT_NAME%.yuv ')
if printDecLog:
    myBatDs.write('> %METHOD_D%_%OUT_NAME%.txt\n\n')
myBatDs.write('\n')
myBatDs.write(f'move %METHOD_D%_%OUT_NAME%.yuv {decPath}\n')

if printDecLog:
    myBatDs.write(f'move %METHOD_D%_%OUT_NAME%.txt Log_Dec\n')

myBatDs.write('ECHO -----------------------------------------------\n')
myBatDs.write('ECHO Terminated Decoding...\n')
myBatDs.write('ECHO ###############################################\n')
myBatDs.close()

if (os.path.isdir(Path + f'{logPath}/') == False) & (printDecLog == True):
    os.mkdir(Path + f'{logPath}')

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

if dirDateTime == False:
    for bidx in range (numBat):
        Command = Path + f'DEC_main{bidx+1}.bat'
        if Allocation == True:
            Command = Alloc_Commands[bidx] + Command
        os.system(Command)
