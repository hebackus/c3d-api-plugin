<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Layouts (.NET) > Layout Settings (.NET) > Plot Device (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-96E2EFD0-B16B-4A3A-BA6A-A9277BBB3610.htm -->

# Plot Device (.NET)

The plot device name for a layout or page setup is stored in the PlotConfigurationName property. The name should match one of the devices on your system, if not the default device will be used. 

You can obtain a list of all available system and non-system devices that AutoCAD has access to using the GetPlotDeviceList method of the PlotSettingsValidator object. The listed devices are the same ones that are displayed in the Plot or Page Setup dialog boxes. 

## Lists the available output devices

This example lists the output devices that are available. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.PlottingServices;
    
    // Lists the available plotters (plot configuration [PC3] files)
    [CommandMethod("PlotterList")]
    public static void PlotterList()
    {
        // Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
    
        acDoc.Editor.WriteMessage("\nPlot devices: ");
    
        foreach (string plotDevice in PlotSettingsValidator.Current.GetPlotDeviceList())
        {
            // Output the names of the available plotter devices
            acDoc.Editor.WriteMessage("\n  " + plotDevice);
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.PlottingServices
    
    ' Lists the available plotters (plot configuration [PC3] files)
    <CommandMethod("PlotterList")> _
    Public Shared Sub PlotterList()
        ' Get the current document and database, and start a transaction
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
    
        acDoc.Editor.WriteMessage(vbLf & "Plot devices: ")
    
        For Each plotDevice As String In PlotSettingsValidator.Current.GetPlotDeviceList()
            ' Output the names of the available plotter devices
            acDoc.Editor.WriteMessage(vbLf & "  " & plotDevice)
        Next
    End Sub
