<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Control the Drawing Windows (.NET) > Zoom and Pan the Current View (.NET) > Define to Window (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-AA770AAA-A008-47A9-9C2B-3ECD040A18ED.htm -->

# Define to Window (.NET)

In AutoCAD, you use the Window option of the ZOOM command to define the area of the drawing that should be displayed in the drawing window. When you define the area to be displayed, the Width and Height properties of the current view are adjusted to match the area defined by the two points specified. Based on the specified points, the CenterPoint property of the view is also moved. 

## Zoom to an area defined by two points

This example code demonstrates how to zoom to a defined area using the Zoom procedure defined in the "Manipulate the Current View" topic. The Zoom procedure is passed the coordinates (1.3,7.8,0) and (13.7,-2.6,0) for the first two arguments to define the area to display. 

No new center point is needed, so a new Point3d object is passed to the procedure. The last argument is used to scale the new view. Scaling the view can be used to create a gap between the area displayed and the edge of the drawing window. 

### C#
    
    
    [CommandMethod("ZoomWindow")]
    static public void ZoomWindow()
    {
        // Zoom to a window boundary defined by 1.3,7.8 and 13.7,-2.6
        Point3d pMin = new Point3d(1.3, 7.8, 0);
        Point3d pMax = new Point3d(13.7, -2.6, 0);
     
        Zoom(pMin, pMax, new Point3d(), 1);
    }

### VB.NET
    
    
    <CommandMethod("ZoomWindow")> _
    Public Sub ZoomWindow()
        '' Zoom to a window boundary defined by 1.3,7.8 and 13.7,-2.6
        Dim pMin As Point3d = New Point3d(1.3, 7.8, 0)
        Dim pMax As Point3d = New Point3d(13.7, -2.6, 0)
     
        Zoom(pMin, pMax, New Point3d(), 1)
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub ZoomWindow()
        Dim point1(0 To 2) As Double
        Dim point2(0 To 2) As Double
        point1(0) = 1.3: point1(1) = 7.8: point1(2) = 0
        point2(0) = 13.7: point2(1) = -2.6: point2(2) = 0
     
        ThisDrawing.Application.ZoomWindow point1, point2
    End Sub
