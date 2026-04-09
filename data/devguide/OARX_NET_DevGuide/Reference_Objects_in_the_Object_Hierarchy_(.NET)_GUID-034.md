<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Basics of the AutoCAD .NET API (.NET) > Access the Object Hierarchy (.NET) > Reference Objects in the Object Hierarchy (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-034504F8-59F8-4D6D-8777-3EF8A9C251DF.htm -->

# Reference Objects in the Object Hierarchy (.NET)

When you work with objects in the AutoCAD .NET API, you can reference some objects directly or through a user-defined variable based on the object you are working with. To reference an objects directly, include the object in the calling hierarchy. For example, the following statement attaches a drawing file to the database of the current drawing. Notice that the hierarchy starts with the Application and then goes to the Database object. From the Database object, the AttachXref method is called: 

## C#
    
    
    string strFName, strBlkName;
    Autodesk.AutoCAD.DatabaseServices.ObjectId objId;
     
    strFName = "c:/clients/Proj 123/grid.dwg";
    strBlkName = System.IO.Path.GetFileNameWithoutExtension(strFName);
     
    objId = Application.DocumentManager.MdiActiveDocument.Database.AttachXref(strFName, strBlkName);

## VB.NET
    
    
    Dim strFName As String, strBlkName As String
    Dim objId As Autodesk.AutoCAD.DatabaseServices.ObjectId
     
    strFName = "c:\clients\Proj 123\grid.dwg"
    strBlkName = System.IO.Path.GetFileNameWithoutExtension(strFName)
     
    objId = Application.DocumentManager.MdiActiveDocument.Database.AttachXref(strFName, strBlkName)

To reference the objects through a user-defined variable, define the variable as the desired type, then set the variable to the appropriate object. For example, the following code defines a variable (acCurDb) of type Autodesk.AutoCAD.DatabaseServices.Database and sets the variable equal to the current database: 

## C#
    
    
    Autodesk.AutoCAD.DatabaseServices.Database acCurDb;
    acCurDb = Application.DocumentManager.MdiActiveDocument.Database;

## VB.NET
    
    
    Dim acCurDb As Autodesk.AutoCAD.DatabaseServices.Database
    acCurDb = Application.DocumentManager.MdiActiveDocument.Database

The following statement then attaches a drawing file to the database using the acCurDb user-defined variable: 

## C#
    
    
    string strFName, strBlkName;
    Autodesk.AutoCAD.DatabaseServices.ObjectId objId;
     
    strFName = "c:/clients/Proj 123/grid.dwg";
    strBlkName = System.IO.Path.GetFileNameWithoutExtension(strFName);
     
    objId = acCurDb.AttachXref(strFName, strBlkName);

## VB.NET
    
    
    Dim strFName As String, strBlkName As String
    Dim objId As Autodesk.AutoCAD.DatabaseServices.ObjectId
     
    strFName = "c:\clients\Proj 123\grid.dwg"
    strBlkName = System.IO.Path.GetFileNameWithoutExtension(strFName)
     
    objId = acCurDb.AttachXref(strFName, strBlkName)

## Retrieve entities from Model space

The following example returns the first entity object in Model space. Similar code can do the same for Paper space entities. Note that all graphical objects are defined as an Entity object: 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("ListEntities")]
    public static void ListEntities()
    {
      // Get the current document and database, and start a transaction
      Document acDoc = Application.DocumentManager.MdiActiveDocument;
      Database acCurDb = acDoc.Database;
     
      using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
      {
          // Open the Block table record for read
          BlockTable acBlkTbl;
          acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                       OpenMode.ForRead) as BlockTable;
     
          // Open the Block table record Model space for read
          BlockTableRecord acBlkTblRec;
          acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                          OpenMode.ForRead) as BlockTableRecord;
     
          int nCnt = 0;
          acDoc.Editor.WriteMessage("\nModel space objects: ");
     
          // Step through each object in Model space and
          // display the type of object found
          foreach (ObjectId acObjId in acBlkTblRec)
          {
              acDoc.Editor.WriteMessage("\n" + acObjId.ObjectClass.DxfName);
     
              nCnt = nCnt + 1;
          }
     
          // If no objects are found then display a message
          if (nCnt == 0)
          {
              acDoc.Editor.WriteMessage("\n  No objects found");
          }
     
          // Dispose of the transaction
      }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("ListEntities")> _
    Public Sub ListEntities()
      '' Get the current document and database, and start a transaction
      Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
      Dim acCurDb As Database = acDoc.Database
     
      Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
          '' Open the Block table record for read
          Dim acBlkTbl As BlockTable
          acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                       OpenMode.ForRead)
     
          '' Open the Block table record Model space for read
          Dim acBlkTblRec As BlockTableRecord
          acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                          OpenMode.ForRead)
     
          Dim nCnt As Integer = 0
          acDoc.Editor.WriteMessage(vbLf & "Model space objects: ")
     
          '' Step through each object in Model space and
          '' display the type of object found
          For Each acObjId As ObjectId In acBlkTblRec
              acDoc.Editor.WriteMessage(vbLf & acObjId.ObjectClass().DxfName)
     
              nCnt = nCnt + 1
          Next
     
          '' If no objects are found then display the following message
          If nCnt = 0 Then
              acDoc.Editor.WriteMessage(vbLf & "  No objects found")
          End If
     
          '' Dispose of the transaction
      End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub ListEntities()
        ' This example returns the first entity in model space
        On Error Resume Next
        Dim entity As AcadEntity
        If ThisDrawing.ModelSpace.count <> 0 Then
            Set entity = ThisDrawing.ModelSpace.Item(0)
            MsgBox entity.ObjectName + _
                   " is the first entity in model space."
        Else
            MsgBox "There are no objects in model space."
        End If
    End Sub
