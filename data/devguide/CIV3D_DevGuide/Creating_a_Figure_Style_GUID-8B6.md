<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Figures > Creating a Figure Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-8B6DC9BA-BC67-4BF9-9ACE-0DAFFC0F65C0.htm -->

# Creating a Figure Style

A figure style controls the visual appearance of figures. The AeccSurveyFigureStyle object has AeccDisplayStyle properties for controlling the color, line type, and visibility of lines and of markers at the figure endpoints, the figure midpoint, at line vertices. The types of markers used are controlled by separate AeccMarkerStyle properties for the start, mid, and end points of the figure, and for all vertexes. Markers can also be drawn at a normal alignment to the orientation of the figure by setting the IsAlignAdditionalMarkersWithFigure, IsAlignMidPointMarkersWithFigure, IsAlignStartAndEndPointMarkersWithFigure, and IsAlignVertexMarkersWithFigure properties to True for the appropriate type of marker.

Additional markers can also be placed along the figure. The nature of these additional markers is set by the AeccSurveyFigureStyle.AdditionalMarkersPlacementMethod property. If the placement method is set for interval placement, then a new marker is placed every _n_ units apart where _n_ is the value of the AeccSurveyFigureStyle.AdditionalMarkersInterval property. If the placement method is set for divided placement, then the figure is divided into _n_ parts of equal length where _n_ is the value of the AeccSurveyFigureStyle.AdditionalMarkersDivideFigureBy property. A marker is placed at each part, including the figure start and end points. If the placement method is set for continuous, then the markers are placed exactly one marker’s width apart along the length of the figure.

You can determine the style of figure drawing by examining the FigureDisplayMode property. There are three ways a figure can be visualized: using figure elevations, flattening the figure to a single elevation, or exaggerating figure elevations. If the figure is flattened to a single elevation, the elevation can be read from the FlattenFigureElevation property. If the figure elevations are exaggerated when displayed, the amount of exaggerations is held in the read-only FigureElevationScaleFactor property.

All figure styles are stored in the AeccSurveyDocument.FigureStyle collection. The figure object’s AeccSurveyFigure.Style property takes the string name of the style to use.

This sample creates a new figure style object and adjusts some of the style settings:
    
    
    Dim oFigureStyles As AeccSurveyFigureStyles
    Dim oFigureStyle As AeccSurveyFigureStyle
    Set oFigureStyles = oSurveyDocument.FigureStyles
    Set oFigureStyle = oFigureStyles.Add(sStylename)
     
    ' Set the style so that additional markers are visible,
    ' blue, and drawn every 20 units along the figure.
    With oFigureStyle
        .AdditionalMarkersDisplayStylePlan.Visible = True
        .AdditionalMarkersDisplayStylePlan.Color = 150 ' blue
        .AdditionalMarkersPlacementMethod = _
          aeccSurveyAdditionalMarkerPlacementMethodAtInterval
        .AdditionalMarkersInterval = 20
    End With
     
    ' Assign the style to a figure.
    oFigure.Style = oFigureStyle.Name
