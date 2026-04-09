<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Advanced Drawing and Organizational Techniques (.NET) > Assign and Retrieve Extended Data (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-92D663FA-0452-44F4-BDAC-0EEF0AF3BD88.htm -->

# Assign and Retrieve Extended Data (.NET)

You can use extended data (xdata) as a means for linking information with objects in a drawing. 

## Assign xdata to all objects in a selection set

This example prompts the user to select objects from the drawing. The selected objects are placed into a selection set, and the specified xdata is attached to all objects in that selection set. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    using Autodesk.AutoCAD.EditorInput;
    
    [CommandMethod("AttachXDataToSelectionSetObjects")]
    public void AttachXDataToSelectionSetObjects()
    {
        // Get the current database and start a transaction
        Database acCurDb;
        acCurDb = Application.DocumentManager.MdiActiveDocument.Database;
    
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
    
        string appName = "MY_APP";
        string xdataStr = "This is some xdata";
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Request objects to be selected in the drawing area
            PromptSelectionResult acSSPrompt = acDoc.Editor.GetSelection();
    
            // If the prompt status is OK, objects were selected
            if (acSSPrompt.Status == PromptStatus.OK)
            {
                // Open the Registered Applications table for read
                RegAppTable acRegAppTbl;
                acRegAppTbl = acTrans.GetObject(acCurDb.RegAppTableId, OpenMode.ForRead) as RegAppTable;
    
                // Check to see if the Registered Applications table record for the custom app exists
                if (acRegAppTbl.Has(appName) == false)
                {
                    using (RegAppTableRecord acRegAppTblRec = new RegAppTableRecord())
                    {
                        acRegAppTblRec.Name = appName;
    
                        acTrans.GetObject(acCurDb.RegAppTableId, OpenMode.ForWrite);
                        acRegAppTbl.Add(acRegAppTblRec);
                        acTrans.AddNewlyCreatedDBObject(acRegAppTblRec, true);
                    }
                }
    
                // Define the Xdata to add to each selected object
                using (ResultBuffer rb = new ResultBuffer())
                {
                    rb.Add(new TypedValue((int)DxfCode.ExtendedDataRegAppName, appName));
                    rb.Add(new TypedValue((int)DxfCode.ExtendedDataAsciiString, xdataStr));
    
                    SelectionSet acSSet = acSSPrompt.Value;
    
                    // Step through the objects in the selection set
                    foreach (SelectedObject acSSObj in acSSet)
                    {
                        // Open the selected object for write
                        Entity acEnt = acTrans.GetObject(acSSObj.ObjectId,
                                                            OpenMode.ForWrite) as Entity;
    
                        // Append the extended data to each object
                        acEnt.XData = rb;
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
    Imports Autodesk.AutoCAD.EditorInput
    
    <CommandMethod("AttachXDataToSelectionSetObjects")> _
    Public Sub AttachXDataToSelectionSetObjects()
        ' Get the current database and start a transaction
        Dim acCurDb As Autodesk.AutoCAD.DatabaseServices.Database
        acCurDb = Application.DocumentManager.MdiActiveDocument.Database
    
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
    
        Dim appName As String = "MY_APP"
        Dim xdataStr As String = "This is some xdata"
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            ' Request objects to be selected in the drawing area
            Dim acSSPrompt As PromptSelectionResult = acDoc.Editor.GetSelection()
    
            ' If the prompt status is OK, objects were selected
            If acSSPrompt.Status = PromptStatus.OK Then
    
                ' Open the Registered Applications table for read
                Dim acRegAppTbl As RegAppTable
                acRegAppTbl = acTrans.GetObject(acCurDb.RegAppTableId, OpenMode.ForRead)
    
                ' Check to see if the Registered Applications table record for the custom app exists
                Dim acRegAppTblRec As RegAppTableRecord
    
                If acRegAppTbl.Has(appName) = False Then
                    acRegAppTblRec = New RegAppTableRecord
                    acRegAppTblRec.Name = appName
    
                    acTrans.GetObject(acCurDb.RegAppTableId, OpenMode.ForWrite)
                    acRegAppTbl.Add(acRegAppTblRec)
                    acTrans.AddNewlyCreatedDBObject(acRegAppTblRec, True)
                End If
    
                ' Define the Xdata to add to each selected object
                Using rb As New ResultBuffer
                    rb.Add(New TypedValue(DxfCode.ExtendedDataRegAppName, appName))
                    rb.Add(New TypedValue(DxfCode.ExtendedDataAsciiString, xdataStr))
    
                    Dim acSSet As SelectionSet = acSSPrompt.Value
    
                    ' Step through the objects in the selection set
                    For Each acSSObj As SelectedObject In acSSet
                        ' Open the selected object for write
                        Dim acEnt As Entity = acTrans.GetObject(acSSObj.ObjectId, _
                                                                OpenMode.ForWrite)
    
                        ' Append the extended data to each object
                        acEnt.XData = rb
                    Next
                End Using
            End If
    
            ' Save the new object to the database
            acTrans.Commit()
    
            ' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub AttachXDataToSelectionSetObjects()
        ' Create the selection set
        Dim sset As Object
        Set sset = ThisDrawing.SelectionSets.Add("SS1")
     
        ' Prompt the user to select objects
        sset.SelectOnScreen
     
        ' Define the xdata
        Dim appName As String, xdataStr As String
        appName = "MY_APP"
        xdataStr = "This is some xdata"
        Dim xdataType(0 To 1) As Integer
        Dim xdata(0 To 1) As Variant
     
        ' Define the values for each array
        ' 1001 indicates the appName
        xdataType(0) = 1001
        xdata(0) = appName
        ' 1000 indicates a string value
        xdataType(1) = 1000
        xdata(1) = xdataStr
     
        ' Loop through all entities in the selection
        ' set and assign the xdata to each entity
        Dim ent As Object
        For Each ent In sset
            ent.SetXData xdataType, xdata
        Next ent
    End Sub

## View the xdata of all objects in a selection set

This example displays the xdata attached with the previous example. If you attach xdata other than strings (type 1000), you will need to revise this code. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    using Autodesk.AutoCAD.EditorInput;
    
    [CommandMethod("ViewXData")]
    public void ViewXData()
    {
        // Get the current database and start a transaction
        Database acCurDb;
        acCurDb = Application.DocumentManager.MdiActiveDocument.Database;
    
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
    
        string appName = "MY_APP";
        string msgstr = "";
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Request objects to be selected in the drawing area
            PromptSelectionResult acSSPrompt = acDoc.Editor.GetSelection();
    
            // If the prompt status is OK, objects were selected
            if (acSSPrompt.Status == PromptStatus.OK)
            {
                SelectionSet acSSet = acSSPrompt.Value;
    
                // Step through the objects in the selection set
                foreach (SelectedObject acSSObj in acSSet)
                {
                    // Open the selected object for read
                    Entity acEnt = acTrans.GetObject(acSSObj.ObjectId,
                                                     OpenMode.ForRead) as Entity;
    
                    // Get the extended data attached to each object for MY_APP
                    ResultBuffer rb = acEnt.GetXDataForApplication(appName);
    
                    // Make sure the Xdata is not empty
                    if (rb != null)
                    {
                        // Get the values in the xdata
                        foreach (TypedValue typeVal in rb)
                        {
                            msgstr = msgstr + "\n" + typeVal.TypeCode.ToString() + ":" + typeVal.Value;
                        }
                    }
                    else
                    {
                        msgstr = "NONE";
                    }
    
                    // Display the values returned
                    Application.ShowAlertDialog(appName + " xdata on " + acEnt.GetType().ToString() + ":\n" + msgstr);
    
                    msgstr = "";
                }
            }
    
            // Ends the transaction and ensures any changes made are ignored
            acTrans.Abort();
    
            // Dispose of the transaction
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    Imports Autodesk.AutoCAD.EditorInput
    
    <CommandMethod("ViewXData")> _
    Public Sub ViewXData()
        ' Get the current database and start a transaction
        Dim acCurDb As Autodesk.AutoCAD.DatabaseServices.Database
        acCurDb = Application.DocumentManager.MdiActiveDocument.Database
    
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
    
        Dim appName As String = "MY_APP"
        Dim msgstr As String = ""
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            ' Request objects to be selected in the drawing area
            Dim acSSPrompt As PromptSelectionResult = acDoc.Editor.GetSelection()
    
            ' If the prompt status is OK, objects were selected
            If acSSPrompt.Status = PromptStatus.OK Then
    
                Dim acSSet As SelectionSet = acSSPrompt.Value
    
                ' Step through the objects in the selection set
                For Each acSSObj As SelectedObject In acSSet
                    ' Open the selected object for read
                    Dim acEnt As Entity = acTrans.GetObject(acSSObj.ObjectId, _
                                                            OpenMode.ForRead)
    
                    ' Get the extended data attached to each object for MY_APP
                    Dim rb As ResultBuffer = acEnt.GetXDataForApplication(appName)
    
                    ' Make sure the Xdata is not empty
                    If Not IsNothing(rb) Then
                        ' Get the values in the xdata
                        For Each typeVal As TypedValue In rb
                            msgstr = msgstr & vbCrLf & typeVal.TypeCode.ToString() & ":" & typeVal.Value
                        Next
                    Else
                        msgstr = "NONE"
                    End If
    
                    ' Display the values returned
                    MsgBox(appName & " xdata on " & VarType(acEnt).ToString() & ":" & vbCrLf & msgstr)
    
                    msgstr = ""
                Next
            End If
    
            ' Ends the transaction and ensures any changes made are ignored
            acTrans.Abort()
    
            ' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub ViewXData()
        ' Find the selection created in previous example
        Dim sset As Object
        Set sset = ThisDrawing.SelectionSets.Item("SS1")
     
        ' Define the xdata variables to hold xdata information
        Dim xdataType As Variant
        Dim xdata As Variant
        Dim xd As Variant
     
        ' Define index counter
        Dim xdi As Integer
        xdi = 0
     
        ' Loop through the objects in the selection set
        ' and retrieve the xdata for the object
        Dim msgstr As String
        Dim appName As String
        Dim ent As AcadEntity
        appName = "MY_APP"
        For Each ent In sset
            msgstr = ""
            xdi = 0
     
            ' Retrieve the appName xdata type and value
            ent.GetXData appName, xdataType, xdata
     
            ' If the xdataType variable is not initialized, there
            ' was no appName xdata to retrieve for that entity
            If VarType(xdataType) <> vbEmpty Then
                For Each xd In xdata
                    msgstr = msgstr & vbCrLf & xdataType(xdi) & ": " & xd
                    xdi = xdi + 1
                Next xd
            End If
     
            ' If the msgstr variable is NULL, there was no xdata
            If msgstr = "" Then msgstr = vbCrLf & "NONE"
            MsgBox appName & " xdata on " & ent.ObjectName & ":" & vbCrLf & msgstr
        Next ent
    End Sub
