<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Layouts (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-5FA86EF3-DEFD-4256-BB1C-56DAC32BD868.htm -->

# Layouts (.NET)

All the geometry of your drawing is contained in layouts. Model space geometry is contained on a single layout named Model. You cannot rename the Model space layout, nor can you create another Model space layout as there can be only one per drawing. 

Paper space geometry is also contained on layouts. You can have many different Paper space layouts in your drawing, each representing a different configuration to print. You can change the name of the Paper space layouts. 

The “*MODEL_SPACE” BlockTableRecord in the BlockTable contains all the geometry in the Model space layout. Because there can be more than one Paper space layout in a drawing, the “*PAPER_SPACE” BlockTableRecord in the BlockTable points to the last active Paper space layout. 

There are two approaches to working with the layouts in a drawing. If you are working with the current drawing, you can use the Layout Manager which is represented by the LayoutManager interface class. When not working with the current drawing, you will need to work with the Layout named dictionary. Even when working with the current drawing, you can work with the Layout named dictionary but the Layout Manager does make certain tasks much easier to perform. 

## List the layouts in the current drawing

This example lists the layouts that are in the current drawing using the Layout Manager. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    
    // List all the layouts in the current drawing
    [CommandMethod("ListLayouts")]
    public void ListLayouts()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Get the layout dictionary of the current database
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            DBDictionary lays = 
                acTrans.GetObject(acCurDb.LayoutDictionaryId, 
                    OpenMode.ForRead) as DBDictionary;
    
            acDoc.Editor.WriteMessage("\nLayouts:");
    
            // Step through and list each named layout and Model
            foreach (DBDictionaryEntry item in lays)
            {
                acDoc.Editor.WriteMessage("\n  " + item.Key);
            }
    
            // Abort the changes to the database
            acTrans.Abort();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    
    ' List all the layouts in the current drawing
    <CommandMethod("ListLayouts")> _
    Public Shared Sub ListLayouts()
        ' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        ' Get the layout dictionary of the current database
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            Dim lays As DBDictionary = _
                acTrans.GetObject(acCurDb.LayoutDictionaryId, OpenMode.ForRead)
    
            acDoc.Editor.WriteMessage(vbLf & "Layouts:")
    
            ' Step through and list each named layout and Model
            For Each item As DBDictionaryEntry In lays
                acDoc.Editor.WriteMessage(vbLf & "  " & item.Key)
            Next
    
            ' Abort the changes to the database
            acTrans.Abort()
        End Using
    End Sub

## Create a layout in the current drawing

This example creates a new layout and sets it current using the Layout Manager. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    
    // Create a new layout with the LayoutManager
    [CommandMethod("CreateLayout")]
    public void CreateLayout()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Get the layout and plot settings of the named pagesetup
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Reference the Layout Manager
            LayoutManager acLayoutMgr = LayoutManager.Current;
    
            // Create the new layout with default settings
            ObjectId objID = acLayoutMgr.CreateLayout("newLayout");
    
            // Open the layout
            Layout acLayout = acTrans.GetObject(objID,
                                                OpenMode.ForRead) as Layout;
    
            // Set the layout current if it is not already
            if (acLayout.TabSelected == false)
            {
                acLayoutMgr.CurrentLayout = acLayout.LayoutName;
            }
    
            // Output some information related to the layout object
            acDoc.Editor.WriteMessage("\nTab Order: " + acLayout.TabOrder +
                                      "\nTab Selected: " + acLayout.TabSelected +
                                      "\nBlock Table Record ID: " +
                                      acLayout.BlockTableRecordId.ToString());
    
            // Save the changes made
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    
    ' Create a new layout with the LayoutManager
    <CommandMethod("CreateLayout")> _
    Public Shared Sub CreateLayout()
        ' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        ' Get the layout and plot settings of the named pagesetup
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            ' Reference the Layout Manager
            Dim acLayoutMgr As LayoutManager = LayoutManager.Current
    
            ' Create the new layout with default settings
            Dim objID As ObjectId = acLayoutMgr.CreateLayout("newLayout")
    
            ' Open the layout
            Dim acLayout As Layout = acTrans.GetObject(objID, _
                                                       OpenMode.ForRead)
    
            ' Set the layout current if it is not already
            If acLayout.TabSelected = False Then
                acLayoutMgr.CurrentLayout = acLayout.LayoutName
            End If
    
            ' Output some information related to the layout object
            acDoc.Editor.WriteMessage(vbLf & "Tab Order: " & acLayout.TabOrder & _
                                      vbLf & "Tab Selected: " & acLayout.TabSelected & _
                                      vbLf & "Block Table Record ID: " & _
                                      acLayout.BlockTableRecordId.ToString())
    
            ' Save the changes made
            acTrans.Commit()
        End Using
    End Sub

## Import a layout from an external drawing

This example imports a layout into the current drawing that is stored in an external drawing. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    
    // Import a layout from an external drawing
    [CommandMethod("ImportLayout")]
    public void ImportLayout()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Specify the layout name and drawing file to work with
        string layoutName = "MAIN AND SECOND FLOOR PLAN";
        string filename = "C:\\AutoCAD\\Sample\\Sheet Sets\\Architectural\\A-01.dwg";
    
        // Create a new database object and open the drawing into memory
        Database acExDb = new Database(false, true);
        acExDb.ReadDwgFile(filename, FileOpenMode.OpenForReadAndAllShare, true, "");
    
        // Create a transaction for the external drawing
        using (Transaction acTransEx = acExDb.TransactionManager.StartTransaction())
        {
            // Get the layouts dictionary
            DBDictionary layoutsEx =
                acTransEx.GetObject(acExDb.LayoutDictionaryId, 
                                    OpenMode.ForRead) as DBDictionary;
    
            // Check to see if the layout exists in the external drawing
            if (layoutsEx.Contains(layoutName) == true)
            {
                // Get the layout and block objects from the external drawing
                Layout layEx =
                    layoutsEx.GetAt(layoutName).GetObject(OpenMode.ForRead) as Layout;
                BlockTableRecord blkBlkRecEx =
                    acTransEx.GetObject(layEx.BlockTableRecordId,
                                        OpenMode.ForRead) as BlockTableRecord;
    
                // Get the objects from the block associated with the layout
                ObjectIdCollection idCol = new ObjectIdCollection();
                foreach (ObjectId id in blkBlkRecEx)
                {
                    idCol.Add(id);
                }
    
                // Create a transaction for the current drawing
                using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
                {
                    // Get the block table and create a new block
                    // then copy the objects between drawings
                    BlockTable blkTbl =
                        acTrans.GetObject(acCurDb.BlockTableId, 
                                          OpenMode.ForWrite) as BlockTable;
    
                    using (BlockTableRecord blkBlkRec = new BlockTableRecord())
                    {
                        int layoutCount = layoutsEx.Count - 1;
    
                        blkBlkRec.Name = "*Paper_Space" + layoutCount.ToString();
                        blkTbl.Add(blkBlkRec);
                        acTrans.AddNewlyCreatedDBObject(blkBlkRec, true);
                        acExDb.WblockCloneObjects(idCol,
                                                  blkBlkRec.ObjectId,
                                                  new IdMapping(),
                                                  DuplicateRecordCloning.Ignore,
                                                  false);
    
                        // Create a new layout and then copy properties between drawings
                        DBDictionary layouts =
                            acTrans.GetObject(acCurDb.LayoutDictionaryId,
                                              OpenMode.ForWrite) as DBDictionary;
    
                        using (Layout lay = new Layout())
                        {
                            lay.LayoutName = layoutName;
                            lay.AddToLayoutDictionary(acCurDb, blkBlkRec.ObjectId);
                            acTrans.AddNewlyCreatedDBObject(lay, true);
                            lay.CopyFrom(layEx);
    
                            DBDictionary plSets =
                                acTrans.GetObject(acCurDb.PlotSettingsDictionaryId,
                                                  OpenMode.ForRead) as DBDictionary;
    
                            // Check to see if a named page setup was assigned to the layout,
                            // if so then copy the page setup settings
                            if (lay.PlotSettingsName != "")
                            {
                                // Check to see if the page setup exists
                                if (plSets.Contains(lay.PlotSettingsName) == false)
                                {
                                    acTrans.GetObject(acCurDb.PlotSettingsDictionaryId, OpenMode.ForWrite);
    
                                    using (PlotSettings plSet = new PlotSettings(lay.ModelType))
                                    {
                                        plSet.PlotSettingsName = lay.PlotSettingsName;
                                        plSet.AddToPlotSettingsDictionary(acCurDb);
                                        acTrans.AddNewlyCreatedDBObject(plSet, true);
    
                                        DBDictionary plSetsEx =
                                            acTransEx.GetObject(acExDb.PlotSettingsDictionaryId,
                                                                OpenMode.ForRead) as DBDictionary;
    
                                        PlotSettings plSetEx =
                                            plSetsEx.GetAt(lay.PlotSettingsName).GetObject(
                                                           OpenMode.ForRead) as PlotSettings;
    
                                        plSet.CopyFrom(plSetEx);
                                    }
                                }
                            }
                        }
                    }
    
                    // Regen the drawing to get the layout tab to display
                    acDoc.Editor.Regen();
    
                    // Save the changes made
                    acTrans.Commit();
                }
            }
            else
            {
                // Display a message if the layout could not be found in the specified drawing
                acDoc.Editor.WriteMessage("\nLayout '" + layoutName +
                                          "' could not be imported from '" + filename + "'.");
            }
    
            // Discard the changes made to the external drawing file
            acTransEx.Abort();
        }
    
        // Close the external drawing file
        acExDb.Dispose();
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    
    ' Import a layout from an external drawing
    <CommandMethod("ImportLayout")> _
    Public Shared Sub ImportLayout()
        ' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        ' Specify the layout name and drawing file to work with
        Dim layoutName As String = "MAIN AND SECOND FLOOR PLAN"
        Dim filename As String = "C:\AutoCAD\Sample\Sheet Sets\Architectural\A-01.dwg"
    
        ' Create a new database object and open the drawing into memory
        Dim acExDb As Database = New Database(False, True)
        acExDb.ReadDwgFile(filename, FileOpenMode.OpenForReadAndAllShare, True, "")
    
        ' Create a transaction for the external drawing
        Using acTransEx As Transaction = acExDb.TransactionManager.StartTransaction()
    
            ' Get the layouts dictionary
            Dim layoutsEx As DBDictionary = _
                acTransEx.GetObject(acExDb.LayoutDictionaryId, OpenMode.ForRead)
    
            ' Check to see if the layout exists in the external drawing
            If layoutsEx.Contains(layoutName) = True Then
    
                ' Get the layout and block objects from the external drawing
                Dim layEx As Layout = _
                    layoutsEx.GetAt(layoutName).GetObject(OpenMode.ForRead)
                Dim blkBlkRecEx As BlockTableRecord = _
                    acTransEx.GetObject(layEx.BlockTableRecordId, OpenMode.ForRead)
    
                ' Get the objects from the block associated with the layout
                Dim idCol As ObjectIdCollection = New ObjectIdCollection()
                For Each id As ObjectId In blkBlkRecEx
                    idCol.Add(id)
                Next
    
                ' Create a transaction for the current drawing
                Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
                    ' Get the block table and create a new block
                    ' then copy the objects between drawings
                    Dim blkTbl As BlockTable = _
                        acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForWrite)
    
                    Using blkBlkRec As New BlockTableRecord
                        blkBlkRec.Name = "*Paper_Space" & CStr(layoutsEx.Count() - 1)
                        blkTbl.Add(blkBlkRec)
                        acTrans.AddNewlyCreatedDBObject(blkBlkRec, True)
                        acExDb.WblockCloneObjects(idCol, _
                                                  blkBlkRec.ObjectId, _
                                                  New IdMapping(), _
                                                  DuplicateRecordCloning.Ignore, _
                                                  False)
    
                        ' Create a new layout and then copy properties between drawings
                        Dim layouts As DBDictionary = _
                            acTrans.GetObject(acCurDb.LayoutDictionaryId, OpenMode.ForWrite)
    
                        Using lay As New Layout
                            lay.LayoutName = layoutName
                            lay.AddToLayoutDictionary(acCurDb, blkBlkRec.ObjectId)
                            acTrans.AddNewlyCreatedDBObject(lay, True)
                            lay.CopyFrom(layEx)
    
                            Dim plSets As DBDictionary = _
                                acTrans.GetObject( _
                                    acCurDb.PlotSettingsDictionaryId, _
                                    OpenMode.ForRead)
    
                            ' Check to see if a named page setup was assigned to the layout,
                            ' if so then copy the page setup settings
                            If lay.PlotSettingsName <> "" Then
    
                                ' Check to see if the page setup exists
                                If plSets.Contains(lay.PlotSettingsName) = False Then
                                    acTrans.GetObject(acCurDb.PlotSettingsDictionaryId, OpenMode.ForWrite)
    
                                    Using plSet As New PlotSettings(lay.ModelType)
                                        plSet.PlotSettingsName = lay.PlotSettingsName
                                        plSet.AddToPlotSettingsDictionary(acCurDb)
                                        acTrans.AddNewlyCreatedDBObject(plSet, True)
    
                                        Dim plSetsEx As DBDictionary = _
                                            acTransEx.GetObject( _
                                                acExDb.PlotSettingsDictionaryId, _
                                                OpenMode.ForRead)
    
                                        Dim plSetEx As PlotSettings = _
                                            plSetsEx.GetAt( _
                                                lay.PlotSettingsName).GetObject( _
                                                OpenMode.ForRead)
    
                                        plSet.CopyFrom(plSetEx)
                                    End Using
                                End If
                            End If
                        End Using
                    End Using
    
                    ' Regen the drawing to get the layout tab to display
                    acDoc.Editor.Regen()
    
                    ' Save the changes made
                    acTrans.Commit()
                End Using
            Else
                ' Display a message if the layout could not be found in the specified drawing
                acDoc.Editor.WriteMessage(vbLf & "Layout '" & layoutName & _
                                          "' could not be imported from '" & filename & "'.")
            End If
    
            ' Discard the changes made to the external drawing file
            acTransEx.Abort()
        End Using
    
        ' Close the external drawing file
        acExDb.Dispose()
    End Sub
