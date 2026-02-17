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
string networkName = "My Network";
ObjectId networkId = Network.Create(doc, ref networkName);
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

// Curved pipe (Civil 3D 2023+)
PipeCurveGeometry curveGeom = new PipeCurveGeometry(...);
ObjectId curvedPipeId = network.AddCurvePipe(pipeFamilyId, pipeSize, curveGeom, false);
```

## Breaking and Moving Pipes

```csharp
// Break a pipe at a point, inserting a structure at the break
ObjectId newPipeId = ObjectId.Null;
network.BreakPipe(pipeIdToBreak, breakPoint, existingStructureId, ref newPipeId);

// Move parts between networks
ObjectIdCollection partIds = new ObjectIdCollection();
partIds.Add(pipeId);
network.MoveParts(partIds, destinationNetworkId);

// Find shortest path between two parts
double minLength = 0;
ObjectIdCollection pathIds = Network.FindShortestNetworkPath(
    startPartId, endPartId, ref minLength);
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
// Connect pipe to structure at start or end
pipe.ConnectToStructure(ConnectorPositionType.Start, structureId, false);
pipe.ConnectToStructure(ConnectorPositionType.End, structureId, false);

// Connect structure to pipe
structure.ConnectToPipe(pipeId, ConnectorPositionType.Start);

// Connect pipe to pipe (creates a new junction structure automatically)
ObjectId newJunctionId = ObjectId.Null;
pipe1.ConnectToPipe(ConnectorPositionType.End, pipe2Id,
    ConnectorPositionType.Start, structFamilyId, structSizeId,
    ref newJunctionId, true /* applyRules */, false /* force */);

// Disconnect pipe at an endpoint
pipe.Disconnect(ConnectorPositionType.Start);
// Disconnect structure from a specific pipe
structure.Disconnect(pipeId);

// Pipe endpoints
ObjectId startStruct = pipe.StartStructureId;
ObjectId endStruct = pipe.EndStructureId;

// Structure connections
int count = structure.ConnectedPipesCount;
string[] pipeNames = structure.GetConnectedPipeNames();
bool flowsIn = structure.IsConnectedPipeFlowingIn(0);
bool flowsOut = structure.IsConnectedPipeFlowingOut(0);
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
pipe.StyleId = pipeStyleId;
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

## Creating Labels with Specific Styles

Individual pipe and structure labels can be created with a specific label style, or the style can be changed after creation via `Label.StyleId`.

```csharp
// Plan pipe label with specific style
ObjectId labelId = PipeLabel.Create(pipeId, 0.5 /* ratio */, labelStyleId);

// Plan structure label with specific style and location
ObjectId sLabelId = StructureLabel.Create(structureId, labelStyleId, labelLocation);

// Profile pipe label with specific style
ObjectId ppLabelId = PipeProfileLabel.Create(
    profileViewPartId, profileViewId, 0.5 /* ratio */, labelStyleId);

// Profile structure label with specific style
ObjectId spLabelId = StructureProfileLabel.Create(
    profileViewId, profileViewPartId, labelStyleId);

// Section pipe label with specific style
ObjectId secPLabelId = PipeSectionLabel.Create(
    sectionViewId, pipeId, sectionPipeNetworkId, partIndex, labelStyleId);

// Section structure label with specific style
ObjectId secSLabelId = StructureSectionLabel.Create(
    sectionViewId, structureId, sectionPipeNetworkId, partIndex, labelStyleId);

// Change an existing label's style
Label label = ts.GetObject(labelId, OpenMode.ForWrite) as Label;
label.StyleId = newLabelStyleId;

// Get existing labels on a pipe or structure
ObjectIdCollection pipeLabels = pipe.GetPipeLabelIds();
ObjectIdCollection structLabels = structure.GetAvailableStructureLabelIds();
```

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

Existing `Interference` objects can be read to get the two intersecting network IDs:

```csharp
Interference interference = ts.GetObject(interferenceId, OpenMode.ForRead) as Interference;
ObjectId net1 = interference.Network1Id;
ObjectId net2 = interference.Network2Id;
```

**Note:** Creating/executing new interference checks programmatically is not exposed in the .NET API. Use the Civil 3D UI to run interference checks, then read the results via the `Interference` class.

## Pressure Pipe Networks

Pressure networks use separate classes from the `AeccPressurePipesMgd` assembly:

```csharp
// Create a pressure network
ObjectId pressNetId = PressurePipeNetwork.Create(db, "My Pressure Network");
PressurePipeNetwork pressNet = ts.GetObject(pressNetId, OpenMode.ForWrite)
    as PressurePipeNetwork;

// Set references
pressNet.ReferenceSurfaceId = surfaceId;
pressNet.ReferenceAlignmentId = alignmentId;
pressNet.PartsListId = partsListId;

// Add parts
LineSegment3d line = new LineSegment3d(startPt, endPt);
ObjectId pipeId = pressNet.AddLinePipe(line, pressurePartSize);
ObjectId fittingId = pressNet.AddFitting(location, fittingPartSize);
ObjectId appurtId = pressNet.AddAppurtenance(location, appurtPartSize);

// Get part collections
ObjectIdCollection pipeIds = pressNet.GetPipeIds();
ObjectIdCollection fittingIds = pressNet.GetFittingIds();
ObjectIdCollection appurtIds = pressNet.GetAppurtenanceIds();

// Set styles on individual parts
PressurePipe pPipe = ts.GetObject(pipeId, OpenMode.ForWrite) as PressurePipe;
pPipe.StyleId = pipeStyleId;

PressureFitting fitting = ts.GetObject(fittingId, OpenMode.ForWrite) as PressureFitting;
fitting.StyleId = fittingStyleId;

PressureAppurtenance appurt = ts.GetObject(appurtId, OpenMode.ForWrite) as PressureAppurtenance;
appurt.StyleId = appurtStyleId;

// Set default label styles at network level
pressNet.PipePlanLabelStyleId = pipeLabelStyleId;
pressNet.FittingPlanLabelStyleId = fittingLabelStyleId;
pressNet.AppurtenancePlanLabelStyleId = appurtLabelStyleId;
pressNet.PipeProfileLabelStyleId = pipeProfileLabelStyleId;
pressNet.FittingProfileLabelStyleId = fittingProfileLabelStyleId;
pressNet.AppurtenanceProfileLabelStyleId = appurtProfileLabelStyleId;

// Swap part size
PressurePartSize newSize = ...; // from parts list
pPipe.SwapPartSize(newSize);
```

The pressure pipe network API follows similar patterns to gravity networks but with separate style collections for pipes, fittings, and appurtenances (three separate style selections needed). Pressure parts use `PressurePartSize` instead of family/size ObjectId pairs.

## Network Catalog Custom Properties

`NetworkCatalogDef` supports declaring custom part parameters:

```csharp
NetworkCatalogDef.DeclareNewParameter(
    "globalContext", "displayContext", "paramName", "paramDesc",
    PartCatalogDataType.Integer, PartParamUsageType.Dynamic,
    "defaultUnits", false /* singleton */, false /* catManagedList */);

NetworkCatalogDef.DeclarePartProperty("globalContext", DomainType.Pipe, PartType.Pipe);
```

## Gotchas

- `ReferenceSurfaceId` is used primarily for pipe rules (e.g., rim elevation relative to surface)
- `Network.Create` takes the network name as `ref string` - Civil 3D may modify the name to avoid duplicates
- Individual pipe/structure labels CAN be created with a specific `labelStyleId` and changed after creation via `Label.StyleId`
- Executing new interference checks is not exposed in .NET, but existing `Interference` objects can be read
- Parts list items are identified by GUID - `PartFamily` can only contain one domain (pipe OR structure)
- When creating a pipe style, add Try/Catch: `Add()` throws if name exists, use `Item()` to get existing
- Connecting pipes directly creates virtual structure joints automatically
- Pressure networks use `PressurePartSize` for part sizing instead of family/size ObjectId pairs
- `Pipe.StyleId` has only a setter override on Pipe/Structure; the getter is inherited from `Entity`

## Label Filtering (from this codebase)

The `LabelFilterHelper` in `SharedTypes.cs` maps parts list prefixes to label style prefixes:
- Gravity: pipes + structures (two style categories)
- Pressure: pipes + fittings + appurtenances (three style categories)

## Related Skills

- `c3d-root-objects` - Accessing networks through CivilDocument
- `c3d-label-styles` - General label style creation
- `c3d-profiles` - Profile views where pipe labels are placed
- `c3d-corridors` - Corridor-pipe interactions
