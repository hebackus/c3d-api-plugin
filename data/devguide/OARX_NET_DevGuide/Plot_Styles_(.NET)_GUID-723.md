<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Plot Styles (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-723C62A6-04CD-4C25-865A-0A05B3B69903.htm -->

# Plot Styles (.NET)

Plot styles are used to override some object properties that control the way an object appears in the output. The plot style assigned to a layout or page setup is stored in the CurrentStyleSheet property. You use the SetCurrentStyleSheet method of the PlotSettingsValidator object to assign a plot style to a PlotSettings object. Based on how a drawing was created, it uses either color-dependent or named plot styles. You can use the PlotStyleMode property of the current database to determine which type of plot style the drawing is using. 

You can obtain a list of all available plot styles using the GetPlotStyleSheetList method of the PlotSettingsValidator object. The listed plot styles are the same ones that are displayed in the Plot or Page Setup dialog boxes. 

## List the available plot style

This example lists the plot styles that are available. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    
    // Lists the available plot styles
    [CommandMethod("PlotStyleList")]
    public static void PlotStyleList()
    {
        // Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
    
        acDoc.Editor.WriteMessage("\nPlot styles: ");
    
        foreach (string plotStyle in PlotSettingsValidator.Current.GetPlotStyleSheetList())
        {
            // Output the names of the available plot styles
            acDoc.Editor.WriteMessage("\n  " + plotStyle);
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    
    ' Lists the available plot styles
    <CommandMethod("PlotStyleList")> _
    Public Shared Sub PlotStyleList()
        ' Get the current document and database, and start a transaction
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
    
        acDoc.Editor.WriteMessage(vbLf & "Plot styles: ")
    
        For Each plotStyle As String In PlotSettingsValidator.Current.GetPlotStyleSheetList()
            ' Output the names of the available plot styles
            acDoc.Editor.WriteMessage(vbLf & "  " & plotStyle)
        Next
    End Sub
