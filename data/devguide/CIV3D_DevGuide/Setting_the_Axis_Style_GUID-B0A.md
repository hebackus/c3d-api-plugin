<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Sections in COM > Section Views > Setting Section View Styles > Setting the Axis Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-B0A54A6F-CAE6-415A-9B1B-D3CE5226F775.htm -->

# Setting the Axis Style

All axis styles are based on the AeccAxisStyle class. The axis style object controls the display style of the axis itself, tick marks and text placed along the axis, and a text annotation describing the purpose of the axis. The annotation text, location, and size is set through the AeccAxisStyle.TitleStyle property, an object of type AeccAxisTitleStyle. The annotation text can use any of the following property fields:

Valid property fields for AeccAxisTitleStyle.Text | Axes  
---|---  
<[Section View Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]> | top, bottom  
<[Section View Width(Uft|P2|RN|AP|Sn|OF)]> | top, bottom  
<[Left Width(Uft|P2|RN|AP|Sn|OF)]> | top, bottom  
<[Right Width(Uft|P2|RN|AP|Sn|OF)]> | top, bottom  
<[Elevation Range(Uft|P2|RN|AP|Sn|OF)]> | left, right, center  
<[Minimum Elevation(Uft|P2|RN|AP|Sn|OF)]> | left, right, center  
<[Maximum Elevation(Uft|P2|RN|AP|Sn|OF)]> | left, right, center  
  
## Axis Tick Marks

Within each axis style are properties for specifying the tick marks placed along the axis. Both major tick marks and minor tick marks are represented by objects of type AeccTickStyle. AeccTickStyle manages the location, size, and visual style of tick marks through its Interval, Size and DisplayStylePlan properties. 

Note:

While most style properties use drawing units, the Interval property uses surface units. 

The AeccTickStyle object also sets what text is displayed at each tick, including any of the following property fields: 

Valid property fields for AeccTickStyle.Text  
---  
<[Section View Point Offset Side(CP)]>  
<[Section View Point Offset(Uft|P3|RN|Sn|OF|AP)]>  
<[Graph View Abscissa Value(Uft|P3|RN|AP|Sn|OF)]>
