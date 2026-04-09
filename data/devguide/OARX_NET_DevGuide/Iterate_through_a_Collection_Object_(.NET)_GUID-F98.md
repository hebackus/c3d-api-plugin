<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Basics of the AutoCAD .NET API (.NET) > Collection Objects (.NET) > Iterate through a Collection Object (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-F98FAC6B-4DC4-489E-B65E-5D8C5E64E534.htm -->

# Iterate through a Collection Object (.NET)

To select a specific member of a Collection object, use the Item or GetAt method. The Item and GetAt methods require a key in the form of a string in which represents the name of the item. With most collections, the Item method is implied, meaning you do not actually need to use method. 

With some Collection objects, you can also use an index number to specify the location of the item within the collection you want to retrieve. The method you can use varies based on the language you are using as well as if you are working with a symbol table or dictionary. 

The following statements show how to access the “MyLayer” table record in Layer symbol table. 

## C#
    
    
    acObjId = acLyrTbl["MyLayer"];

## VB.NET
    
    
    acObjId = acLyrTbl.Item("MyLayer")
     
    acObjId = acLyrTbl("MyLayer")

## VBA/ActiveX Code Reference
    
    
    acLayer = ThisDrawing.Layers.Item("MyLayer")
     
    acLayer = ThisDrawing.Layers("MyLayer")

## Iterate through the LayerTable object

The following example iterates through the LayerTable object and displays the names of all its layer table records: 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("IterateLayers")]
    public static void IterateLayers()
    {
      // Get the current document and database, and start a transaction
      Document acDoc = Application.DocumentManager.MdiActiveDocument;
      Database acCurDb = acDoc.Database;
     
      using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
      {
          // This example returns the layer table for the current database
          LayerTable acLyrTbl;
          acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId,
                                       OpenMode.ForRead) as LayerTable;
     
          // Step through the Layer table and print each layer name
          foreach (ObjectId acObjId in acLyrTbl)
          {
              LayerTableRecord acLyrTblRec;
              acLyrTblRec = acTrans.GetObject(acObjId,
                                              OpenMode.ForRead) as LayerTableRecord;
     
              acDoc.Editor.WriteMessage("\n" + acLyrTblRec.Name);
          }
     
          // Dispose of the transaction
      }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("IterateLayers")> _
    Public Sub IterateLayers()
      '' Get the current document and database, and start a transaction
      Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
      Dim acCurDb As Database = acDoc.Database
     
      Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
          '' This example returns the layer table for the current database
          Dim acLyrTbl As LayerTable
          acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId, _
                                       OpenMode.ForRead)
     
          '' Step through the Layer table and print each layer name
          For Each acObjId As ObjectId In acLyrTbl
              Dim acLyrTblRec As LayerTableRecord
              acLyrTblRec = acTrans.GetObject(acObjId, OpenMode.ForRead)
     
              acDoc.Editor.WriteMessage(vbLf & acLyrTblRec.Name)
          Next
     
          '' Dispose of the transaction
      End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub IterateLayers()
        ' Iterate through the collection
        On Error Resume Next
     
        Dim lay As AcadLayer
        Dim msg As String
        msg = ""
        For Each lay In ThisDrawing.Layers
            msg = msg + lay.Name + vbCrLf
        Next
     
        ThisDrawing.Utility.prompt msg
    End Sub

## Find the layer table record named MyLayer in the LayerTable object

The following example checks the LayerTable object to determine if the layer named MyLayer exists or not, and displays the appropriate message: 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("FindMyLayer")]
    public static void FindMyLayer()
    {
      // Get the current document and database, and start a transaction
      Document acDoc = Application.DocumentManager.MdiActiveDocument;
      Database acCurDb = acDoc.Database;
     
      using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
      {
          // Returns the layer table for the current database
          LayerTable acLyrTbl;
          acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId,
                                       OpenMode.ForRead) as LayerTable;
     
          // Check to see if MyLayer exists in the Layer table
          if (acLyrTbl.Has("MyLayer") != true)
          {
              acDoc.Editor.WriteMessage("\n'MyLayer' does not exist");
          }
          else
          {
              acDoc.Editor.WriteMessage("\n'MyLayer' exists");
          }
     
          // Dispose of the transaction
      }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("FindMyLayer")> _
    Public Sub FindMyLayer()
      '' Get the current document and database, and start a transaction
      Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
      Dim acCurDb As Database = acDoc.Database
     
      Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
          '' Returns the layer table for the current database
          Dim acLyrTbl As LayerTable
          acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId, _
                                       OpenMode.ForRead)
     
          '' Check to see if MyLayer exists in the Layer table
          If Not acLyrTbl.Has("MyLayer") Then
              acDoc.Editor.WriteMessage(vbLf & "'MyLayer' does not exist")
          Else
              acDoc.Editor.WriteMessage(vbLf & "'MyLayer' exists")
          End If
     
          '' Dispose of the transaction
      End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub FindMyLayer()
        ' Use the Item method to find a layer named MyLayer
        On Error Resume Next
        Dim ABCLayer As AcadLayer
        Set ABCLayer = ThisDrawing.Layers("MyLayer")
        If Err <> 0 Then
            ThisDrawing.Utility.prompt "'MyLayer' does not exist"
        Else
            ThisDrawing.Utility.prompt "'MyLayer' exists"
        End If
    End Sub
