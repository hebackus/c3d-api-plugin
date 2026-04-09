<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Advanced Drawing and Organizational Techniques (.NET) > Use Blocks and Attributes (.NET) > Work with Blocks (.NET) > Define Blocks (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-DF67671C-101D-4917-808B-DD2C5BE3C7E9.htm -->

# Define Blocks (.NET)

To create a new block, create a new BlockTableRecord object and use the Add method to append it to the BlockTable object. Once you create a BlockTableRecord object, use the Name property to assign a name to the block and the objects to be displayed when the block is inserted into the drawing with the AppendEntity method. 

You then add any geometrical object, or another block, to the newly created BlockTableRecord object. Objects are added to the BlockTableRecord object with the AppendEntity method. You can then insert an instance of the block into the drawing by creating a new BlockReference object and appending it to model space or the BlockTableRecord object that is associated with a Layout object. An inserted block is an object called a block reference. 

You can also create a block by using the WBlock method to write objects out to a separate drawing file. The drawing file can then be used as a block definition for other drawings. AutoCAD considers any drawing you insert into another drawing to be a block. 

For more information on defining blocks, see “About Defining Blocks” in the product Help system. 

## Define a block

This example defines a block and adds a circle to the block definition. It then inserts the block into the drawing as a block reference. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    
    [CommandMethod("CreatingABlock")]
    public void CreatingABlock()
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
    
    <CommandMethod("CreatingABlock")> _
    Public Sub CreatingABlock()
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
                    End Using
                End Using
            End If
    
            ' Save the new object to the database
            acTrans.Commit()
    
            ' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CreatingABlock()
        ' Define the block
        Dim blockObj As AcadBlock
        Dim insertionPnt(0 To 2) As Double
        insertionPnt(0) = 0
        insertionPnt(1) = 0
        insertionPnt(2) = 0
        Set blockObj = ThisDrawing.Blocks.Add(insertionPnt, "CircleBlock")
    
        ' Add a circle to the block
        Dim center(0 To 2) As Double
        Dim radius As Double
        center(0) = 0
        center(1) = 0
        center(2) = 0
        rad = 2
        blockObj.AddCircle(center, rad)
    End Sub
