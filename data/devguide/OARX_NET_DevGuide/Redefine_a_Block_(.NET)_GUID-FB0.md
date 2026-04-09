<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Advanced Drawing and Organizational Techniques (.NET) > Use Blocks and Attributes (.NET) > Work with Blocks (.NET) > Redefine a Block (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-FB03D1E5-2C84-4078-92EF-9FB2D57CA1C5.htm -->

# Redefine a Block (.NET)

Use any of the Block object methods and properties to redefine a block. When you redefine a block, all the references to that block in the drawing are immediately updated to reflect the new definition. 

Redefinition affects previous and future insertions of a block. Constant attributes are lost and replaced by any new constant attributes. Variable attributes remain unchanged, even if the new block has no attributes. 

## Redefine the objects in a block definition

This example creates a block and adds a circle to the definition of the block. The block is then inserted into the drawing as a block reference. The circle in the block definition is updated, and the block reference is updated automatically. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    
    [CommandMethod("RedefiningABlock")]
    public void RedefiningABlock()
    {
        // Get the current database and start a transaction
        Database acCurDb;
        acCurDb = Application.DocumentManager.MdiActiveDocument.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Block table for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead) as BlockTable;
    
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
    
                        // Insert the block into the current space
                        using (BlockReference acBlkRef = new BlockReference(new Point3d(0, 0, 0), acBlkTblRec.Id))
                        {
                            BlockTableRecord acModelSpace;
                            acModelSpace = acTrans.GetObject(acCurDb.CurrentSpaceId, OpenMode.ForWrite) as BlockTableRecord;
    
                            acModelSpace.AppendEntity(acBlkRef);
                            acTrans.AddNewlyCreatedDBObject(acBlkRef, true);
    
                            Application.ShowAlertDialog("CircleBlock has been created.");
                        }
                    }
                }
            }
            else
            {
                // Redefine the block if it exists
                BlockTableRecord acBlkTblRec =
                    acTrans.GetObject(acBlkTbl["CircleBlock"], OpenMode.ForWrite) as BlockTableRecord;
    
                // Step through each object in the block table record
                foreach (ObjectId objID in acBlkTblRec)
                {
                    DBObject dbObj = acTrans.GetObject(objID, OpenMode.ForRead) as DBObject;
    
                    // Revise the circle in the block
                    if (dbObj is Circle)
                    {
                        Circle acCirc = dbObj as Circle;
    
                        acTrans.GetObject(objID, OpenMode.ForWrite);
                        acCirc.Radius = acCirc.Radius * 2;
                    }
                }
    
                // Update existing block references
                foreach (ObjectId objID in acBlkTblRec.GetBlockReferenceIds(false, true))
                {
                    BlockReference acBlkRef = acTrans.GetObject(objID, OpenMode.ForWrite) as BlockReference;
                    acBlkRef.RecordGraphicsModified(true);
                }
    
                Application.ShowAlertDialog("CircleBlock has been revised.");
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
    
    <CommandMethod("RedefiningABlock")> _
    Public Sub RedefiningABlock()
        ' Get the current database and start a transaction
        Dim acCurDb As Autodesk.AutoCAD.DatabaseServices.Database
        acCurDb = Application.DocumentManager.MdiActiveDocument.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            ' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead)
    
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
    
                        ' Insert the block into the current space
                        Using acBlkRef As New BlockReference(New Point3d(0, 0, 0), acBlkTblRec.Id)
    
                            Dim acModelSpace As BlockTableRecord
                            acModelSpace = acTrans.GetObject(acCurDb.CurrentSpaceId, OpenMode.ForWrite)
    
                            acModelSpace.AppendEntity(acBlkRef)
                            acTrans.AddNewlyCreatedDBObject(acBlkRef, True)
    
                            MsgBox("CircleBlock has been created.")
                        End Using
                    End Using
                End Using
            Else
                ' Redefine the block if it exists
                Dim acBlkTblRec As BlockTableRecord = _
                    acTrans.GetObject(acBlkTbl.Item("CircleBlock"), OpenMode.ForWrite)
    
                ' Step through each object in the block table record
                For Each objID As ObjectId In acBlkTblRec
    
                    Dim dbObj As DBObject = acTrans.GetObject(objID, OpenMode.ForRead)
    
                    ' Revise the circle in the block
                    If TypeOf dbObj Is Circle Then
                        Dim acCirc As Circle = dbObj
    
                        acTrans.GetObject(objID, OpenMode.ForWrite)
                        acCirc.Radius = acCirc.Radius * 2
                    End If
                Next
    
                ' Update existing block references
                For Each objID As ObjectId In acBlkTblRec.GetBlockReferenceIds(False, True)
                    Dim acBlkRef As BlockReference = acTrans.GetObject(objID, OpenMode.ForWrite)
                    acBlkRef.RecordGraphicsModified(True)
                Next
    
                MsgBox("CircleBlock has been revised.")
            End If
    
            ' Save the new object to the database
            acTrans.Commit()
    
            ' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub RedefiningABlock()
        ' Define the block
        Dim blockObj As AcadBlock
        Dim insertionPnt(0 To 2) As Double
        insertionPnt(0) = 0
        insertionPnt(1) = 0
        insertionPnt(2) = 0
        
        On Error Resume Next
        Set blockObj = Blocks("CircleBlock")
        Err.Clear
        
        If blockObj Is Nothing Then
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
            Set blockRefObj = ThisDrawing.ActiveLayout.Block.InsertBlock(insertionPnt, "CircleBlock", 1, 1, 1, 0)
        Else
            Set blockObj = ThisDrawing.Blocks.Item("CircleBlock")
            
            Dim acObj As AcadObject
            
            ' Redefine the circle objects in the block
            For Each acObj In blockObj
                If TypeOf acObj Is AcadCircle Then
                    Dim acCirc As AcadCircle
                    Set acCirc = acObj
                    acCirc.radius = acCirc.radius * 2
                End If
            Next
            
            ' Update the blocks in the drawing
            Regen acAllViewports
        End If
    End Sub
