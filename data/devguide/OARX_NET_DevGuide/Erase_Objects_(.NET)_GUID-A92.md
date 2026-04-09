<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Erase Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-A9283274-3E5B-4739-975B-03A30536EE64.htm -->

# Erase Objects (.NET)

You can delete non-graphical and graphical objects with the Erase method. 

Caution: While many non-graphical objects, such as the Layer table and Model space block table records have an Erase method, it should not be called. If Erase is called on one of these objects, an error will occur. 

## Create and erase a polyline

This example creates a lightweight polyline, then erases it. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("EraseObject")]
    public static void EraseObject()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Block table for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                         OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Model space for write
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                            OpenMode.ForWrite) as BlockTableRecord;
    
            // Create a lightweight polyline
            using (Polyline acPoly = new Polyline())
            {
                acPoly.AddVertexAt(0, new Point2d(2, 4), 0, 0, 0);
                acPoly.AddVertexAt(1, new Point2d(4, 2), 0, 0, 0);
                acPoly.AddVertexAt(2, new Point2d(6, 4), 0, 0, 0);
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPoly);
                acTrans.AddNewlyCreatedDBObject(acPoly, true);
    
                // Update the display and display an alert message
                acDoc.Editor.Regen();
                Application.ShowAlertDialog("Erase the newly added polyline.");
    
                // Erase the polyline from the drawing
                acPoly.Erase(true);
            }
    
            // Save the new object to the database
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("EraseObject")> _
    Public Sub EraseObject()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead)
    
            '' Open the Block table record Model space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForWrite)
    
            '' Create a lightweight polyline
            Using acPoly As Polyline = New Polyline()
                acPoly.AddVertexAt(0, New Point2d(2, 4), 0, 0, 0)
                acPoly.AddVertexAt(1, New Point2d(4, 2), 0, 0, 0)
                acPoly.AddVertexAt(2, New Point2d(6, 4), 0, 0, 0)
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPoly)
                acTrans.AddNewlyCreatedDBObject(acPoly, True)
    
                '' Update the display and display an alert message
                acDoc.Editor.Regen()
                Application.ShowAlertDialog("Erase the newly added polyline.")
    
                '' Erase the polyline from the drawing
                acPoly.Erase(True)
            End Using
    
            '' Save the new object to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub EraseObject()
        ' Create the polyline
        Dim lwpolyObj As AcadLWPolyline
        Dim vertices(0 To 5) As Double
        vertices(0) = 2: vertices(1) = 4
        vertices(2) = 4: vertices(3) = 2
        vertices(4) = 6: vertices(5) = 4
        Set lwpolyObj = ThisDrawing.ModelSpace. _
                                         AddLightWeightPolyline(vertices)
        ZoomAll
        ' Erase the polyline
        lwpolyObj.Delete
        ThisDrawing.Regen acActiveViewport
    End Sub
