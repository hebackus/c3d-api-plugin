<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Control the Drawing Windows (.NET) > Use Named Views (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-076B6391-F375-454E-BFB2-533BDCA9E23D.htm -->

# Use Named Views (.NET)

You can name and save a view you want to reuse. When you no longer need the view, you can remove it. 

Named views are stored in the View table, one of the named symbol tables in a drawing database. A named view is created with the Add method to add a new view to the View table. When you add the new named view to the View table, a default model space view is created. 

You name the view when you create it. The name of the view can be up to 255 characters long and contain letters, digits, and the special characters dollar sign ($), hyphen (-), and underscore (_). 

A named view can be removed from the View table by simply use the Erase method of the ViewTableRecord object you want to remove. 

## Add a named view and set it current

The following example adds a named view to the drawing and sets it current. 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Runtime;
     
    [CommandMethod("CreateNamedView")]
    public static void CreateNamedView()
    {
        // Get the current database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the View table for read
            ViewTable acViewTbl;
            acViewTbl = acTrans.GetObject(acCurDb.ViewTableId,
                                            OpenMode.ForRead) as ViewTable;
    
            // Check to see if the named view 'View1' exists
            if (acViewTbl.Has("View1") == false)
            {
                // Open the View table for write
                acTrans.GetObject(acCurDb.ViewTableId, OpenMode.ForWrite);
    
                // Create a new View table record and name the view 'View1'
                using (ViewTableRecord acViewTblRec = new ViewTableRecord())
                {
                    acViewTblRec.Name = "View1";
    
                    // Add the new View table record to the View table and the transaction
                    acViewTbl.Add(acViewTblRec);
                    acTrans.AddNewlyCreatedDBObject(acViewTblRec, true);
    
                    // Set 'View1' current
                    acDoc.Editor.SetCurrentView(acViewTblRec);
                }
    
                // Commit the changes
                acTrans.Commit();
            }
    
            // Dispose of the transaction
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Runtime
     
    <CommandMethod("CreateNamedView")> _
    Public Sub CreateNamedView()
        '' Get the current database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the View table for read
            Dim acViewTbl As ViewTable
            acViewTbl = acTrans.GetObject(acCurDb.ViewTableId, OpenMode.ForRead)
    
            '' Check to see if the named view 'View1' exists
            If (acViewTbl.Has("View1") = False) Then
                '' Open the View Table for write
                acTrans.GetObject(acCurDb.ViewTableId, OpenMode.ForWrite)
    
                '' Create a new View table record and name the view "View1"
                Using acViewTblRec As ViewTableRecord = New ViewTableRecord()
                    acViewTblRec.Name = "View1"
    
                    '' Add the new View table record to the View table and the transaction
                    acViewTbl.Add(acViewTblRec)
                    acTrans.AddNewlyCreatedDBObject(acViewTblRec, True)
    
                    '' Set 'View1' current
                    acDoc.Editor.SetCurrentView(acViewTblRec)
                End Using
    
                '' Commit the changes
                acTrans.Commit()
            End If
    
            '' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CreateNamedView()
        ' Add a named view to the views collection
        Dim viewObj As AcadView
        Set viewObj = ThisDrawing.Views.Add("View1")
     
        ThisDrawing.ActiveViewport.SetView viewObj
    End Sub

## Erase a named view

The following example erases a named view from the drawing. 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Runtime;
     
    [CommandMethod("EraseNamedView")]
    public static void EraseNamedView()
    {
        // Get the current database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the View table for read
            ViewTable acViewTbl;
            acViewTbl = acTrans.GetObject(acCurDb.ViewTableId,
                                            OpenMode.ForRead) as ViewTable;
    
            // Check to see if the named view 'View1' exists
            if (acViewTbl.Has("View1") == true)
            {
                // Open the View table for write
                acTrans.GetObject(acCurDb.ViewTableId, OpenMode.ForWrite);
    
                // Get the named view
                ViewTableRecord acViewTblRec;
                acViewTblRec = acTrans.GetObject(acViewTbl["View1"],
                                                    OpenMode.ForWrite) as ViewTableRecord;
    
                // Remove the named view from the View table
                acViewTblRec.Erase();
    
                // Commit the changes
                acTrans.Commit();
            }
    
            // Dispose of the transaction
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Runtime
     
    <CommandMethod("EraseNamedView")> _
    Public Sub EraseNamedView()
        '' Get the current database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the View table for read
            Dim acViewTbl As ViewTable
            acViewTbl = acTrans.GetObject(acCurDb.ViewTableId, OpenMode.ForRead)
    
            '' Check to see if the named view 'View1' exists
            If (acViewTbl.Has("View1") = True) Then
                '' Open the View table for write
                acTrans.GetObject(acCurDb.ViewTableId, OpenMode.ForWrite)
    
                '' Get the named view
                Dim acViewTblRec As ViewTableRecord
                acViewTblRec = acTrans.GetObject(acViewTbl("View1"), OpenMode.ForWrite)
    
                '' Remove the named view from the View table
                acViewTblRec.Erase()
    
                '' Commit the changes
                acTrans.Commit()
            End If
    
            '' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub EraseNamedView()
        On Error Resume Next
        Dim viewObj As AcadView
        Set viewObj = ThisDrawing.Views("View1")
     
        If Err = 0 Then
          ' Delete the view
          viewObj.Delete
        End If
    End Sub
