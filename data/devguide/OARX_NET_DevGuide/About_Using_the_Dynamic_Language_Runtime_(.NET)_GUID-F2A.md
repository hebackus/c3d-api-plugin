<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Open and Close Objects (.NET) > About Using the Dynamic Language Runtime (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-F2A96EC2-B693-498E-8425-258A0CE3653F.htm -->

# About Using the Dynamic Language Runtime (.NET)

The AutoCAD Managed .NET API allows you to utilize the Dynamic Language Runtime (DLR) that was introduced with .NET 4.0. 

Using DLR allows you to access objects directly without having to: 

  * Open an object for read or write, and then close the object once you are done. 
  * Utilize transactions to commit the changes made. 

You can access the properties and methods of an object directly once you have obtained its ObjectId when using DLR. After you have obtained an ObjectId, you can assign the ObjectId to a variable of the data type: 

  * Object in VB.NET 
  * dynamic in C# 

Obtaining an ObjectId varies by how the object is saved to the database. For objects stored in a table or dictionary, you can access its ObjectId by: 

  * Using the Item method of an ObjectId to access an element in the collection. 
  * Creating a reference to the ObjectId of the table or dictionary and assigning it to a variable, and then accessing the element of the array. 

The following sample code shows both options for accessing an object that is stored in a table or dictionary with DLR: 

### C#
    
    
    // Item method
    dynamic acCurDb = HostApplicationServices.WorkingDatabase;
    dynamic acMSpace = acCurDb.BlockTableId.Item(BlockTableRecord.ModelSpace);
    
    // Reference an element directly from a collection
    dynamic acCurDb = HostApplicationServices.WorkingDatabase;
    dynamic acBlkTbl = acCurDb.BlockTableId;
    dynamic acMSpace = acBlkTbl[BlockTableRecord.ModelSpace];

### VB.NET
    
    
    '' Item method
    Dim acCurDb As Object = HostApplicationServices.WorkingDatabase
    Dim acMSpace As Object = acCurDb.BlockTableId.Item(BlockTableRecord.ModelSpace)
    
    '' Reference an element directly from a collection
    Dim acCurDb As Object = HostApplicationServices.WorkingDatabase
    Dim acBlkTbl As Object = acCurDb.BlockTableId
    Dim acMSpace As Object = acBlkTbl(BlockTableRecord.ModelSpace)

Important: When working with DLR and C#, you will need to reference the Microsoft.CSharp library. 

## Working with the GetEnumerator Method

When using the GetEnumerator method with DLR, you need to explicitly dispose of the enumerator object once you are done working with it. The following sample demonstrates how to dispose of the enumerator when you are done with it. 

### C#
    
    
    dynamic acCurDb = HostApplicationServices.WorkingDatabase;
    var acLtypeTbl = acCurDb.LinetypeTableId;
    var acTblEnum = acLtypeTbl.GetEnumerator();
    ...
    acTblEnum.Dispose();

### VB.NET
    
    
    Dim acCurDb As Object = HostApplicationServices.WorkingDatabase
    Dim acLtypeTbl As Object = acCurDb.LinetypeTableId
    Dim acTblEnum As Object = acLtypeTbl.GetEnumerator()
    ...
    acTblEnum.Dispose()

## Using LINQ Queries

You can utilize LINQ queries to query the contents of a table or dictionary in a drawing with DLR. The following sample demonstrates the use of LINQ queries to query which layers have certain states assigned to them in the current drawing. 

### C#
    
    
    [CommandMethod("LINQ")]
    public static void LINQExample()
    {
        dynamic db = HostApplicationServices.WorkingDatabase;
        dynamic doc = Application.DocumentManager.MdiActiveDocument;
    
        var layers = db.LayerTableId;
        for (int i = 0; i < 2; i++)
        {
            var newrec = layers.Add(new LayerTableRecord());
            newrec.Name = "Layer" + i.ToString();
            if (i == 0)
                newrec.IsFrozen = true;
            if (i == 1)
                newrec.IsOff = true;
        }
    
        var OffLayers = from l in (IEnumerable<dynamic>)layers
                        where l.IsOff
                        select l;
    
        doc.Editor.WriteMessage("\nLayers Turned Off:");
    
        foreach (dynamic rec in OffLayers)
            doc.Editor.WriteMessage("\n - " + rec.Name);
    
        var frozenOrOffNames = from l in (IEnumerable<dynamic>)layers
                                where l.IsFrozen == true || l.IsOff == true
                                select l;
    
        doc.Editor.WriteMessage("\nLayers Frozen or Turned Off:");
    
        foreach (dynamic rec in frozenOrOffNames)
            doc.Editor.WriteMessage("\n - " + rec.Name);
    }

### VB.NET
    
    
    <CommandMethod("LINQ")> _
    Public Sub LINQExample()
        Dim db As Object = HostApplicationServices.WorkingDatabase
        Dim doc As Object = Application.DocumentManager.MdiActiveDocument
    
        Dim layers = db.LayerTableId
        For i As Integer = 0 To 2
            Dim newrec As Object = layers.Add(New LayerTableRecord())
            newrec.Name = "Layer" + i.ToString()
    
            If i = 0 Then newrec.IsFrozen = True
            If i = 1 Then newrec.IsOff = True
        Next
    
        Dim OffLayers = From l In CType(CTypeDynamic(layers, GetType(IEnumerable(Of Object))),  _
                                  IEnumerable(Of Object))
                               Where l.IsOff
                               Select l
    
        doc.Editor.WriteMessage(vbLf + "Layers Turned Off:")
    
        For Each rec As Object In OffLayers
            doc.Editor.WriteMessage(vbLf + " - " + rec.Name)
        Next
    
        Dim frozenOrOffNames = From l In CType(CTypeDynamic(layers, GetType(IEnumerable(Of Object))),  _
                                         IEnumerable(Of Object))
                                      Where l.IsFrozen = True Or l.IsOff = True
                                      Select l
    
        doc.Editor.WriteMessage(vbLf + "Layers Frozen or Turned Off:")
    
        For Each rec As Object In frozenOrOffNames
            doc.Editor.WriteMessage(vbLf + " - " + rec.Name)
        Next
    End Sub

## Sample Code

The sample code on this page uses the following name spaces: 
    
    
    Autodesk.AutoCAD.Runtime
    Autodesk.AutoCAD.ApplicationServices
    Autodesk.AutoCAD.DatabaseServices
    Autodesk.AutoCAD.Colors
    Autodesk.AutoCAD.Geometry

The following sample code demonstrates how to add a Line to the current space; without and with DLR. 

### C# without Dynamic Language Runtime (DLR)
    
    
    [CommandMethod("ADDLINE")]
    public static void AddLine()
    {
        // Get the current database
        Database acCurDb = HostApplicationServices.WorkingDatabase;
    
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
    
            // Create a line that starts at 5,5 and ends at 12,3
            using (Line acLine = new Line(new Point3d(5, 5, 0),
                                          new Point3d(12, 3, 0)))
            {
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acLine);
                acTrans.AddNewlyCreatedDBObject(acLine, true);
            }
    
            // Save the new object to the database
            acTrans.Commit();
        }
    }

### C# with Dynamic Language Runtime (DLR)
    
    
    [CommandMethod("ADDLINE")]
    public static void AddLine()
    {
        // Get the current database
        dynamic acCurDb = HostApplicationServices.WorkingDatabase;
    
        // Create a dynamic reference to model or paper space
        dynamic acSpace = acCurDb.CurrentSpaceId;
    
        // Create a line that starts at 5,5 and ends at 12,3
        dynamic acLine = new Line(new Point3d(5, 5, 0),
                                  new Point3d(12, 3, 0));
    
        // Add the new object to the current space
        acSpace.AppendEntity(acLine);
    }

### VB.NET without Dynamic Language Runtime (DLR)
    
    
    <CommandMethod("ADDLINE")> _
    Public Sub AddLine()
        '' Get the current database
        Dim acCurDb As Database = HostApplicationServices.WorkingDatabase
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            '' Open the current space for write
            Dim acSpace As BlockTableRecord
            acSpace = acTrans.GetObject(acCurDb.CurrentSpaceId, _
                                        OpenMode.ForWrite)
    
            '' Create a line that starts at 5,5 and ends at 12,3
            Using acLine As Line = New Line(New Point3d(5, 5, 0),
                                            New Point3d(12, 3, 0))
    
                '' Add the new object to the block table record and the transaction
                acSpace.AppendEntity(acLine)
                acTrans.AddNewlyCreatedDBObject(acLine, True)
            End Using
    
            '' Save the new object to the database
            acTrans.Commit()
        End Using
    End Sub

### VB.NET with Dynamic Language Runtime (DLR)
    
    
    <CommandMethod("ADDLINE")> _
    Public Sub AddLine()
        '' Get the current database
        Dim acCurDb As Object = HostApplicationServices.WorkingDatabase
    
        '' Create a dynamic reference to model or paper space
        Dim acSpace As Object = acCurDb.CurrentSpaceId
    
        '' Create a line that starts at 5,5 and ends at 12,3
        Dim acLine As Object = New Line(New Point3d(5, 5, 0),
                                        New Point3d(12, 3, 0))
    
        '' Add the new object to the current space
        acSpace.AppendEntity(acLine)
    End Sub

The following sample code demonstrates how to add a Layer to the current database; without and with DLR. 

### C# without Dynamic Language Runtime (DLR)
    
    
    [CommandMethod("ADDLAYER")]
    public static void AddLayer()
    {
        // Get the current database
        Database acCurDb = HostApplicationServices.WorkingDatabase;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Returns the layer table for the current database
            LayerTable acLyrTbl;
            acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId,
                                         OpenMode.ForRead) as LayerTable;
    
            // Check to see if MyLayer exists in the Layer table
            if (acLyrTbl.Has("MyLayer") != true)
            {
                // Open the Layer Table for write
                acTrans.GetObject(acCurDb.LayerTableId, OpenMode.ForWrite);
    
                // Create a new layer named "MyLayer"
                using (LayerTableRecord acLyrTblRec = new LayerTableRecord())
                {
                    acLyrTblRec.Name = "MyLayer";
    
                    // Assign the ACI color 3 to the new layer
                    Color acClr = Color.FromColorIndex(ColorMethod.ByAci, 3);
                    acLyrTblRec.Color = acClr;
    
                    // Add the new layer table record to the layer table and the transaction
                    acLyrTbl.Add(acLyrTblRec);
                    acTrans.AddNewlyCreatedDBObject(acLyrTblRec, true);
                }
    
                // Commit the changes
                acTrans.Commit();
            }
    
            // Dispose of the transaction
        }
    }

### C# with Dynamic Language Runtime (DLR)
    
    
    [CommandMethod("ADDLAYER")]
    public static void AddLayer()
    {
        // Get the current database
        dynamic acCurDb = HostApplicationServices.WorkingDatabase;
    
        dynamic acLyrTbl = acCurDb.LayerTableId;
    
        // Check to see if MyLayer exists in the Layer table
        if (acLyrTbl.Has("MyLayer") != true)
        {
            // Create a new layer named "MyLayer"
            dynamic acLyrTblRec = new LayerTableRecord();
            acLyrTblRec.Name = "MyLayer";
    
            // Assign the ACI color 3 to the new layer
            dynamic acClr = Color.FromColorIndex(ColorMethod.ByAci, 3);
            acLyrTblRec.Color = acClr;
    
            // Add the new layer table record to the layer table
            acLyrTbl.Add(acLyrTblRec);
        }
    }

### VB.NET without Dynamic Language Runtime (DLR)
    
    
    <CommandMethod("ADDLAYER")> _
    Public Sub AddLayer()
        '' Get the current database
        Dim acCurDb As Database = HostApplicationServices.WorkingDatabase
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            '' Returns the layer table for the current database
            Dim acLyrTbl As LayerTable
            acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId, OpenMode.ForRead)
    
            '' Check to see if MyLayer exists in the Layer table
            If Not acLyrTbl.Has("MyLayer") Then
                '' Open the Layer Table for write
                acTrans.GetObject(acCurDb.LayerTableId, OpenMode.ForWrite)
    
                '' Create a new layer named "MyLayer"
                Using acLyrTblRec As LayerTableRecord = New LayerTableRecord()
                    acLyrTblRec.Name = "MyLayer"
    
                    '' Assign the ACI color 3 to the new layer
                    Dim acClr As Color = Color.FromColorIndex(ColorMethod.ByAci, 3)
                    acLyrTblRec.Color = acClr
    
                    '' Add the new layer table record to the layer table and the transaction
                    acLyrTbl.Add(acLyrTblRec)
                    acTrans.AddNewlyCreatedDBObject(acLyrTblRec, True)
                End Using
    
                '' Commit the changes
                acTrans.Commit()
            End If
    
            '' Dispose of the transaction
        End Using
    End Sub

### VB.NET with Dynamic Language Runtime (DLR)
    
    
    <CommandMethod("ADDLAYER")> _
    Public Sub AddLayer()
        '' Get the current database
        Dim acCurDb As Object = HostApplicationServices.WorkingDatabase
    
        Dim acLyrTbl As Object = acCurDb.LayerTableId
    
        '' Check to see if MyLayer exists in the Layer table
        If Not acLyrTbl.Has("MyLayer") Then
            '' Create a new layer named "MyLayer"
            Dim acLyrTblRec As LayerTableRecord = New LayerTableRecord()
            acLyrTblRec.Name = "MyLayer"
    
            '' Assign the ACI color 3 to the new layer
            Dim acClr As Color = Color.FromColorIndex(ColorMethod.ByAci, 3)
            acLyrTblRec.Color = acClr
    
            '' Add the new layer table record to the layer table
            acLyrTbl.Add(acLyrTblRec)
        End If
    End Sub

The following demonstrates how to step through and list all the objects in the current space; without and with DLR. 

### C# without Dynamic Language Runtime (DLR)
    
    
    [CommandMethod("LISTOBJECTS")]
    public static void ListObjects()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = HostApplicationServices.WorkingDatabase;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Block table record Model space for write
            BlockTableRecord acSpace;
            acSpace = acTrans.GetObject(acCurDb.CurrentSpaceId,
                                        OpenMode.ForRead) as BlockTableRecord;
    
            // Step through the current space
            foreach (ObjectId objId in acSpace)
            {
                // Display the class and current layer of the object
                Entity acEnt = (Entity)acTrans.GetObject(objId, OpenMode.ForRead);
                acDoc.Editor.WriteMessage("\nObject Class: " + acEnt.GetRXClass().Name +
                                          "\nCurrent Layer: " + acEnt.Layer + 
                                           "\n");
            }
            acTrans.Commit();
        }
    }

### C# with Dynamic Language Runtime (DLR)
    
    
    [CommandMethod("LISTOBJECTS")]
    public static void ListObjects()
    {
        // Get the current document and database
        dynamic acDoc = Application.DocumentManager.MdiActiveDocument;
        dynamic acCurDb = HostApplicationServices.WorkingDatabase;
    
        // Create a dynamic reference to model or paper space
        dynamic acSpace = acCurDb.CurrentSpaceId;
    
        // Step through the current space
        foreach (dynamic acEnt in acSpace)
        {
            // Display the class and current layer of the object
            acDoc.Editor.WriteMessage("\nObject Class: " + acEnt.GetRXClass().Name +
                                      "\nCurrent Layer: " + acEnt.Layer +
                                      "\n");
        }
    }

### VB.NET without Dynamic Language Runtime (DLR)
    
    
    <CommandMethod("LISTOBJECTS")> _
    Public Sub ListObjects()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = HostApplicationServices.WorkingDatabase
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            '' Open the Block table record Model space for write
            Dim acSpace As BlockTableRecord
            acSpace = acTrans.GetObject(acCurDb.CurrentSpaceId, OpenMode.ForRead)
    
            '' Step through the current space
            For Each objId As ObjectId In acSpace
                '' Display the class and current layer of the object
                Dim acEnt As Entity = acTrans.GetObject(objId, OpenMode.ForRead)
    
                acDoc.Editor.WriteMessage(vbCrLf + "Object Class: " + acEnt.GetRXClass().Name + _
                                          vbCrLf + "Current Layer: " + acEnt.Layer + _
                                          vbCrLf)
            Next objId
    
            acTrans.Commit()
        End Using
    End Sub

### VB.NET with Dynamic Language Runtime (DLR)
    
    
    <CommandMethod("LISTOBJECTS")> _
    Public Sub ListObjects()
        '' Get the current document and database
        Dim acDoc As Object = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Object = HostApplicationServices.WorkingDatabase
    
        '' Create a dynamic reference to model or paper space
        Dim acSpace As Object = acCurDb.CurrentSpaceId
    
        '' Step through the current space
        For Each acEnt As Object In CTypeDynamic(acSpace, GetType(System.Collections.IEnumerable))
            '' Display the class and current layer of the object
            acDoc.Editor.WriteMessage(vbCrLf + "Object Class: " + acEnt.GetRXClass().Name + _
                                      vbCrLf + "Current Layer: " + acEnt.Layer + _
                                      vbCrLf)
        Next acEnt
    End Sub
