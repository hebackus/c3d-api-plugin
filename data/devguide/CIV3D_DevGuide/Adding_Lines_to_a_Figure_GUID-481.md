<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Figures > Adding Lines to a Figure -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-48128431-B7FD-4041-9E20-4AA0896481D5.htm -->

# Adding Lines to a Figure

Each line added to a figure is drawn from the endpoint of the previous line or arc. The new line can be drawn to a particular point location, for a distance along an absolute azimuth, or for a distance along an azimuth relative to the direction of the previous line. If the figure has no lines or arcs, then the first line added will only set the point that the next line or arc is drawn from.

## AddLineByPoint

AddLineByPoint adds a line to the figure to the specified point location. An optional parameter can specify a survey point to reference so that whenever it changes the figure vertex will change as well.
    
    
    ' Draw a line to the location of survey point 3001.
    Dim oPoint1 As AeccSurveyPoint
    Set oPoint1 = oSurveyProject.GetPointByNumber(3001)
    oFigure.AddLineByPoint oPoint1.Easting, oPoint1.Northing, 3001
    

## AddLineByAzimuthDistance

AddLineByAzimuthDistance adds a line to the figure of the specified length and of the specified angle from the major axis of the survey project.
    
    
    ' Draw a line 30 meters long at 10 degrees from the major axis.
    oFigure.AddLineByAzimuthDistance 0.17453, 30
    

## AddLineByDeltaAzimuthDistance

AddLineByDeltaAzimuthDistance adds a line to the figure of the specified length and of the specified angle from the endpoint of the previous line. 
    
    
    ' Draw a line 20 meters long at 270 degrees from the
    ' previous line.
    oFigure.AddLineByDeltaAzimuthDistance 4.7124, 20
