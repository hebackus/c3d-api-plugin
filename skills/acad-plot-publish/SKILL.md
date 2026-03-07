---
name: acad-plot-publish
description: PlotSettings, PlotSettingsValidator, PlotEngine single-sheet plotting, batch publishing with DSD, named page setups, plot to file (PDF/DWF/PLT), plot device enumeration, plot preview, BACKGROUNDPLOT, PlotReactorManager events
---

# AutoCAD Plotting and Publishing

Use this skill when plotting layouts to printers or files (PDF, DWF, PLT), configuring plot devices and paper sizes, managing named page setups, batch publishing multiple sheets, displaying plot progress, or reacting to plot events.

## PlotSettings and PlotSettingsValidator

Every `Layout` inherits from `PlotSettings`. Use `PlotSettingsValidator` to modify plot parameters on a layout or standalone `PlotSettings` object.

### Configuring a Layout for Plotting

```csharp
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    Layout layout = (Layout)tr.GetObject(layoutId, OpenMode.ForWrite);
    PlotSettingsValidator psv = PlotSettingsValidator.Current;

    // Always refresh after opening or changing device
    psv.RefreshLists(layout);

    // Set the plot device
    psv.SetPlotConfigurationName(layout, "DWG To PDF.pc3", null);

    // Refresh again to load media list for the new device
    psv.RefreshLists(layout);

    // Set paper size by canonical name
    psv.SetCanonicalMediaName(layout, "ANSI_D_(22.00_x_34.00_Inches)");

    // Set plot area type
    psv.SetPlotType(layout, Autodesk.AutoCAD.DatabaseServices.PlotType.Layout);

    // Set 1:1 scale
    psv.SetUseStandardScale(layout, true);
    psv.SetStdScaleType(layout, StdScaleType.StdScale1To1);

    // Center the plot on the paper
    psv.SetPlotCentered(layout, true);

    // Set rotation
    psv.SetPlotRotation(layout, PlotRotation.Degrees000);

    tr.Commit();
}
```

### Custom Scale

```csharp
psv.SetUseStandardScale(layout, false);
psv.SetCustomPrintScale(layout, new CustomScale(1.0, 1.0));  // numerator, denominator
```

### Plot Area Types

```csharp
// PlotType enum values:
psv.SetPlotType(layout, PlotType.Layout);   // plot the full layout paper area
psv.SetPlotType(layout, PlotType.Extents);  // plot to drawing extents
psv.SetPlotType(layout, PlotType.Display);  // plot what is currently displayed
psv.SetPlotType(layout, PlotType.Limits);   // plot to drawing limits
psv.SetPlotType(layout, PlotType.View);     // plot a named view
psv.SetPlotType(layout, PlotType.Window);   // plot a user-defined window

// For Window plot type, set the window corners
psv.SetPlotWindowArea(layout, new Extents2d(
    new Point2d(0, 0),        // lower-left
    new Point2d(100, 75)));   // upper-right
```

### Plot Rotation

```csharp
psv.SetPlotRotation(layout, PlotRotation.Degrees000);   // portrait
psv.SetPlotRotation(layout, PlotRotation.Degrees090);   // landscape
psv.SetPlotRotation(layout, PlotRotation.Degrees180);   // inverted portrait
psv.SetPlotRotation(layout, PlotRotation.Degrees270);   // inverted landscape
```

## Plot Style Tables (CTB vs STB)

A drawing uses either color-dependent plot styles (`.ctb`) or named plot styles (`.stb`), set at drawing creation. The active mode is stored in the `PSTYLEMODE` system variable.

### Setting the Plot Style Table

```csharp
PlotSettingsValidator psv = PlotSettingsValidator.Current;

// Assign a CTB or STB file
psv.SetCurrentStyleSheet(layout, "monochrome.ctb");

// List available plot style tables for the current device
StringCollection styleSheets = psv.GetPlotStyleSheetList();
foreach (string name in styleSheets)
{
    ed.WriteMessage($"\n  {name}");
}
```

### Checking Drawing Style Mode

```csharp
// PSTYLEMODE: 1 = color-dependent (CTB), 0 = named (STB)
int mode = (int)Application.GetSystemVariable("PSTYLEMODE");
bool isCtb = (mode == 1);
```

## PlotEngine -- Single-Sheet Plotting

`PlotEngine` drives the plot loop for one layout at a time.

### Plot a Single Layout to PDF

```csharp
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    Layout layout = (Layout)tr.GetObject(layoutId, OpenMode.ForRead);
    PlotInfo plotInfo = new PlotInfo();
    plotInfo.Layout = layoutId;

    // Validate the plot info against the layout settings
    PlotInfoValidator piv = new PlotInfoValidator();
    piv.MediaMatchingPolicy = MatchingPolicy.MatchEnabled;
    piv.Validate(plotInfo);

    // Check if a plot is already in progress
    if (PlotFactory.ProcessPlotState == ProcessPlotState.NotPlotting)
    {
        using (PlotEngine engine = PlotFactory.CreatePublishEngine())
        {
            engine.BeginPlot(null, null);
            engine.BeginDocument(plotInfo, doc.Name, null,
                1,               // copies
                true,            // plot to file
                @"C:\Output\Sheet1.pdf");

            PlotPageInfo pageInfo = new PlotPageInfo();
            engine.BeginPage(pageInfo, plotInfo, true, null);
            engine.BeginGenerateGraphics(null);
            engine.EndGenerateGraphics(null);
            engine.EndPage(null);

            engine.EndDocument(null);
            engine.EndPlot(null);
        }
    }

    tr.Commit();
}
```

### Multi-Page PDF (Multiple Layouts)

```csharp
if (PlotFactory.ProcessPlotState == ProcessPlotState.NotPlotting)
{
    using (PlotEngine engine = PlotFactory.CreatePublishEngine())
    {
        engine.BeginPlot(null, null);

        // First layout
        engine.BeginDocument(plotInfo1, doc.Name, null, 1, true,
            @"C:\Output\Combined.pdf");

        PlotPageInfo pageInfo1 = new PlotPageInfo();
        engine.BeginPage(pageInfo1, plotInfo1, true, null);
        engine.BeginGenerateGraphics(null);
        engine.EndGenerateGraphics(null);
        engine.EndPage(null);

        // Second layout -- same document, new page
        PlotPageInfo pageInfo2 = new PlotPageInfo();
        engine.BeginPage(pageInfo2, plotInfo2, true, null);
        engine.BeginGenerateGraphics(null);
        engine.EndGenerateGraphics(null);
        engine.EndPage(null);

        engine.EndDocument(null);
        engine.EndPlot(null);
    }
}
```

## PlotProgressDialog

Provides a standard progress dialog during plotting.

```csharp
using (PlotProgressDialog ppd = new PlotProgressDialog(false, 1, true))
{
    ppd.set_PlotMsgString(PlotMessageIndex.DialogTitle, "Plotting Sheets");
    ppd.set_PlotMsgString(PlotMessageIndex.SheetName, $"Sheet: {layout.LayoutName}");
    ppd.set_PlotMsgString(PlotMessageIndex.CancelSheetButtonMessage, "Cancel Sheet");
    ppd.set_PlotMsgString(PlotMessageIndex.CancelJobButtonMessage, "Cancel Job");
    ppd.LowerPlotProgressRange = 0;
    ppd.UpperPlotProgressRange = 100;
    ppd.PlotProgressPos = 0;

    ppd.OnBeginPlot();
    ppd.IsVisible = true;

    using (PlotEngine engine = PlotFactory.CreatePublishEngine())
    {
        engine.BeginPlot(ppd, null);
        engine.BeginDocument(plotInfo, doc.Name, null, 1, true, outputPath);

        ppd.OnBeginSheet();
        ppd.SheetProgressPos = 0;

        PlotPageInfo pageInfo = new PlotPageInfo();
        engine.BeginPage(pageInfo, plotInfo, true, null);
        engine.BeginGenerateGraphics(null);
        engine.EndGenerateGraphics(null);
        engine.EndPage(null);

        ppd.SheetProgressPos = 100;
        ppd.OnEndSheet();

        engine.EndDocument(null);
        engine.EndPlot(null);
    }

    ppd.PlotProgressPos = 100;
    ppd.OnEndPlot();
}
```

## Batch Publishing with DSD

`Publisher` and `DsdData` / `DsdEntryCollection` enable batch publishing of multiple sheets to a single multi-sheet DWF, PDF, or plotter output.

### Creating a DSD for Batch Publish

```csharp
using Autodesk.AutoCAD.Publishing;

// Build the DSD entry collection
DsdEntryCollection entries = new DsdEntryCollection();

foreach (string layoutName in layoutNames)
{
    DsdEntry entry = new DsdEntry();
    entry.DwgFile = doc.Name;           // full path to the DWG
    entry.Layout = layoutName;           // layout tab name
    entry.Title = layoutName;            // sheet title in output
    entry.Nps = "";                      // named page setup (empty = use layout settings)
    entries.Add(entry);
}

// Configure the DSD data
DsdData dsd = new DsdData();
dsd.SheetType = SheetType.MultiPdf;     // or SinglePdf, MultiDwf, SingleDwf
dsd.ProjectPath = @"C:\Output\";
dsd.DestinationName = @"C:\Output\AllSheets.pdf";
dsd.SetDsdEntryCollection(entries);

// Optionally set prompt for file name
dsd.PromptForDwfName = false;

// Write a temporary DSD file (Publisher requires a file path)
string dsdPath = Path.Combine(Path.GetTempPath(), "publish.dsd");
dsd.WriteDsd(dsdPath);

// Re-read to ensure valid format (workaround for known API quirk)
dsd.ReadDsd(dsdPath);
```

### Publishing the DSD

```csharp
// Disable background plotting for foreground publish
short bgPlot = (short)Application.GetSystemVariable("BACKGROUNDPLOT");
Application.SetSystemVariable("BACKGROUNDPLOT", (short)0);

try
{
    Publisher publisher = Application.Publisher;
    publisher.PublishExecute(dsd, PlotProgressDialog);
}
finally
{
    Application.SetSystemVariable("BACKGROUNDPLOT", bgPlot);
    File.Delete(dsdPath);
}
```

### SheetType Values

```csharp
SheetType.MultiPdf      // all sheets into one PDF
SheetType.SinglePdf      // each sheet as a separate PDF
SheetType.MultiDwf       // all sheets into one DWF
SheetType.SingleDwf      // each sheet as a separate DWF
SheetType.OriginalDevice // use the device assigned to each layout
```

## Named Page Setups

Named page setups are `PlotSettings` objects stored in the plot settings dictionary. They capture device, paper size, scale, style table, and plot area for reuse across layouts.

### Saving a Named Page Setup

```csharp
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    // Create a standalone PlotSettings (not tied to a layout)
    PlotSettings ps = new PlotSettings(false);  // false = paper space
    ps.CopyFrom(layout);                         // copy current layout settings
    ps.PlotSettingsName = "ANSI D PDF";
    ps.AddToPlotSettingsDictionary(db);
    tr.AddNewlyCreatedDBObject(ps, true);

    tr.Commit();
}
```

### Restoring a Named Page Setup

```csharp
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    DBDictionary plotSettingsDict = (DBDictionary)tr.GetObject(
        db.PlotSettingsDictionaryId, OpenMode.ForRead);

    if (plotSettingsDict.Contains("ANSI D PDF"))
    {
        PlotSettings ps = (PlotSettings)tr.GetObject(
            plotSettingsDict.GetAt("ANSI D PDF"), OpenMode.ForRead);

        Layout layout = (Layout)tr.GetObject(layoutId, OpenMode.ForWrite);
        layout.CopyFrom(ps);
    }

    tr.Commit();
}
```

### Enumerating Page Setups

```csharp
DBDictionary plotSettingsDict = (DBDictionary)tr.GetObject(
    db.PlotSettingsDictionaryId, OpenMode.ForRead);

foreach (DBDictionaryEntry entry in plotSettingsDict)
{
    PlotSettings ps = (PlotSettings)tr.GetObject(entry.Value, OpenMode.ForRead);
    ed.WriteMessage($"\n  {ps.PlotSettingsName}: {ps.PlotConfigurationName} " +
        $"({ps.CanonicalMediaName})");
}
```

## Plot to File (PDF, DWF, PLT)

Output format is determined by the plot device (PC3 file or system printer).

### Common Plot Devices

| Device | Output |
|--------|--------|
| `DWG To PDF.pc3` | PDF file |
| `DWFx ePlot (XPS Compatible).pc3` | DWFx file |
| `DWF6 ePlot.pc3` | DWF file |
| `PublishToWeb JPG.pc3` | JPEG file |
| `PublishToWeb PNG.pc3` | PNG file |
| Any HP-GL/2 PC3 | PLT file |

### Generating a PLT File

```csharp
psv.SetPlotConfigurationName(layout, "HP DesignJet.pc3", null);
psv.RefreshLists(layout);
psv.SetCanonicalMediaName(layout, "ANSI_D_(22.00_x_34.00_Inches)");

// In BeginDocument, set plotToFile = true and provide the output path
engine.BeginDocument(plotInfo, doc.Name, null, 1, true,
    @"C:\Output\Plan.plt");
```

## PlotConfig and Device Enumeration

### Listing Available Plot Devices

```csharp
PlotSettingsValidator psv = PlotSettingsValidator.Current;
psv.RefreshLists(layout);

StringCollection devices = psv.GetPlotDeviceList();
foreach (string device in devices)
{
    ed.WriteMessage($"\n  Device: {device}");
}
```

### Listing Paper Sizes for a Device

```csharp
psv.SetPlotConfigurationName(layout, "DWG To PDF.pc3", null);
psv.RefreshLists(layout);

StringCollection mediaNames = psv.GetCanonicalMediaNameList(layout);
for (int i = 0; i < mediaNames.Count; i++)
{
    string canonical = mediaNames[i];
    string localName = psv.GetLocaleMediaName(layout, i);
    ed.WriteMessage($"\n  {canonical}  ({localName})");
}
```

### PlotConfig Object

```csharp
using Autodesk.AutoCAD.PlottingServices;

PlotConfig config = PlotConfigManager.CurrentConfig;
ed.WriteMessage($"\nDevice: {config.DeviceName}");
ed.WriteMessage($"\nDriver: {config.DriverName}");
ed.WriteMessage($"\nMax paper: {config.MaxMediaWidth} x {config.MaxMediaHeight}");
ed.WriteMessage($"\nPlot to file: {config.IsPlotToFile}");

// Get canonical media names
string[] mediaNames = config.CanonicalMediaNames;
foreach (string name in mediaNames)
{
    MediaBounds bounds = config.GetMediaBounds(name);
    ed.WriteMessage($"\n  {name}: " +
        $"page {bounds.PageSize.X:F2} x {bounds.PageSize.Y:F2}, " +
        $"printable {bounds.LowerLeftPrintableArea} to {bounds.UpperRightPrintableArea}");
}
```

## Preview Plot

```csharp
// Preview requires that the layout is current
LayoutManager.Current.CurrentLayout = layout.LayoutName;

PlotInfo plotInfo = new PlotInfo();
plotInfo.Layout = layout.ObjectId;

PlotInfoValidator piv = new PlotInfoValidator();
piv.MediaMatchingPolicy = MatchingPolicy.MatchEnabled;
piv.Validate(plotInfo);

// Show the standard plot preview window
PreviewEndPlotInfo previewResult;
using (PlotEngine engine = PlotFactory.CreatePreviewEngine(
    (int)PreviewEngineFlags.Plot))
{
    engine.BeginPlot(null, null);
    engine.BeginDocument(plotInfo, doc.Name, null, 1, false, null);

    PlotPageInfo pageInfo = new PlotPageInfo();
    engine.BeginPage(pageInfo, plotInfo, true, null);
    engine.BeginGenerateGraphics(null);
    engine.EndGenerateGraphics(null);
    engine.EndPage(null);

    previewResult = new PreviewEndPlotInfo();
    engine.EndDocument(previewResult);
    engine.EndPlot(null);
}
```

## BACKGROUNDPLOT System Variable

Controls whether plotting runs in the foreground or background.

```csharp
// 0 = foreground (required for PlotEngine API usage)
// 1 = background for plot commands
// 2 = background for publish commands
// 3 = background for both plot and publish

short bgPlot = (short)Application.GetSystemVariable("BACKGROUNDPLOT");

// Disable background plotting before API-driven plot
Application.SetSystemVariable("BACKGROUNDPLOT", (short)0);

// ... perform plot ...

// Restore original value
Application.SetSystemVariable("BACKGROUNDPLOT", bgPlot);
```

Background plotting must be disabled (set to 0) when using `PlotEngine` or `Publisher.PublishExecute` from .NET. If background plot is active, the API call may silently fail or produce incomplete output.

## PlotReactorManager Events

`PlotReactorManager` provides events before, during, and after plot operations.

```csharp
PlotReactorManager prm = new PlotReactorManager();

prm.BeginPlot += (sender, e) =>
{
    ed.WriteMessage("\nPlot started.");
};

prm.BeginDocument += (sender, e) =>
{
    ed.WriteMessage($"\nPlotting document: {e.DocumentName}");
};

prm.BeginPage += (sender, e) =>
{
    ed.WriteMessage($"\nPlotting page {e.SheetNumber}.");
};

prm.EndPage += (sender, e) =>
{
    ed.WriteMessage($"\nFinished page.");
};

prm.EndDocument += (sender, e) =>
{
    ed.WriteMessage($"\nDocument plot complete.");
};

prm.EndPlot += (sender, e) =>
{
    ed.WriteMessage($"\nPlot job finished.");
};

prm.PlotCancelled += (sender, e) =>
{
    ed.WriteMessage("\nPlot was cancelled.");
};
```

Keep the `PlotReactorManager` instance alive (e.g., as a static field) for the duration of the session. If it is garbage collected, events stop firing.

## Gotchas

- `PlotSettingsValidator` methods modify the target `PlotSettings`/`Layout` object directly -- it must be opened `ForWrite` before calling any PSV method
- `psv.RefreshLists()` must be called after `SetPlotConfigurationName()` and before querying paper sizes -- otherwise the media list is stale from the previous device
- `PlotFactory.ProcessPlotState` must be `NotPlotting` before calling `CreatePublishEngine()` -- check it first to avoid `eAlreadyActive` errors
- `BACKGROUNDPLOT` must be set to `0` before using `PlotEngine` or `Publisher.PublishExecute` from .NET -- background mode causes silent failures
- `PlotEngine` calls must follow the exact sequence: `BeginPlot` -> `BeginDocument` -> (`BeginPage` -> `BeginGenerateGraphics` -> `EndGenerateGraphics` -> `EndPage`)* -> `EndDocument` -> `EndPlot` -- skipping or reordering steps throws
- `PlotProgressDialog` constructor's first parameter (`isPreview`) should be `false` for actual plotting
- `DsdData.WriteDsd()` then `ReadDsd()` round-trip is required for `PublishExecute` -- passing an in-memory DSD without writing to disk fails
- Canonical media names are device-specific and may differ between PC3 files -- always query `GetCanonicalMediaNameList()` after setting the device
- `PlotSettings(false)` creates paper space settings; `PlotSettings(true)` creates model space settings -- using the wrong constructor causes unexpected behavior
- `PlotFactory.CreatePreviewEngine()` opens a modal preview window and blocks until the user closes it
- The `PlotReactorManager` instance must be kept alive (static field) -- if garbage collected, events silently stop
- Plotting from a modeless dialog requires wrapping the plot call in `Document.LockDocument()` or using `DocumentLock`
- `Publisher.PublishExecute` does not return errors -- subscribe to `PlotReactorManager` events or check output files to verify success
- When plotting multiple pages to one PDF, all pages must be sent within the same `BeginDocument`/`EndDocument` pair

## Related Skills

- `acad-layouts-viewports` -- layouts inherit from PlotSettings; viewport configuration determines what gets plotted
- `acad-layers` -- layer IsPlottable property and viewport layer overrides affect plot output
- `acad-linetypes-textstyles` -- lineweights and linetypes render differently depending on plot scale and PrintLineweights setting
