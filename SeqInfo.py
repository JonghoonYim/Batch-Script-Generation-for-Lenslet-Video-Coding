class SeqInfo():
    def __init__(self, seqName,  Raw_or_Sq, camType, sizeSq, numFrame, qpSetOption, qpSet, setLevel, valLevel, isKepGal):
        self.seqName     = seqName
        self.numLLx      =  70 if camType == 'R8'     else 100 if camType == 'R5'     else  66 if camType == 'THU'      else None
        self.numLLy      = 108 if camType == 'R8'     else  86 if camType == 'R5'     else  42 if camType == 'THU'      else None
        self.sizeSq      = sizeSq
        self.wdt         = self.sizeSq * self.numLLx if Raw_or_Sq == False     else 3840 if camType == 'R8'    else 2048 if camType == 'R5'    else  4080 if camType == 'THU'   else None
        self.hgt         = self.sizeSq * self.numLLy if Raw_or_Sq == False     else 2160 if camType == 'R8'    else 2048 if camType == 'R5'    else  3068 if camType == 'THU'   else None
        self.frameRate   = 30
        self.numFrame    = numFrame
        self.intraPeriod = 32
        self.qpSet       = qpSet if qpSetOption == 0    else [22, 27, 32, 37] if qpSetOption == 1       else [24, 30, 36, 42] if qpSetOption == 2       else [36, 40, 44, 48] # if qpSetOption == 3
        self.valLevel    = valLevel if setLevel         else None
        self.isKepGal    = isKepGal



# ============== Sequence List (DO NOT MODIFY THIS BLOCK) =================
# Refer to the EE and CTC document below: 
# MDS23560_WG04_N0456, Description of exploration experiments on lenslet video coding, ISO/IEC JTC1/SC29/WG04, Online, January 2024.
# There are 15 Plenoptic 2.0 sequeneces in total.
# Argument Rule: (seqName,  Raw_or_Sq, camType, sizeSq, numFrame, qpSetOption, qpSet, setLevel, valLevel)

def getSeqList(Raw_or_Sq, numFrame, qpSetOption, setLevel, valLevel):
    SeqList = [
        # [00 ~ 02] Previous Raytrix R8 sequences
        SeqInfo("Boxer_IrishMan_Gladiator", # 00
                Raw_or_Sq, camType='R8', sizeSq=24, 
                numFrame=numFrame, 
                qpSetOption=qpSetOption, qpSet=[33, 40, 45, 49], 
                setLevel=setLevel, valLevel=valLevel, isKepGal=1),   

        SeqInfo("ChessPieces",              # 01
                Raw_or_Sq, camType='R8', sizeSq=24, 
                numFrame=numFrame, 
                qpSetOption=qpSetOption, qpSet=[37, 41, 45, 49], 
                setLevel=setLevel, valLevel=valLevel, isKepGal=1),   

        SeqInfo("ChessPieces_MovingCamera", # 02
                Raw_or_Sq, camType='R8', sizeSq=24, 
                numFrame=numFrame, 
                qpSetOption=qpSetOption, qpSet=[37, 41, 45, 49], 
                setLevel=setLevel, valLevel=valLevel, isKepGal=1),

        # [03 ~ 06] Raytrix R8 sequences by ULB-SKKU
        SeqInfo("UnicornLinearCam",         # 03
                Raw_or_Sq, camType='R8', sizeSq=24, 
                numFrame=numFrame, 
                qpSetOption=qpSetOption, qpSet=[33, 39, 45, 50], 
                setLevel=setLevel, valLevel=valLevel, isKepGal=1),

        SeqInfo("ComplexObjectMove",        # 04
                Raw_or_Sq, camType='R8', sizeSq=24, 
                numFrame=numFrame, 
                qpSetOption=qpSetOption, qpSet=[37, 41, 46, 51], 
                setLevel=setLevel, valLevel=valLevel, isKepGal=1),

        SeqInfo("ComplexObjectMoveLinearCam", # 05
                Raw_or_Sq, camType='R8', sizeSq=24, 
                numFrame=numFrame, 
                qpSetOption=qpSetOption, qpSet=[33, 39, 45, 51], 
                setLevel=setLevel, valLevel=valLevel, isKepGal=1),
        
        SeqInfo("ComplexObjectMoveRandomCam", # 06
                Raw_or_Sq, camType='R8', sizeSq=24, 
                numFrame=numFrame, 
                qpSetOption=qpSetOption, qpSet=[33, 39, 45, 50], 
                setLevel=setLevel, valLevel=valLevel, isKepGal=1),
                
        # [07 ~ 10] Raytrix R5 sequences by Nagoya
        SeqInfo("NagoyaDataleading",        # 07
                Raw_or_Sq, camType='R5', sizeSq=16, 
                numFrame=numFrame, 
                qpSetOption=qpSetOption, qpSet=[38, 43, 49, 51], 
                setLevel=setLevel, valLevel=valLevel, isKepGal=1),

        SeqInfo("NagoyaFujita",             # 08
                Raw_or_Sq, camType='R5', sizeSq=16, 
                numFrame=numFrame, 
                qpSetOption=qpSetOption, qpSet=[36, 40, 45, 49], 
                setLevel=setLevel, valLevel=valLevel, isKepGal=1),

        SeqInfo("NagoyaOrigami",            # 09
                Raw_or_Sq, camType='R5', sizeSq=16, 
                numFrame=numFrame, 
                qpSetOption=qpSetOption, qpSet=[36, 40, 45, 49], 
                setLevel=setLevel, valLevel=valLevel, isKepGal=1),
        
        SeqInfo("NagoyaTunnel_Train_2c",    # 10
                Raw_or_Sq, camType='R5', sizeSq=16, 
                numFrame=numFrame, 
                qpSetOption=qpSetOption, qpSet=[36, 40, 45, 49], 
                setLevel=setLevel, valLevel=valLevel, isKepGal=1),
                
        # [11 ~ 14] Single-focused sequences by Tsinghua University Group
        SeqInfo("Boys",                     # 11
                Raw_or_Sq, camType='THU', sizeSq=48, # 48!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
                numFrame=numFrame, 
                qpSetOption=qpSetOption, qpSet=[36, 40, 45, 49], 
                setLevel=setLevel, valLevel=valLevel, isKepGal=0),
                
        SeqInfo("Cars",                     # 12
                Raw_or_Sq, camType='THU', sizeSq=48, # 48!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
                numFrame=numFrame, 
                qpSetOption=qpSetOption, qpSet=[36, 40, 45, 49], 
                setLevel=setLevel, valLevel=valLevel, isKepGal=0),

        SeqInfo("Experimenting",            # 13
                Raw_or_Sq, camType='THU', sizeSq=48, # 48!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
                numFrame=numFrame, 
                qpSetOption=qpSetOption, qpSet=[36, 40, 45, 49], 
                setLevel=setLevel, valLevel=valLevel, isKepGal=0),
                
        SeqInfo("Matryoshka",               # 14
                Raw_or_Sq, camType='THU', sizeSq=48, # 48!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
                numFrame=numFrame, 
                qpSetOption=qpSetOption, qpSet=[36, 40, 45, 49],
                setLevel=setLevel, valLevel=valLevel, isKepGal=0)
    ]
    return SeqList
