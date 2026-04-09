<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Control the Drawing Windows (.NET) > Zoom and Pan the Current View (.NET) > Display Drawing Extents and Limits (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-70B3140A-14F1-4F54-AF5F-8DEDB444C3BA.htm -->

# Display Drawing Extents and Limits (.NET)

The extents or limits of a drawing are used to define the boundary in which the outermost objects appear in or the area defined by the limits of the current space. 

## Calculate the extents of the current space

The extents of the current space can be accessed from the Database object using the following properties: 

  * **Extmin and Extmax** \- Returns the extents of Model space. 
  * **Pextmin and Pextmax** \- Returns the extents of the current Paper space layout. 

Once the extents of the current space is obtained, you can calculate the new values for the Width and Height properties of the current view. The new width for the view is calculated using the following formula: 
    
    
    dWidth = MaxPoint.X - MinPoint.X

The new height for the view is calculated using the following formula: 
    
    
    dHeight = MaxPoint.Y - MinPoint.Y

After the width and height of the view are calculated, the center point of the view can be calculated. The center point of the view can be obtained using the following formula: 
    
    
    dCenterX = (MaxPoint.X + MinPoint.X) * 0.5
    dCenterY = (MaxPoint.Y + MinPoint.Y) * 0.5

## Calculate the limits of the current space

To change the display of a drawing based on the limits of the current space, you use the Limmin and Limmax , and Plimmin and Plimmax properties of the Database object. After the points that define the limits of the current space are returned, you can use the previously mentioned formulas to calculate the width, height and center points of the new view. 

## Zoom in to the extents and limits of the current space

This example code demonstrates how to display the extents of limits of the current space using the Zoom procedure defined in the "Manipulate the Current View" topic. 

While the Zoom procedure is passed a total of four values, the first two values passed should be the points that define the minimum and maximum points of the area to be displayed. The third value is defined as a new 3D point and is ignored by the procedure, while the last value is used to resize the image of the drawing so it is not completely fill the entire drawing window. 

### C#
    
    
    [CommandMethod("ZoomExtents")]
    static public void ZoomExtents()
    {
        // Zoom to the extents of the current space
        Zoom(new Point3d(), new Point3d(), new Point3d(), 1.01075);
    }
     
    [CommandMethod("ZoomLimits")]
    static public void ZoomLimits()
    {
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
     
        // Zoom to the limits of Model space
        Zoom(new Point3d(acCurDb.Limmin.X, acCurDb.Limmin.Y, 0),
             new Point3d(acCurDb.Limmax.X, acCurDb.Limmax.Y, 0),
             new Point3d(), 1);
    }

### VB.NET
    
    
    <CommandMethod("ZoomExtents")> _
    Public Sub ZoomExtents()
        '' Zoom to the extents of the current space
        Zoom(New Point3d(), New Point3d(), New Point3d(), 1.01075)
    End Sub
     
    <CommandMethod("ZoomLimits")> _
    Public Sub ZoomLimits()
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
     
        '' Zoom to the limits of Model space
        Zoom(New Point3d(acCurDb.Limmin.X, acCurDb.Limmin.Y, 0), _
             New Point3d(acCurDb.Limmax.X, acCurDb.Limmax.Y, 0), _
             New Point3d(), 1)
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub ZoomExtents()
        ThisDrawing.Application.ZoomExtents
    End Sub
     
    Sub ZoomLimits()
        Dim point1(0 To 2) As Double
        Dim point2(0 To 2) As Double
     
        point1(0) = ThisDrawing.GetVariable("LIMMIN")(0)
        point1(1) = ThisDrawing.GetVariable("LIMMIN")(1)
        point1(2) = 0#
     
        point2(0) = ThisDrawing.GetVariable("LIMMAX")(0)
        point2(1) = ThisDrawing.GetVariable("LIMMAX")(1)
        point2(2) = 0#
     
        ThisDrawing.Application.ZoomWindow point1, point2
    End Sub
