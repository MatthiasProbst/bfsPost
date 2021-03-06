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
  VARLIST =  [47]
  LINEARINTERPCONST = 0
  LINEARINTERPMODE = DONTCHANGE
$!EXTENDEDCOMMAND 
  COMMANDPROCESSORID = 'excsv'
  # turbulent case (sparc):
  COMMAND = 'VarNames:FrOp=1:ZnCount=1:ZnList=[5]:VarCount=3:VarList=[1,2,47]:ValSep=",":FNAME="CSVFILENAMEPATH/CSVFILENAME.csv"'
$!RemoveVar |MFBD|


#-----------------------------------------------------------------
#Tecplot variables:
#1	X
#2	Y
#3	Z
#4	Conductivity
#5	Specific Heat
#6	Density
#7	Static Entropy
#8	Shear Strain Rate
#9	Static Enthalpy
#10	X Wall Heat Flux
#11	Y Wall Heat Flux
#12	Z Wall Heat Flux
#13	Volume Porosity
#14	Pressure
#15	Absolute Pressure
#16	Total Pressure
#17	Temperature
#18	Turbulent Kinetic Energy
#19	Aspect Ratio
#20	Courant Number
#21	Volume of Finite Volumes
#22	X Bul Momentum Flow Rate
#23	Y Bild Momentum Flow Rate
#24	Z Bild Momentum Flow Rate
#25	X Pressure.Gradient
#26	Y Pressure.Gradient
#27	Z Pressure.Gradient
#28	X Velocity u.Gradient
#29	Y Velocity u.Gradient
#30	Z Velocity u.Gradient
#31	X Velocity v.Gradient
#32	Y Velocity v.Gradient
#33	Z Velocity v.Gradient
#34	X Velocity w.Gradient
#35	Y Velocity w.Gradient
#36	Z Velocity w.Gradient
#37	X Wall Scale.Gradient
#38	Y Wall Scale.Gradient
#39	Z Wall Scale.Gradient
#40	Mesh Expansion factor
#41	orthogonality Angle
#42	Real Partition Number
#43	Specific Heat Capacity at Constant Volume
#44	Specific Volume
#45	First Blending Funcition for BSL and SST model
#46	Second Blending function for SST model
#47	X Wall Shear
#48	Y Wall Shear
#49	Z Wall Shear
#50	Turbulence Eddy Dissipation
#51	Turbulence Eddy Frequency
#52	Wall Distance
#53	Wall Scale
#54	U
#55	V
#56	W
#57	U
#58	V
#59	W
#60	Dynamic Viscosity
#61	Eddy Viscosity
#62	Y Plus
#63	Solver Y Plus
#64	Node UserID
#65	Element UserId
#66	Material ID
#67	Part ID
#68	Property ID
