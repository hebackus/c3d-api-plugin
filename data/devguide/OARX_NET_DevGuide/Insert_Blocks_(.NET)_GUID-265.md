<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Advanced Drawing and Organizational Techniques (.NET) > Use Blocks and Attributes (.NET) > Work with Blocks (.NET) > Insert Blocks (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-2656E245-6EAA-41A3-ABE9-742868182821.htm -->

# Insert Blocks (.NET)

You can insert blocks defined in the block table of the current drawing after creating a BlockReference object and then appending it to a BlockTableRecord object with the AppendEntity method. When you create a new BlockReference, you pass the constructor the origin for the block reference to be inserted at and the ObjectID of the BlockTableRecord object the geometry should be inherited from. 

You can also insert an entire drawing file into the current drawing by using the ReadDwgFile method to open a drawing file in memory, and then use the Insert method to insert the drawing in memory into the current drawing. When you insert an entire drawing into another drawing, AutoCAD treats the inserted drawing like any other block reference. Subsequent insertions reference the block definition (which contains the geometric description of the block) with different position, scale, and rotation settings. 

If you change the original drawing after inserting it, the changes have no effect on the inserted block. If you want the inserted block to reflect the changes you made to the original drawing, you can redefine the block by reinserting the original drawing. 

By default, AutoCAD uses the coordinate (0, 0, 0) as the base point when inserting a drawing file. You can change the base point of a drawing by opening the original drawing and using the SetSystemVariable method to specify a different insertion base point for the INSBASE system variable. AutoCAD uses the new base point the next time you insert the drawing. 

If the drawing you insert contains PaperSpace objects, those objects are not included in the current drawing's block definition. To use the PaperSpace objects in another drawing, open the original drawing and define the PaperSpace objects as a block. You can insert the drawing into another drawing in either paper space or model space. 

A block reference cannot be iterated to find the original objects that compose it. However, you can iterate the original block definition, or you can explode the block reference into its original components. 

You can also insert an array of blocks using the MInsertBlock object. This object type does not insert a single block into your drawing, as using the BlockReference object does, but instead inserts an array of the specified block. 

For more information on inserting blocks, see “About Inserting Blocks” in the product Help system. 

## Define and insert a block

This example defines a block and adds a circle to the block definition. It then inserts the block into the drawing as a block reference. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    
    [CommandMethod("InsertingABlock")]
    public void InsertingABlock()
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
    
    <CommandMethod("InsertingABlock")> _
    Public Sub InsertingABlock()
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
                End Using
            End If
    
            ' Save the new object to the database
            acTrans.Commit()
    
            ' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub InsertingABlock()
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
    End Sub
