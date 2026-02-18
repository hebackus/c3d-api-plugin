---
name: c3d-label-styles
description: Label style creation, components (text, line, block, tick, direction arrow, reference text, text-for-each), property fields, style hierarchy, draw order, and style sharing between drawings
---

# Civil 3D Label Styles

Use this skill when creating, modifying, or querying label styles for any Civil 3D element (points, alignments, pipes, structures, etc.).

## Label Style Overview

All Civil 3D annotations are governed by `LabelStyle` objects. A label style can include text labels, tick marks, lines, markers, direction arrows, reference text, and text-for-each components. Label styles support parent-child hierarchies where child styles inherit from their parent.

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

// Copy an existing style as a sibling (same parent)
LabelStyle existing = ts.GetObject(existingStyleId, OpenMode.ForRead) as LabelStyle;
ObjectId copyId = existing.CopyAsSibling("CopiedStyleName");
```

## Label Style Hierarchy (Parent/Child)

Label styles support a parent-child tree. Child styles inherit settings from their parent.

```csharp
LabelStyle parentStyle = ts.GetObject(parentStyleId, OpenMode.ForWrite) as LabelStyle;

// Add a child style
ObjectId childId = parentStyle.AddChild("ChildStyleName");

// Query children
int childCount = parentStyle.ChildrenCount;
ObjectId firstChildId = parentStyle[0];           // by index
ObjectId namedChildId = parentStyle["ChildName"];  // by name

// Get parent
ObjectId parentId = parentStyle.ParentLabelStyleId;

// Get all descendants (children, grandchildren, etc.)
ObjectIdCollection allDescendants = parentStyle.GetDescendantIds();

// Remove children
parentStyle.RemoveChild(0);                // by index
parentStyle.RemoveChild("ChildStyleName"); // by name
parentStyle.RemoveAllDescendants();        // remove entire subtree
```

## Label Style Properties (LabelStyleBase)

Access label-level properties through `LabelStyle.Properties`:

```csharp
LabelStyle oLabelStyle = ts.GetObject(styleId, OpenMode.ForWrite) as LabelStyle;
LabelStyleBase props = oLabelStyle.Properties;

// Label settings
props.Label.Visibility.Value = true;
props.Label.Layer.Value = "C-ANNO";
props.Label.TextStyle.Value = "Standard";
props.Label.DisplayMode.Value = LabelDisplayModeType.AsComposed;

// Behavior settings
props.Behavior.OrientationReference.Value = OrientationReferenceType.WorldCoordinateSystem;
props.Behavior.InsertOption.Value = LabelInsertionType.InTheMiddleOfCurve;
props.Behavior.InsideCurveOption.Value = LabelInsideCurveType.InsideCurve;

// Plan readability
props.PlanReadability.PlanReadable.Value = true;
props.PlanReadability.PlanReadableBias.Value = 1.5708; // radians (90 degrees)
props.PlanReadability.FlipAnchorsWithText.Value = true;

// Leader settings
props.Leader.Visibility.Value = true;
props.Leader.Shape.Value = LeaderShapeType.StraightLeader;
props.Leader.ArrowheadStyle.Value = "Closed Filled";
props.Leader.ArrowheadSize.Value = 0.1;
props.Leader.Color.Value = Autodesk.AutoCAD.Colors.Color.FromColorIndex(
    Autodesk.AutoCAD.Colors.ColorMethod.ByAci, 7);

// Dragged state components
props.DraggedStateComponents.DisplayType.Value = LabelContentDisplayType.AsComposed;
props.DraggedStateComponents.BorderVisibility.Value = true;
props.DraggedStateComponents.BorderType.Value = TextBorderType.Rectangular;
props.DraggedStateComponents.TextHeight.Value = 0.08;
props.DraggedStateComponents.Gap.Value = 0.01;
props.DraggedStateComponents.UseBackgroundMask.Value = true;
props.DraggedStateComponents.LeaderAttachment.Value = LeaderAttachmentType.TopOfTopLine;
props.DraggedStateComponents.LeaderJustification.Value = true;
```

## Label Style Component Types

Components are the building blocks of a label:

| Type | Enum Value | Description |
|------|-----------|-------------|
| Text | `LabelStyleComponentType.Text` | Text content with property fields |
| Line | `LabelStyleComponentType.Line` | Line segments |
| Block | `LabelStyleComponentType.Block` | Block/symbol references |
| Tick | `LabelStyleComponentType.Tick` | Tick marks (block-based) |
| ReferenceText | `LabelStyleComponentType.ReferenceText` | Text referencing another object |
| DirectionArrow | `LabelStyleComponentType.DirectionArrow` | Direction indicators |
| TextForEach | `LabelStyleComponentType.TextForEach` | Repeated text per curve/spiral/pipe |

Use `IsSupportedComponent()` to check whether a component type is valid for a given label style before adding it.

## Adding Components

```csharp
// Check if a component type is supported before adding
if (oLabelStyle.IsSupportedComponent(LabelStyleComponentType.Tick))
{
    oLabelStyle.AddComponent("New Tick", LabelStyleComponentType.Tick);
}

// Add a line component
ObjectId lineComponentId = oLabelStyle.AddComponent(
    "New Line Component", LabelStyleComponentType.Line);

// ReferenceText requires a selected type parameter
ObjectId refTextId = oLabelStyle.AddReferenceTextComponent(
    "Ref Surface Elev", ReferenceTextComponentSelectedType.Surface);
// ReferenceTextComponentSelectedType values: Alignment, CogoPoint, Parcel, Profile, Surface

// TextForEach requires a selected type parameter
ObjectId textForEachId = oLabelStyle.AddTextForEachComponent(
    "Curve Data", TextForEachComponentSelectedType.Curve);
// TextForEachComponentSelectedType values: Curve, Spiral, CurveOrSpiral,
//   StructureAllPipes, StructureInFlowPipes, StructureOutFlowPipes,
//   IntersectionAllAlignment
```

## Removing Components

```csharp
// Remove a component by name
oLabelStyle.RemoveComponent("Old Text Component");
```

## Querying Components

```csharp
// Get total component count (all types)
int totalCount = oLabelStyle.GetComponentsCount();

// Get count of text components
int textCount = oLabelStyle.GetComponentsCount(LabelStyleComponentType.Text);

// Get all text components
ObjectIdCollection textComps = oLabelStyle.GetComponents(
    LabelStyleComponentType.Text);

// Access first text component
var textComp = ts.GetObject(textComps[0], OpenMode.ForWrite)
    as LabelStyleTextComponent;
```

## Component Draw Order

Control the visual stacking order of components:

```csharp
// Get current draw order
ObjectId[] drawOrder = oLabelStyle.GetComponentsDrawOrder();

// Swap two components by index
oLabelStyle.SwitchComponentsDrawOrder(0, 2);

// Set the entire draw order at once
oLabelStyle.SetComponentsDrawOrder(new ObjectId[] { id1, id2, id3 });
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

## Text Component Properties

```csharp
var textComp = ts.GetObject(textCompId, OpenMode.ForWrite)
    as LabelStyleTextComponent;

// General
textComp.General.Visible.Value = true;
textComp.General.Name = "My Text";
textComp.General.AnchorLocation.Value = /* AnchorLocationType value */;
textComp.General.AnchorComponent.Value = "Feature";
textComp.General.UsedIn.Value = LayoutModeType.PlanAndProfile;
textComp.General.SpanOutsideSegments.Value = false;

// Text
textComp.Text.Contents.Value = "<[Station Value(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>";
textComp.Text.Height.Value = 0.08;
textComp.Text.MaxWidth.Value = 0.0;
textComp.Text.Angle.Value = 0.0;
textComp.Text.XOffset.Value = 0.0;
textComp.Text.YOffset.Value = -0.01;
textComp.Text.Attachment.Value = LabelTextAttachmentType.TopCenter;
textComp.Text.Color.Value = Autodesk.AutoCAD.Colors.Color.FromColorIndex(
    Autodesk.AutoCAD.Colors.ColorMethod.ByAci, 2);

// Border
textComp.Border.Visible.Value = true;
textComp.Border.BorderType.Value = TextBorderType.Rectangular;
textComp.Border.Gap.Value = 0.005;
textComp.Border.BackgroundMask.Value = true;
textComp.Border.Color.Value = Autodesk.AutoCAD.Colors.Color.FromColorIndex(
    Autodesk.AutoCAD.Colors.ColorMethod.ByAci, 7);
```

## Line Component Properties

```csharp
var lineComp = ts.GetObject(lineCompId, OpenMode.ForWrite)
    as LabelStyleLineComponent;

// General
lineComp.General.Visible.Value = true;
lineComp.General.Name = "My Line";
lineComp.General.StartAnchorPoint.Value = /* AnchorLocationType value */;
lineComp.General.StartPointAnchorComponent.Value = "Feature";
lineComp.General.UseEndPointAnchor.Value = true;
lineComp.General.EndAnchorPoint.Value = /* AnchorLocationType value */;
lineComp.General.EndPointAnchorComponent.Value = "My Text";
lineComp.General.UsedIn.Value = LayoutModeType.PlanAndProfile;

// Line
lineComp.Line.LengthType.Value = LabelStyleLengthType.Fixed;  // Fixed or PercentOfLabel
lineComp.Line.FixedLength.Value = 0.015;
lineComp.Line.PercentLength.Value = 50.0;  // used when LengthType is PercentOfLabel
lineComp.Line.Angle.Value = 2.094; // radians = 120 degrees
lineComp.Line.StartPointXOffset.Value = 0.005;
lineComp.Line.StartPointYOffset.Value = -0.005;
lineComp.Line.EndPointXOffset.Value = 0.0;
lineComp.Line.EndPointYOffset.Value = 0.0;
lineComp.Line.Color.Value = Autodesk.AutoCAD.Colors.Color.FromColorIndex(
    Autodesk.AutoCAD.Colors.ColorMethod.ByAci, 40);
```

**Note:** `LabelStyleLineComponent.StyleLine.Length` is deprecated since Civil 2012. Use `FixedLength` with `LengthType` set to `LabelStyleLengthType.Fixed` instead.

## Block Component Properties

```csharp
var blockComp = ts.GetObject(blockCompId, OpenMode.ForWrite)
    as LabelStyleBlockComponent;

// General
blockComp.General.Visible.Value = true;
blockComp.General.Name = "My Block";
blockComp.General.AnchorLocation.Value = /* AnchorLocationType value */;
blockComp.General.AnchorComponent.Value = "Feature";
blockComp.General.UsedIn.Value = LayoutModeType.PlanAndProfile;

// Block
blockComp.Block.BlockName.Value = "MyBlockDef";
blockComp.Block.BlockHeight.Value = 0.1;
blockComp.Block.RotationAngle.Value = 0.0;
blockComp.Block.Attachment.Value = BlockAttachmentType.MiddleCenter;
blockComp.Block.XOffset.Value = 0.0;
blockComp.Block.YOffset.Value = 0.0;
blockComp.Block.Color.Value = Autodesk.AutoCAD.Colors.Color.FromColorIndex(
    Autodesk.AutoCAD.Colors.ColorMethod.ByAci, 1);
```

## Tick Component Properties

```csharp
var tickComp = ts.GetObject(tickCompId, OpenMode.ForWrite)
    as LabelStyleTickComponent;

// General
tickComp.General.Visible.Value = true;
tickComp.General.Name = "My Tick";

// Tick (uses block definitions for tick marks)
tickComp.Tick.BlockName.Value = "TickBlock";
tickComp.Tick.BlockHeight.Value = 0.05;
tickComp.Tick.RotationAngle.Value = 0.0;
tickComp.Tick.AlignWithObject.Value = true;
tickComp.Tick.Color.Value = Autodesk.AutoCAD.Colors.Color.FromColorIndex(
    Autodesk.AutoCAD.Colors.ColorMethod.ByAci, 3);
```

## Direction Arrow Component Properties

```csharp
var arrowComp = ts.GetObject(arrowCompId, OpenMode.ForWrite)
    as LabelStyleDirectionArrowComponent;

// General
arrowComp.General.Visible.Value = true;
arrowComp.General.Name = "My Arrow";
arrowComp.General.AnchorLocation.Value = /* AnchorLocationType value */;
arrowComp.General.AnchorComponent.Value = "Feature";
arrowComp.General.UsedIn.Value = LayoutModeType.PlanAndProfile;
arrowComp.General.SpanOutsideSegments.Value = false;

// Direction Arrow
arrowComp.DirectionArrow.ArrowheadStyle.Value = "Closed Filled";
arrowComp.DirectionArrow.ArrowheadSize.Value = 0.1;
arrowComp.DirectionArrow.FixedLength.Value = true;
arrowComp.DirectionArrow.LengthOrMinimumLength.Value = 0.3;
arrowComp.DirectionArrow.RotationAngle.Value = 0.0;
arrowComp.DirectionArrow.XOffset.Value = 0.0;
arrowComp.DirectionArrow.YOffset.Value = 0.0;
arrowComp.DirectionArrow.Color.Value = Autodesk.AutoCAD.Colors.Color.FromColorIndex(
    Autodesk.AutoCAD.Colors.ColorMethod.ByAci, 5);
```

## Reference Text Component

Reference text pulls property fields from another Civil 3D object (alignment, point, parcel, profile, or surface). It inherits all `StyleText` and `StyleBorder` properties from the text component.

```csharp
// Must use the specialized add method
ObjectId refId = oLabelStyle.AddReferenceTextComponent(
    "Surface Elev", ReferenceTextComponentSelectedType.Surface);
var refComp = ts.GetObject(refId, OpenMode.ForWrite)
    as LabelStyleReferenceTextComponent;

// Read-only: which object type this references
string objType = refComp.General.ReferenceTextObjectType;

// Text and Border properties work identically to LabelStyleTextComponent
refComp.Text.Contents.Value = "ELEV=<[Surface Elevation(Uft|P2|RN|AP|Sn|OF)]>";
refComp.Text.Height.Value = 0.08;
refComp.Border.Visible.Value = false;
```

## TextForEach Component

Repeats text for each curve, spiral, or pipe in the labeled feature. It inherits text/border properties from the text component and adds content fields for curves and spirals.

```csharp
// Must use the specialized add method
ObjectId tfeId = oLabelStyle.AddTextForEachComponent(
    "Curve Info", TextForEachComponentSelectedType.CurveOrSpiral);
var tfeComp = ts.GetObject(tfeId, OpenMode.ForWrite)
    as LabelStyleTextForEachComponent;

// Read-only: what this iterates over
string iterType = tfeComp.General.TextForEach;

// Separate content strings for curves and spirals
tfeComp.Text.Contents.Value = "Default text";
tfeComp.Text.CurveContents.Value = "R=<[Radius(Uft|P2|RN|AP|Sn|OF)]>";
tfeComp.Text.SpiralContents.Value = "L=<[Spiral Length(Uft|P2|RN|AP|Sn|OF)]>";
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
ObjectId styleId = doc.Styles.LabelStyles
    .AlignmentLabelStyles.MajorStationLabelStyles[0];
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

## Default Label Style Settings

Each `LabelStyleCollection` has a `DefaultLabelStyle` that controls ambient defaults for new label styles:

```csharp
LabelStyleCollection coll = doc.Styles.LabelStyles
    .PointLabelStyles.LabelStyles;

LabelStyleDefault defaults = coll.DefaultLabelStyle;
defaults.Label.TextStyle.Value = "Standard";
defaults.Label.Visibility.Value = true;
defaults.Components.TextHeight.Value = 0.08;
defaults.Leader.Visibility.Value = false;
defaults.Behavior.OrientationReference.Value =
    OrientationReferenceType.WorldCoordinateSystem;
defaults.PlanReadability.PlanReadable.Value = true;

// Access expressions defined for this collection
ExpressionCollection expressions = coll.Expressions;
```

## Label Style Filtering (from this codebase)

The `LabelFilterHelper` class in `SharedTypes.cs` filters label styles by:
- **View type keyword** (e.g., "Plan", "Profile", "Section")
- **Parts list prefix** (e.g., "P_Sanitary" -> "U_P")

## Gotchas

- New label styles are initialized from ambient settings - may already contain components
- Use `IsSupportedComponent()` to verify a component type is valid before adding it; adding an unsupported type may compile but produce no visible result
- Labels depend on graphical objects (blocks) that may not exist in the current document
- The `.Value` pattern applies to all label properties (e.g., `component.General.Visible.Value = true`)
- Ambient settings determine units - account for different drawings having different unit settings
- Duplicate component names throw `ArgumentException`
- `LabelStyleLineComponent.StyleLine.Length` is deprecated since Civil 3D 2012 - use `FixedLength` with `LengthType` instead
- `ReferenceText` and `TextForEach` components must be added via their specialized methods (`AddReferenceTextComponent` / `AddTextForEachComponent`), not the generic `AddComponent`
- Component names passed to `RemoveComponent()` must match exactly (case-sensitive)

## Related Skills

- `c3d-root-objects` - Accessing styles through CivilDocument
- `c3d-pipe-networks` - Pipe and structure label styles
- `c3d-alignments` - Alignment label set styles
- `c3d-points` - Point label styles and description keys
