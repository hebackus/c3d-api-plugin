<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Pipe Networks in COM > Pipes > Creating Pipe Label Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-A07154E4-D5EF-4CEA-8F5A-437B2E16D4AB.htm -->

# Creating Pipe Label Styles

The collection of all pipe label styles in a document is found in the AeccPipeDatabase.PipeNetworkLabelStyles.PipeLabelStyles property, which is a standard AeccLabelStyles object. For more information, see [Label Styles](<GUID-CB057BA7-7EAE-4915-9B90-8451776C1407.htm>). 

Note:

The label style of a particular pipe cannot be set using the API.

Pipe label styles can use the following property fields in the contents of any text component. 

Valid property fields for AeccLabelStyleTextComponent.Contents in pipes  
---  
<[Cross Sectional Shape(CP)]>  
<[Wall Thickness(Uin|P3|RN|AP|Sn|OF)]>  
<[Material(CP)]>  
<[Minimum Curve Radius(Uft|P3|RN|AP|Sn|OF)]>  
<[Manning Coefficient(P3|RN|AP|Sn|OF)]>  
<[Hazen Williams Coefficient(P3|RN|AP|Sn|OF)]>  
<[Darcy Weisbach Factor(P3|RN|AP|Sn|OF)]>  
<[Inner Pipe Diameter(Uin|P3|RN|AP|Sn|OF)]>  
<[Inner Pipe Width(Uin|P3|RN|AP|Sn|OF)]>  
<[Inner Pipe Height(Uin|P3|RN|AP|Sn|OF)]>  
<[Name(CP)]>  
<[Description(CP)]>  
<[Network Name(CP)]>  
<[Reference Alignment Name(CP)]>  
<[Pipe Start Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[Start Offset(Uft|P3|RN|AP|Sn|OF)]>  
<[Start Offset Side(CP)]>  
<[Pipe End Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[End Offset Side(Uft|P3|RN|AP|Sn|OF)]>  
<[End Offset(CP)]>  
<[Reference Surface Name(CP)]>  
<[Pipe Slope(FP|P2|RN|AP|Sn|OF)]>  
<[Pipe Start Structure(CP)]>  
<[Pipe Start Northing(Uft|P4|RN|AP|Sn|OF)]>  
<[Pipe Start Easting(Uft|P4|RN|AP|Sn|OF)]>  
<[Start Invert Elevation(Uft|P3|RN|AP|Sn|OF)]>  
<[Start Centerline Elevation(Uft|P3|RN|AP|Sn|OF)]>  
<[Start Crown Elevation(Uft|P3|RN|AP|Sn|OF)]>  
<[Pipe End Structure(CP)]>  
<[Pipe End Northing(Uft|P4|RN|AP|Sn|OF)]>  
<[Pipe End Easting(Uft|P4|RN|AP|Sn|OF)]>  
<[End Invert Elevation(Uft|P3|RN|AP|Sn|OF)]>  
<[End Centerline Elevation(Uft|P3|RN|AP|Sn|OF)]>  
<[End Crown Elevation(Uft|P3|RN|AP|Sn|OF)]>  
<[2D Length - Center to Center(Uft|P3|RN|AP|Sn|OF)]>  
<[3D Length - Center to Center(Uft|P3|RN|AP|Sn|OF)]>  
<[2D Length - To Inside Edges(Uft|P3|RN|AP|Sn|OF)]>  
<[3D Length - To Inside Edges(Uft|P3|RN|AP|Sn|OF)]>  
<[Pipe Bearing(Udeg|FDMSdSp|MB|P6|RN|DSn|CU|AP|OF)]>  
<[Pipe Start Direction in plan(Udeg|FDMSdSp|MB|P6|RN|DSn|CU|AP|OF)]>  
<[Pipe End Direction in plan(Udeg|FDMSdSp|MB|P6|RN|DSn|CU|AP|OF)]>  
<[Pipe Radius(Uft|P3|RN|AP|Sn|OF)]>  
<[Pipe Chord Length(Uft|P3|RN|AP|Sn|OF)]>  
<[Radius Point Northing(Uft|P4|RN|AP|Sn|OF)]>  
<[Radius Point Easting(Uft|P4|RN|AP|Sn|OF)]>  
<[Minimum Cover(Uft|P3|RN|AP|Sn|OF)]>  
<[Maximum Cover(Uft|P3|RN|AP|Sn|OF)]>  
<[Pipe Outer Diameter or Width(Uin|P3|RN|AP|Sn|OF)]>  
<[Pipe Inner Diameter or Width(Uin|P3|RN|AP|Sn|OF)]>  
<[Drop Across Span(Uft|P3|RN|AP|Sn|OF)]>  
<[Total Slope Across Span(FP|P2|RN|AP|Sn|OF)]>  
<[Number of Pipes in Span(Sn)]>
