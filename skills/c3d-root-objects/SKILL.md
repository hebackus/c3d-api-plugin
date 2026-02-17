---
name: c3d-root-objects
description: CivilApplication, CivilDocument, transactions, collections, settings hierarchy, and document locking patterns
---

# Civil 3D Root Objects and Common Concepts

Use this skill when accessing base Civil 3D objects, working with transactions, iterating collections, or configuring settings.

## Root Object Hierarchy

```
CivilApplication
  └── ActiveDocument (CivilDocument)
        ├── GetAlignmentIds()
        ├── GetSitelessAlignmentIds()
        ├── GetSiteIds()
        ├── GetSurfaceIds()
        ├── GetPipeNetworkIds()
        ├── CorridorCollection
        ├── CogoPoints
        ├── PointGroups
        ├── Styles (StylesRoot)
        │     ├── AlignmentStyles
        │     ├── ProfileStyles
        │     ├── ProfileViewStyles
        │     ├── SurfaceStyles
        │     ├── PipeStyles
        │     ├── StructureStyles
        │     ├── PointStyles
        │     ├── InterferenceStyles
        │     ├── AssemblyStyles
        │     ├── LinkStyles
        │     ├── ShapeStyles
        │     ├── CodeSetStyles
        │     ├── PartsListSet
        │     ├── LabelStyles (all label style roots)
        │     ├── LabelSetStyles
        │     └── ProfileViewBandSetStyles
        └── Settings (SettingsRoot)
              ├── DrawingSettings
              └── GetSettings<T>() / GetFeatureSettings<T>()
```

## Accessing Application and Document

```csharp
using Autodesk.Civil.ApplicationServices;

CivilDocument doc = CivilApplication.ActiveDocument;
```

**Note:** `CivilApplication` does NOT inherit from AutoCAD's `Application`. For application-level access (open documents, main window), use `Autodesk.AutoCAD.ApplicationServices.Application` directly.

## Transaction Pattern

All Civil 3D object reads/writes MUST be inside a Transaction:

```csharp
using (Transaction ts = Application.DocumentManager.MdiActiveDocument
    .Database.TransactionManager.StartTransaction())
{
    // Read objects
    Alignment align = ts.GetObject(alignId, OpenMode.ForRead) as Alignment;

    // Write objects (must open ForWrite)
    align = ts.GetObject(alignId, OpenMode.ForWrite) as Alignment;
    align.StyleId = newStyleId;

    // MUST commit for changes to persist
    ts.Commit();
}
```

**Best practice:** Use `using` statement for automatic disposal. Otherwise, explicitly dispose in a `finally` block.

## ObjectId Collections

Collections return `ObjectIdCollection` (not typed objects). You must cast via `Transaction.GetObject()`:

```csharp
ObjectIdCollection alignmentIds = doc.GetAlignmentIds();
foreach (ObjectId objId in alignmentIds)
{
    Alignment align = ts.GetObject(objId, OpenMode.ForRead) as Alignment;
    ed.WriteMessage("Alignment: {0}\n", align.Name);
}
```

## Creating Styles

```csharp
// Add returns ObjectId of new style
ObjectId styleId = doc.Styles.PointStyles.Add("MyStyle");
PointStyle style = ts.GetObject(styleId, OpenMode.ForWrite) as PointStyle;
style.Elevation = 114.6;
ts.Commit(); // Required for add/modify to take effect
```

## Handling Duplicate Names

```csharp
try
{
    // Throws ArgumentException if style doesn't exist
    ObjectId styleId = doc.Styles.PointStyles["Name"];
}
catch (ArgumentException e)
{
    ed.WriteMessage(e.Message);
}
```

## Document Locking (for Modeless Forms / Toolbox)

When code runs outside document context (modeless dialogs, .NET toolbox execution), explicitly lock the document:

```csharp
using (DocumentLock locker = Application.DocumentManager
    .MdiActiveDocument.LockDocument())
{
    // Perform document/database modifications here
    CivilApplication.ActiveDocument.Settings
        .DrawingSettings.AmbientSettings.Station.Precision.Value = 2;
}
```

## Settings Hierarchy

Settings apply at three levels (each can override the previous):

1. **Drawing level** - `doc.Settings.DrawingSettings` (units, zone, abbreviations, ambient settings)
2. **Feature level** - `doc.Settings.GetSettings<SettingsAlignment>()` (overrides drawing ambient for that feature)
3. **Command level** - `doc.Settings.GetSettings<SettingsCmdCreateAlignmentLayout>()` (overrides both)

```csharp
// Feature settings
SettingsAlignment alignSettings = doc.Settings.GetSettings<SettingsAlignment>();
var angleSettings = alignSettings.Angle;
ed.WriteMessage("Precision: {0}, Unit: {1}\n",
    angleSettings.Precision.Value, angleSettings.Unit.Value);

// Command settings
SettingsCmdCreateAlignmentLayout cmdSettings =
    doc.Settings.GetSettings<SettingsCmdCreateAlignmentLayout>();
ed.WriteMessage("AlignmentType: {0}",
    cmdSettings.AlignmentTypeOption.AlignmentType.Value);
```

**Note:** Feature settings are in domain-specific namespaces (e.g., `Autodesk.Civil.Land.Settings` for alignments). Drawing/ambient settings are in `Autodesk.Civil.Settings`.

## Property Value Pattern

In the .NET API, most properties use `Property*` classes implementing `IProperty`. Access values via `.Value`:

```csharp
// COM: oComponent.Visibility = True
// .NET: oComponent.General.Visible.Value = true;
```

## Error Handling Pattern

```csharp
[CommandMethod("MYCOMMAND")]
public void MyCommand()
{
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
    try
    {
        using (Transaction ts = ...)
        {
            // work
            ts.Commit();
        }
    }
    catch (System.Exception e)
    {
        ed.WriteMessage("\nError: {0}\n", e.Message);
    }
}
```

## Surface Namespace Conflict

`Surface` exists in both `Autodesk.AutoCAD.DatabaseServices` and `Autodesk.Civil.DatabaseServices`. Disambiguate with alias:

```csharp
using CivSurface = Autodesk.Civil.DatabaseServices.Surface;
```

## Gotchas

- Adding an element with a duplicate name throws an error - trap it
- Accessing a non-existent item throws `ArgumentException`
- Removing an in-use item throws an error
- `ObjectIdCollection` implements `IList` - can use `foreach` or index access
- Properties in .NET use `.Value` getter/setter (unlike COM's direct property access)
- Some properties have moved to sub-properties (e.g., `Visibility` -> `General.Visible`)

## Related Skills

- `c3d-project-setup` - Project configuration and references
- `c3d-label-styles` - Label style creation and components
