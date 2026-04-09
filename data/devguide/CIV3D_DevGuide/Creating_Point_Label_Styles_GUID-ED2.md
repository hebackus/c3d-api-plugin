<!-- Developer's Guide > API Developer's Guide > Points > Point Style > Creating Point Label Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-ED251152-F18E-4582-B31A-EC5B5EFC3958.htm -->

# Creating Point Label Styles

Any text labels or graphical markers displayed at the point location are set by assigning a label style ObjectId to the CogoPoint.LabelStyleId property. The collection of these label styles is accessed through the CivilDocument.Styles.LabelStyles.PointLabelStyles property. 

Point label styles can use the following property fields in the contents of any text components: 

Valid property fields for LabelStyle TextComponent Contents   
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
  
For more general information about creating and using label styles, see the [Label Styles](<GUID-641D7838-292D-43FD-AA50-140B7D9B774F.htm>) section.
