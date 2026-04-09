<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Basics of the AutoCAD .NET API (.NET) > Collection Objects (.NET) > Erase a Member of a Collection Object (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-A4927721-5F7E-4FC7-9A00-E6BD1609F7B8.htm -->

# Erase a Member of a Collection Object (.NET)

Members from a collection object can be erased using the Erase method found on the member object. For example, the following code erases the layer MyLayer from the LayerTable object. 

Before you erase a layer from a drawing, you should make sure it can be safely removed. To determine if a layer or another named object such as a block or text style can be erased, you should use the Purge method. 

## C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
     
    [CommandMethod("RemoveMyLayer")]
    public static void RemoveMyLayer()
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
          if (acLyrTbl.Has("MyLayer") == true)
          {
              LayerTableRecord acLyrTblRec;
              acLyrTblRec = acTrans.GetObject(acLyrTbl["MyLayer"],
                                              OpenMode.ForWrite) as LayerTableRecord;
     
              try
              {
                  acLyrTblRec.Erase();
                  acDoc.Editor.WriteMessage("\n'MyLayer' was erased");
     
                  // Commit the changes
                  acTrans.Commit();
              }
              catch
              {
                  acDoc.Editor.WriteMessage("\n'MyLayer' could not be erased");
              }
          }
          else
          {
              acDoc.Editor.WriteMessage("\n'MyLayer' does not exist");
          }
     
          // Dispose of the transaction
      }
    }

## VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
     
    <CommandMethod("RemoveMyLayer")> _
    Public Sub RemoveMyLayer()
      '' Get the current document and database, and start a transaction
      Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
      Dim acCurDb As Database = acDoc.Database
     
      Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
          '' Returns the layer table for the current database
          Dim acLyrTbl As LayerTable
          acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId, _
                                       OpenMode.ForRead)
     
          '' Check to see if MyLayer exists in the Layer table
          If acLyrTbl.Has("MyLayer") = True Then
              Dim acLyrTblRec As LayerTableRecord
              acLyrTblRec = acTrans.GetObject(acLyrTbl("MyLayer"), _
                                              OpenMode.ForWrite)
     
              Try
                  acLyrTblRec.Erase()
                  acDoc.Editor.WriteMessage(vbLf & "'MyLayer' was erased")
     
                  '' Commit the changes
                  acTrans.Commit()
              Catch
                  acDoc.Editor.WriteMessage(vbLf & "'MyLayer' could not be erased")
              End Try
          Else
              acDoc.Editor.WriteMessage(vbLf & "'MyLayer' does not exist")
          End If
     
          '' Dispose of the transaction
      End Using
    End Sub

## VBA/ActiveX Code Reference
    
    
    Sub RemoveMyLayer()
      On Error Resume Next
     
      '' Get the layer "MyLayer" from the Layers collection
      Dim ABCLayer As AcadLayer
      Set ABCLayer = ThisDrawing.Layers.Item("MyLayer")
     
      '' Check for an error, if no error occurs the layer exists
      If Err = 0 Then
     
        '' Delete the layer
        ABCLayer.Delete
     
        '' Clear the current error
        Err.Clear
     
        '' Get the layer again if it is found the layer could not be removed
        Set ABCLayer = ThisDrawing.Layers.Item("MyLayer")
     
        '' Check for error, if an error is encountered the layer was removed
        If Err <> 0 Then
          ThisDrawing.Utility.prompt "'MyLayer' was removed"
        Else
          ThisDrawing.Utility.prompt "'MyLayer' could not be removed"
        End If
      Else
        ThisDrawing.Utility.prompt "'MyLayer' does not exist"
      End If
    End Sub

Once an object has been erased, you should not attempt to access the object again later in the program; otherwise an error will occur. The above sample tests to see if the object exists before it is accessed again. When a request to erase an object is made, you should check to see if the object exists with the Has method or use a Try statement to catch any exceptions that occur.
