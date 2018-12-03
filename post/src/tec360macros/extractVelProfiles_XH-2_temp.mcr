#!MC 1410
$!VarSet |MFBD| = '/home/ws/ht72/Projekte/Forschungsprojekte/BackwardFacingStep2/cfx/100_basic'
$!READDATASET  '"StandardSyntax" "1.0" "FEALoaderVersion" "436" "FILENAME_File" "/home/ws/ht72/Projekte/Forschungsprojekte/BackwardFacingStep2/cfx/500_pocket/test/def_file_001.res" "AutoAssignStrandIDs" "Yes"'
  DATASETREADER = 'ANSYS CFX (FEA)'
$!CREATERECTANGULARZONE 
  IMAX = 1
  JMAX = 100
  KMAX = 1
  X1 = -.050
  Y1 = 0.025
  Z1 = 0
  X2 = -.050
  Y2 = 0.050
  Z2 = 0
$!RENAMEDATASETZONE ZONE = 6 NAME = 'XH-2'
$!LINEARINTERPOLATE 
  SOURCEZONES =  [1]
  DESTINATIONZONE = 6
  VARLIST =  [14,16,41,44-45]
  LINEARINTERPCONST = 0
  LINEARINTERPMODE = DONTCHANGE
$!EXTENDEDCOMMAND 
  COMMANDPROCESSORID = 'excsv'
  # laminar case:
  COMMAND = 'VarNames:FrOp=1:ZnCount=1:ZnList=[6]:VarCount=7:VarList=[1-2,14,16,41,44-45]:ValSep=",":FNAME="/home/ws/ht72/Projekte/Forschungsprojekte/BackwardFacingStep2/cfx/500_pocket/test/post/XH-2.csv"'
$!RemoveVar |MFBD|
