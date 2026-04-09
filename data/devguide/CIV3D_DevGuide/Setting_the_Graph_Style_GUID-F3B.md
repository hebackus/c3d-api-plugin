<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Profiles in COM > Profile Views > Setting Profile View Styles > Setting the Graph Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-F3B6483D-EDFB-4C16-8EB3-B06009879C7C.htm -->

# Setting the Graph Style

The graph is managed by an object of type AeccGraphStyle. This object can be used to change the grid and the title of the graph. The grid is controlled by the AeccGraphStyle.GridStyle property, an object of type AeccGridStyle. The grid style sets the amount of empty space above and below the extents of the section through the AeccGridStyle.GridsAboveMaxElevation and AeccGridStyle.GridsBelowDatum properties. The grid style also manages the line styles of major and minor vertical and horizontal gridlines with the AeccGridStyle properties MajorVerticalDisplayStylePlan, MajorHorizontalDisplayStylePlan, MinorVerticalDisplayStylePlan, and MinorHorizontalDisplayStylePlan. The AeccGridLines.VerticalPosition and AeccGridLines.HorizontalPosition properties tell which axis to use to position the grid lines.

## Graph Title

The title of the graph is controlled by the AeccGraphStyle.TitleStyle property, an object of type AeccGraphTitleStyle. The title style object can adjust the position, style, and border of the title. The text of the title can include any of the following property fields:

Valid property fields for AeccGraphTitleStyle.Text  
---  
<[Graph View Name(CP)]>  
<[Parent Alignment(CP)]>  
<[Drawing Scale(P4|RN|AP|OF)]>  
<[Graph View Vertical Scale(P4|RN|AP|OF)]>  
<[Graph View Vertical Exageration(P4|RN|AP|OF)]>  
<[Profile View Start Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[Profile View End Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[Profile View Minimum Elevation(Uft|P2|RN|AP|Sn|OF)]>  
<[Profile View Maximum Elevation(Uft|P3|RN|AP|Sn|OF)]>
