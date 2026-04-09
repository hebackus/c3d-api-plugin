<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Control the Drawing Windows (.NET) > Zoom and Pan the Current View (.NET) > Scale a View (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-25131FDB-7C20-44C1-B3F2-BACD27F7C116.htm -->

# Scale a View (.NET)

If you need to increase or decrease the magnification of the image in the drawing window, you change the Width and Height properties of the current view. When resizing a view, make sure to change the Width and Height properties by the same factor. The scale factor you calculate when resizing the current view will commonly be based on one of the following situations: 

  * Relative to the drawing limits 
  * Relative to the current view 
  * Relative to paper space units 

## Zoom in on the active drawing using a specified scale

This example code demonstrates how to reduce the current view by 50% using the Zoom procedure defined in the " Manipulate the Current View" topic. 

While the Zoom procedure is passed a total of four values, the first two are new 3D points which are not used. The third value passed is the center point to use in resizing the view and the last value passed is the scale factor to use in resizing the view. 

### C#
    
    
    [CommandMethod("ZoomScale")]
    static public void ZoomScale()
    {
        // Get the current document
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
     
        // Get the current view
        using (ViewTableRecord acView = acDoc.Editor.GetCurrentView())
        {
            // Get the center of the current view
            Point3d pCenter = new Point3d(acView.CenterPoint.X,
                                          acView.CenterPoint.Y, 0);
     
            // Set the scale factor to use
            double dScale = 0.5;
     
            // Scale the view using the center of the current view
            Zoom(new Point3d(), new Point3d(), pCenter, 1 / dScale);
        }
    }

### VB.NET
    
    
    <CommandMethod("ZoomScale")> _
    Public Sub ZoomScale()
        '' Get the current document
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
     
        '' Get the current view
        Using acView As ViewTableRecord = acDoc.Editor.GetCurrentView()
            '' Get the center of the current view
            Dim pCenter As Point3d = New Point3d(acView.CenterPoint.X, _
                                                 acView.CenterPoint.Y, 0)
     
            '' Set the scale factor to use
            Dim dScale As Double = 0.5
     
            '' Scale the view using the center of the current view
            Zoom(New Point3d(), New Point3d(), pCenter, 1 / dScale)
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub ZoomScale()
        Dim scalefactor As Double
        Dim scaletype As Integer
     
        scalefactor = 0.5
        scaletype = acZoomScaledRelative
     
        ThisDrawing.Application.ZoomScaled scalefactor, scaletype
    End Sub
