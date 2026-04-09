<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Plot Your Drawing (.NET) > Plot From Model Space (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-6E0B1F7B-7B0E-4E3E-B1FD-018E0A3673BE.htm -->

# Plot From Model Space (.NET)

Typically, when you plot a large drawing such as a floor plan, you specify a scale to convert the real drawing units into plotted inches or millimeters. However, when you plot from Model space, the defaults that are used if there are no settings specified include plot to system printer, plot the current display, scaled to fit, 0 rotation, and 0,0 offset. 

You use a PlotSettings object to modify the plot settings of the layout to plot, and then validate the plot settings with a PlotSettingsValidator object before passing the PlotSettings object to a PlotInfo object. Once the PlotInfo object is defined, you can use the PlotEngine object to plot the layout or sheet. 

## Plot the current layout

This example plots the extents of the current layout to a DWF file with a name of MyPlot. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.PlottingServices;
     
    // Plots the current layout to a DWF file
    [CommandMethod("PlotLayout")]
    public static void PlotLayout()
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
    
            // Get the PlotInfo from the layout
            using (PlotInfo acPlInfo = new PlotInfo())
            {
                acPlInfo.Layout = acLayout.ObjectId;
    
                // Get a copy of the PlotSettings from the layout
                using (PlotSettings acPlSet = new PlotSettings(acLayout.ModelType))
                {
                    acPlSet.CopyFrom(acLayout);
    
                    // Update the PlotSettings object
                    PlotSettingsValidator acPlSetVdr = PlotSettingsValidator.Current;
    
                    // Set the plot type
                    acPlSetVdr.SetPlotType(acPlSet, Autodesk.AutoCAD.DatabaseServices.PlotType.Extents);
    
                    // Set the plot scale
                    acPlSetVdr.SetUseStandardScale(acPlSet, true);
                    acPlSetVdr.SetStdScaleType(acPlSet, StdScaleType.ScaleToFit);
    
                    // Center the plot
                    acPlSetVdr.SetPlotCentered(acPlSet, true);
    
                    // Set the plot device to use
                    acPlSetVdr.SetPlotConfigurationName(acPlSet, "DWF6 ePlot.pc3", "ANSI_A_(8.50_x_11.00_Inches)");
    
                    // Set the plot info as an override since it will
                    // not be saved back to the layout
                    acPlInfo.OverrideSettings = acPlSet;
    
                    // Validate the plot info
                    using (PlotInfoValidator acPlInfoVdr = new PlotInfoValidator())
                    {
                        acPlInfoVdr.MediaMatchingPolicy = MatchingPolicy.MatchEnabled;
                        acPlInfoVdr.Validate(acPlInfo);
    
                        // Check to see if a plot is already in progress
                        if (PlotFactory.ProcessPlotState == ProcessPlotState.NotPlotting)
                        {
                            using (PlotEngine acPlEng = PlotFactory.CreatePublishEngine())
                            {
                                // Track the plot progress with a Progress dialog
                                using (PlotProgressDialog acPlProgDlg = new PlotProgressDialog(false, 1, true))
                                {
                                    using ((acPlProgDlg))
                                    {
                                        // Define the status messages to display 
                                        // when plotting starts
                                        acPlProgDlg.set_PlotMsgString(PlotMessageIndex.DialogTitle, "Plot Progress");
                                        acPlProgDlg.set_PlotMsgString(PlotMessageIndex.CancelJobButtonMessage, "Cancel Job");
                                        acPlProgDlg.set_PlotMsgString(PlotMessageIndex.CancelSheetButtonMessage, "Cancel Sheet");
                                        acPlProgDlg.set_PlotMsgString(PlotMessageIndex.SheetSetProgressCaption, "Sheet Set Progress");
                                        acPlProgDlg.set_PlotMsgString(PlotMessageIndex.SheetProgressCaption, "Sheet Progress");
    
                                        // Set the plot progress range
                                        acPlProgDlg.LowerPlotProgressRange = 0;
                                        acPlProgDlg.UpperPlotProgressRange = 100;
                                        acPlProgDlg.PlotProgressPos = 0;
    
                                        // Display the Progress dialog
                                        acPlProgDlg.OnBeginPlot();
                                        acPlProgDlg.IsVisible = true;
    
                                        // Start to plot the layout
                                        acPlEng.BeginPlot(acPlProgDlg, null);
    
                                        // Define the plot output
                                        acPlEng.BeginDocument(acPlInfo, acDoc.Name, null, 1, true, "c:\\myplot");
    
                                        // Display information about the current plot
                                        acPlProgDlg.set_PlotMsgString(PlotMessageIndex.Status, "Plotting: " + acDoc.Name + " - " + acLayout.LayoutName);
    
                                        // Set the sheet progress range
                                        acPlProgDlg.OnBeginSheet();
                                        acPlProgDlg.LowerSheetProgressRange = 0;
                                        acPlProgDlg.UpperSheetProgressRange = 100;
                                        acPlProgDlg.SheetProgressPos = 0;
    
                                        // Plot the first sheet/layout
                                        using (PlotPageInfo acPlPageInfo = new PlotPageInfo())
                                        {
                                            acPlEng.BeginPage(acPlPageInfo, acPlInfo, true, null);
                                        }
    
                                        acPlEng.BeginGenerateGraphics(null);
                                        acPlEng.EndGenerateGraphics(null);
    
                                        // Finish plotting the sheet/layout
                                        acPlEng.EndPage(null);
                                        acPlProgDlg.SheetProgressPos = 100;
                                        acPlProgDlg.OnEndSheet();
    
                                        // Finish plotting the document
                                        acPlEng.EndDocument(null);
    
                                        // Finish the plot
                                        acPlProgDlg.PlotProgressPos = 100;
                                        acPlProgDlg.OnEndPlot();
                                        acPlEng.EndPlot(null);
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.PlottingServices
     
    ' Plots the current layout to a DWF file
    <CommandMethod("PlotLayout")> _
    Public Shared Sub PlotLayout()
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
    
            ' Get the PlotInfo from the layout
            Using acPlInfo As PlotInfo = New PlotInfo()
                acPlInfo.Layout = acLayout.ObjectId
    
                ' Get a copy of the PlotSettings from the layout
                Using acPlSet As PlotSettings = New PlotSettings(acLayout.ModelType)
                    acPlSet.CopyFrom(acLayout)
    
                    ' Update the PlotSettings object
                    Dim acPlSetVdr As PlotSettingsValidator = _
                        PlotSettingsValidator.Current
    
                    ' Set the plot type
                    acPlSetVdr.SetPlotType(acPlSet, _
                                           DatabaseServices.PlotType.Extents)
    
                    ' Set the plot scale
                    acPlSetVdr.SetUseStandardScale(acPlSet, True)
                    acPlSetVdr.SetStdScaleType(acPlSet, StdScaleType.ScaleToFit)
    
                    ' Center the plot
                    acPlSetVdr.SetPlotCentered(acPlSet, True)
    
                    ' Set the plot device to use
                    acPlSetVdr.SetPlotConfigurationName(acPlSet, "DWF6 ePlot.pc3", _
                                                        "ANSI_A_(8.50_x_11.00_Inches)")
    
                    ' Set the plot info as an override since it will
                    ' not be saved back to the layout
                    acPlInfo.OverrideSettings = acPlSet
    
                    ' Validate the plot info
                    Using acPlInfoVdr As PlotInfoValidator = New PlotInfoValidator()
                        acPlInfoVdr.MediaMatchingPolicy = MatchingPolicy.MatchEnabled
                        acPlInfoVdr.Validate(acPlInfo)
    
                        ' Check to see if a plot is already in progress
                        If PlotFactory.ProcessPlotState = _
                            ProcessPlotState.NotPlotting Then
    
                            Using acPlEng As PlotEngine = _
                                PlotFactory.CreatePublishEngine()
    
                                ' Track the plot progress with a Progress dialog
                                Using acPlProgDlg As PlotProgressDialog = _
                                    New PlotProgressDialog(False, 1, True)
    
                                    Using (acPlProgDlg)
                                        ' Define the status messages to display 
                                        ' when plotting starts
                                        acPlProgDlg.PlotMsgString( _
                                            PlotMessageIndex.DialogTitle) = "Plot Progress"
                                        acPlProgDlg.PlotMsgString( _
                                            PlotMessageIndex.CancelJobButtonMessage) = _
                                                                   "Cancel Job"
                                        acPlProgDlg.PlotMsgString( _
                                            PlotMessageIndex.CancelSheetButtonMessage) = _
                                                                   "Cancel Sheet"
                                        acPlProgDlg.PlotMsgString( _
                                            PlotMessageIndex.SheetSetProgressCaption) = _
                                                                   "Sheet Set Progress"
                                        acPlProgDlg.PlotMsgString( _
                                            PlotMessageIndex.SheetProgressCaption) = _
                                                                   "Sheet Progress"
    
                                        ' Set the plot progress range
                                        acPlProgDlg.LowerPlotProgressRange = 0
                                        acPlProgDlg.UpperPlotProgressRange = 100
                                        acPlProgDlg.PlotProgressPos = 0
    
                                        ' Display the Progress dialog
                                        acPlProgDlg.OnBeginPlot()
                                        acPlProgDlg.IsVisible = True
    
                                        ' Start to plot the layout
                                        acPlEng.BeginPlot(acPlProgDlg, Nothing)
    
                                        ' Define the plot output
                                        acPlEng.BeginDocument(acPlInfo, _
                                                              acDoc.Name, _
                                                              Nothing, _
                                                              1, _
                                                              True, _
                                                              "c:\myplot")
    
                                        ' Display information about the current plot
                                        acPlProgDlg.PlotMsgString( _
                                            PlotMessageIndex.Status) = _
                                            "Plotting: " & acDoc.Name & _
                                            " - " & acLayout.LayoutName
    
                                        ' Set the sheet progress range
                                        acPlProgDlg.OnBeginSheet()
                                        acPlProgDlg.LowerSheetProgressRange = 0
                                        acPlProgDlg.UpperSheetProgressRange = 100
                                        acPlProgDlg.SheetProgressPos = 0
    
                                        ' Plot the first sheet/layout
                                        Using acPlPageInfo As PlotPageInfo = _
                                            New PlotPageInfo()
                                            acPlEng.BeginPage(acPlPageInfo, _
                                                              acPlInfo, _
                                                              True, _
                                                              Nothing)
                                        End Using
    
                                        acPlEng.BeginGenerateGraphics(Nothing)
                                        acPlEng.EndGenerateGraphics(Nothing)
    
                                        ' Finish plotting the sheet/layout
                                        acPlEng.EndPage(Nothing)
                                        acPlProgDlg.SheetProgressPos = 100
                                        acPlProgDlg.OnEndSheet()
    
                                        ' Finish plotting the document
                                        acPlEng.EndDocument(Nothing)
    
                                        ' Finish the plot
                                        acPlProgDlg.PlotProgressPos = 100
                                        acPlProgDlg.OnEndPlot()
                                        acPlEng.EndPlot(Nothing)
                                    End Using
                                End Using
                            End Using
                        End If
                    End Using
                End Using
            End Using
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub PlotLayout()
        ' Set the extents and scale of the plot area
        ThisDrawing.ActiveLayout.PlotType = acExtents
        ThisDrawing.ActiveLayout.StandardScale = acScaleToFit
     
        ' Center the plot
        ThisDrawing.ActiveLayout.CenterPlot = True
     
        ' Set the plot device to use
        ThisDrawing.ActiveLayout.ConfigName = "DWF6 ePlot.pc3"
     
        ' Set the plot output size
        ThisDrawing.ActiveLayout.CanonicalMediaName = "ANSI_A_(8.50_x_11.00_Inches)"
     
        ' Set the number of copies to one
        ThisDrawing.Plot.NumberOfCopies = 1
     
        ' Initiate the plot
        ThisDrawing.Plot.PlotToFile "c:\myplot"
    End Sub

The device name can be specified using the ConfigName property. This device can be overridden in the PlotToDevice method by specifying a PC3 file.
