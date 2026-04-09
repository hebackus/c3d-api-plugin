---
name: c3d-custom-subassemblies
description: Custom subassembly .NET design — CorridorState, SubassemblyGenerator, targets, SATemplate
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
5. Handle errors with `corridorState.RecordError()` (not exceptions — see Gotchas)

## Support Files

| File | Purpose |
|------|---------|
| `CodesSpecific` | Defines point, link, and shape codes used by the subassembly |
| `Utilities` | Helper methods for common calculations |

Key utility methods:
- `Utilities.GetSide()` - determine left/right side
- `Utilities.RecordWarning()` - legacy VBA/Subassembly Composer helper; in .NET use `corridorState.RecordError()` instead

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
