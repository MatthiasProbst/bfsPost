#!MC 1410
$!VarSet |MFBD| = '/home/ws/ht72/Projekte/Forschungsprojekte/BackwardFacingStep2/cfx/100_basic'
$!READDATASET  '"StandardSyntax" "1.0" "FEALoaderVersion" "436" "FILENAME_File" "RESFILEPATH" "AutoAssignStrandIDs" "Yes"'
  DATASETREADER = 'ANSYS CFX (FEA)'
$!CREATERECTANGULARZONE 
  IMAX = 2900
  JMAX = 1
  KMAX = 1
  X1 = 0
  Y1 = 0
  Z1 = 0
  X2 = 2.900
  Y2 = 0
  Z2 = 0
$!RENAMEDATASETZONE ZONE = 6 NAME = 'CSVFILENAME'
$!LINEARINTERPOLATE 
  SOURCEZONES =  [1]
  DESTINATIONZONE = 6
  # cfx-turbulent:
  VARLIST =  [41]
  LINEARINTERPCONST = 0
  LINEARINTERPMODE = DONTCHANGE
$!EXTENDEDCOMMAND 
  COMMANDPROCESSORID = 'excsv'
  # turbulent case (sparc):
  COMMAND = 'VarNames:FrOp=1:ZnCount=1:ZnList=[5]:VarCount=3:VarList=[1,2,41]:ValSep=",":FNAME="CSVFILENAMEPATH/CSVFILENAME.csv"'
$!RemoveVar |MFBD|
