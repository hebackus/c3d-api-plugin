<!-- Developer's Guide > API Developer's Guide > Profiles > Profile Views > Setting Profile View Styles > Setting the Graph Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-DF0B67A2-61EC-4282-BBBB-5C813C99613F.htm -->

# Setting the Graph Style

The graph is managed by objects of type GraphStyle and GridStyle. These objects can be used to change the scale, title, and grid of the graph. 

The grid is controlled by the ProfileViewStyle.GridStyle property, an object of type GridStyle. The grid style sets the amount of empty space above and below the extents of the section through the GridStyle.GridPaddingAbove and GridStyle.GridPaddingBottom properties. The grid style also manages the line styles of major and minor vertical and horizontal gridlines with the DisplayStyle.PlotStyle property accessed by the GetDisplayStylePlan() method. 

## Graph Title

The title of the graph is controlled by the GraphStyle.TitleStyle property, an object of type GraphTitleStyle. The title style object can adjust the position, style, and border of the title. The text of the title can include any of the following property fields:

Valid property fields for GraphTitleStyle.Text  
---  
<[Graph View Name(CP)]>  
<[Parent Alignment(CP)]>  
<[Drawing Scale(P4|RN|AP|OF)]>  
<[Graph View Vertical Scale(P4|RN|AP|OF)]>  
<[Graph View Vertical Exaggeration(P4|RN|AP|OF)]>  
<[Profile View Start Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[Profile View End Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[Profile View Minimum Elevation(Uft|P2|RN|AP|Sn|OF)]>  
<[Profile View Maximum Elevation(Uft|P3|RN|AP|Sn|OF)]>
