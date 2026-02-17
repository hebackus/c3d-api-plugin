---
name: c3d-surfaces
description: TIN, Grid, and Volume surfaces - creation, point data, breaklines, contours, boundaries, smoothing, snapshots, and analysis
---

# Civil 3D Surfaces

Use this skill when working with surface objects (TIN, Grid, Volume) - creating, modifying, querying, or analyzing surfaces.

## Surface Class Hierarchy

```
Surface (base)
├── TinSurface          - Triangulated Irregular Network
├── GridSurface         - Regular grid of elevations
├── TinVolumeSurface    - Volume between two TIN surfaces
└── GridVolumeSurface   - Volume between two Grid surfaces
```

## Namespace Conflict Warning

`Surface` exists in both `Autodesk.AutoCAD.DatabaseServices` and `Autodesk.Civil.DatabaseServices`. Use an alias:

```csharp
using CivSurface = Autodesk.Civil.DatabaseServices.Surface;
```

## Accessing Surfaces

```csharp
ObjectIdCollection surfaceIds = doc.GetSurfaceIds();
foreach (ObjectId surfaceId in surfaceIds)
{
    CivSurface oSurface = surfaceId.GetObject(OpenMode.ForRead) as CivSurface;
    ed.WriteMessage("Surface: {0}, Type: {1}\n",
        oSurface.Name, oSurface.GetType().ToString());
}
```

Prompt user to select a TIN surface:

```csharp
PromptEntityOptions options = new PromptEntityOptions("\nSelect a TIN Surface: ");
options.SetRejectMessage("\nThe selected object is not a TIN Surface.");
options.AddAllowedClass(typeof(TinSurface), true);
PromptEntityResult result = editor.GetEntity(options);
if (result.Status == PromptStatus.OK)
    return result.ObjectId;
```

## Surface Properties

```csharp
// General properties (resource-intensive - call once, reuse)
GeneralSurfaceProperties genProps = oSurface.GetGeneralProperties();
// genProps.MinimumElevation, MaximumElevation, MeanElevation
// genProps.MinimumCoordinateX/Y, MaximumCoordinateX/Y
// genProps.NumberOfPoints

// TIN-specific
TinSurfaceProperties tinProps = ((TinSurface)oSurface).GetTinProperties();
// tinProps.NumberOfTriangles, Min/MaxTriangleArea, Min/MaxTriangleLength

// Grid-specific
GridSurfaceProperties gridProps = ((GridSurface)oSurface).GetGridProperties();
// gridProps.SpacingX, SpacingY, Orientation
```

## Creating Surfaces

### TIN Surface (empty)

```csharp
ObjectId surfaceStyleId = doc.Styles.SurfaceStyles[0];
ObjectId surfaceId = TinSurface.Create("MySurface", surfaceStyleId);
TinSurface surface = surfaceId.GetObject(OpenMode.ForWrite) as TinSurface;

// Add points
Point3dCollection points = new Point3dCollection();
points.Add(new Point3d(x, y, z));
surface.AddVertices(points);
ts.Commit();
```

### TIN Surface from .tin File

```csharp
Database db = Application.DocumentManager.MdiActiveDocument.Database;
ObjectId tinSurfaceId = TinSurface.CreateFromTin(db, @"path\to\file.tin");
```

### Grid Surface (empty)

```csharp
// Create with 25x25 spacing, 0 degree orientation
ObjectId surfaceId = GridSurface.Create("MyGrid", 25, 25, 0.0, surfaceStyleId);
GridSurface surface = surfaceId.GetObject(OpenMode.ForWrite) as GridSurface;

// Add points by grid location
GridLocation loc = new GridLocation(row, col);
surface.AddPoint(loc, elevation);
```

### Grid Surface from DEM

```csharp
ObjectId gridSurfaceId = GridSurface.CreateFromDEM(demFilePath, surfaceStyleId);
```

### Volume Surface

```csharp
ObjectId surfaceId = TinVolumeSurface.Create("VolSurface", baseId, comparisonId);
```

## Adding Boundaries

Boundaries are closed polygons that affect triangle visibility. Types: `Data Clip`, `Outer`, `Hide`, `Show`.

```csharp
ObjectId[] boundaries = { polylineId };
TinSurface oSurface = surfaceId.GetObject(OpenMode.ForWrite) as TinSurface;

oSurface.BoundariesDefinition.AddBoundaries(
    new ObjectIdCollection(boundaries),
    100,  // mid-ordinate distance
    Autodesk.Civil.Land.SurfaceBoundaryType.Outer,
    true  // use non-destructive breaklines
);
oSurface.Rebuild(); // Must rebuild after adding boundaries
```

**Note:** The rebuild icon in the GUI is NOT displayed when boundaries are modified via .NET API.

## Breaklines

### Standard Breakline
Adds points and recomputes triangles:
```csharp
oSurface.BreaklinesDefinition.AddStandardBreaklines(
    new ObjectIdCollection(lines),
    10,   // maximumDistance (supplementing distance)
    5,    // weedingDistance
    5,    // weedingAngle
    0     // mid-ordinate distance
);
```

### Non-Destructive Breakline
Does not remove triangle edges, places new points at intersections:
```csharp
oSurface.BreaklinesDefinition.AddNonDestructiveBreaklines(
    new ObjectIdCollection(lines), 1 /* mid-ordinate */);
```

### Proximity Breakline
Uses nearest existing surface points:
```csharp
oSurface.BreaklinesDefinition.AddProximityBreaklines(
    new ObjectIdCollection(lines), 1 /* mid-ordinate */);
```

### Import Breaklines from FLT File
```csharp
oSurface.BreaklinesDefinition.ImportBreaklinesFromFile("file.flt");
// Note: link to file is NOT maintained - breaklines are copied in
```

## Adding Contours

```csharp
// From polyline ObjectIdCollection
oSurface.ContoursDefinition.AddContours(
    new ObjectIdCollection(polylineIds),
    weedingDistance, weedingAngle, maximumDistance, midOrdinateDistance);

// Optional: minimize flat areas
SurfaceMinimizeFlatAreaOptions flatOptions = new SurfaceMinimizeFlatAreaOptions();
oSurface.ContoursDefinition.AddContours(polyIds, wd, wa, md, mod, flatOptions);
```

## Adding Point Data

### From Point File
```csharp
PointFileFormatCollection ptFileFormats =
    PointFileFormatCollection.GetPointFileFormats(
        HostApplicationServices.WorkingDatabase);
ObjectId ptFormatId = ptFileFormats["PENZD (space delimited)"];
oSurface.PointFilesDefinition.AddPointFile(penzdFile, ptFormatId);
```

### From DEM Files
```csharp
oSurface.DEMFilesDefinition.AddDEMFile(demFilePath);
```

## Smoothing

### Natural Neighbor Interpolation (NNI)
```csharp
SurfacePointOutputOptions output = new SurfacePointOutputOptions();
output.OutputLocations = SurfacePointOutputLocationsType.Centroids;
output.OutputRegions = new Point3dCollection[] { regionPoints };
SurfaceOperationSmooth op = oSurface.SmoothSurfaceByNNI(output);
```

### Kriging
```csharp
KrigingMethodOptions krigingOpts = new KrigingMethodOptions();
krigingOpts.SemivariogramModel = KrigingSemivariogramType.Spherical;
krigingOpts.SampleVertices = oSurface.GetVerticesInsidePolylines(...);
SurfaceOperationSmooth op = oSurface.SmoothSurfaceByKriging(output, krigingOpts);
```

### Output Location Types
- `EdgeMidPoints` - requires `Edges` (array of `TinSurfaceEdge`)
- `RandomPoints` - requires `RandomPointsNumber` and `OutputRegions`
- `Centroids` - requires `OutputRegions`
- `GridBased` - requires `OutputRegions`, `GridSpacingX/Y`, `GridOrientation`

## Performance: Snapshots

```csharp
if (oSurface.HasSnapshot)
    oSurface.RemoveSnapshot();

oSurface.CreateSnapshot();      // Records current triangle state
oSurface.RebuildSnapshot();     // Updates existing snapshot (errors if none exists)
oSurface.RemoveSnapshot();      // Removes snapshot
```

**Warning:** `RebuildSnapshot()` and `CreateSnapshot()` can error if surface is out-of-date. Check `HasSnapshot` first.

## Gotchas

- `GetGeneralProperties()` is resource-intensive - call once and reuse
- Import from LandXML is NOT supported in .NET - use COM API
- Adding point groups to TIN surface via API is NOT supported
- `ExtractContour()` / `ExtractBorder()` are NOT available in .NET - use COM
- Surface must be rebuilt after boundary changes via API
- Wall breaklines cannot create perfectly vertical walls in TIN surfaces
- Contour altitude uses z-value of the FIRST point only, regardless of other vertices

## Related Skills

- `c3d-root-objects` - Accessing surfaces through CivilDocument
- `c3d-profiles` - Surface profiles along alignments
- `c3d-corridors` - Corridor surfaces
