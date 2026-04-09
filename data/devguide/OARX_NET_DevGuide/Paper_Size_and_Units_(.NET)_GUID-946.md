<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Layouts (.NET) > Layout Settings (.NET) > Paper Size and Units (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-946669A9-E813-4D12-828A-44986E388AA2.htm -->

# Paper Size and Units (.NET)

The choice of paper sizes for a layout depends on the plotter or device configured for output. Each plotter or device has a standard list of available output sizes which can be obtained using the GetCanonicalMediaNameList method of the PlotSettingsValidator object. The GetLocaleMediaName method of the PlotSettingsValidator object can be used to return the output size displayed in the Plot or Page Setup dialog boxes. The paper size assigned to a layout can be queried with the CanonicalMediaName property. 

You can also query the units for a layout using the PlotPaperUnits property. This property returns one of three values defined by the PlotPaperUnit enum: Inches, Millimeters, or Pixels. If your plotter is configured for raster output, the output size is returned in pixels. 

## Lists the available paper sizes for an output device

This example lists the paper sizes for the _DWF6 ePlot.pc3_ output device. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.PlottingServices;
    
    // Lists the available local media names for a specified plot configuration (PC3) file
    [CommandMethod("PlotterLocalMediaNameList")]
    public static void PlotterLocalMediaNameList()
    {
        // Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
    
        using(PlotSettings plSet = new PlotSettings(true))
        {
            PlotSettingsValidator acPlSetVdr = PlotSettingsValidator.Current;
    
            // Set the Plotter and page size
            acPlSetVdr.SetPlotConfigurationName(plSet, "DWF6 ePlot.pc3",
                                                "ANSI_A_(8.50_x_11.00_Inches)");
    
            acDoc.Editor.WriteMessage("\nCanonical and Local media names: ");
    
            int cnt = 0;
    
            foreach (string mediaName in acPlSetVdr.GetCanonicalMediaNameList(plSet))
            {
                // Output the names of the available media for the specified device
                acDoc.Editor.WriteMessage("\n  " + mediaName + " | " +
                                          acPlSetVdr.GetLocaleMediaName(plSet, cnt));
    
                cnt = cnt + 1;
            }
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.PlottingServices
    
    ' Lists the available local media names for a specified plot configuration (PC3) file
    <CommandMethod("PlotterLocalMediaNameList")> _
    Public Shared Sub PlotterLocalMediaNameList()
        ' Get the current document and database, and start a transaction
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
    
        Using plSet As PlotSettings = New PlotSettings(True)
            Dim acPlSetVdr As PlotSettingsValidator = PlotSettingsValidator.Current
    
            ' Set the Plotter and page size
            acPlSetVdr.SetPlotConfigurationName(plSet, "DWF6 ePlot.pc3", _
                                                "ANSI_A_(8.50_x_11.00_Inches)")
    
            acDoc.Editor.WriteMessage(vbLf & "Canonical and Local media names: ")
    
            Dim cnt As Integer = 0
    
            For Each mediaName As String In acPlSetVdr.GetCanonicalMediaNameList(plSet)
    
                ' Output the names of the available media for the specified device
                acDoc.Editor.WriteMessage(vbLf & "  " & mediaName & " | " & _
                                          acPlSetVdr.GetLocaleMediaName(plSet, cnt))
    
                cnt = cnt + 1
            Next
        End Using
    End Sub
