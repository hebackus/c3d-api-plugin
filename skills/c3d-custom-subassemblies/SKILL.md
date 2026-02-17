---
name: c3d-custom-subassemblies
description: Custom subassembly design in .NET - naming, parameters, superelevation, CorridorState, SubassemblyGenerator, targets, SATemplate pattern, and tool catalog
---

# Custom Subassemblies Using .NET

Use this skill when creating custom subassembly components for corridors in Civil 3D.

## Overview

Custom subassemblies can be written in any .NET language (C# or VB.NET). They define cross-sectional shapes that are placed along corridor baselines. The `SubassemblyGeometryGenerateMode.UseDotNet` mode enables compiled .NET assemblies to serve as subassembly geometry generators.

## Naming Conventions

- No spaces or special characters
- PascalCase with uppercase first letter per word
- Group by component type as prefix: `LaneBasic`, `ShoulderExtended`, `CurbTypeA`
- For fixed-dimension variants, create separate subassemblies (e.g., `CurbTypeA` through `CurbTypeE`) rather than one with many parameters

## Attachment Methodology

Most subassemblies have a single attachment point extending in one direction. Special cases:

| Category | Behavior |
|----------|----------|
| **Medians** | Insert left and right simultaneously about a centerline. Attachment point may not be on the median surface (e.g., above a depressed median ditch). |
| **Components Joining Two Roadways** | Need two attachment points - normal attachment on one side, marked point attachment on the other. |
| **Rehabilitation/Overlay** | Calculations based on existing roadway section shape rather than design centerline. |

## Input Parameter Types

| Parameter | Description |
|-----------|-------------|
| **Widths** | Horizontal distance between two points. Positive values extend in insertion direction (left/right). Candidates for alignment targeting. |
| **Offsets** | Horizontal distance from corridor baseline. Positive = right, negative = left. |
| **% Slopes** | Rise-to-run ratio. Unitless (-0.05) or percent (-5%). Use same convention across catalog. |
| **Ratio Slopes** | Run-to-rise ratio (e.g., 4:1). May be signed or unsigned depending on context. |
| **Point/Link/Shape Codes** | Usually hard-coded for consistency. Exception: generic link subassemblies where user assigns codes. |

**Design guidance:** Generally, widths, depths, and slopes should be variable (not fixed). Provide default values usable in most situations.

## Superelevation Behavior

Key considerations:
- Where is the superelevation pivot point?
- How does it relate to the Profile Grade Line (PGL)?

Common pivot/PGL combinations:
- Both at crown of road
- Both at inside edge-of-traveled-way (divided road)
- Both at one edge-of-traveled-way (undivided road)
- Pivot at inside edge, PGL at centerline
- On divided crowned roads: PGL at crown points, pivot at inside ETW
- On divided uncrowned: both above median at centerline

Special superelevation behaviors:
- **Broken Back Subbase** - break point in subbase on high side
- **Shoulder Breakover** - maximum slope difference between lane and shoulder
- **Curbs-and-Gutters** - high-side gutter behavior changes in superelevation

## Target Mapping (Civil 3D 2013+)

Subassemblies can target object types beyond alignments/profiles:

### ParamLogicalNameType Enum

All values in `Autodesk.Civil.Runtime.ParamLogicalNameType`:

| Value | Description |
|-------|-------------|
| `None` | No target type |
| `Surface` | Surface target |
| `Alignment` | Alignment target (legacy - use OffsetTarget for broader support) |
| `Profile` | Profile target (legacy - use ElevationTarget for broader support) |
| `OffsetTarget` | Alignments, feature lines, survey figures, polylines |
| `ElevationTarget` | Profiles, feature lines, survey figures, 3D polylines |
| `OffsetTargetPipe` | Pipe network offset targets |
| `ElevationTargetPipe` | Pipe network elevation targets |

The `OffsetTarget`/`ElevationTarget` types (Civil 3D 2013+) accept a wider range of object types than the legacy `Alignment`/`Profile` types. Prefer the newer types for new subassemblies.

### WidthOffsetTarget Class

Used to get offset distances from offset targets (alignments, feature lines, polylines, pipe networks).

```csharp
// Constructor
var offsetTarget = new WidthOffsetTarget(targetObjectId);

// Get perpendicular distance from alignment to target, outputs XY at intersection
double dist = offsetTarget.GetDistanceToAlignment(
    alignmentId, stationOnAlignment,
    ref xOnTarget, ref yOnTarget);

// Overload with explicit side
double dist = offsetTarget.GetDistanceToAlignment(
    alignmentId, stationOnAlignment, AlignmentSide.Left,
    ref xOnTarget, ref yOnTarget);

// Get nearest pipe from a pipe network target
offsetTarget.GetNearestPipeOfNetworkToAlignment(
    alignmentId, stationOnAlignment, AlignmentSide.Right, ref pipeId);
```

### SlopeElevationTarget Class

Used to get elevations from elevation targets (profiles, feature lines, 3D polylines, pipe networks).

```csharp
// Constructor
var elevationTarget = new SlopeElevationTarget(targetObjectId);

// Get elevation at a station along the alignment
double elev = elevationTarget.GetElevation(
    alignmentId, stationOnAlignment, AlignmentSide.Left);

// Overload without explicit side
double elev = elevationTarget.GetElevation(alignmentId, stationOnAlignment);

// Get nearest pipe from a pipe network target
elevationTarget.GetNearestPipeOfNetworkToAlignment(
    alignmentId, stationOnAlignment, AlignmentSide.Right, ref pipeId);
```

### Example: Getting Elevation from Target with Fallback

```csharp
double offsetElev;
try
{
    offsetElev = elevationTarget.GetElevation(
        corridorState.CurrentAlignmentId,
        corridorState.CurrentStation,
        AlignmentSide.Right);
}
catch
{
    corridorState.RecordError(
        CorridorError.LogicalNameNotFound,
        CorridorErrorLevel.AsWarning,
        "Target not found - using default slope",
        "BasicLaneTransition",
        false);
    offsetElev = corridorState.CurrentElevation + width * slope;
}
```

## SubassemblyGenerator Class

The `SubassemblyGenerator` controls how a subassembly's geometry is produced. Set via `Subassembly.GeometryGenerator`.

```csharp
// Constructor: SubassemblyGenerator(SubassemblyGeometryGenerateMode mode, string projectOrAssemblyName, string macroOrClassName)
var generator = new SubassemblyGenerator(
    SubassemblyGeometryGenerateMode.UseDotNet,
    "MySubassemblies.dll",        // ProjectOrAssemblyName - the compiled assembly
    "MyNamespace.MySubassembly"   // MacroOrClassName - fully qualified class name
);
subassembly.GeometryGenerator = generator;
```

### SubassemblyGeometryGenerateMode Enum

| Value | Description |
|-------|-------------|
| `HardCoded` | Built-in geometry (stock subassemblies) |
| `UseVBA` | VBA macro-based (legacy) |
| `UseCOM` | COM object-based |
| `UseDotNet` | .NET assembly-based (preferred for custom subassemblies) |

## CorridorState Object

The `CorridorState` object (`Autodesk.Civil.Runtime`) provides access to the current corridor processing state.

### Current Position and Context

```csharp
corridorState.CurrentStation              // Current station being processed
corridorState.CurrentElevation            // Current elevation at station
corridorState.CurrentOffset               // Current offset from baseline
corridorState.CurrentAssemblyElevation    // Assembly insertion elevation
corridorState.CurrentAssemblyOffset       // Assembly insertion offset
corridorState.CurrentSubassemblyElevation // Subassembly attachment elevation
corridorState.CurrentSubassemblyOffset    // Subassembly attachment offset
corridorState.CurrentAssemblyFixedElevation // Fixed elevation (for offset assemblies)
corridorState.CurrentAssemblyFixedOffset    // Fixed offset (for offset assemblies)
corridorState.CurrentAssemblyOffsetIsFixed  // Whether offset assembly uses fixed values
corridorState.CurrentRegionStartStation   // Start station of current region
corridorState.CurrentRegionEndStation     // End station of current region
corridorState.Mode                        // CorridorMode: None, Layout, or Design
```

### Object Identity

```csharp
corridorState.CurrentCorridorId           // ObjectId of current corridor
corridorState.CurrentCorridorName         // Name of current corridor
corridorState.CurrentAssemblyId           // ObjectId of current assembly
corridorState.CurrentAssemblyName         // Name of current assembly
corridorState.CurrentSubassemblyId        // ObjectId of current subassembly
corridorState.CurrentSubassemblyName      // Name of current subassembly
corridorState.CurrentAlignmentId          // ObjectId of current alignment
corridorState.CurrentProfileId            // ObjectId of current profile
corridorState.CurrentBaselineId           // ObjectId of current baseline
corridorState.CurrentAlignmentIsOffsetAlignment // Whether alignment is an offset alignment
```

### Parameter Collections

```csharp
corridorState.ParamsLong                  // Long parameters collection
corridorState.ParamsDouble                // Double parameters collection
corridorState.ParamsString                // String parameters collection
corridorState.ParamsBool                  // Boolean parameters collection
corridorState.ParamsOffsetTarget          // Offset target parameters
corridorState.ParamsElevationTarget       // Elevation target parameters
corridorState.ParamsAlignment             // Alignment parameters
corridorState.ParamsProfile               // Profile parameters
corridorState.ParamsSurface               // Surface parameters
corridorState.ParamsPoint                 // Point parameters
// Each also has a Global variant (e.g., ParamsLongGlobal) for corridor-wide parameters
```

### Geometry Collections

```csharp
corridorState.Points                      // PointCollection - output points
corridorState.Links                       // LinkCollection - output links
corridorState.Shapes                      // ShapeCollection - output shapes
```

### Surface Intersection Methods

```csharp
// Intersect a slope line with a surface (single intersection)
IPoint IntersectSurface(ObjectId surfaceId, ObjectId alignmentId,
    IPoint origin, bool lookRight, double slope)

// Intersect with max distance limit
IPoint IntersectSurface(ObjectId surfaceId, ObjectId alignmentId,
    IPoint origin, bool lookRight, double slope, double maxDistance)

// Intersect with multiple points required
IPoint[] IntersectSurface(ObjectId surfaceId, ObjectId alignmentId,
    IPoint origin, bool lookRight, double slope, int pointsRequired)

// Check if a point is above a surface
bool IsAboveSurface(ObjectId surfaceId, ObjectId alignmentId, IPoint point)
bool IsAboveSurface(ObjectId surfaceId, ObjectId alignmentId, IPoint point,
    double minimumAmountAbove)

// Sample a surface section between two points
SampledSectionLinkCollection SampleSection(ObjectId surfaceId, ObjectId alignmentId,
    IPoint point1, IPoint point2)
```

### Link and Alignment Intersection

```csharp
// Intersect a slope line with an existing link by code
IPoint IntersectLink(IPoint origin, bool lookRight, double slope, string linkCode)

// Intersect with an alignment
IPoint IntersectAlignment(ObjectId targetAlignmentId, ObjectId alignmentId,
    IPoint origin, bool lookRight)
IPoint IntersectAlignment(ObjectId targetAlignmentId, ObjectId alignmentId,
    IPoint origin, bool lookRight, double maxDistance)
```

### Coordinate Conversion

```csharp
// Station-Offset-Elevation to XYZ
void SoeToXyz(ObjectId alignmentId, double station, double offset, double elevation,
    ref double X, ref double Y, ref double Z)

// XYZ to Station-Offset-Elevation
void XyzToSoe(ObjectId alignmentId, double X, double Y, double Z,
    ref double station, ref double offset, ref double elevation)
```

### Superelevation Axis of Rotation

```csharp
void SetAxisOfRotationInformation(bool isPotentialPivot, double superElevationSlope,
    SuperelevationCrossSegmentType superElevationSlopeType, bool isReversedSlope)
void SetAxisOfRotationSERange(double applySE_StartOffset, double applySE_EndOffset)
void SetAxisOfRotationCrownPoint(uint crownPointIndex)
```

### Error Recording

```csharp
// Record an error during corridor processing
void RecordError(CorridorError error, CorridorErrorLevel errorLevel,
    string description, string source, bool showInEventViewer)
```

#### CorridorErrorLevel Enum

| Value | Description |
|-------|-------------|
| `None` | No error |
| `Informational` | Informational message |
| `AsWarning` | Warning level |
| `Severe` | Severe error |

#### Common CorridorError Values

| Value | Description |
|-------|-------------|
| `LogicalNameNotFound` | Target logical name not resolved |
| `NoSideslopeIntersectFound` | Side slope did not intersect surface |
| `ParameterNotFound` | Required parameter missing |
| `ElevationAtStationNotFound` | Could not get elevation at station |
| `NoLinkIntersectFound` | Slope line did not intersect link |
| `NoMarkedPointFound` | Marked point not found |
| `StopProcessingGroup` | Stop processing the current group |

## SATemplate Pattern

The SATemplate (SubAssembly Template) pattern is the standard structure for custom subassembly code:

1. Define input parameters
2. Read current corridor state
3. Calculate geometry based on parameters and targets
4. Create points, links, and shapes with appropriate codes
5. Handle errors with `Utilities.RecordWarning()`

## Subassembly Class Properties

Key properties on the `Subassembly` object (`Autodesk.Civil.DatabaseServices`):

| Property | Type | Description |
|----------|------|-------------|
| `Origin` | `Point3d` | Insertion point (get/set) |
| `Side` | `SubassemblySideType` | Left or Right (get/set) |
| `HasSide` | `bool` | Whether side is assigned (get) |
| `Status` | `SubassemblyStatus` | UpToDate, OutOfDate, or FileNotFound (get) |
| `Version` | `string` | Subassembly version string (get) |
| `GeometryGenerator` | `SubassemblyGenerator` | Controls geometry generation mode and source (get/set) |
| `IsFromSubassemblyComposer` | `bool` | Whether created in Subassembly Composer (get) |
| `IsDynamic` | `bool` | Whether subassembly is dynamic (get) |
| `UseEmbeddedProject` | `bool` | Whether to use embedded project (get/set) |
| `CodeSetStyleName` | `string` | Code set style for display (get/set) |
| `AssemblyId` | `ObjectId` | Parent assembly (get) |
| `HasParentAssembly` | `bool` | Whether attached to an assembly (get) |
| `OffsetToParentAssembly` | `Vector2d` | Offset from parent assembly (get/set) |
| `OffsetToAssembly` | `Vector2d` | Offset to assembly (get/set) |
| `PointIndexHookTo` | `int` | Hook point index on parent subassembly (get/set) |
| `SubassemblyHookTo` | `ObjectId` | Parent subassembly this hooks to (get) |
| `DefaultLoopInLayoutMode` | `bool` | Whether to loop in layout mode (get/set) |
| `DefaultLoopOffsetInLayoutMode` | `double` | Loop offset distance (get/set) |

### Subassembly Parameter Collections

```csharp
subassembly.ParamsString    // ParamStringCollection
subassembly.ParamsDouble    // ParamDoubleCollection
subassembly.ParamsLong      // ParamLongCollection
subassembly.ParamsBool      // ParamBoolCollection
```

### Subassembly Geometry Collections

```csharp
subassembly.Points          // PointCollection
subassembly.Links           // LinkCollection
subassembly.Shapes          // ShapeCollection
```

### Subassembly Methods

```csharp
subassembly.Run()                          // Execute the subassembly generator
subassembly.EraseAllParams()               // Remove all parameters
subassembly.ShowHelp()                     // Display help
subassembly.GetResourceString("resId")     // Get localized string by ID
```

## SubassemblyCollection Import Methods

The `SubassemblyCollection` provides methods to import subassemblies into the drawing:

```csharp
// Import from ATC catalog file
ObjectId ImportSubassembly(string name, string atcFilePath, string itemId, Point3d location)

// Import a stock (built-in) subassembly by class name
ObjectId ImportStockSubassembly(string name, string className, Point3d location)

// Import from SAC PKT package
ObjectId ImportSACSubassembly(string name, string pktFilePath, Point3d location)

// Create from existing entity (polyline, etc.)
ObjectId Add(string name, ObjectId entityId, double midOrdinateDist, LinkCreationType linkCreationOption)

// Remove
bool Remove(ObjectId subassemblyId)
```

## Support Files

| File | Purpose |
|------|---------|
| `CodesSpecific` | Defines point, link, and shape codes used by the subassembly |
| `Utilities` | Helper methods for common calculations |

Key utility methods:
- `Utilities.GetSide()` - determine left/right side
- `Utilities.RecordWarning()` - log corridor processing warnings

## Tool Catalog

Custom subassemblies are distributed via tool catalogs.

### ATC File Format

The Autodesk Tool Catalog (`.atc`) file is an XML file defining:
- Categories and subcategories
- Individual tools (subassemblies)
- Parameters, descriptions, and help references

### Cover Page

The catalog cover page provides:
- Catalog name and description
- Version information
- Publisher information

### Registry File

Associates the tool catalog with Civil 3D so it appears in the tool palette.

### PKT Package Export

Package subassemblies for distribution:
1. Compile the .NET assembly (C# or VB.NET)
2. Create the ATC catalog file
3. Create registry entries
4. Export as PKT package

## Gotchas

- Custom subassemblies can be written in C# or VB.NET using `SubassemblyGeometryGenerateMode.UseDotNet`
- Always handle the case where targets are not found (use try/catch)
- Use `corridorState.RecordError()` instead of throwing exceptions to avoid crashing corridor processing
- Point, link, and shape codes should be consistent across all subassemblies in a catalog
- Consider both normal crown and superelevation conditions
- `WidthOffsetTarget.GetDistanceToAlignment()` returns XY coordinates at the perpendicular intersection point (not a station value)
- Check `corridorState.Mode` to handle `CorridorMode.Layout` vs `CorridorMode.Design` differently when needed
- The `Subassembly.Status` property can be `FileNotFound` if the source assembly is missing - check before calling `Run()`

## Related Skills

- `c3d-corridors` - Corridor structure, baselines, assemblies
- `c3d-alignments` - Alignments and superelevation
- `c3d-profiles` - Profiles used as corridor baselines
