<!-- Developer's Guide > API Developer's Guide > Creating Custom Subassemblies Using .NET > The Subassembly Tool Catalog > Creating a Tool Catalog ATC File > Tool Catalog Data Type Information -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-870042BA-5ED8-4E71-96C8-4A44C97EA5FE.htm -->

# Tool Catalog Data Type Information

The following tables describe the data types that can be used to define the variable that stores parameter values in the corridor modeling tool catalog _.atc_ file. 

Boolean Data TypesData Type | Type String | Description  
---|---|---  
Bool | 0 | 0 = True; 1 = False.  
BoolNoYes | 1 | 0 = Yes; 1 = No.  
BoolDisabledEnabled | 5 | 0 = Enabled; 1 = Disabled.  
BoolOffOn | 6 | 0 = On; 1 = Off.  
BoolRightLeft | 7 | 0 = Right; 1 = Left.  
  
Long Data TypesData Type | Type String | Description  
---|---|---  
Long | 0 | Any integer  
NonZeroLong | 1 | Any non-zero integer  
NonNegativeLong | 2 | Zero or any positive integer  
NonNegativeNonZeroLong | 3 | Any non-zero positive integer  
NonPositiveLong | 4 | Zero or any negative integer  
NonPositiveNonZeroLong | 5 | Any non-zero negative integer  
  
Double Data TypesData Types | Type String | Description  
---|---|---  
Double | 0 | Any double value  
NonNegativeDouble | 1 | Zero or any positive double value  
NonNegativeNonZeroDouble | 2 | Any non-zero positive double value  
NonPositiveDouble | 3 | Zero or any negative double value  
NonPositiveNonZeroDouble | 4 | Any non-zero negative double value  
NonZeroDouble | 5 | Any non-zero double value  
Grade | 8 | Slope or grade input values  
TransparentCmdGrade | 9 | Grade input values  
TransparentCmdSlope | 10 | Slope input values  
Angle | 14 | Angular values  
ConvergenceAngle | 15 | Convergence angular value  
Distance | 16 | Distance values in feet or meters  
Dimension | 17 | Dimension values in inches or millimeters  
Elevation | 21 | Elevation values  
Percent | 25 | Percent values
