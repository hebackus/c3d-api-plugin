<!-- Developer's Guide > API Developer's Guide > Profiles > Profile Views > Setting Profile View Styles > Setting the Axis Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-00C698BC-D956-4106-9FF4-8307F1C77819.htm -->

# Setting the Axis Style

All axis styles are based on the AxisStyle class. The axis style object controls the display style of the axis itself, tick marks and text placed along the axis, and a text annotation describing the axis’s purpose. The annotation text, location, and size is set through the AxisStyle.TitleStyle property, an object of type AxisTitleStyle. The annotation text can use any of the following property fields:

Valid property fields for AxisTitleStyle.Text   
---  
<[Profile View Minimum Elevation(Uft|P3|RN|AP|Sn|OF)]>  
<[Profile View Maximum Elevation(Uft|P3|RN|AP|Sn|OF)]>  
<[Profile View Start Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[Profile View End Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
  
## Axis Tick Marks

Within each axis style are properties for specifying the tick marks placed along the axis. Both major tick marks and minor tick marks are represented by objects of type AxisTickStyle. The AxisTickStyle class manages the location, size, and visual style of tick marks through its Interval, Size and other properties. Note that while most style properties use drawing units, the Interval property uses the actual ground units of the surface. The AxisTickStyle object also determines the text that is displayed at each tick, including the following property fields:

Valid property fields for TickStyle.Text | Axis  
---|---  
<[Station Value(Uft|FS|P0|RN|AP|Sn|TP|B2|EN|W0|OF)]> | horizontal  
<[Raw Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]> | horizontal   
<[Graph View Abscissa Value(Uft|P4|RN|AP|Sn|OF)]> | horizontal   
<[Profile View Point Elevation(Uft|P1|RN|AP|Sn|OF)]> | vertical   
<[Graph View Ordinate Value(Uft|P3|RN|AP|Sn|OF)]> | vertical
