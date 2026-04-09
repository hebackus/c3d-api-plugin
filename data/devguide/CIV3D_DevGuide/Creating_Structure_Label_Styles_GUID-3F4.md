<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Pipe Networks in COM > Structures > Creating Structure Label Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-3F47B9EB-981B-4684-9C7C-A84DAF80E32B.htm -->

# Creating Structure Label Styles

The collection of all structure label styles in a document is found in the AeccPipeDatabase.PipeNetworkLabelStyles.StructureLabelStyles property, which is a standard AeccLabelStyles object. For more information, see [Label Styles](<GUID-CB057BA7-7EAE-4915-9B90-8451776C1407.htm>). 

Note:

The label style of a particular structure cannot be set using the API.

Structure label styles can use the following property fields in the contents of any text component: 

Valid property fields for AeccLabelStyleTextComponent.Contents in structures  
---  
<[Name(CP)]>  
<[Description(CP)]>  
<[Network Name(CP)]>  
<[Structure Rotation Angle(Udeg|FD|P4|RN|AP|OF)]>  
<[Reference Alignment Name(CP)]>  
<[Structure Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[Structure Offset(Uft|P3|RN|AP|Sn|OF)]>  
<[Structure Offset Side(CP)]>  
<[Reference Surface Name(CP)]>  
<[Connected Pipes(Sn)]>  
<[Structure Northing(Uft|P4|RN|AP|Sn|OF)]>  
<[Structure Easting(Uft|P4|RN|AP|Sn|OF)]>  
<[Automatic Surface Adjustment]>  
<[Insertion Rim Elevation(Uft|P3|RN|AP|Sn|OF)]>  
<[Sump Elevation(Uft|P3|RN|AP|Sn|OF)]>  
<[Surface Adjustment Value(Uft|P3|RN|AP|Sn|OF)]>  
<[Control Sump By:(CP)]>  
<[Sump Depth(P3|RN|AP|Sn|OF)]>  
<[Surface Elevation At Insertion Point(Uft|P3|RN|AP|Sn|OF)]>  
<[Structure Shape(CP)]>  
<[Vertical Pipe Clearance(Uin|P3|RN|AP|Sn|OF)]>  
<[Rim to Sump Height(Uft|P3|RN|AP|Sn|OF)]>  
<[Wall Thickness(Uin|P3|RN|AP|Sn|OF)]>  
<[Floor Thickness(Uin|P3|RN|AP|Sn|OF)]>  
<[Material(CP)]>  
<[Frame(CP)]>  
<[Grate(CP)]>  
<[Cover(CP)]>  
<[Frame Height(Uin|P3|RN|AP|Sn|OF)]>  
<[Frame Diameter(Uin|P3|RN|AP|Sn|OF)]>  
<[Frame Length(Uin|P3|RN|AP|Sn|OF)]>  
<[Frame Width(Uin|P3|RN|AP|Sn|OF)]>  
<[Barrel Height(Uft|P3|RN|AP|Sn|OF)]>  
<[Barrel Pipe Clearance(Uin|P3|RN|AP|Sn|OF)]>  
<[Cone Height(Uin|P3|RN|AP|Sn|OF)]>  
<[Slab Thickness(Uin|P3|RN|AP|Sn|OF)]>  
<[Inner Structure Diameter(Uin|P3|RN|AP|Sn|OF)]>  
<[Inner Structure Length(Uin|P3|RN|AP|Sn|OF)]>  
<[Inner Structure Width(Uin|P3|RN|AP|Sn|OF)]>  
<[Headwall Base Width(Uin|P3|RN|AP|Sn|OF)]>  
<[Headwall Base Thickness(Uin|P3|RN|AP|Sn|OF)]>
