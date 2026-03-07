---
name: acad-layouts-viewports
description: Paper space layouts, layout manager, viewport creation and configuration, viewport properties, model space vs paper space, plot settings, viewport layer overrides, layout events
---

# AutoCAD Layouts and Viewports

Use this skill when creating or managing paper space layouts, inserting and configuring viewports, switching between model space and paper space, setting viewport properties (scale, center, locked, layer overrides), or configuring plot settings on layouts.

## Model Space vs Paper Space

AutoCAD drawings contain one model space and one or more paper space layouts. Each layout is backed by a `BlockTableRecord`.

```csharp
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    BlockTable bt = (BlockTable)tr.GetObject(db.BlockTableId, OpenMode.ForRead);

    // Model space block table record
    BlockTableRecord modelSpace = (BlockTableRecord)tr.GetObject(
        bt[BlockTableRecord.ModelSpace], OpenMode.ForRead);

    // Paper space block table record (the first/default paper space)
    BlockTableRecord paperSpace = (BlockTableRecord)tr.GetObject(
        bt[BlockTableRecord.PaperSpace], OpenMode.ForRead);

    // Current space (model or paper depending on active tab)
    BlockTableRecord currentSpace = (BlockTableRecord)tr.GetObject(
        db.CurrentSpaceId, OpenMode.ForWrite);

    tr.Commit();
}
```

- `BlockTableRecord.ModelSpace` is the string constant `"*Model_Space"`
- `BlockTableRecord.PaperSpace` is the string constant `"*Paper_Space"`
- Additional paper space layouts use `"*Paper_Space0"`, `"*Paper_Space1"`, etc.

## Layout Access

### LayoutManager

```csharp
LayoutManager layoutMgr = LayoutManager.Current;

// Get the current layout name
string currentName = layoutMgr.CurrentLayout;

// Get layout count (includes "Model" tab)
int count = layoutMgr.LayoutCount;

// Switch to a layout by name
layoutMgr.CurrentLayout = "Layout1";
```

### Enumerating Layouts via LayoutDictionary

```csharp
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    DBDictionary layoutDict = (DBDictionary)tr.GetObject(
        db.LayoutDictionaryId, OpenMode.ForRead);

    foreach (DBDictionaryEntry entry in layoutDict)
    {
        Layout layout = (Layout)tr.GetObject(entry.Value, OpenMode.ForRead);
        ed.WriteMessage($"\n{layout.LayoutName} (Tab order: {layout.TabOrder})");
    }

    tr.Commit();
}
```

### Getting a Layout by Name

```csharp
DBDictionary layoutDict = (DBDictionary)tr.GetObject(
    db.LayoutDictionaryId, OpenMode.ForRead);

if (layoutDict.Contains("Sheet 1"))
{
    Layout layout = (Layout)tr.GetObject(
        layoutDict.GetAt("Sheet 1"), OpenMode.ForRead);
    ObjectId blockId = layout.BlockTableRecordId;
}
```

## Layout Properties

- `LayoutName` (string, get/set) — display name on the tab
- `TabOrder` (int, get/set) — position in the tab bar (0 = Model)
- `TabSelected` (bool, get/set) — whether this tab is active
- `BlockTableRecordId` (ObjectId, get-only) — associated paper space BTR
- `ModelType` (bool, get-only) — true for the Model tab, false for paper space
- `PlotPaperSize` (Point2d, get-only) — current paper dimensions
- `PlotOrigin` (Point2d, get-only) — plot origin offset
- `PlotRotation` (PlotRotation, get-only) — plot rotation angle
- `Extents` (Extents3d) — layout extents
- `Limits` (Point2d Min/Max) — limits of the layout

## Creating Layouts

### Create a New Layout

```csharp
LayoutManager layoutMgr = LayoutManager.Current;

// CreateLayout returns the ObjectId of the new layout
ObjectId newLayoutId = layoutMgr.CreateLayout("My New Sheet");

using (Transaction tr = db.TransactionManager.StartTransaction())
{
    Layout newLayout = (Layout)tr.GetObject(newLayoutId, OpenMode.ForWrite);
    newLayout.TabOrder = layoutMgr.LayoutCount;  // place at end

    tr.Commit();
}
```

### Copy an Existing Layout

```csharp
LayoutManager layoutMgr = LayoutManager.Current;

// CopyLayout copies the source layout including all entities and settings
layoutMgr.CopyLayout("Layout1", "Layout1 - Copy");
```

### Delete a Layout

```csharp
LayoutManager layoutMgr = LayoutManager.Current;

// Cannot delete the Model tab or the last paper space layout
layoutMgr.DeleteLayout("Sheet to Remove");
```

### Rename a Layout

```csharp
LayoutManager layoutMgr = LayoutManager.Current;
layoutMgr.RenameLayout("OldName", "NewName");
```

## Viewport Creation

### Creating a Viewport in Paper Space

```csharp
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    BlockTable bt = (BlockTable)tr.GetObject(db.BlockTableId, OpenMode.ForRead);
    Layout layout = (Layout)tr.GetObject(
        layoutMgr.GetLayoutId("Sheet 1"), OpenMode.ForRead);
    BlockTableRecord paperBtr = (BlockTableRecord)tr.GetObject(
        layout.BlockTableRecordId, OpenMode.ForWrite);

    Viewport vp = new Viewport();
    vp.CenterPoint = new Point3d(5.5, 4.25, 0);   // center in paper space units
    vp.Width = 8.0;                                  // width in paper space units
    vp.Height = 5.0;                                 // height in paper space units

    paperBtr.AppendEntity(vp);
    tr.AddNewlyCreatedDBObject(vp, true);

    // Set the view target (model space coordinates to display)
    vp.ViewTarget = new Point3d(1000, 2000, 0);
    vp.ViewCenter = new Point2d(1000, 2000);
    vp.ViewHeight = 250.0;  // controls zoom level (model space units visible)

    // Set custom scale (e.g., 1:50)
    vp.CustomScale = 1.0 / 50.0;

    // Turn the viewport on
    vp.On = true;

    // Lock the viewport to prevent accidental zoom/pan
    vp.Locked = true;

    tr.Commit();
}
```

### Overall Viewport (Layout Default)

Every paper space layout has an overall viewport (the paper boundary) with `Number = 1`. It is created automatically and should not be deleted.

```csharp
// Find the overall viewport
ObjectIdCollection vpIds = layout.GetViewports();
foreach (ObjectId vpId in vpIds)
{
    Viewport vp = (Viewport)tr.GetObject(vpId, OpenMode.ForRead);
    if (vp.Number == 1)
    {
        // This is the overall (paper space boundary) viewport
        continue;
    }
    // Process user-created viewports
}
```

## Viewport Properties

- `CenterPoint` (Point3d, get/set) — center in paper space coordinates
- `Width` (double, get/set) — viewport width in paper space units
- `Height` (double, get/set) — viewport height in paper space units
- `ViewCenter` (Point2d, get/set) — model space center point displayed
- `ViewTarget` (Point3d, get/set) — model space target point
- `ViewHeight` (double, get/set) — visible model space height (controls zoom)
- `ViewDirection` (Vector3d, get/set) — view direction vector
- `TwistAngle` (double, get/set) — rotation of the view in radians
- `CustomScale` (double, get/set) — viewport scale (paper/model ratio)
- `StandardScale` (StandardScaleType, get/set) — predefined scale enum
- `On` (bool, get/set) — viewport is active and displays model space
- `Locked` (bool, get/set) — prevent interactive zoom/pan
- `Number` (int, get-only) — viewport number (1 = overall paper viewport)
- `UcsPerViewport` (bool, get/set) — save UCS per viewport
- `ShadePlot` (ShadePlotType, get/set) — visual style for plotting
- `VisualStyleId` (ObjectId, get/set) — visual style applied in viewport
- `EffectivePlotStyleSheet` (string, get-only) — resolved plot style sheet
- `NonRectClipEntityId` (ObjectId, get/set) — clipping boundary entity
- `NonRectClipOn` (bool, get/set) — enable non-rectangular clipping
- `GridOn` (bool, get/set) — grid visibility in viewport
- `UcsIconVisible` (bool, get/set) — UCS icon visibility
- `Layer` (string, get/set) — layer of the viewport boundary entity

### Standard Scale Types

```csharp
vp.StandardScale = StandardScaleType.ScaleToFit;
vp.StandardScale = StandardScaleType.CustomScale;
// Other values: Scale1To1, Scale1To2, Scale1To4, Scale1To5, Scale1To8,
// Scale1To10, Scale1To16, Scale1To20, Scale1To30, Scale1To40, Scale1To50,
// Scale1To100, Scale2To1, Scale4To1, Scale8To1, Scale10To1, Scale100To1
```

## Viewport Configuration

### Setting Viewport Scale and Center

```csharp
Viewport vp = (Viewport)tr.GetObject(vpId, OpenMode.ForWrite);

// Center the view on model space coordinates
vp.ViewCenter = new Point2d(5000, 3000);
vp.ViewTarget = new Point3d(5000, 3000, 0);

// Set scale: CustomScale = paper_units / model_units
// For 1" = 20' scale (1:240 when base unit is inches):
vp.CustomScale = 1.0 / 240.0;

// Or use ViewHeight to control zoom (model space units visible vertically)
// ViewHeight = viewport_paper_height / custom_scale
vp.ViewHeight = vp.Height / vp.CustomScale;
```

### Non-Rectangular (Clipped) Viewports

```csharp
// Create a clipping boundary (circle, polyline, etc.)
Circle clipBoundary = new Circle(new Point3d(5, 4, 0), Vector3d.ZAxis, 3.0);
paperBtr.AppendEntity(clipBoundary);
tr.AddNewlyCreatedDBObject(clipBoundary, true);

// Assign the clip boundary to the viewport
vp.NonRectClipEntityId = clipBoundary.ObjectId;
vp.NonRectClipOn = true;
```

## Viewport Layer Property Overrides

Viewport-specific layer overrides control per-viewport layer visibility, color, linetype, lineweight, transparency, and plot style without affecting other viewports or model space.

### VP Freeze (Per-Viewport Layer Visibility)

```csharp
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    Viewport vp = (Viewport)tr.GetObject(vpId, OpenMode.ForWrite);
    LayerTable lt = (LayerTable)tr.GetObject(db.LayerTableId, OpenMode.ForRead);

    // Freeze layers in this viewport
    ObjectIdCollection freezeIds = new ObjectIdCollection();
    freezeIds.Add(lt["C-TOPO-CONTOUR"]);
    freezeIds.Add(lt["C-ROAD-CENTERLINE"]);
    vp.FreezeLayersInViewport(freezeIds.GetEnumerator());

    // Thaw layers in this viewport
    ObjectIdCollection thawIds = new ObjectIdCollection();
    thawIds.Add(lt["C-TOPO-CONTOUR"]);
    vp.ThawLayersInViewport(thawIds.GetEnumerator());

    tr.Commit();
}
```

### Checking VP Frozen State

```csharp
LayerTableRecord layer = (LayerTableRecord)tr.GetObject(layerId, OpenMode.ForRead);

// Check if a layer is frozen in a specific viewport
bool isFrozenInVp = layer.IsVpFrozen(vpId);
```

### VP Color, Linetype, Lineweight, Transparency Overrides

```csharp
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    Viewport vp = (Viewport)tr.GetObject(vpId, OpenMode.ForWrite);
    LayerTable lt = (LayerTable)tr.GetObject(db.LayerTableId, OpenMode.ForRead);
    ObjectId layerId = lt["C-ROAD-CURB"];

    // Set viewport-specific color override
    vp.SetLayerPropertyOverrides(layerId,
        new LayerPropertyOverrides
        {
            Color = Color.FromColorIndex(ColorMethod.ByAci, 1),  // red in this VP
            Linetype = db.ContinuousLinetype,
            LineWeight = LineWeight.LineWeight050,
            Transparency = new Transparency(30),
            IsOverriddenColor = true,
            IsOverriddenLinetype = true,
            IsOverriddenLineWeight = true,
            IsOverriddenTransparency = true
        });

    // Remove overrides for a layer
    vp.RemoveLayerPropertyOverrides(layerId);

    tr.Commit();
}
```

### Default Viewport Visibility for New Viewports

```csharp
LayerTableRecord layer = (LayerTableRecord)tr.GetObject(layerId, OpenMode.ForWrite);

// When false, new viewports will have this layer frozen by default
layer.ViewportVisibilityDefault = false;
```

## Switching Layouts Programmatically

```csharp
// Switch active layout tab
LayoutManager layoutMgr = LayoutManager.Current;
layoutMgr.CurrentLayout = "Sheet 1";

// Switch to model space
layoutMgr.CurrentLayout = "Model";

// Set active viewport in paper space (MSPACE/PSPACE equivalent)
// Use Editor.SwitchToModelSpace / SwitchToPaperSpace for interactive switching
Document doc = Application.DocumentManager.MdiActiveDocument;
Editor ed = doc.Editor;

// Switch to model space within the current paper space layout
ed.SwitchToModelSpace();

// Switch back to paper space
ed.SwitchToPaperSpace();
```

### Activating a Specific Viewport

```csharp
// Set the active viewport by viewport number
// MdiActiveDocument.Editor.CurrentViewportObjectId targets a specific VP
ed.CurrentViewportObjectId = vpId;
```

## Plot Settings on Layouts

Every `Layout` inherits from `PlotSettings`. Use `PlotSettingsValidator` to configure plot parameters.

### Configuring Plot Settings

```csharp
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    Layout layout = (Layout)tr.GetObject(layoutId, OpenMode.ForWrite);
    PlotSettingsValidator psv = PlotSettingsValidator.Current;

    // Refresh the list of available devices
    psv.RefreshLists(layout);

    // Set the plot device (printer/plotter)
    psv.SetPlotConfigurationName(layout, "DWG To PDF.pc3", null);

    // Refresh after device change to get available paper sizes
    psv.RefreshLists(layout);

    // Set the paper size
    StringCollection mediaNames = psv.GetCanonicalMediaNameList(layout);
    // Find desired paper size (e.g., "ANSI_D_(22.00_x_34.00_Inches)")
    foreach (string media in mediaNames)
    {
        string localName = psv.GetLocaleMediaName(layout, media);
        if (localName.Contains("22") && localName.Contains("34"))
        {
            psv.SetCanonicalMediaName(layout, media);
            break;
        }
    }

    // Set plot area
    psv.SetPlotType(layout, Autodesk.AutoCAD.DatabaseServices.PlotType.Layout);
    // Other PlotType values: Display, Extents, Limits, View, Window

    // Set plot scale
    psv.SetUseStandardScale(layout, true);
    psv.SetStdScaleType(layout, StdScaleType.StdScale1To1);

    // Or set a custom scale
    psv.SetUseStandardScale(layout, false);
    psv.SetCustomPrintScale(layout, new CustomScale(1.0, 1.0));

    // Plot offset (center the plot)
    psv.SetPlotCentered(layout, true);
    // Or set manual offset
    // psv.SetPlotOrigin(layout, new Point2d(0.5, 0.25));

    // Plot style table
    psv.SetCurrentStyleSheet(layout, "monochrome.ctb");

    // Plot rotation
    psv.SetPlotRotation(layout, PlotRotation.Degrees000);

    tr.Commit();
}
```

### PlotSettings Properties (inherited by Layout)

- `PlotConfigurationName` (string, get-only) — plotter/device name
- `CanonicalMediaName` (string, get-only) — paper size canonical name
- `PlotSettingsName` (string, get/set) — page setup name
- `CurrentStyleSheet` (string, get-only) — plot style table (.ctb or .stb)
- `PlotType` (PlotType, get-only) — plot area type
- `PlotRotation` (PlotRotation, get-only) — rotation
- `PlotPaperSize` (Point2d, get-only) — paper dimensions
- `PlotOrigin` (Point2d, get-only) — plot origin offset
- `PlotPaperMargins` (Extents2d, get-only) — non-printable margins
- `UseStandardScale` (bool, get-only) — using standard vs custom scale
- `StdScale` (double, get-only) — standard scale value
- `CustomPrintScale` (CustomScale, get-only) — custom scale
- `PlotCentered` (bool, get-only) — plot centered on paper
- `PlotHidden` (bool, get/set) — plot with hidden lines removed
- `PlotPlotStyles` (bool, get/set) — apply plot styles
- `PrintLineweights` (bool, get/set) — print lineweights
- `ScaleLineweights` (bool, get/set) — scale lineweights with plot scale
- `DrawViewportsFirst` (bool, get/set) — draw paper space last
- `ShadePlot` (ShadePlotType, get/set) — shade plot mode

### Page Setups (Named PlotSettings)

```csharp
// Access the plot settings dictionary for named page setups
DBDictionary plotSettingsDict = (DBDictionary)tr.GetObject(
    db.PlotSettingsDictionaryId, OpenMode.ForRead);

foreach (DBDictionaryEntry entry in plotSettingsDict)
{
    PlotSettings ps = (PlotSettings)tr.GetObject(entry.Value, OpenMode.ForRead);
    ed.WriteMessage($"\nPage setup: {ps.PlotSettingsName}");
}

// Apply a named page setup to a layout
layout.CopyFrom(pageSetupPlotSettings);
```

## Layout Events

```csharp
LayoutManager layoutMgr = LayoutManager.Current;

// Fires when the current layout tab changes
layoutMgr.LayoutSwitched += (sender, e) =>
{
    ed.WriteMessage($"\nSwitched to layout: {e.LayoutName}");
};

// Fires when a layout is about to be renamed
layoutMgr.LayoutRenamed += (sender, e) =>
{
    ed.WriteMessage($"\nLayout renamed: {e.OldName} -> {e.NewName}");
};

// Fires when a layout is about to be removed
layoutMgr.LayoutRemoved += (sender, e) =>
{
    ed.WriteMessage($"\nLayout removed: {e.LayoutName}");
};

// Fires when a layout is created or copied
layoutMgr.LayoutCreated += (sender, e) =>
{
    ed.WriteMessage($"\nLayout created: {e.LayoutName}");
};

// Fires when tab order changes
layoutMgr.LayoutsReordered += (sender, e) =>
{
    ed.WriteMessage("\nLayout tabs reordered.");
};
```

## Gotchas

- The Model tab is a layout too (`Layout.ModelType == true`) and is always present in the layout dictionary -- do not delete it
- Every paper space layout auto-creates an overall viewport (`Number == 1`) representing the paper boundary -- do not erase it
- `Viewport.On = true` must be set explicitly after creation or the viewport appears blank
- `Viewport.CustomScale` is paper/model ratio: `1/50.0` means 1 paper unit = 50 model units
- `ViewHeight` and `CustomScale` are linked -- setting one recalculates the other; set `CustomScale` last if you need a precise scale
- `PlotSettingsValidator` methods modify the Layout object directly -- the Layout must be opened `ForWrite` before calling them
- `psv.RefreshLists()` must be called after `SetPlotConfigurationName()` before querying paper sizes -- otherwise the media list is stale
- `LayoutManager.CurrentLayout` setter throws if the layout name does not exist
- `FreezeLayersInViewport()` and `ThawLayersInViewport()` take an `IEnumerator` of ObjectIds, not an `ObjectIdCollection` directly -- call `.GetEnumerator()` on the collection
- Layer `"0"` cannot be VP-frozen
- Viewport layer overrides only take effect when the viewport is on and the layout is active
- `CopyLayout` copies all entities including viewports and their configurations
- `DeleteLayout` cannot remove the last remaining paper space layout
- `Layout.TabOrder` is 0-based with 0 reserved for Model -- paper space layouts start at 1
- Setting `Locked = true` on a viewport prevents user zoom/pan but code can still modify `ViewCenter` and `ViewHeight`

## Related Skills

- `acad-layers` — viewport layer property overrides extend base layer properties per-viewport
- `acad-blocks` — each layout is backed by a BlockTableRecord; layout entities live in paper space BTRs
- `acad-plot-publish` — batch plotting and publishing across multiple layouts
- `acad-editor-input` — switching layouts and activating viewports programmatically via Editor
