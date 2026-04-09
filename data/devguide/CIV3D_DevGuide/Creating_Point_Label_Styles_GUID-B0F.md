<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Points in COM > Style > Creating Point Label Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-B0F8C51F-BF84-4D2A-A60F-ECB55B3CBF3F.htm -->

# Creating Point Label Styles

Any text labels or graphical markers displayed at the point location are set by assigning a label style object to the AeccPoint.LabelStyle property. The collection of these label styles is accessed through the AeccDocument.PointLabelStyle property. 

Point label styles can use the following property fields in the contents of any text components:

Valid property fields for AeccLabelStyleTextComponent.Contents  
---  
<[Name(CP)]>  
<[Point Number]>  
<[Northing(Uft|P4|RN|AP|Sn|OF)]>  
<[Easting(Uft|P4|RN|AP|Sn|OF)]>  
<[Raw Description(CP)]>  
<[Full Description(CP)]>  
<[Point Elevation(Uft|P3|RN|AP|Sn|OF)]>  
<[Latitude(Udeg|FDMSdSp|P6|RN|DPSn|CU|AP|OF)]>  
<[Longitude(Udeg|FDMSdSp|P6|RN|DPSn|CU|AP|OF)]>  
<[Grid Northing(Uft|P4|RN|AP|Sn|OF)]>  
<[Grid Easting(Uft|P4|RN|AP|Sn|OF)]>  
<[Scale Factor(P3|RN|AP|OF)]>  
<[Convergence(Udeg|FDMSdSp|P6|RN|AP|OF)]>  
<[Survey Point]>  
  
Label styles are described in detail in the chapter 1 section [Label Styles](<GUID-CB057BA7-7EAE-4915-9B90-8451776C1407.htm>).
