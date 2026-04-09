<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Plot Settings and Page Setups (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-56BD3247-471C-4471-A238-FFDFDC3BD2E4.htm -->

# Plot Settings and Page Setups (.NET)

A PlotSettings object is similar to a Layout object, as both contain identical plot information and this is because the Layout class is derived from the PlotSettings class. The main difference is that a Layout object has an associated BlockTableRecord object containing the geometry to plot. A PlotSettings object is not associated with a particular BlockTableRecord object, but are stored in the PlotSettings dictionary in a drawing. PlotSettings objects are known as page setups in the AutoCAD user interface and are accessed from the Page Setup Manager. A page setup can be applied to a layout or used as a way to override the settings of a layout when plotting or publishing. 

## List the available page setups

This example lists the page setups contained in a drawing. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.PlottingServices;
    
    // Lists the available page setups
    [CommandMethod("ListPageSetup")]
    public static void ListPageSetup()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            DBDictionary plSettings = acTrans.GetObject(acCurDb.PlotSettingsDictionaryId,
                                                        OpenMode.ForRead) as DBDictionary;
    
            acDoc.Editor.WriteMessage("\nPage Setups: ");
    
            // List each named page setup
            foreach (DBDictionaryEntry item in plSettings)
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
    Imports Autodesk.AutoCAD.PlottingServices
    
    ' Lists the available page setups
    <CommandMethod("ListPageSetup")> _
    Public Shared Sub ListPageSetup()
        ' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        ' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            Dim plSettings As DBDictionary = _
                acTrans.GetObject(acCurDb.PlotSettingsDictionaryId, OpenMode.ForRead)
    
            acDoc.Editor.WriteMessage(vbLf & "Page Setups: ")
    
            ' List each named page setup
            For Each item As DBDictionaryEntry In plSettings
                acDoc.Editor.WriteMessage(vbLf & "  " & item.Key)
            Next
    
            ' Abort the changes to the database
            acTrans.Abort()
        End Using
    End Sub

## Create a new page setup

This example creates a new page setup based on the current layout. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.PlottingServices;
    
    // Creates a new page setup or edits the page set if it exists
    [CommandMethod("CreateOrEditPageSetup")]
    public static void CreateOrEditPageSetup()
    {
        // Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
    
            DBDictionary plSets = acTrans.GetObject(acCurDb.PlotSettingsDictionaryId,
                                                    OpenMode.ForRead) as DBDictionary;
            DBDictionary vStyles = acTrans.GetObject(acCurDb.VisualStyleDictionaryId,
                                                     OpenMode.ForRead) as DBDictionary;
    
            PlotSettings acPlSet = default(PlotSettings);
            bool createNew = false;
    
            // Reference the Layout Manager
            LayoutManager acLayoutMgr = LayoutManager.Current;
    
            // Get the current layout and output its name in the Command Line window
            Layout acLayout = acTrans.GetObject(acLayoutMgr.GetLayoutId(acLayoutMgr.CurrentLayout),
                                                OpenMode.ForRead) as Layout;
    
            // Check to see if the page setup exists
            if (plSets.Contains("MyPageSetup") == false)
            {
                createNew = true;
    
                // Create a new PlotSettings object: 
                //    True - model space, False - named layout
                acPlSet = new PlotSettings(acLayout.ModelType);
                acPlSet.CopyFrom(acLayout);
    
                acPlSet.PlotSettingsName = "MyPageSetup";
                acPlSet.AddToPlotSettingsDictionary(acCurDb);
                acTrans.AddNewlyCreatedDBObject(acPlSet, true);
            }
            else
            {
                acPlSet = plSets.GetAt("MyPageSetup").GetObject(OpenMode.ForWrite) as PlotSettings;
            }
    
            // Update the PlotSettings object
            try
            {
                PlotSettingsValidator acPlSetVdr = PlotSettingsValidator.Current;
    
                // Set the Plotter and page size
                acPlSetVdr.SetPlotConfigurationName(acPlSet, "DWF6 ePlot.pc3", "ANSI_B_(17.00_x_11.00_Inches)");
    
                // Set to plot to the current display
                if (acLayout.ModelType == false)
                {
                    acPlSetVdr.SetPlotType(acPlSet, Autodesk.AutoCAD.DatabaseServices.PlotType.Layout);
                }
                else
                {
                    acPlSetVdr.SetPlotType(acPlSet, Autodesk.AutoCAD.DatabaseServices.PlotType.Extents);
    
                    acPlSetVdr.SetPlotCentered(acPlSet, true);
                }
    
                // Use SetPlotWindowArea with PlotType.Window
                //acPlSetVdr.SetPlotWindowArea(plSet,
                //                             new Extents2d(New Point2d(0.0, 0.0),
                //                             new Point2d(9.0, 12.0)));
    
                // Use SetPlotViewName with PlotType.View
                //acPlSetVdr.SetPlotViewName(plSet, "MyView");
    
                // Set the plot offset
                acPlSetVdr.SetPlotOrigin(acPlSet, new Point2d(0, 0));
    
                // Set the plot scale
                acPlSetVdr.SetUseStandardScale(acPlSet, true);
                acPlSetVdr.SetStdScaleType(acPlSet, StdScaleType.ScaleToFit);
                acPlSetVdr.SetPlotPaperUnits(acPlSet, PlotPaperUnit.Inches);
                acPlSet.ScaleLineweights = true;
    
                // Specify if plot styles should be displayed on the layout
                acPlSet.ShowPlotStyles = true;
    
                // Rebuild plotter, plot style, and canonical media lists 
                // (must be called before setting the plot style)
                acPlSetVdr.RefreshLists(acPlSet);
    
                // Specify the shaded viewport options
                acPlSet.ShadePlot = PlotSettingsShadePlotType.AsDisplayed;
    
                acPlSet.ShadePlotResLevel = ShadePlotResLevel.Normal;
    
                // Specify the plot options
                acPlSet.PrintLineweights = true;
                acPlSet.PlotTransparency = false;
                acPlSet.PlotPlotStyles = true;
                acPlSet.DrawViewportsFirst = true;
    
                // Use only on named layouts - Hide paperspace objects option
                // plSet.PlotHidden = true;
    
                // Specify the plot orientation
                acPlSetVdr.SetPlotRotation(acPlSet, PlotRotation.Degrees000);
    
                // Set the plot style
                if (acCurDb.PlotStyleMode == true)
                {
                    acPlSetVdr.SetCurrentStyleSheet(acPlSet, "acad.ctb");
                }
                else
                {
                    acPlSetVdr.SetCurrentStyleSheet(acPlSet, "acad.stb");
                }
    
                // Zoom to show the whole paper
                acPlSetVdr.SetZoomToPaperOnUpdate(acPlSet, true);
            }
            catch (Autodesk.AutoCAD.Runtime.Exception es)
            {
                System.Windows.Forms.MessageBox.Show(es.Message);
            }
    
            // Save the changes made
            acTrans.Commit();
    
            if (createNew == true)
            {
                acPlSet.Dispose();
            }
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.PlottingServices
    
    ' Creates a new page setup or edits the page set if it exists
    <CommandMethod("CreateOrEditPageSetup")> _
    Public Shared Sub CreateOrEditPageSetup()
        ' Get the current document and database, and start a transaction
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            Dim plSets As DBDictionary = _
                acTrans.GetObject(acCurDb.PlotSettingsDictionaryId, OpenMode.ForRead)
            Dim vStyles As DBDictionary = _
                acTrans.GetObject(acCurDb.VisualStyleDictionaryId, OpenMode.ForRead)
    
            Dim acPlSet As PlotSettings
            Dim createNew As Boolean = False
    
            ' Reference the Layout Manager
            Dim acLayoutMgr As LayoutManager = LayoutManager.Current
    
            ' Get the current layout and output its name in the Command Line window
            Dim acLayout As Layout = _
                acTrans.GetObject(acLayoutMgr.GetLayoutId(acLayoutMgr.CurrentLayout), _
                                  OpenMode.ForRead)
    
            ' Check to see if the page setup exists
            If plSets.Contains("MyPageSetup") = False Then
                createNew = True
    
                ' Create a new PlotSettings object: 
                '    True - model space, False - named layout
                acPlSet = New PlotSettings(acLayout.ModelType)
                acPlSet.CopyFrom(acLayout)
    
                acPlSet.PlotSettingsName = "MyPageSetup"
                acPlSet.AddToPlotSettingsDictionary(acCurDb)
                acTrans.AddNewlyCreatedDBObject(acPlSet, True)
            Else
                acPlSet = plSets.GetAt("MyPageSetup").GetObject(OpenMode.ForWrite)
            End If
    
            ' Update the PlotSettings object
            Try
                Dim acPlSetVdr As PlotSettingsValidator = PlotSettingsValidator.Current
    
                ' Set the Plotter and page size
                acPlSetVdr.SetPlotConfigurationName(acPlSet, _
                                                    "DWF6 ePlot.pc3", _
                                                    "ANSI_B_(17.00_x_11.00_Inches)")
    
                ' Set to plot to the current display
                If acLayout.ModelType = False Then
                    acPlSetVdr.SetPlotType(acPlSet, _
                                           DatabaseServices.PlotType.Layout)
                Else
                    acPlSetVdr.SetPlotType(acPlSet, _
                                           DatabaseServices.PlotType.Extents)
    
                    acPlSetVdr.SetPlotCentered(acPlSet, True)
                End If
    
                ' Use SetPlotWindowArea with PlotType.Window
                'acPlSetVdr.SetPlotWindowArea(plSet, _
                '                             New Extents2d(New Point2d(0.0, 0.0), _
                '                             New Point2d(9.0, 12.0)))
    
                ' Use SetPlotViewName with PlotType.View
                'acPlSetVdr.SetPlotViewName(plSet, "MyView")
    
                ' Set the plot offset
                acPlSetVdr.SetPlotOrigin(acPlSet, _
                                         New Point2d(0, 0))
    
                ' Set the plot scale
                acPlSetVdr.SetUseStandardScale(acPlSet, True)
                acPlSetVdr.SetStdScaleType(acPlSet, StdScaleType.ScaleToFit)
                acPlSetVdr.SetPlotPaperUnits(acPlSet, PlotPaperUnit.Inches)
                acPlSet.ScaleLineweights = True
    
                ' Specify if plot styles should be displayed on the layout
                acPlSet.ShowPlotStyles = True
    
                ' Rebuild plotter, plot style, and canonical media lists 
                ' (must be called before setting the plot style)
                acPlSetVdr.RefreshLists(acPlSet)
    
                ' Specify the shaded viewport options
                acPlSet.ShadePlot = PlotSettingsShadePlotType.AsDisplayed
    
                acPlSet.ShadePlotResLevel = ShadePlotResLevel.Normal
    
                ' Specify the plot options
                acPlSet.PrintLineweights = True
                acPlSet.PlotTransparency = False
                acPlSet.PlotPlotStyles = True
                acPlSet.DrawViewportsFirst = True
    
                ' Use only on named layouts - Hide paperspace objects option
                ' plSet.PlotHidden = True
    
                ' Specify the plot orientation
                acPlSetVdr.SetPlotRotation(acPlSet, PlotRotation.Degrees000)
    
                ' Set the plot style
                If acCurDb.PlotStyleMode = True Then
                    acPlSetVdr.SetCurrentStyleSheet(acPlSet, "acad.ctb")
                Else
                    acPlSetVdr.SetCurrentStyleSheet(acPlSet, "acad.stb")
                End If
    
                ' Zoom to show the whole paper
                acPlSetVdr.SetZoomToPaperOnUpdate(acPlSet, True)
            Catch es As Autodesk.AutoCAD.Runtime.Exception
                MsgBox(es.Message)
            End Try
    
            ' Save the changes made
            acTrans.Commit()
    
            If createNew = True Then
                acPlSet.Dispose()
            End If
        End Using
    End Sub

## Assign a page setup to a layout

This example assigns a page setup to the current layout. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.PlottingServices;
    
    // Assigns a page setup to a layout
    [CommandMethod("AssignPageSetupToLayout")]
    public static void AssignPageSetupToLayout()
    {
        // Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Reference the Layout Manager
            LayoutManager acLayoutMgr = LayoutManager.Current;
    
            // Get the current layout and output its name in the Command Line window
            Layout acLayout = acTrans.GetObject(acLayoutMgr.GetLayoutId(acLayoutMgr.CurrentLayout),
                                                OpenMode.ForRead) as Layout;
    
            DBDictionary acPlSet = acTrans.GetObject(acCurDb.PlotSettingsDictionaryId,
                                                     OpenMode.ForRead) as DBDictionary;
    
            // Check to see if the page setup exists
            if (acPlSet.Contains("MyPageSetup") == true)
            {
                PlotSettings plSet = acPlSet.GetAt("MyPageSetup").GetObject(OpenMode.ForRead) as PlotSettings;
    
                // Update the layout
                acTrans.GetObject(acLayoutMgr.GetLayoutId(acLayoutMgr.CurrentLayout), OpenMode.ForWrite);
                acLayout.CopyFrom(plSet);
    
                // Save the new objects to the database
                acTrans.Commit();
            }
            else
            {
                // Ignore the changes made
                acTrans.Abort();
            }
        }
    
        // Update the display
        acDoc.Editor.Regen();
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.PlottingServices
    
    ' Assigns a page setup to a layout
    <CommandMethod("AssignPageSetupToLayout")> _
    Public Shared Sub AssignPageSetupToLayout()
        ' Get the current document and database, and start a transaction
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            ' Reference the Layout Manager
            Dim acLayoutMgr As LayoutManager = LayoutManager.Current
    
            ' Get the current layout and output its name in the Command Line window
            Dim acLayout As Layout = _
                acTrans.GetObject(acLayoutMgr.GetLayoutId(acLayoutMgr.CurrentLayout), _
                                  OpenMode.ForRead)
    
            Dim acPlSet As DBDictionary = _
                acTrans.GetObject(acCurDb.PlotSettingsDictionaryId, OpenMode.ForRead)
    
            ' Check to see if the page setup exists
            If acPlSet.Contains("MyPageSetup") = True Then
                Dim plSet As PlotSettings = _
                    acPlSet.GetAt("MyPageSetup").GetObject(OpenMode.ForRead)
    
                ' Update the layout
                acTrans.GetObject(acLayoutMgr.GetLayoutId(acLayoutMgr.CurrentLayout), OpenMode.ForWrite)
                acLayout.CopyFrom(plSet)
    
                ' Save the new objects to the database
                acTrans.Commit()
            Else
                ' Ignore the changes made
                acTrans.Abort()
            End If
        End Using
    
        ' Update the display
        acDoc.Editor.Regen()
    End Sub
