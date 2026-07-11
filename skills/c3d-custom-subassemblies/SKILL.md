---
name: c3d-custom-subassemblies
description: Custom subassembly .NET design — CorridorState, SubassemblyGenerator, targets, SATemplate
---

# Custom Subassemblies Using .NET

Use this skill when creating custom subassembly components for corridors in Civil 3D. This skill is
the API/mechanics reference (SATemplate lifecycle, targets, `.atc`, build/deploy). For a need→stock-file
lookup index, worked `DrawImplement` recipes (median, daylight, marked-point join, conditional, SE-AOR),
and the point/link/shape code catalog mined from Autodesk's 120 VB stock subassemblies, use
`c3d-subassembly-patterns`.

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
| `StopProcessingConditional` | Halt the subassemblies placed after a conditional gate (see Core Mechanics → Conditional) |
| `Failure` | Catch-all for an unhandled exception (used by the base no-throw wrappers) |
| `ValueShouldNotBeLessThanOrEqualToZero` | Input validation — value must be positive |

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
- `Utilities.RecordWarning()` — the *stock VB sample's* helper wraps `corridorState.RecordError()`. Our C# port `SaUtilities.RecordWarning(cs, error, description, source)` is the equivalent and is the approved way to log in coded subassemblies (don't throw).

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

## C# Scaffold — GpdSubassemblies Pattern

This repo has a working C# subassembly scaffold at `CSharp/GpdSubassemblies/`. Use it as the starting point for any new coded subassembly — **do not start from scratch**.

### Quickstart: copy LaneGpd

```
CSharp/GpdSubassemblies/
  SubassemblyBase.cs          ← abstract base (DO NOT EDIT — translate of SATemplate.vb)
  Codes.cs                    ← shared point/link/shape code constants
  SaUtilities.cs              ← side constants, GetFlip(), GetAlignmentAndOrigin()
  Subassemblies/
    LaneGpd.cs                ← template — copy this, rename class, edit geometry
    DaylightToSurfaceGpd.cs   ← surface-target example (IntersectSurface pattern)
  content/
    GpdSubassemblies.atc      ← tool catalog — add one <Tool> block per subassembly
```

**To add a new subassembly:**
1. Copy `LaneGpd.cs`, rename class (PascalCase, no spaces)
2. Update param constants and `DrawImplement()` geometry
3. Add a `<Tool>` block to `content/GpdSubassemblies.atc`
4. Build — post-build target copies DLL to `content/` automatically

### SubassemblyBase entry points

```csharp
// Public entry points (called by corridor engine — do NOT override these):
public void GetLogicalNames()   // wraps GetLogicalNamesImplement()
public void GetInputParameters()  // wraps GetInputParametersImplement()
public void GetOutputParameters() // wraps GetOutputParametersImplement()
public void Draw()               // wraps DrawImplement() — ABSTRACT, must override

// Override these in your subassembly:
protected virtual void GetLogicalNamesImplement(CorridorState cs)  { }
protected virtual void GetInputParametersImplement(CorridorState cs) { }
protected virtual void GetOutputParametersImplement(CorridorState cs) { }
protected abstract void DrawImplement(CorridorState cs);

// Helpers on the base (read scalars via the indexer — Add() is a SETTER, never read with it):
protected double GetDouble(CorridorState cs, string name, double defaultValue)
protected int    GetInt(CorridorState cs, string name, int defaultValue)
protected string GetString(CorridorState cs, string name, string defaultValue)
protected void   SetDouble(CorridorState cs, string name, double defaultValue, double value)
protected void   SetInt(CorridorState cs, string name, int defaultValue, int value)
```

### Points → Links → Shapes recipe

```csharp
protected override void DrawImplement(CorridorState cs)
{
    // 1. Read parameters (GetInt/GetDouble read the existing param via the indexer — never Add() to read)
    int side    = GetInt(cs, "Side", 0);
    double width = GetDouble(cs, "Width", 12.0);
    double flip  = SaUtilities.GetFlip(side);  // +1 right, -1 left

    // 2. Layout mode stub (draw a ghost so subassembly is visible before corridor is computed)
    if (cs.Mode == CorridorMode.Layout)
    {
        var lo = cs.Points.Add(0, 0, "");
        var ld = cs.Points.Add(flip * width, 0, "");
        cs.Links.Add(lo, ld, Codes.Top, CorridorLinkDisplay.DashedWithArrowhead);
        return;
    }

    // 3. Add points (all offsets/elevations relative to attachment origin = 0,0)
    var pts = cs.Points;
    var p1 = pts.Add(0,           0,            "");  p1.Codes.TryAdd(Codes.Crown);
    var p2 = pts.Add(flip*width,  width*slope,  "");  p2.Codes.TryAdd(Codes.ETW);
    var p3 = pts.Add(0,          -depth,        "");  p3.Codes.TryAdd(Codes.CrownSubBase);
    var p4 = pts.Add(flip*width,  width*slope-depth, ""); p4.Codes.TryAdd(Codes.ETWSubBase);

    // 4. Add links
    var lnks = cs.Links;
    var lTop  = lnks.Add(p1, p2, Codes.Top);  lTop.Codes.TryAdd(Codes.Pave);
    var lSide = lnks.Add(p2, p4, "");
    var lBot  = lnks.Add(p4, p3, Codes.Datum); lBot.Codes.TryAdd(Codes.SubBase);
    var lBack = lnks.Add(p3, p1, "");

    // 5. Add shape (closed region — pass the links that form its boundary)
    cs.Shapes.Add(new Link[] { lTop, lSide, lBot, lBack }, Codes.Pave1);

    // 6. Write output parameters back
    SetDouble(cs, "Width", 12.0, width);
}
```

### Surface target (logical name) pattern

```csharp
// In GetLogicalNamesImplement:
var p = cs.ParamsLong.Add("TargetDTM", (int)ParamLogicalNameType.Surface);
p.DisplayName = "Existing Ground Surface";

// In DrawImplement — read the surface ObjectId from the COLLECTION (.Value(name)), NOT the
// indexer: the indexer / individual Param.Value getter does not return the user-assigned target.
// Matches Autodesk's stock DaylightStandard.vb and our DaylightToSurfaceGpd.cs.
ObjectId surfId = ObjectId.Null;
try { surfId = cs.ParamsSurface.Value("TargetDTM"); } catch { }
if (surfId.IsNull)
{
    SaUtilities.RecordWarning(cs, CorridorError.LogicalNameNotFound,
        "Surface target 'TargetDTM' not set.", nameof(MySubassembly));
    return;
}

// Intersect the surface:
SaUtilities.GetAlignmentAndOrigin(cs, out var alignId, out var origin);
bool isFill = cs.IsAboveSurface(surfId, alignId, origin);
double slope = isFill ? -fillSlope : cutSlope;
IPoint? pt = cs.IntersectSurface(surfId, alignId, origin, lookRight: side == SaUtilities.Right, slope);
if (pt == null)
{
    SaUtilities.RecordWarning(cs, CorridorError.NoSideslopeIntersectFound,
        "No intersection found at this station.", nameof(MySubassembly));
    return;
}
```

### Safe param reading — indexer for scalars, `.Value(name)` for targets

There are **two** different accessors, and confusing them silently freezes every parameter at its
default. (Verified against shipping `SubassemblyBase.cs` / `OdotGuardrailMgs.cs`.)

```csharp
// SCALAR params (double/long/string/bool) — read via the INDEXER:
double width = cs.ParamsDouble["Width"].Value;     // what GetDouble/GetInt/GetString do internally

// TARGETS (surface/alignment/offset/elevation) — read via the COLLECTION method:
ObjectId surfId   = cs.ParamsSurface.Value("TargetDTM");        // ObjectId
WidthOffsetTarget wot = cs.ParamsOffsetTarget.Value("TargetHA"); // then GetDistanceToAlignment(...)
```

**`cs.ParamsDouble.Add(name, default)` is a SETTER**, not a read. Calling `Add(name, d).Value` to
*read* overwrites the user's value with the default on every section — the symptom is "the
subassembly ignores all parameter and Left/Right changes." Use `Add()` only to **declare** (in
`GetInputParametersImplement`) and to **write back** computed outputs (in the `Set*` helpers). Always
read scalars through the base `GetDouble()`/`GetInt()`/`GetString()` helpers, which use the indexer.

See `c3d-subassembly-patterns` (Reading params vs. targets) for the full rule table and the
DB-invisibility caveat below.

### .atc registration format

```xml
<Tool>
  <ItemID idValue="{generate-a-new-GUID-here}"/>
  <Properties>
    <ItemName>My Subassembly (GPD)</ItemName>
    <Description>Short description shown in tool palette.</Description>
    <Keywords>keyword1 keyword2 GPD subassembly</Keywords>
    <Time createdUniversalDateTime="2026-01-01T00:00:00"
          modifiedUniversalDateTime="2026-01-01T00:00:00"/>
  </Properties>
  <Source/>
  <Data>
    <AeccDbSubassembly>
      <GeometryGenerateMode>UseDotNet</GeometryGenerateMode>
      <DotNetClass Assembly="C:\full\path\to\GpdSubassemblies.dll">
        GpdSubassemblies.Subassemblies.MySubassembly
      </DotNetClass>
      <Params>
        <!-- DataType: lowercase string literal — "long", "double", or "string".            -->
        <!-- TypeInfo selects how the value RENDERS in the Properties grid (see table below). -->
        <!-- ALWAYS store distances in FEET; pick the display unit with TypeInfo:             -->
        <!--   16 (Distance)  -> feet,  e.g. 12.0 shows 12.000'   (lane width)                -->
        <!--   17 (Dimension) -> inches, e.g.  0.5 shows  6.000"  (curb height: store 0.5 ft) -->
        <!--    0 (Double)    -> bare number, e.g. 6.0 shows 6.000 (counts, ratios, in/ft)     -->
        <!-- long enum params take NO TypeInfo — just DataType="long" + an <Enum> block.       -->
        <Side  DataType="long" DisplayName="Side" Description="Left or Right">0
          <Enum>
            <Right DisplayName="Right">0</Right>
            <Left  DisplayName="Left">1</Left>
          </Enum>
        </Side>
        <Width DataType="double" TypeInfo="16" DisplayName="Width" Description="Lane width (ft)">12</Width>
      </Params>
    </AeccDbSubassembly>
    <Units>foot</Units>
  </Data>
</Tool>
```

**Key points:**
- `Assembly=` must be an **absolute path** to the DLL (or a path relative to Civil 3D's working directory). The `%AECCCONTENT_DIR%` env var only expands at runtime for catalogs in the Autodesk content folder.
- Post-build target in `GpdSubassemblies.csproj` copies the DLL to `content/` — the `.atc` points there. The path is already set in the repo's catalog.
- Generate a unique GUID for each `<ItemID idValue>` — duplicates cause Civil 3D to silently skip the tool.

### TypeInfo → how a parameter renders (empirically verified)

`TypeInfo` is the ordinal of `Autodesk.Civil.Runtime.TypeInfoDouble` / `TypeInfoLong` / `TypeInfoBool`.
It controls **only the display format** in the Properties grid — the stored number is whatever you
put in the catalog. Values below were read back from a live placement with the **GPDSAPROBE** probe
(stored `6.0` unless noted):

| TypeInfo | Enum (Double) | Renders | Use for |
|---|---|---|---|
| `0` | Double | `6.000` (bare) | counts, ratios, slope in **in/ft** |
| `1` | NonNegativeDouble | `6.000` | non-negative bare number |
| `8` | Grade | `-500.00%` (value = rise/run) | grade |
| `10` | TransparentCmdSlope | `-12.00:1` (for `-0.0833`) | slope ratio (run:rise) |
| `14` | Angle | degrees — **value treated as radians** | angles (store radians) |
| `16` | Distance | `6.000'` — **drawing-unit FEET** | a length measured in feet (lane width) |
| `17` | Dimension | `72.000"` — **feet × 12, inches** | inch dimensions (store **feet**: `0.5` → `6.000"`) |
| `25` | Percent | `-12%` (for `-12.5`) | percent |

Rules that fall out of this:
- **Store every distance in feet** (the geometry library works in feet). Choose the *display* with
  TypeInfo: `16` shows feet, `17` shows inches, `0` shows a bare number. A 6-inch curb is `0.5` with
  `TypeInfo="17"`. Do **not** use `16` for an inch dimension — it renders feet (`0.5'`, not `6"`).
- **Long enum params carry NO TypeInfo** — they render as a dropdown from their `<Enum>` block alone.

### Catalog is the SOLE metadata source — `GetInputParametersImplement` is Add-only (native-crash gotcha)

`GetInputParametersImplement` must **only** `cs.ParamsX.Add(key, default)`. **Never** set `TypeInfo`,
call `AddEnumData`, or set `IsReadOnly` / `DisplayOrder` **in code**. All of that metadata lives in the
catalog `.atc`/`.xtp`. Doing both double-types the parameter across the managed/native boundary and
triggers an **uncatchable native `AccessViolation` when Civil 3D consumes the param set at placement**
(the base-class `try/catch` cannot intercept it — Civil 3D just crashes). Every stock subassembly is
Add-only; mirror them. The **GPDSAPROBE** DEBUG command (`CSharp/SubassemblyProbe/`) dumps a placed
subassembly's per-parameter `TypeInfo` + settings to `%TEMP%\gpd-saprobe.{json,txt}` — use it to read
how any given catalog entry actually renders.

## Core Mechanics — Mined Patterns

Compact reference for mechanics that recur across the stock subassemblies. Full `DrawImplement`
recipes live in `c3d-subassembly-patterns`.

### Medians / dual attachment

Medians attach at the **centerline and draw both sides from one origin** — there is **no `Side`/flip
param**. Mirror each point about `x = 0`. The depressed-median variant (`MedianDepressed.vb`) also
needs a `MarkPoint` subassembly **upstream** (it joins to that mark). Components that join two
roadways use a normal attachment on one side and a **marked-point** attachment on the other.

### Marked points (joining two roadways)

A producer subassembly drops a named mark; a consumer finds it and links to it. Names are
**upper-cased** in the stock samples — normalize with `ToUpperInvariant()` on both ends.

```csharp
// Produce: cs.ParamsPoint.Add(name.ToUpperInvariant()).SetPoint(worldX, worldY, worldZ);
// Consume: ParamPoint mark = cs.ParamsPoint.Value(name.ToUpperInvariant());  // collection accessor
//          double dx = mark.Offset - origin.Offset;  double dy = mark.Elevation - origin.Elevation;
```

If the mark is missing, `RecordError(CorridorError.NoMarkedPointFound, …)` and return. See
`MarkPoint.vb` / `LinkToMarkedPoint.vb`, and recipe R2.

### Conditional subassemblies (cut/fill gate)

`ConditionalCutOrFill.vb` / `ConditionalHorizontalTarget.vb` **emit no geometry**. They test a
condition and, on failure, halt the subassemblies placed **after** them:

```csharp
cs.RecordError(CorridorError.StopProcessingConditional, CorridorErrorLevel.None, "", source, false);
```

Place a conditional *before* whatever it guards. See recipe R3.

### Superelevation axis of rotation

A lane that can be an SE pivot reads the alignment cross-slope at the station
(`Alignment.GetCrossSlopeAtStation` with a `SuperelevationCrossSegmentType`) and registers itself:

```csharp
cs.SetAxisOfRotationInformation(isPotentialPivot, slope, segType, isReversed);
cs.SetAxisOfRotationCrownPoint(1u);   // 1-BASED point index; 0 = "no crown point", not "first"
```

The stock VB adjusts a 1-based crown index down by one for an internal C++ array — **you do not** in
C#, but `SetAxisOfRotationCrownPoint` itself still takes the **1-based** point number. See
`LaneSuperelevationAOR.vb`, recipe R5, and the `c3d-superelevation` skill.

### Offset-baseline origin

Always get the attachment point through `SaUtilities.GetAlignmentAndOrigin(cs, out alignId, out
origin)` — it uses `CurrentOffset`/`CurrentElevation` (the attachment point) and adds
`CurrentAssemblyFixedOffset`/`Elevation` for fixed-offset baselines. Using
`CurrentSubassemblyOffset/Elevation` instead casts `IntersectSurface` from the wrong place and every
daylight misses the surface. (Mirrors stock `Utilities.GetAlignmentAndOrigin` / `AdjustOffset`.)

### Output parameters & DisplayName

Mark computed values `ParamAccessType.Output` and give them a readable `DisplayName` so they show in
section reports / QTO. Stock VB sets `DisplayName` to a **numeric resource-string ID** (e.g. `"3280"`)
for localization; in our coded subassemblies just use a plain readable string
(`postLen.DisplayName = "Post Length"`). See `OdotGuardrailMgs.GetOutputParametersImplement`.

## Converting Subassembly Composer (PKT) to .NET

A `.pkt` is a ZIP container. Inspect it read-only — no extraction needed:

```csharp
using System.IO.Compression;
using var zip = ZipFile.OpenRead(@"C:\ProgramData\Autodesk\C3D 2026\enu\Subassemblies\Imperial\Berm.pkt");
foreach (var e in zip.Entries) Console.WriteLine(e.FullName);
// → Berm.atc, Berm.xaml, 000a545a....dll  (SAC-authored PKT)
// → or: MyLib.dll, MyLib.atc              (.NET-coded PKT, no XAML)
```

### Two PKT content types

| Type | Contents | Logic | Conversion path |
|---|---|---|---|
| **SAC-authored** | `*.atc` + WF `*.xaml` flowchart + thin wrapper DLL | Windows Workflow Foundation activities | Translate XAML → C# `DrawImplement` (see table below) |
| **.NET-coded** | real `*.dll` + `*.atc`, no XAML | Compiled C# or VB.NET | Decompile with ILSpy; already structured as `SATemplate` subclass |

Both types share the `.atc` format (`GeometryGenerateMode=UseDotNet`) — params come free from the embedded `.atc`.

### WF-XAML → C# `DrawImplement` mapping

| WF Activity / construct | C# equivalent |
|---|---|
| `FlowDecision` (True/False branches) | `if (condition) { ... } else { ... }` |
| `Sequence` | Statement block `{ ... }` |
| `FlowStep` | A single statement |
| `Variable<T>` | Local variable `T name = defaultValue;` |
| `Assign<T>` | `name = expression;` |
| `AddPoint` activity | `cs.Points.Add(offset, elevation, code)` |
| `AddLink` activity | `cs.Links.Add(p1, p2, code)` |
| `AddShape` activity | `cs.Shapes.Add(links, code)` |
| `IntersectSurface` activity | `cs.IntersectSurface(surfId, alignId, origin, lookRight, slope)` |
| `IsAboveSurface` activity | `cs.IsAboveSurface(surfId, alignId, point)` |
| `GetParam` / `InputVariable` | read from `cs.ParamsDouble`/`cs.ParamsLong` (or `.atc` default) |

Params declared in the embedded `.atc` map 1:1 to `GetInputParametersImplement` declarations.

### Conversion effort estimate

| Complexity | Example | Estimate |
|---|---|---|
| Simple | Berm (7 params, 1 flowdecision) | 1–3 hours |
| Medium | EvenSlopeDitch (multi-param, 3 decisions) | 3–8 hours |
| Complex | DaylightStandard (surface targets, superelevation, SE branches) | 1 day+ |

**No Autodesk auto-converter exists.** Conversion is manual but mechanical — the WF activities map 1:1 to `CorridorState` calls.

### Reference corpus

- ~100 stock PKTs: `C:\ProgramData\Autodesk\C3D 2026\enu\Subassemblies\Imperial\`
- SAC installed locally: `C:\Program Files\Autodesk\Subassembly Composer 2026\` and `…2027\`
- A future PKT→C# skeleton generator is a deferred option (not yet built).

## Gotchas

- Custom subassemblies can be written in C# or VB.NET using `SubassemblyGeometryGenerateMode.UseDotNet`
- **Separate DLL required.** The subassembly DLL is loaded by the corridor processor via the `.atc` `Assembly=` path, NOT by AutoCAD's netload/appload mechanism. It must be a standalone class library project (`GpdSubassemblies.csproj`), not a folder glob-linked into the main meta-project (`C3DPlugins.csproj`). These are two different loading contexts.
- Always handle the case where targets are not found (use try/catch)
- Use `corridorState.RecordError()` instead of throwing exceptions to avoid crashing corridor processing
- Point, link, and shape codes should be consistent across all subassemblies in a catalog
- Consider both normal crown and superelevation conditions
- `WidthOffsetTarget.GetDistanceToAlignment()` returns XY coordinates at the perpendicular intersection point (not a station value)
- Check `corridorState.Mode` to handle `CorridorMode.Layout` vs `CorridorMode.Design` differently when needed
- The `Subassembly.Status` property can be `FileNotFound` if the source assembly is missing - check before calling `Run()`
- **`DrawingUnitType` has `Feet` and `Meters` only** — NOT `Imperial`. Use `DrawingUnitType.Feet` for Imperial unit checks.
- **`CorridorError` has no `UnhandledException` member** — use `CorridorError.Failure` for catch-all exception recording.
- `ParamLong.Value` returns **`int`** in C# (not `long` — VB.NET's `Long` maps to `Int32`). Use `int` everywhere.
- **Read targets via the collection `.Value(name)`, scalars via the indexer.** `cs.ParamsSurface.Value("Name")` → `ObjectId`, `cs.ParamsOffsetTarget.Value("Name")` → `WidthOffsetTarget`, `cs.ParamsElevationTarget.Value("Name")` → `SlopeElevationTarget`, `cs.ParamsPoint.Value("Name")` → `ParamPoint` (marked point). Scalars (`ParamsDouble`/`ParamsLong`/`ParamsString`) read via the indexer `cs.ParamsDouble["Name"].Value`. The individual `Param.Value` getter does NOT return an assigned offset/elevation target.
- **DB-invisible accessors:** the param/target collections inherit a generic `ParamCollectionBase<T>` whose members don't reflect into `api_combined_2026.db` (`ParamSurfaceCollection`/`ParamOffsetTargetCollection` show "No members"). So `code-verifier`/DB lookups will false-positive on `.Value(name)`, `GetDistanceToAlignment`, `GetElevation` — these are real (proven by the stock VB samples and our shipping code). Do not "fix" them away.
- Debugging: coded subassemblies run inside corridor rebuild, NOT in a command context. Attach VS debugger to `acad.exe`, set a breakpoint in `DrawImplement`, then force a corridor rebuild (select corridor → right-click → Rebuild) to hit it.

## Related Skills

- `c3d-subassembly-patterns` — Stock-SA lookup index, worked `DrawImplement` recipes, code reference
- `c3d-corridors` — Corridor structure, baselines, assemblies
- `c3d-superelevation` — Alignment cross-slope / axis-of-rotation reads for SE-aware subassemblies
- `c3d-alignments` — Alignments and superelevation
- `c3d-profiles` — Profiles used as corridor baselines
