---
name: c3d-label-styles
description: Label style creation, components (text, line, block, tick), property fields, and style sharing between drawings
---

# Civil 3D Label Styles

Use this skill when creating, modifying, or querying label styles for any Civil 3D element (points, alignments, pipes, structures, etc.).

## Label Style Overview

All Civil 3D annotations are governed by `LabelStyle` objects. A label style can include text labels, tick marks, lines, markers, and direction arrows.

## Creating a Label Style

```csharp
CivilDocument doc = CivilApplication.ActiveDocument;

// Point label style
ObjectId labelStyleId = doc.Styles.LabelStyles
    .PointLabelStyles.LabelStyles.Add("NewPointLabelStyle");

// Alignment label styles are in LabelSetStyles
// Pipe label styles
// doc.Styles.LabelStyles.PipeLabelStyles  (LabelStylesPipeRoot)
// Structure label styles
// doc.Styles.LabelStyles.StructureLabelStyles (LabelStylesStructureRoot)
```

## Label Style Component Types

Components are the building blocks of a label:

| Type | Enum Value | Description |
|------|-----------|-------------|
| Text | `LabelStyleComponentType.Text` | Text content with property fields |
| Line | `LabelStyleComponentType.Line` | Line segments |
| Block | `LabelStyleComponentType.Block` | Block/symbol references |
| Tick | `LabelStyleComponentType.Tick` | Major/minor tick marks |
| ReferenceText | `LabelStyleComponentType.ReferenceText` | Referenced text |
| DirectionArrow | `LabelStyleComponentType.DirectionArrow` | Direction indicators |
| TextForEach | `LabelStyleComponentType.TextForEach` | Repeated text per item |

**Not all component types are valid for all label style types.** For example, adding a tick to a point label has no visible effect.

## Adding Components

```csharp
// Add a line component
ObjectId lineComponentId = oLabelStyle.AddComponent(
    "New Line Component", LabelStyleComponentType.Line);

// Get the new component for modification
var newLineComponent = ts.GetObject(lineComponentId, OpenMode.ForWrite)
    as LabelStyleLineComponent;

// CRITICAL: Set Visible to true
newLineComponent.General.Visible.Value = true;
newLineComponent.Line.Color.Value =
    Autodesk.AutoCAD.Colors.Color.FromColorIndex(
        Autodesk.AutoCAD.Colors.ColorMethod.ByAci, 40);
newLineComponent.Line.Angle.Value = 2.094; // radians = 120 degrees
newLineComponent.Line.Length.Value = -0.015; // negative = opposite direction
newLineComponent.Line.StartPointXOffset.Value = 0.005;
newLineComponent.Line.StartPointYOffset.Value = -0.005;
```

## Querying Components

```csharp
// Get count of text components
int count = oLabelStyle.GetComponentsCount(LabelStyleComponentType.Text);

// Get all text components
ObjectIdCollection textComps = oLabelStyle.GetComponents(
    LabelStyleComponentType.Text);

// Access first text component
var textComp = ts.GetObject(textComps[0], OpenMode.ForWrite)
    as LabelStyleTextComponent;
```

## Check for Existing Components (Ambient Settings)

New label styles inherit components from ambient settings. Always check before adding:

```csharp
if (oLabelStyle.GetComponentsCount(LabelStyleComponentType.Text) == 0)
{
    oLabelStyle.AddComponent("New Text", LabelStyleComponentType.Text);
}

// Then modify the first one:
ObjectIdCollection textCompCol = oLabelStyle.GetComponents(
    LabelStyleComponentType.Text);
var newTextComponent = ts.GetObject(textCompCol[0], OpenMode.ForWrite)
    as LabelStyleTextComponent;
```

## Property Fields in Label Text

Text content uses property fields with the format:
```
<[Property name (modifier1|modifier2|...|modifierN)]>
```

Modifiers are optional, can be in any order. Multiple fields can be combined with normal text.

```csharp
var textComp = ts.GetObject(textCompCol[0], OpenMode.ForWrite)
    as LabelStyleTextComponent;

// Design speed and station
textComp.Text.Contents.Value = "SPD=<[Design Speed(P0|RN|AP|Sn)]>";
textComp.Text.Contents.Value += " STA=<[Station Value(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>";
```

### Common Property Field Modifiers

| Modifier | Meaning |
|----------|---------|
| `Uft` | Unit: feet |
| `Um` | Unit: meters |
| `Udeg` | Unit: degrees |
| `P0`-`P6` | Precision (decimal places) |
| `RN` | Round nearest |
| `AP` | Apply |
| `Sn` | Sign |
| `FS` | Full station |
| `CP` | Current precision |
| `OF` | Offset |
| `TP` | Thousands separator |
| `EN` | Engineering notation |
| `W0` | Width zero-fill |
| `B2` | Base 2 |

### Point Label Property Fields

```
<[Name(CP)]>
<[Point Number]>
<[Northing(Uft|P4|RN|AP|Sn|OF)]>
<[Easting(Uft|P4|RN|AP|Sn|OF)]>
<[Raw Description(CP)]>
<[Full Description(CP)]>
<[Point Elevation(Uft|P3|RN|AP|Sn|OF)]>
<[Latitude(Udeg|FDMSdSp|P6|RN|DPSn|CU|AP|OF)]>
<[Longitude(Udeg|FDMSdSp|P6|RN|DPSn|CU|AP|OF)]>
<[Grid Northing(Uft|P4|RN|AP|Sn|OF)]>
<[Grid Easting(Uft|P4|RN|AP|Sn|OF)]>
```

### Alignment Label Property Fields

```
<[Station Value(Uft|FS|P0|RN|AP|Sn|TP|B2|EN|W0|OF)]>
<[Raw Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>
<[Northing(Uft|P4|RN|AP|Sn|OF)]>
<[Easting(Uft|P4|RN|AP|Sn|OF)]>
<[Design Speed(P3|RN|AP|Sn|OF)]>
<[Alignment Name(CP)]>
<[Alignment Description(CP)]>
<[Alignment Length(Uft|P3|RN|AP|Sn|OF)]>
<[Alignment Start Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>
<[Alignment End Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>
```

## Sharing Styles Between Drawings

Export styles to another open drawing:

```csharp
// Export a single style
ObjectId styleId = doc.Styles.LabelSetStyles
    .AlignmentLabelSetStyles.MajorStationLabelStyles[0];
LabelStyle style = ts.GetObject(styleId, OpenMode.ForRead) as LabelStyle;

Database destDb = null;
foreach (Document d in Application.DocumentManager)
{
    if (d.Name.Equals("Drawing1.dwg")) destDb = d.Database;
}

// StyleConflictResolverType: how to handle name conflicts
style.ExportTo(destDb, StyleConflictResolverType.Override);

// Export collections of styles
StyleBase.ExportTo(styleCollection, destDb, StyleConflictResolverType.Override);
```

## Label Style Filtering (from this codebase)

The `LabelFilterHelper` class in `SharedTypes.cs` filters label styles by:
- **View type keyword** (e.g., "Plan", "Profile", "Section")
- **Parts list prefix** (e.g., "P_Sanitary" -> "U_P")

## Gotchas

- New label styles are initialized from ambient settings - may already contain components
- Adding an invalid component type (e.g., tick to a point label) compiles but has no visible effect
- Labels depend on graphical objects (blocks) that may not exist in the current document
- The `.Value` pattern applies to all label properties (e.g., `component.General.Visible.Value = true`)
- Ambient settings determine units - account for different drawings having different unit settings
- Duplicate component names throw `ArgumentException`

## Related Skills

- `c3d-root-objects` - Accessing styles through CivilDocument
- `c3d-pipe-networks` - Pipe and structure label styles
- `c3d-alignments` - Alignment label set styles
- `c3d-points` - Point label styles and description keys
