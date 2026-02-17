---
name: c3d-pipe-networks
description: Gravity and pressure pipe networks - creation, pipes, structures, parts lists, labels, styles, and interference checks
---

# Civil 3D Pipe Networks

Use this skill when working with gravity or pressure pipe networks - creating networks, pipes, structures, labels, styles, or interference checks.

## Accessing Pipe Networks

```csharp
CivilDocument doc = CivilApplication.ActiveDocument;
ObjectIdCollection networkIds = doc.GetPipeNetworkIds();

foreach (ObjectId netId in networkIds)
{
    Network network = ts.GetObject(netId, OpenMode.ForRead) as Network;
    ed.WriteMessage("Network: {0}\n", network.Name);
}
```

## Pipe-Specific Ambient Settings

```csharp
SettingsPipeNetwork oSettings =
    doc.Settings.GetSettings<SettingsPipeNetwork>() as SettingsPipeNetwork;

// Get pipe rules
ed.WriteMessage("Pipe rules: {0}\n", oSettings.Rules.Pipe.Value);

// Set default units
oSettings.Angle.Unit.Value = Autodesk.Civil.AngleUnitType.Radian;
oSettings.Coordinate.Unit.Value = Autodesk.Civil.LinearUnitType.Foot;
oSettings.Distance.Unit.Value = Autodesk.Civil.LinearUnitType.Foot;
```

Settings classes: `SettingsPipe`, `SettingsPipeNetwork`, `SettingsStructure` (all inherit from `SettingsAmbient`).

## Parts Lists

Parts lists contain families of pipe and structure types:

```csharp
PartsListCollection partsListCol = doc.Styles.PartsListSet;

foreach (ObjectId plId in partsListCol)
{
    PartsList partsList = ts.GetObject(plId, OpenMode.ForWrite) as PartsList;
    ed.WriteMessage("Parts List: {0}\n", partsList.Name);

    // Get pipe families
    ObjectIdCollection pipeFamilies =
        partsList.GetPartFamilyIdsByDomain(DomainType.Pipe);

    foreach (ObjectId pfId in pipeFamilies)
    {
        PartFamily family = ts.GetObject(pfId, OpenMode.ForWrite) as PartFamily;
        ed.WriteMessage("  Family: {0}\n", family.Name);

        // Access size filters and data fields
        SizeFilterRecord sizeFilter = family.PartSizeFilter;
        SizeFilterField material = sizeFilter.GetParamByContextAndIndex(
            PartContextType.Material, 0);
    }
}
```

## Creating a Pipe Network

```csharp
ObjectId networkId = Network.Create(doc, "My Network");
Network network = ts.GetObject(networkId, OpenMode.ForWrite) as Network;

// Set reference surface (for pipe rules like rim elevation)
network.ReferenceSurfaceId = surfaceId;

// Get parts list
ObjectId partsListId = doc.Styles.PartsListSet["Standard"];
PartsList partsList = ts.GetObject(partsListId, OpenMode.ForWrite) as PartsList;

// Get pipe family and size
ObjectId pipeFamilyId = partsList["Concrete Pipe"];
PartFamily pipeFamily = ts.GetObject(pipeFamilyId, OpenMode.ForWrite) as PartFamily;
ObjectId pipeSize = pipeFamily[0]; // First size

// Get structure family and size
ObjectId structFamilyId = partsList["Rectangular EndSection"];
PartFamily structFamily = ts.GetObject(structFamilyId, OpenMode.ForWrite) as PartFamily;
ObjectId structSize = structFamily[0];
```

## Creating Pipes

```csharp
// Straight pipe
LineSegment3d line = new LineSegment3d(
    new Point3d(30, 9, 0), new Point3d(33, 7, 0));
ObjectId newPipeId = ObjectId.Null;
network.AddLinePipe(pipeFamilyId, pipeSize, line, ref newPipeId, false);

// Curved pipe
// network.AddCurvePipe(...)
```

## Creating Structures

```csharp
Point3d location = new Point3d(30, 9, 0);
ObjectId newStructId = ObjectId.Null;
network.AddStructure(structFamilyId, structSize, location,
    0 /* rotation */, ref newStructId, true);
```

## Connecting Pipes and Structures

```csharp
// Connect pipe to structure
pipe.ConnectToStructure(structureId, isStart: true);

// Connect structure to pipe
structure.ConnectToPipe(pipeId);

// Pipe endpoints
ObjectId startStruct = pipe.StartStructureId;
ObjectId endStruct = pipe.EndStructureId;

// Structure connections
var connectedPipes = structure.ConnectedPipe; // read-only collection
```

**Note:** Connecting pipes directly creates a virtual `Structure` as the joint. Disconnect a pipe before connecting to a different structure.

## Dynamic Part Properties

```csharp
Pipe oPipe = ts.GetObject(pipeId, OpenMode.ForRead) as Pipe;
PartDataField[] dataFields = oPipe.PartData.GetAllDataFields();

foreach (PartDataField field in dataFields)
{
    ed.WriteMessage("Name: {0}, Desc: {1}, Type: {2}, Value: {3}\n",
        field.Name, field.Description, field.DataType, field.Value);
}
```

## Pipe Styles

```csharp
ObjectId pipeStyleId = doc.Styles.PipeStyles.Add("My Pipe Style");
PipeStyle style = ts.GetObject(pipeStyleId, OpenMode.ForWrite) as PipeStyle;

// Plan view sizing
style.PlanOption.WallSizeType = PipeWallSizeType.UserDefinedWallSize;
style.PlanOption.WallSizeOptions = PipeUserDefinedType.UseDrawingScale;
style.PlanOption.InnerDiameter = 0.0021;
style.PlanOption.OuterDiameter = 0.0024;
style.PlanOption.EndSizeType = PipeEndSizeType.UserDefinedEndSize;

// Colors
style.GetDisplayStylePlan(PipeDisplayStylePlanType.OutsideWalls).Color =
    Color.FromRgb(255, 191, 0); // orange
style.GetDisplayStylePlan(PipeDisplayStylePlanType.InsideWalls).Color =
    Color.FromRgb(191, 0, 255); // violet

// Hatching
style.GetHatchStylePlan().Pattern = "DOTS";
style.GetHatchStylePlan().HatchType = HatchType.PreDefined;
style.PlanOption.HatchOptions = PipeHatchType.HatchToInnerWalls;

// Assign to pipe
pipe.Style = pipeStyle;
```

## Structure Styles

```csharp
ObjectId structStyleId = doc.Styles.StructureStyles.Add("My Struct Style");
StructureStyle style = ts.GetObject(structStyleId, OpenMode.ForWrite) as StructureStyle;

style.GetDisplayStylePlan(StructureDisplayStylePlanType.Structure).Color =
    Color.FromRgb(255, 191, 0);
style.PlanOption.SizeType = StructureSizeOptionsType.UseDrawingScale;
style.PlanOption.Size = 0.0035;

// Assign via property
structure.StyleId = structStyleId;
// or: structure.StyleName = "My Struct Style";
```

## Pipe and Structure Label Styles

```csharp
// Pipe label styles
var pipeLabelStyles = doc.Styles.LabelStyles.PipeLabelStyles;
// Contains: cross section, plan/profile view, default styles

// Structure label styles
var structLabelStyles = doc.Styles.LabelStyles.StructureLabelStyles;
```

**Limitation:** The label style of an individual pipe or structure cannot be set using the .NET API.

## Interference Checks

Interference check styles control the display of intersections:

```csharp
ObjectId intStyleId = doc.Styles.InterferenceStyles.Add("My Interference Style");
InterferenceStyle intStyle = ts.GetObject(intStyleId, OpenMode.ForWrite)
    as InterferenceStyle;

// Symbol display
intStyle.GetDisplayStylePlan(InterferenceDisplayStyleType.Symbol).Visible = true;

// Marker style
ObjectId markerStyleId = intStyle.MarkerStyle;
MarkerStyle marker = ts.GetObject(markerStyleId, OpenMode.ForWrite) as MarkerStyle;
marker.MarkerType = MarkerDisplayType.UseCustomMarker;
marker.CustomMarkerStyle = CustomMarkerType.CustomMarkerX;
marker.CustomMarkerSuperimposeStyle = CustomMarkerSuperimposeType.Circle;
marker.SizeType = MarkerSizeType.AbsoluteUnits;
marker.MarkerSize = 5.5;

// Model options
// InterferenceModelType.TrueSolid - 3D model of intersection
// InterferenceModelType.Sphere - sphere at intersection
```

**Limitation:** Performing interference checks and listing interferences are NOT supported in the .NET API. Only interference styles are supported.

## Pressure Pipe Networks

Pressure networks use separate classes:

```csharp
// Classes: PressurePipeNetwork, PressurePipe, PressureFitting, PressureAppurtenance
```

The pressure pipe network API follows similar patterns to gravity networks but with separate style collections for pipes, fittings, and appurtenances (three separate style selections needed).

## Gotchas

- `ReferenceSurfaceId` is used primarily for pipe rules (e.g., rim elevation relative to surface)
- Dynamic properties created with `NetworkCatalogDef` are NOT supported in .NET
- Individual pipe/structure label styles CANNOT be set via .NET API
- Interference check execution and listing are NOT supported in .NET - only styles
- Parts list items are identified by GUID - `PartFamily` can only contain one domain (pipe OR structure)
- When creating a pipe style, add Try/Catch: `Add()` throws if name exists, use `Item()` to get existing
- Connecting pipes directly creates virtual structure joints automatically

## Label Filtering (from this codebase)

The `LabelFilterHelper` in `SharedTypes.cs` maps parts list prefixes to label style prefixes:
- Gravity: pipes + structures (two style categories)
- Pressure: pipes + fittings + appurtenances (three style categories)

## Related Skills

- `c3d-root-objects` - Accessing networks through CivilDocument
- `c3d-label-styles` - General label style creation
- `c3d-profiles` - Profile views where pipe labels are placed
- `c3d-corridors` - Corridor-pipe interactions
