<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Layouts (.NET) > Layout Settings (.NET) > Query and Set Layout Settings (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-9B330DCF-6A4E-4C58-B5C1-085E34912077.htm -->

# Query and Set Layout Settings (.NET)

The following example shows how to query and change the device of the current layout. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.PlottingServices;
     
    // Changes the plot settings for a layout directly
    [CommandMethod("ChangeLayoutPlotSettings")]
    public static void ChangeLayoutPlotSettings()
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
    
            // Output the name of the current layout and its device
            acDoc.Editor.WriteMessage("\nCurrent layout: " + acLayout.LayoutName);
    
            acDoc.Editor.WriteMessage("\nCurrent device name: " + acLayout.PlotConfigurationName);
    
            // Get a copy of the PlotSettings from the layout
            using (PlotSettings acPlSet = new PlotSettings(acLayout.ModelType))
            {
                acPlSet.CopyFrom(acLayout);
    
                // Update the PlotConfigurationName property of the PlotSettings object
                PlotSettingsValidator acPlSetVdr = PlotSettingsValidator.Current;
                acPlSetVdr.SetPlotConfigurationName(acPlSet, "DWG To PDF.pc3", "ANSI_B_(11.00_x_17.00_Inches)");
    
                // Zoom to show the whole paper
                acPlSetVdr.SetZoomToPaperOnUpdate(acPlSet, true);
    
                // Update the layout
                acTrans.GetObject(acLayoutMgr.GetLayoutId(acLayoutMgr.CurrentLayout), OpenMode.ForWrite);
                acLayout.CopyFrom(acPlSet);
            }
    
            // Output the name of the new device assigned to the layout
            acDoc.Editor.WriteMessage("\nNew device name: " + acLayout.PlotConfigurationName);
    
            // Save the new objects to the database
            acTrans.Commit();
        }
    
        // Update the display
        acDoc.Editor.Regen();
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.PlottingServices
     
    ' Changes the plot settings for a layout directly
    <CommandMethod("ChangeLayoutPlotSettings")> _
    Public Shared Sub ChangeLayoutPlotSettings()
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
    
            ' Output the name of the current layout and its device
            acDoc.Editor.WriteMessage(vbLf & "Current layout: " & _
                                      acLayout.LayoutName)
    
            acDoc.Editor.WriteMessage(vbLf & "Current device name: " & _
                                      acLayout.PlotConfigurationName)
    
            ' Get a copy of the PlotSettings from the layout
            Using acPlSet As PlotSettings = New PlotSettings(acLayout.ModelType)
                acPlSet.CopyFrom(acLayout)
    
                ' Update the PlotConfigurationName property of the PlotSettings object
                Dim acPlSetVdr As PlotSettingsValidator = PlotSettingsValidator.Current
                acPlSetVdr.SetPlotConfigurationName(acPlSet, "DWG To PDF.pc3", _
                                                    "ANSI_B_(11.00_x_17.00_Inches)")
    
                ' Zoom to show the whole paper
                acPlSetVdr.SetZoomToPaperOnUpdate(acPlSet, True)
    
                ' Update the layout
                acTrans.GetObject(acLayoutMgr.GetLayoutId(acLayoutMgr.CurrentLayout), OpenMode.ForWrite)
                acLayout.CopyFrom(acPlSet)
            End Using
    
            ' Output the name of the new device assigned to the layout
            acDoc.Editor.WriteMessage(vbLf & "New device name: " & _
                                      acLayout.PlotConfigurationName)
    
            ' Save the new objects to the database
            acTrans.Commit()
        End Using
    
        ' Update the display
        acDoc.Editor.Regen()
    End Sub

### VBA/ActiveX Code Reference
    
    
    Public Sub ChangePlotSetting()
        Dim layoutObj As AcadLayout
        Set layoutObj = ThisDrawing.ActiveLayout
     
        ' Output the name of the current layout and its device
        ThisDrawing.Utility.Prompt vbLf & "Current layout: " & layoutObj.Name
        ThisDrawing.Utility.Prompt vbLf & "Current device name: " & _
                                   layoutObj.ConfigName
     
        ' Change the name of the output device for the current layout
        layoutObj.RefreshPlotDeviceInfo
        layoutObj.ConfigName = "DWF6 ePlot.pc3"
        layoutObj.CanonicalMediaName = "ANSI_A_(8.50_x_11.00_Inches)"
     
        ' Output the name of the new device assigned to the layout
        ThisDrawing.Utility.Prompt vbLf & "Current device name: " & _
                                   layoutObj.ConfigName & vbLf
    End Sub
