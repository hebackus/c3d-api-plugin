<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Sections in COM > Section Views > Setting Section View Styles > Setting Graph Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-02E81C04-84AD-4BD5-B508-D32694E06274.htm -->

# Setting Graph Styles

The graph is managed by an object of type AeccGraphStyle. This object can be used to change the grid and the title of the graph. The grid is controlled by the AeccGraphStyle.GridStyle property, an object of type AeccGridStyle. The grid style sets the amount of empty space above and below the extents of the section through the AeccGridStyle.GridsAboveMaxElevation and AeccGridStyle.GridsBelowDatum properties. The grid style also manages the line styles of major and minor vertical and horizontal gridlines with the AeccGridStyle properties MajorVerticalDisplayStylePlan, MajorHorizontalDisplayStylePlan, MinorVerticalDisplayStylePlan, and MinorHorizontalDisplayStylePlan. The AeccGridLines.HorizontalPosition and AeccGridLines.VerticalPosition properties tell which tick marks to use to position the grid lines for the axis. 

## Graph Title

The title of the graph is controlled by the AeccGraphStyle.TitleStyle property, an object of type AeccGraphTitleStyle. The title style object can adjust the position, style, and border of the title. The text of the title can include any of the following property fields:

Valid property fields for AeccGraphTitleStyle.Text  
---  
<[Section View Description(CP)]>  
<[Section View Name(CP)]>  
<[Parent Alignment(CP)]>  
<[Section View Station(Uft|FS|P3|RN|Sn|OF|AP|B2|TP|EN|W0|DZY)]>  
<[Section View Datum Value(Uft|P3|RN|AP|Sn|OF)]>  
<[Section View Width(Uft|P3|RN|AP|Sn|OF)]>  
<[Left Width(Uft|P3|RN|AP|Sn|OF)]>  
<[Right Width(Uft|P3|RN|AP|Sn|OF)]>  
<[Drawing Scale(P3|RN|AP|OF)]>  
<[Graph View Vertical Scale(P3|RN|AP|OF)]>  
<[Graph View Vertical Exageration(P3|RN|AP|OF)]>  
<[Sample Line Name(CP)]>  
<[Sample Line Group(CP)]>  
<[Sample Line Number(Sn)]>
