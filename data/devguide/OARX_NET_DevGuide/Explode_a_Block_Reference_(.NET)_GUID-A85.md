<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Advanced Drawing and Organizational Techniques (.NET) > Use Blocks and Attributes (.NET) > Work with Blocks (.NET) > Explode a Block Reference (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-A853CD73-58A9-4380-B8E2-B3451C94C46B.htm -->

# Explode a Block Reference (.NET)

Use the Explode method to break a block reference. By exploding a block reference, you can modify the block or add to or delete the objects that define it. 

## Display the results of an exploded block reference

This example creates a block and adds a circle to the definition of the block. The block is then inserted into the drawing as a block reference. The block reference is then exploded, and the objects resulting from the explode process are displayed along with their object types. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    
    [CommandMethod("ExplodingABlock")]
    public void ExplodingABlock()
    {
        // Get the current database and start a transaction
        Database acCurDb;
        acCurDb = Application.DocumentManager.MdiActiveDocument.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Block table for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead) as BlockTable;
    
            ObjectId blkRecId = ObjectId.Null;
    
            if (!acBlkTbl.Has("CircleBlock"))
            {
                using (BlockTableRecord acBlkTblRec = new BlockTableRecord())
                {
                    acBlkTblRec.Name = "CircleBlock";
    
                    // Set the insertion point for the block
                    acBlkTblRec.Origin = new Point3d(0, 0, 0);
    
                    // Add a circle to the block
                    using (Circle acCirc = new Circle())
                    {
                        acCirc.Center = new Point3d(0, 0, 0);
                        acCirc.Radius = 2;
    
                        acBlkTblRec.AppendEntity(acCirc);
    
                        acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForWrite);
                        acBlkTbl.Add(acBlkTblRec);
                        acTrans.AddNewlyCreatedDBObject(acBlkTblRec, true);
                    }
    
                    blkRecId = acBlkTblRec.Id;
                }
            }
            else
            {
                blkRecId = acBlkTbl["CircleBlock"];
            }
    
            // Insert the block into the current space
            if (blkRecId != ObjectId.Null)
            {
                using (BlockReference acBlkRef = new BlockReference(new Point3d(0, 0, 0), blkRecId))
                {
                    BlockTableRecord acCurSpaceBlkTblRec;
                    acCurSpaceBlkTblRec = acTrans.GetObject(acCurDb.CurrentSpaceId, OpenMode.ForWrite) as BlockTableRecord;
    
                    acCurSpaceBlkTblRec.AppendEntity(acBlkRef);
                    acTrans.AddNewlyCreatedDBObject(acBlkRef, true);
    
                    using (DBObjectCollection dbObjCol = new DBObjectCollection())
                    {
                        acBlkRef.Explode(dbObjCol);
    
                        foreach (DBObject dbObj in dbObjCol)
                        {
                            Entity acEnt = dbObj as Entity;
    
                            acCurSpaceBlkTblRec.AppendEntity(acEnt);
                            acTrans.AddNewlyCreatedDBObject(dbObj, true);
    
                            acEnt = acTrans.GetObject(dbObj.ObjectId, OpenMode.ForWrite) as Entity;
    
                            acEnt.ColorIndex = 1;
                            Application.ShowAlertDialog("Exploded Object: " + acEnt.GetRXClass().DxfName);
                        }
                    }
                }
            }
    
            // Save the new object to the database
            acTrans.Commit();
    
            // Dispose of the transaction
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    
    <CommandMethod("ExplodingABlock")> _
    Public Sub ExplodingABlock()
        ' Get the current database and start a transaction
        Dim acCurDb As Autodesk.AutoCAD.DatabaseServices.Database
        acCurDb = Application.DocumentManager.MdiActiveDocument.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            ' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead)
    
            Dim blkRecId As ObjectId = ObjectId.Null
    
            If Not acBlkTbl.Has("CircleBlock") Then
                Using acBlkTblRec As New BlockTableRecord
                    acBlkTblRec.Name = "CircleBlock"
    
                    ' Set the insertion point for the block
                    acBlkTblRec.Origin = New Point3d(0, 0, 0)
    
                    ' Add a circle to the block
                    Using acCirc As New Circle
                        acCirc.Center = New Point3d(0, 0, 0)
                        acCirc.Radius = 2
    
                        acBlkTblRec.AppendEntity(acCirc)
    
                        acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForWrite)
                        acBlkTbl.Add(acBlkTblRec)
                        acTrans.AddNewlyCreatedDBObject(acBlkTblRec, True)
                    End Using
    
                    blkRecId = acBlkTblRec.Id
                End Using
            Else
                blkRecId = acBlkTbl("CircleBlock")
            End If
    
            ' Insert the block into the current space
            If blkRecId <> ObjectId.Null Then
                Using acBlkRef As New BlockReference(New Point3d(0, 0, 0), blkRecId)
    
                    Dim acCurSpaceBlkTblRec As BlockTableRecord
                    acCurSpaceBlkTblRec = acTrans.GetObject(acCurDb.CurrentSpaceId, OpenMode.ForWrite)
    
                    acCurSpaceBlkTblRec.AppendEntity(acBlkRef)
                    acTrans.AddNewlyCreatedDBObject(acBlkRef, True)
    
                    Using dbObjCol As New DBObjectCollection
                        acBlkRef.Explode(dbObjCol)
    
                        For Each dbObj As DBObject In dbObjCol
                            Dim acEnt As Entity = dbObj
    
                            acCurSpaceBlkTblRec.AppendEntity(acEnt)
                            acTrans.AddNewlyCreatedDBObject(dbObj, True)
    
                            acEnt = acTrans.GetObject(dbObj.ObjectId, OpenMode.ForWrite)
    
                            acEnt.ColorIndex = 1
                            MsgBox("Exploded Object: " & acEnt.GetRXClass().DxfName)
                        Next
                    End Using
                End Using
            End If
    
            ' Save the new object to the database
            acTrans.Commit()
    
            ' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub ExplodingABlock()
        ' Define the block
        Dim blockObj As AcadBlock
        Dim insertionPnt(0 To 2) As Double
        insertionPnt(0) = 0
        insertionPnt(1) = 0
        insertionPnt(2) = 0
        Set blockObj = ThisDrawing.Blocks.Add(insertionPnt, "CircleBlock")
     
        ' Add a circle to the block
        Dim circleObj As AcadCircle
        Dim center(0 To 2) As Double
        Dim radius As Double
        center(0) = 0
        center(1) = 0
        center(2) = 0
        rad = 2
        Set circleObj = blockObj.AddCircle(center, rad)
     
        ' Insert the block
        Dim blockRefObj As AcadBlockReference
        insertionPnt(0) = 0
        insertionPnt(1) = 0
        insertionPnt(2) = 0
        Set blockRefObj = ThisDrawing.ModelSpace.InsertBlock(insertionPnt, "CircleBlock", 1, 1, 1, 0)
    
        ' Explode the block reference
        Dim explodedObjects As Variant
        explodedObjects = blockRefObj.Explode
     
        ' Loop through the exploded objects
        Dim I As Integer
        For I = 0 To UBound(explodedObjects)
            explodedObjects(I).Color = acRed
            explodedObjects(I).Update
            MsgBox "Exploded Object " & I & ": " & explodedObjects(I).ObjectName
        Next
    End Sub
