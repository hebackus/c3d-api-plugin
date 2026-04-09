<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Control the Drawing Windows (.NET) > Use Tiled Viewports (.NET) > Make A Tiled Viewport Current (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-728723FC-E8A3-4001-83CF-D728E9DB419C.htm -->

# Make A Tiled Viewport Current (.NET)

You enter points and select objects in the current viewport. To make a viewport current, use the CVPORT system variable and specify the viewport by its number that you want to set current. 

You can iterate through existing viewports to find a particular viewport. To do this, identify the Viewport table records with the name "*Active" using the Name property. 

## Split a viewport, then iterate through the windows

This example splits the active viewport into two horizontal windows. It then iterates through all the tiled viewports in the drawing and displays the viewport name and the lower-left and upper-right corner for each viewport. 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("SplitAndIterateModelViewports")]
    public static void SplitAndIterateModelViewports()
    {
        // Get the current database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Viewport table for write
            ViewportTable acVportTbl;
            acVportTbl = acTrans.GetObject(acCurDb.ViewportTableId,
                                            OpenMode.ForWrite) as ViewportTable;
    
            // Open the active viewport for write
            ViewportTableRecord acVportTblRec;
            acVportTblRec = acTrans.GetObject(acDoc.Editor.ActiveViewportId,
                                                OpenMode.ForWrite) as ViewportTableRecord;
    
            using (ViewportTableRecord acVportTblRecNew = new ViewportTableRecord())
            {
                // Add the new viewport to the Viewport table and the transaction
                acVportTbl.Add(acVportTblRecNew);
                acTrans.AddNewlyCreatedDBObject(acVportTblRecNew, true);
    
                // Assign the name '*Active' to the new Viewport
                acVportTblRecNew.Name = "*Active";
    
                // Use the existing lower left corner for the new viewport
                acVportTblRecNew.LowerLeftCorner = acVportTblRec.LowerLeftCorner;
    
                // Get half the X of the existing upper corner
                acVportTblRecNew.UpperRightCorner = new Point2d(acVportTblRec.UpperRightCorner.X,
                                                                acVportTblRec.LowerLeftCorner.Y +
                                                                ((acVportTblRec.UpperRightCorner.Y -
                                                                    acVportTblRec.LowerLeftCorner.Y) / 2));
    
                // Recalculate the corner of the active viewport
                acVportTblRec.LowerLeftCorner = new Point2d(acVportTblRec.LowerLeftCorner.X,
                                                            acVportTblRecNew.UpperRightCorner.Y);
    
                // Update the display with the new tiled viewports arrangement
                acDoc.Editor.UpdateTiledViewportsFromDatabase();
    
                // Step through each object in the symbol table
                foreach (ObjectId acObjId in acVportTbl)
                {
                    // Open the object for read
                    ViewportTableRecord acVportTblRecCur;
                    acVportTblRecCur = acTrans.GetObject(acObjId,
                                                            OpenMode.ForRead) as ViewportTableRecord;
    
                    if (acVportTblRecCur.Name == "*Active")
                    {
                        Application.SetSystemVariable("CVPORT", acVportTblRecCur.Number);
    
                        Application.ShowAlertDialog("Viewport: " + acVportTblRecCur.Number +
                                                    " is now active." +
                                                    "\nLower left corner: " +
                                                    acVportTblRecCur.LowerLeftCorner.X + ", " +
                                                    acVportTblRecCur.LowerLeftCorner.Y +
                                                    "\nUpper right corner: " +
                                                    acVportTblRecCur.UpperRightCorner.X + ", " +
                                                    acVportTblRecCur.UpperRightCorner.Y);
                    }
                }
            }
    
            // Commit the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("SplitAndIterateModelViewports")> _
    Public Sub SplitAndIterateModelViewports()
        '' Get the current database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Viewport table for write
            Dim acVportTbl As ViewportTable
            acVportTbl = acTrans.GetObject(acCurDb.ViewportTableId, _
                                           OpenMode.ForWrite)
    
            '' Open the active viewport for write
            Dim acVportTblRec As ViewportTableRecord
            acVportTblRec = acTrans.GetObject(acDoc.Editor.ActiveViewportId, _
                                              OpenMode.ForWrite)
    
            Using acVportTblRecNew As ViewportTableRecord = New ViewportTableRecord()
    
                '' Add the new viewport to the Viewport table and the transaction
                acVportTbl.Add(acVportTblRecNew)
                acTrans.AddNewlyCreatedDBObject(acVportTblRecNew, True)
    
                '' Assign the name '*Active' to the new Viewport
                acVportTblRecNew.Name = "*Active"
    
                '' Use the existing lower left corner for the new viewport
                acVportTblRecNew.LowerLeftCorner = acVportTblRec.LowerLeftCorner
    
                '' Get half the X of the existing upper corner
                acVportTblRecNew.UpperRightCorner = New Point2d(acVportTblRec.UpperRightCorner.X, _
                                                                acVportTblRec.LowerLeftCorner.Y + _
                                                                ((acVportTblRec.UpperRightCorner.Y - _
                                                                  acVportTblRec.LowerLeftCorner.Y) / 2))
    
                '' Recalculate the corner of the active viewport
                acVportTblRec.LowerLeftCorner = New Point2d(acVportTblRec.LowerLeftCorner.X, _
                                                            acVportTblRecNew.UpperRightCorner.Y)
    
                '' Update the display with the new tiled viewports arrangement
                acDoc.Editor.UpdateTiledViewportsFromDatabase()
    
                '' Step through each object in the symbol table
                For Each acObjId As ObjectId In acVportTbl
                    '' Open the object for read
                    Dim acVportTblRecCur As ViewportTableRecord
                    acVportTblRecCur = acTrans.GetObject(acObjId, _
                                                         OpenMode.ForRead)
    
                    If (acVportTblRecCur.Name = "*Active") Then
                        Application.SetSystemVariable("CVPORT", acVportTblRecCur.Number)
    
                        Application.ShowAlertDialog("Viewport: " & acVportTblRecCur.Number & _
                                                    " is now active." & _
                                                    vbLf & "Lower left corner: " & _
                                                    acVportTblRecCur.LowerLeftCorner.X & ", " & _
                                                    acVportTblRecCur.LowerLeftCorner.Y & _
                                                    vbLf & "Upper right corner: " & _
                                                    acVportTblRecCur.UpperRightCorner.X & ", " & _
                                                    acVportTblRecCur.UpperRightCorner.Y)
                    End If
                Next
            End Using
    
            '' Commit the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub SplitandInterateModelViewports()
        ' Get the active viewport
        Dim vportObj As AcadViewport
        Set vportObj = ThisDrawing.ActiveViewport
     
        ' Split the viewport into 2 windows
        vportObj.Split acViewport2Horizontal
     
        ' Iterate through the viewports,
        ' highlighting each viewport and displaying
        ' the upper right and lower left corners
        ' for each.
        Dim vport As AcadViewport
        Dim LLCorner As Variant
        Dim URCorner As Variant
     
        For Each vport In ThisDrawing.Viewports
            ThisDrawing.ActiveViewport = vport
            LLCorner = vport.LowerLeftCorner
            URCorner = vport.UpperRightCorner
            MsgBox "Viewport: " & vport.Name & " is now active." & _
                   vbCrLf & "Lower left corner: " & _
                   LLCorner(0) & ", " & LLCorner(1) & vbCrLf & _
                   "Upper right corner: " & _
                   URCorner(0) & ", " & URCorner(1)
        Next vport
    End Sub
