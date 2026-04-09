<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Develop Applications (.NET) > Handle Errors (.NET) > Trap Runtime Errors (.NET) > Compare Error Handlers in VBA or VB to .NET (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-4E52F256-8DA4-494F-92EA-A18EE07BE806.htm -->

# Compare Error Handlers in VBA or VB to .NET (.NET)

Error handling in VBA or VB is done using the On Error statements. While the On Error statements can be used with VB.NET without any problems, it is recommended to utilize Try statements instead. Try statements are more flexibility than the On Error Resume Next and On Error GoTo Label statements or VBA and VB. 

The use of On Error Resume Next and On Error GoTo Label statements can be rewritten using Try-Catch statements. The following shows how an On Error GoTo Label statement can be rewritten using Try-Catch. 

### On Error - VBA
    
    
    Sub ColorEntities()
        On Error GoTo MyErrorHandler
     
        Dim entry As Object
        For Each entry In ThisDrawing.ModelSpace
            entry.color = acRed
        Next entry
     
        ' Important! Exit the subroutine before the error handler
      Exit Sub
     
    MyErrorHandler:
        MsgBox entry.EntityName + " is on a locked layer." + _
                                  " The handle is: " + entry.Handle
      Resume Next
    End Sub

### Try-Catch - C#
    
    
    [CommandMethod("ColorEntities")]
    public void ColorEntities()
    {
        // ' Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // ' Open the Block table record for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead) as BlockTable;
    
            // ' Open the Block table record Model space for read
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace], OpenMode.ForRead) as BlockTableRecord;
    
            // ' Step through each object in Model space
            foreach (ObjectId acObjId in acBlkTblRec)
            {
                try
                {
                    Entity acEnt;
                    acEnt = acTrans.GetObject(acObjId, OpenMode.ForWrite) as Entity;
    
                    acEnt.ColorIndex = 1;
                }
                catch
                {
                    Application.ShowAlertDialog(acObjId.ObjectClass.DxfName + " is on a locked layer." + " The handle is: " + acObjId.Handle.ToString());
                }
            }
    
            acTrans.Commit();
        }
    }

### Try-Catch - .NET
    
    
    <CommandMethod("ColorEntities")> _
    Public Sub ColorEntities()
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
     
          Dim acObjId As ObjectId
     
          '' Step through each object in Model space
          For Each acObjId In acBlkTblRec
              Try
                  Dim acEnt As Entity
                  acEnt = acTrans.GetObject(acObjId, _
                                            OpenMode.ForWrite)
     
                  acEnt.ColorIndex = 1
              Catch
                  Application.ShowAlertDialog(acObjId.ObjectClass.DxfName & _
                                              " is on a locked layer." & _
                                              " The handle is: " & acObjId.Handle.ToString())
              End Try
          Next
     
          acTrans.Commit()
      End Using
    End Sub
