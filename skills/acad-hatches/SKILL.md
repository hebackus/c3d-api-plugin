---
name: acad-hatches
description: Hatches and gradient fills - pattern creation, boundary loops (polyline and entity-based), gradient fills, associativity, hatch styles
---

# AutoCAD Hatches and Gradient Fills

Use this skill when creating or modifying hatch patterns, solid fills, or gradient fills in drawings.

## Creating a Hatch Pattern

```csharp
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    BlockTableRecord btr = (BlockTableRecord)tr.GetObject(
        db.CurrentSpaceId, OpenMode.ForWrite);

    Hatch hatch = new Hatch();
    hatch.SetDatabaseDefaults();
    hatch.Normal = Vector3d.ZAxis;
    hatch.Elevation = 0.0;

    // Step 1: Add to database FIRST (required before SetHatchPattern and AppendLoop)
    btr.AppendEntity(hatch);
    tr.AddNewlyCreatedDBObject(hatch, true);

    // Step 2: Set pattern AFTER AppendEntity, BEFORE AppendLoop
    hatch.SetHatchPattern(HatchPatternType.PreDefined, "ANSI31");
    hatch.PatternScale = 1.0;
    hatch.PatternAngle = 0.0;

    // Step 3: Set Associative BEFORE AppendLoop
    hatch.Associative = true;

    // Step 4: Add boundary loop
    ObjectIdCollection boundaryIds = new ObjectIdCollection();
    boundaryIds.Add(polylineId);  // closed polyline as boundary
    hatch.AppendLoop(HatchLoopTypes.External, boundaryIds);

    // Evaluate to generate hatch lines
    hatch.EvaluateHatch(true);

    tr.Commit();
}
```

## Boundary Loop Types

### From Entity IDs (most common)

```csharp
ObjectIdCollection outerBoundary = new ObjectIdCollection();
outerBoundary.Add(outerPolylineId);
hatch.AppendLoop(HatchLoopTypes.External, outerBoundary);

// Add island (inner boundary)
ObjectIdCollection innerBoundary = new ObjectIdCollection();
innerBoundary.Add(innerCircleId);
hatch.AppendLoop(HatchLoopTypes.Default, innerBoundary);
```

### From Polyline Vertices (with bulge)

```csharp
Point2dCollection vertices = new Point2dCollection();
vertices.Add(new Point2d(0, 0));
vertices.Add(new Point2d(100, 0));
vertices.Add(new Point2d(100, 100));
vertices.Add(new Point2d(0, 100));

DoubleCollection bulges = new DoubleCollection();
bulges.Add(0); bulges.Add(0); bulges.Add(0); bulges.Add(0);

hatch.AppendLoop(HatchLoopTypes.External | HatchLoopTypes.Polyline,
    vertices, bulges);
```

### From 2D Curve Edges

```csharp
Curve2dCollection edges = new Curve2dCollection();
IntegerCollection edgeTypes = new IntegerCollection();

edges.Add(new LineSegment2d(new Point2d(0, 0), new Point2d(100, 0)));
edgeTypes.Add((int)HatchEdgeType.Line);  // 1

edges.Add(new CircularArc2d(
    new Point2d(100, 0), new Point2d(100, 50), new Point2d(100, 100)));
edgeTypes.Add((int)HatchEdgeType.CircularArc);  // 2

edges.Add(new LineSegment2d(new Point2d(100, 100), new Point2d(0, 0)));
edgeTypes.Add((int)HatchEdgeType.Line);

hatch.AppendLoop(HatchLoopTypes.External, edges, edgeTypes);
```

### Using HatchLoop Object

```csharp
HatchLoop loop = new HatchLoop(HatchLoopTypes.External);
// loop is read-only after construction; use for inspection:
// loop.Curves, loop.Polyline, loop.LoopType, loop.IsPolyline

hatch.AppendLoop(loop);
```

## Loop Management

```csharp
int loopCount = hatch.NumberOfLoops;
HatchLoopTypes loopType = hatch.LoopTypeAt(0);
HatchLoop loop = hatch.GetLoopAt(0);

// Insert loop at specific position
hatch.InsertLoopAt(1, HatchLoopTypes.Default, boundaryIds);
hatch.InsertLoopAt(1, hatchLoop);

// Remove loop
hatch.RemoveLoopAt(0);

// Get associated objects for a loop
ObjectIdCollection assocIds = hatch.GetAssociatedObjectIdsAt(0);
ObjectIdCollection allAssocIds = hatch.GetAssociatedObjectIds();
hatch.RemoveAssociatedObjectIds();
```

## Solid Fill

```csharp
Hatch hatch = new Hatch();
hatch.SetDatabaseDefaults();
hatch.Normal = Vector3d.ZAxis;
hatch.SetHatchPattern(HatchPatternType.PreDefined, "SOLID");
// IsSolidFill will be true
```

## Gradient Fills

```csharp
Hatch gradient = new Hatch();
gradient.SetDatabaseDefaults();
gradient.Normal = Vector3d.ZAxis;
gradient.HatchObjectType = HatchObjectType.GradientObject;

// Set gradient type
gradient.SetGradient(GradientPatternType.PreDefinedGradient, "LINEAR");
// Other names: "CYLINDER", "INVCYLINDER", "SPHERICAL", "INVSPHERICAL",
//              "HEMISPHERICAL", "INVHEMISPHERICAL", "CURVED", "INVCURVED"

gradient.GradientAngle = Math.PI / 4;  // 45 degrees

// Two-color gradient
gradient.GradientOneColorMode = false;
GradientColor[] colors = new GradientColor[2];
colors[0] = new GradientColor(Color.FromRgb(255, 0, 0), 0.0f);   // start
colors[1] = new GradientColor(Color.FromRgb(0, 0, 255), 1.0f);   // end
gradient.SetGradientColors(colors);

// One-color gradient (single color with tint)
gradient.GradientOneColorMode = true;
gradient.ShadeTintValue = 0.5f;  // 0 = dark, 1 = light
gradient.GradientShift = 0.0f;

// Add boundary and evaluate
btr.AppendEntity(gradient);
tr.AddNewlyCreatedDBObject(gradient, true);
gradient.AppendLoop(HatchLoopTypes.External, boundaryIds);
gradient.EvaluateHatch(true);
```

**Gradient methods:**
- `SetGradient(GradientPatternType type, string name)` - set gradient pattern
- `GetGradientColors()` -> `GradientColor[]` - get color stops
- `SetGradientColors(GradientColor[] colors)` - set color stops
- `EvaluateGradientColorAt(float value)` -> `Color` - sample color at position (0-1)

## Hatch Properties

**Pattern:**
- `PatternName` (string, get-only) - current pattern name
- `PatternType` (HatchPatternType, get-only) - UserDefined=0, PreDefined=1, CustomDefined=2
- `PatternScale` (double, get/set) - pattern scale
- `PatternAngle` (double, get/set) - pattern angle in radians
- `PatternSpace` (double, get/set) - spacing for user-defined patterns
- `PatternDouble` (bool, get/set) - double pattern (crosshatch)
- `Origin` (Point2d, get/set) - pattern origin

**Gradient:**
- `GradientName` (string, get-only) - gradient pattern name
- `GradientType` (GradientPatternType, get-only) - PreDefinedGradient=0, UserDefinedGradient=1
- `GradientAngle` (double, get/set) - gradient rotation angle in radians
- `GradientOneColorMode` (bool, get/set) - single color mode
- `GradientShift` (float, get/set) - shift factor
- `ShadeTintValue` (float, get/set) - shade/tint for one-color mode

**State:**
- `HatchObjectType` (HatchObjectType, get/set) - HatchObject=0, GradientObject=1
- `IsHatch` (bool, get-only) - true if hatch pattern
- `IsGradient` (bool, get-only) - true if gradient fill
- `IsSolidFill` (bool, get-only) - true if solid fill
- `HatchStyle` (HatchStyle, get/set) - Normal=0, Outer=1, Ignore=2
- `Associative` (bool, get/set) - boundary association
- `BackgroundColor` (Color, get/set)

**Geometry:**
- `Normal` (Vector3d, get/set)
- `Elevation` (double, get/set)
- `Area` (double, get-only) - computed area
- `NumberOfLoops` (int, get-only)
- `NumberOfHatchLines` (int, get-only)
- `NumberOfPatternDefinitions` (int, get-only)

**Methods:**
- `SetHatchPattern(HatchPatternType type, string name)` - set pattern
- `EvaluateHatch(bool underEstimateNumLines)` - regenerate hatch lines
- `GetHatchLinesData()` -> `Line2dCollection` - get computed hatch lines
- `GetHatchLineDataAt(int index)` -> `Line2d`
- `GetPatternDefinitionAt(int index)` -> `PatternDefinition`

## HatchLoop Properties

- `Curves` (Curve2dCollection, get-only) - edge curves
- `Polyline` (BulgeVertexCollection, get-only) - polyline vertices with bulge
- `LoopType` (HatchLoopTypes, get-only) - type flags
- `IsPolyline` (bool, get-only) - polyline vs edge loop

## Enums

**HatchLoopTypes** (flags): Default=0x0, External=0x1, Polyline=0x2, Derived=0x4, Textbox=0x8, Outermost=0x10, NotClosed=0x20, SelfIntersecting=0x40, TextIsland=0x80, Duplicate=0x100

**HatchEdgeType:** Line=1, CircularArc=2, EllipticalArc=3, Spline=4

**HatchStyle:** Normal=0 (fills between nested boundaries), Outer=1 (outermost boundary only), Ignore=2 (ignores internal boundaries)

**HatchPatternType:** UserDefined=0, PreDefined=1, CustomDefined=2

**HatchObjectType:** HatchObject=0, GradientObject=1

**GradientPatternType:** PreDefinedGradient=0, UserDefinedGradient=1

## Gotchas

- Set the pattern type/name BEFORE adding loops and BEFORE calling `EvaluateHatch`
- `AppendLoop` must be called AFTER `AppendEntity` and `AddNewlyCreatedDBObject` - the hatch must be in the database first
- `EvaluateHatch(true)` underestimates line count (faster); `EvaluateHatch(false)` is accurate but slower
- For user-defined patterns, use `PatternSpace` instead of `PatternScale`; set `PatternDouble = true` for crosshatch
- `Associative` must be set to `true` BEFORE adding boundary loops for associativity to work
- Boundary loops must be closed - open boundaries cause `EvaluateHatch` to fail silently
- The outer boundary should use `HatchLoopTypes.External`; inner islands should use `HatchLoopTypes.Default`
- `HatchStyle.Normal` alternates fill between nested boundaries; `Outer` fills only the outermost; `Ignore` fills everything
- For gradients, set `HatchObjectType = HatchObjectType.GradientObject` before calling `SetGradient`
- `PatternName` and `PatternType` are read-only - use `SetHatchPattern()` to change them
- After changing `PatternScale`, `PatternAngle`, or `PatternSpace`, you **must re-call `SetHatchPattern(type, name)`** before calling `EvaluateHatch()` — otherwise the change has no visual effect
- BulgeVertex `Bulge` value: 0 = straight segment, positive = counterclockwise arc, negative = clockwise arc; `tan(includedAngle/4)`
