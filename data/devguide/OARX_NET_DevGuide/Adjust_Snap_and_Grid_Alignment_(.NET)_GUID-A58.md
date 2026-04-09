<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Draw With Precision (.NET) > Adjust Snap and Grid Alignment (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-A588F7CE-C810-49CB-B88A-00B416B9956B.htm -->

# Adjust Snap and Grid Alignment (.NET)

The grid is a visual guideline to measure distances, while Snap mode is used to restrict cursor movement. In addition to setting the spacing for the grid and Snap mode, you can adjust the rotation and type of snap used. 

If you need to draw along a specific alignment or angle, you can rotate the snap angle. The center point of the snap angle rotation is the snap base point. 

Note: After changing the snap and grid settings for the active viewport, you should use the UpdateTiledViewportsFromDatabase method of the Editor object to update the display of the drawing area. 

Snap and grid do not affect points specified through the AutoCAD .NET API, but do affect points specified in the drawing area by the user if they are requested to enter input using methods such as GetPoint or GetEntity. 

## Change the grid and snap settings

This example changes the snap base point to (1,1) and the snap rotation angle to 30 degrees. The grid is turned on the spacing is adjusted so that the changes are visible. 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("ChangeGridAndSnap")]
    public static void ChangeGridAndSnap()
    {
      // Get the current database
      Document acDoc = Application.DocumentManager.MdiActiveDocument;
      Database acCurDb = acDoc.Database;
     
      // Start a transaction
      using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
      {
          // Open the active viewport
          ViewportTableRecord acVportTblRec;
          acVportTblRec = acTrans.GetObject(acDoc.Editor.ActiveViewportId,
                                            OpenMode.ForWrite) as ViewportTableRecord;
     
          // Turn on the grid for the active viewport
          acVportTblRec.GridEnabled = true;
     
          // Adjust the spacing of the grid to 1, 1
          acVportTblRec.GridIncrements = new Point2d(1, 1);
     
          // Turn on the snap mode for the active viewport
          acVportTblRec.SnapEnabled = true;
     
          // Adjust the snap spacing to 0.5, 0.5
          acVportTblRec.SnapIncrements = new Point2d(0.5, 0.5);
     
          // Change the snap base point to 1, 1
          acVportTblRec.SnapBase = new Point2d(1, 1);
     
          // Change the snap rotation angle to 30 degrees (0.524 radians)
          acVportTblRec.SnapAngle = 0.524;
     
          // Update the display of the tiled viewport
          acDoc.Editor.UpdateTiledViewportsFromDatabase();
     
          // Commit the changes and dispose of the transaction
          acTrans.Commit();
      }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("ChangeGridAndSnap")> _
    Public Sub ChangeGridAndSnap()
      '' Get the current database
      Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
      Dim acCurDb As Database = acDoc.Database
     
      '' Start a transaction
      Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
     
          '' Open the active viewport
          Dim acVportTblRec As ViewportTableRecord
          acVportTblRec = acTrans.GetObject(acDoc.Editor.ActiveViewportId, _
                                            OpenMode.ForWrite)
     
          '' Turn on the grid for the active viewport
          acVportTblRec.GridEnabled = True
     
          '' Adjust the spacing of the grid to 1, 1
          acVportTblRec.GridIncrements = New Point2d(1, 1)
     
          '' Turn on the snap mode for the active viewport
          acVportTblRec.SnapEnabled = True
     
          '' Adjust the snap spacing to 0.5, 0.5
          acVportTblRec.SnapIncrements = New Point2d(0.5, 0.5)
     
          '' Change the snap base point to 1, 1
          acVportTblRec.SnapBase = New Point2d(1, 1)
     
          '' Change the snap rotation angle to 30 degrees (0.524 radians)
          acVportTblRec.SnapAngle = 0.524
     
          '' Update the display of the tiled viewport
          acDoc.Editor.UpdateTiledViewportsFromDatabase()
     
          '' Commit the changes and dispose of the transaction
          acTrans.Commit()
      End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub ChangeGridAndSnap()
        ' Turn on the grid for the active viewport
        ThisDrawing.ActiveViewport.GridOn = True
     
        ' Adjust the spacing of the grid to 1, 1
        ThisDrawing.ActiveViewport.SetGridSpacing 1, 1
     
        ' Turn on the snap mode for the active viewport
        ThisDrawing.ActiveViewport.SnapOn = True
     
        ' Adjust the snap spacing to 0.5, 0.5
        ThisDrawing.ActiveViewport.SetSnapSpacing 0.5, 0.5
     
        ' Change the snap base point to 1, 1
        Dim newBasePoint(0 To 1) As Double
        newBasePoint(0) = 1: newBasePoint(1) = 1
        ThisDrawing.ActiveViewport.SnapBasePoint = newBasePoint
     
        ' Change the snap rotation angle to 30 degrees (0.524 radians)
        Dim rotationAngle As Double
        rotationAngle = 0.524
        ThisDrawing.ActiveViewport.SnapRotationAngle = rotationAngle
     
        ' Reset the viewport
        ThisDrawing.ActiveViewport = ThisDrawing.ActiveViewport
    End Sub
