<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Open and Close Objects (.NET) > Open and Close Objects Without the Transaction Manager (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-BF06F786-DDA6-4603-B5E5-25A35A4130A3.htm -->

# Open and Close Objects Without the Transaction Manager (.NET)

Transactions make it easier to open and work with multiple objects, but they are not the only way to open and edit objects. Other than using a transaction, you can open and close objects using the Open and Close methods. You still need to obtain an object Id to use the Open method. Like the GetObject method used with transactions, you need to specify an open mode and the return value is an object. 

If you make changes to an object after you opened it with the Open method, you can use the Cancel method to rollback all the changes made since it was opened. Cancel must be called on each object in which you want to rollback. Objects must also be properly disposed of with the Dispose method after an object is closed or you can use the Using statement to close and dispose of an object. 

Note: Objects must be paired with an open and close operation. If you use the Open method without the Using statement, you must call either the Close or Cancel method on an opened object. Failure to close an object will lead to read access violations and cause AutoCAD to become unstable. 

If you need to work with a single object, using the Open and Close methods can reduce the number of lines of code that you might otherwise have to write compared to working with the Transaction Manager. However, using transactions is the recommended way of opening and closing objects. 

Caution: You should not directly use the Open and Close methods when using transactions, as objects might not get opened or closed properly by the Transaction Manager which could cause AutoCAD to become unstable. Instead, use the StartOpenCloseTransation method to create an OpenCloseTransaction object which wraps the Open and Close methods. 

## Query objects (manually open and close objects)

This example demonstrates how to manually open and close objects without using a transaction and the GetObject method. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("OpenCloseObjectId")]
    public static void OpenCloseObjectId()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Open the Block table for read
        BlockTable acBlkTbl = null;
    
        try
        {
            acBlkTbl = acCurDb.BlockTableId.Open(OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Model space for read
            BlockTableRecord acBlkTblRec = null;
    
            try
            {
                acBlkTblRec = acBlkTbl[BlockTableRecord.ModelSpace].Open(OpenMode.ForRead) as BlockTableRecord;
    
                // Step through the Block table record
                foreach (ObjectId acObjId in acBlkTblRec)
                {
                    acDoc.Editor.WriteMessage("\nDXF name: " + acObjId.ObjectClass.DxfName);
                    acDoc.Editor.WriteMessage("\nObjectID: " + acObjId.ToString());
                    acDoc.Editor.WriteMessage("\nHandle: " + acObjId.Handle.ToString());
                    acDoc.Editor.WriteMessage("\n");
                }
            }
            catch (Autodesk.AutoCAD.Runtime.Exception es)
            {
                System.Windows.Forms.MessageBox.Show(es.Message);
            }
            finally
            {
                // Close the Block table
                if (!acBlkTblRec.ObjectId.IsNull)
                {
                    // Close the Block table record
                    acBlkTblRec.Close();
                    acBlkTblRec.Dispose();
                }
            }
        }
        catch (Autodesk.AutoCAD.Runtime.Exception es)
        {
            System.Windows.Forms.MessageBox.Show(es.Message);
        }
        finally
        {
            // Close the Block table
            if (!acBlkTbl.ObjectId.IsNull)
            {
                acBlkTbl.Close();
                acBlkTbl.Dispose();
            }
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("OpenCloseObjectId")> _
    Public Sub OpenCloseObjectId()
        ' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        ' Open the Block table for read
        Dim acBlkTbl As BlockTable = Nothing
    
        Try
            acBlkTbl = acCurDb.BlockTableId.Open(OpenMode.ForRead)
    
            ' Open the Block table record Model space for read
            Dim acBlkTblRec As BlockTableRecord = Nothing
    
            Try
                acBlkTblRec = acBlkTbl(BlockTableRecord.ModelSpace).Open(OpenMode.ForRead)
    
                ' Step through the Block table record
                For Each acObjId As ObjectId In acBlkTblRec
                    acDoc.Editor.WriteMessage(vbLf & "DXF name: " & acObjId.ObjectClass().DxfName)
                    acDoc.Editor.WriteMessage(vbLf & "ObjectID: " & acObjId.ToString())
                    acDoc.Editor.WriteMessage(vbLf & "Handle: " & acObjId.Handle.ToString())
                    acDoc.Editor.WriteMessage(vbLf)
                Next
            Catch es As Autodesk.AutoCAD.Runtime.Exception
                MsgBox(es.Message)
            Finally
                ' Close the Block table record
                If Not acBlkTbl.ObjectId.IsNull Then
                    acBlkTblRec.Close()
                    acBlkTblRec.Dispose()
                End If
            End Try
    
        Catch es As Autodesk.AutoCAD.Runtime.Exception
            MsgBox(es.Message)
        Finally
            ' Close the Block table
            If Not acBlkTbl.ObjectId.IsNull Then
                acBlkTbl.Close()
                acBlkTbl.Dispose()
            End If
        End Try
    End Sub

## Query objects (Using statement)

The following example demonstrates how to open and close objects with the Using statement instead of manually closing and disposing of objects. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("OpenCloseObjectIdWithUsing")]
    public static void OpenCloseObjectIdWithUsing()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Open the Block table for read
        using (BlockTable acBlkTbl = acCurDb.BlockTableId.Open(OpenMode.ForRead) as BlockTable)
        {
            // Open the Block table record Model space for read
            using (BlockTableRecord acBlkTblRec = acBlkTbl[BlockTableRecord.ModelSpace].Open(OpenMode.ForRead)
                                                    as BlockTableRecord)
            {
                // Step through the Block table record
                foreach (ObjectId acObjId in acBlkTblRec)
                {
                    acDoc.Editor.WriteMessage("\nDXF name: " + acObjId.ObjectClass.DxfName);
                    acDoc.Editor.WriteMessage("\nObjectID: " + acObjId.ToString());
                    acDoc.Editor.WriteMessage("\nHandle: " + acObjId.Handle.ToString());
                    acDoc.Editor.WriteMessage("\n");
                }
    
            // Close the Block table record
            }
    
            // Close the Block table
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("OpenCloseObjectIdWithUsing")> _
    Public Sub OpenCloseObjectIdWithUsing()
        ' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        ' Open the Block table for read
        Using acBlkTbl As BlockTable = acCurDb.BlockTableId.Open(OpenMode.ForRead)
    
            ' Open the Block table record Model space for read
            Using acBlkTblRec As BlockTableRecord = acBlkTbl(BlockTableRecord.ModelSpace).Open(OpenMode.ForRead)
    
                ' Step through the Block table record
                For Each acObjId As ObjectId In acBlkTblRec
                    acDoc.Editor.WriteMessage(vbLf & "DXF name: " & acObjId.ObjectClass().DxfName)
                    acDoc.Editor.WriteMessage(vbLf & "ObjectID: " & acObjId.ToString())
                    acDoc.Editor.WriteMessage(vbLf & "Handle: " & acObjId.Handle.ToString())
                    acDoc.Editor.WriteMessage(vbLf)
                Next
    
                ' Close the Block table record
            End Using
    
            ' Close the Block table
        End Using
    End Sub

## Add a new object to the database

This example demonstrates how to create a new object and append it to Model space without using the Transaction Manager. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("AddNewCircleOpenClose")]
    public static void AddNewCircleOpenClose()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Open the Block table for read
        using (BlockTable acBlkTbl = acCurDb.BlockTableId.Open(OpenMode.ForRead) as BlockTable)
        {
            // Open the Block table record Model space for write
            using (BlockTableRecord acBlkTblRec = acBlkTbl[BlockTableRecord.ModelSpace].Open(OpenMode.ForWrite)
                                                    as BlockTableRecord)
            {
                // Create a circle with a radius of 3 at 5,5
                using (Circle acCirc = new Circle())
                {
                    acCirc.Center = new Point3d(5, 5, 0);
                    acCirc.Radius = 3;
    
                    // Add the new object to Model space and the transaction
                    acBlkTblRec.AppendEntity(acCirc);
    
                    // Close and dispose the circle object
                }
    
                // Close the Block table record
            }
    
            // Close the Block table
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("AddNewCircleOpenClose")> _
    Public Sub AddNewCircleOpenClose()
        ' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        ' Open the Block table for read
        Using acBlkTbl As BlockTable = = acCurDb.BlockTableId.Open(OpenMode.ForRead)
    
            ' Open the Block table record Model space for write
            Using acBlkTblRec As BlockTableRecord = acBlkTbl(BlockTableRecord.ModelSpace).Open(OpenMode.ForWrite)
    
                ' Create a circle with a radius of 3 at 5,5
                Using acCirc As Circle = New Circle()
                    acCirc.Center = New Point3d(5, 5, 0)
                    acCirc.Radius = 3
    
                    ' Add the new object to Model space and the transaction
                    acBlkTblRec.AppendEntity(acCirc)
    
                    ' Close the circle object
                End Using
    
                ' Close the Block table record
            End Using
    
            ' Close the Block table
        End Using
    End Sub
