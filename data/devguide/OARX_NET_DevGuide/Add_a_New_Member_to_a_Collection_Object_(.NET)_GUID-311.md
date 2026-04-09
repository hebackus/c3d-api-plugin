<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Basics of the AutoCAD .NET API (.NET) > Collection Objects (.NET) > Add a New Member to a Collection Object (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-31193942-2AEB-4BFF-A861-6279EE8394A2.htm -->

# Add a New Member to a Collection Object (.NET)

To add a new member to the collection, use the Add method. For example, the following code creates a new layer and adds it to the Layer table: 

## C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("AddMyLayer")]
    public static void AddMyLayer()
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
              // Open the Layer Table for write
              acTrans.GetObject(acCurDb.LayerTableId, OpenMode.ForWrite);
     
              // Create a new layer table record and name the layer "MyLayer"
              using (LayerTableRecord acLyrTblRec = new LayerTableRecord())
              {
                  acLyrTblRec.Name = "MyLayer";
     
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

## VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("AddMyLayer")> _
    Public Sub AddMyLayer()
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
              '' Open the Layer Table for write
              acTrans.GetObject(acCurDb.LayerTableId, OpenMode.ForWrite)
     
              '' Create a new layer table record and name the layer "MyLayer"
              Using acLyrTblRec As LayerTableRecord = New LayerTableRecord
                  acLyrTblRec.Name = "MyLayer"
     
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

## VBA/ActiveX Code Reference
    
    
    Sub AddMyLayer()
        Dim newLayer as AcadLayer
        Set newLayer = ThisDrawing.Layers.Add("MyLayer")
    End Sub
