---
name: c3d-surfaces
description: TIN, Grid, and Volume surfaces - creation, point data, breaklines, contours, boundaries, smoothing, snapshots, extraction, and analysis
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

## Querying Elevation, Slope, and Direction

```csharp
// Available on the base Surface class - works for TIN and Grid surfaces
double elev = oSurface.FindElevationAtXY(x, y);
double slope = oSurface.FindSlopeAtXY(x, y);
double direction = oSurface.FindDirectionAtXY(x, y);

// Get intersection point with a ray
Point3d hitPoint = oSurface.GetIntersectionPoint(startPoint, direction);

// Find all points where a line segment crosses the surface
Point3dCollection crossings = oSurface.FindPointsAlongLine(lineSegment3d);
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

### TIN Surface from LandXML

```csharp
// Preferred overload - specify both the new surface name and the source surface name in the XML
ObjectId surfaceId = TinSurface.CreateFromLandXML(
    db,
    "NewSurfaceName",
    @"path\to\file.xml",
    "LandXMLSurfaceName");  // name of the surface inside the LandXML file

// Deprecated overload (Civil 2022+): 3-parameter version is obsolete
// ObjectId surfaceId = TinSurface.CreateFromLandXML(db, "SurfaceName", @"path\to\file.xml");
```

### TIN Surface by Cropping

Create a new surface from a region of an existing surface:

```csharp
// Crop using AutoCAD objects (polylines, etc.) and a point inside the region
ObjectId croppedId = TinSurface.CreateByCropping(
    db, "CroppedSurface", srcSurfaceId,
    new ObjectIdCollection(new[] { polylineId }),
    new Point2d(insideX, insideY));

// Crop using a Point3d boundary
ObjectId croppedId = TinSurface.CreateByCropping(
    db, "CroppedSurface", srcSurfaceId, point3dCollection);

// Crop using a Point2d boundary
ObjectId croppedId = TinSurface.CreateByCropping(
    db, "CroppedSurface", srcSurfaceId, point2dCollection);
```

### TIN Surface from Corridor Surface

```csharp
ObjectId surfaceId = TinSurface.CreateFromCorridorSurface("MySurface", corridorSurface);
```

### TIN Surface from IMX File

```csharp
ObjectId surfaceId = TinSurface.CreateFromIMX(
    db, surfaceStyleId, @"path\to\file.imx",
    "SurfaceName", gitHash, query, doCoordSysConversion: true);
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
// TIN volume surface
ObjectId surfaceId = TinVolumeSurface.Create("VolSurface", baseId, comparisonId, styleId);

// Grid volume surface
ObjectId surfaceId = GridVolumeSurface.Create(
    "GridVolSurface", baseId, comparisonId, spacingX, spacingY, orientation, styleId);
```

## Volume Surface Properties

```csharp
// Get volume data from a TIN or Grid volume surface
TinVolumeSurface volSurface = surfaceId.GetObject(OpenMode.ForRead) as TinVolumeSurface;

// Adjust cut/fill factors (read/write)
volSurface.CutFactor = 1.0;
volSurface.FillFactor = 1.15;

// Get computed volume properties
VolumeSurfaceProperties volProps = volSurface.GetVolumeProperties();
// volProps.UnadjustedCutVolume, UnadjustedFillVolume, UnadjustedNetVolume
// volProps.AdjustedCutVolume, AdjustedFillVolume, AdjustedNetVolume
// volProps.CutFactor, FillFactor
// volProps.BaseSurface, ComparisonSurface (ObjectIds)
```

### Bounded Volume Calculation (Any Surface)

```csharp
// Calculate cut/fill volumes within a polygon region on any surface
Point3dCollection polygon = new Point3dCollection();
polygon.Add(new Point3d(x1, y1, 0));
polygon.Add(new Point3d(x2, y2, 0));
polygon.Add(new Point3d(x3, y3, 0));

SurfaceVolumeInfo volInfo = oSurface.GetBoundedVolumes(polygon, datumElevation);
// volInfo.Cut, volInfo.Fill, volInfo.Net

// Without datum elevation
SurfaceVolumeInfo volInfo = oSurface.GetBoundedVolumes(polygon);
```

## Adding Point Data

### From Point Groups

```csharp
// Add a point group as a data source for the surface
TinSurface oSurface = surfaceId.GetObject(OpenMode.ForWrite) as TinSurface;
SurfaceOperationAddPointGroup op = oSurface.PointGroupsDefinition.AddPointGroup(pointGroupId);
oSurface.Rebuild();
```

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

## Extracting Contours and Borders

Both `TinSurface` and `GridSurface` support contour and border extraction. These methods create AutoCAD geometry in the drawing and return the ObjectIds.

### Extract Border
```csharp
// Extract surface boundary as polylines
// SurfaceExtractionSettingsType: Plan or Model
ObjectIdCollection borderIds = tinSurface.ExtractBorder(SurfaceExtractionSettingsType.Plan);
```

### Extract Contours
```csharp
// Extract contours at a specific elevation
ObjectIdCollection ids = tinSurface.ExtractContoursAt(elevation);

// With smoothing
ObjectIdCollection ids = tinSurface.ExtractContoursAt(
    elevation, ContourSmoothingType.SplineCurve, smoothFactor: 5);

// Extract contours at a regular interval
ObjectIdCollection ids = tinSurface.ExtractContours(interval: 2.0);

// With smoothing
ObjectIdCollection ids = tinSurface.ExtractContours(
    interval: 2.0, ContourSmoothingType.AddVertices, smoothFactor: 3);

// Extract contours within an elevation range
ObjectIdCollection ids = tinSurface.ExtractContours(
    lowElev: 100.0, highElev: 200.0, interval: 5.0);

// With smoothing
ObjectIdCollection ids = tinSurface.ExtractContours(
    lowElev: 100.0, highElev: 200.0, interval: 5.0,
    ContourSmoothingType.SplineCurve, smoothFactor: 4);
```

### Extract Major/Minor Contours
```csharp
// Uses the surface style's contour interval settings
ObjectIdCollection majorIds = tinSurface.ExtractMajorContours(
    SurfaceExtractionSettingsType.Plan);
ObjectIdCollection minorIds = tinSurface.ExtractMinorContours(
    SurfaceExtractionSettingsType.Plan);

// With smoothing
ObjectIdCollection majorIds = tinSurface.ExtractMajorContours(
    SurfaceExtractionSettingsType.Plan,
    ContourSmoothingType.SplineCurve, smoothFactor: 5);
```

### Extract Watershed and Gridded
```csharp
ObjectIdCollection watershedIds = tinSurface.ExtractWatershed(
    SurfaceExtractionSettingsType.Plan);
ObjectIdCollection griddedIds = tinSurface.ExtractGridded(
    SurfaceExtractionSettingsType.Plan);
```

### ContourSmoothingType Values
- `AddVertices` - adds intermediate vertices for smoother appearance
- `SplineCurve` - fits a spline curve through contour points

### SurfaceExtractionSettingsType Values
- `Plan` - extract for plan view
- `Model` - extract for 3D model view

## Vertex and Edge Manipulation (TIN)

```csharp
TinSurface oSurface = surfaceId.GetObject(OpenMode.ForWrite) as TinSurface;

// Add a single vertex
SurfaceOperationAddTinVertex op = oSurface.AddVertex(new Point2d(x, y));
// or with elevation
SurfaceOperationAddTinVertex op = oSurface.AddVertex(new Point3d(x, y, z));

// Find a vertex at a location
TinSurfaceVertex vertex = oSurface.FindVertexAtXY(x, y);

// Move a vertex to a new XY location
oSurface.MoveVertex(vertex, new Point2d(newX, newY));

// Change vertex elevation
oSurface.SetVertexElevation(vertex, newElevation);

// Raise multiple vertices by a delta
oSurface.RaiseVertices(vertices, deltaElevation);

// Delete a vertex
oSurface.DeleteVertex(vertex);

// Delete multiple vertices
oSurface.DeleteVertices(vertexCollection);

// Swap a triangle edge (flip the shared edge between two triangles)
TinSurfaceEdge edge = oSurface.FindEdgeAtXY(x, y);
oSurface.SwapEdge(edge);

// Add/delete lines (triangle edges)
oSurface.AddLine(vertex1, vertex2);
oSurface.DeleteLine(edge);
oSurface.DeleteLines(edgeCollection);
```

## Grid Point Manipulation

```csharp
GridSurface gridSurface = surfaceId.GetObject(OpenMode.ForWrite) as GridSurface;

// Add/modify points
gridSurface.AddPoint(new GridLocation(row, col), elevation);
gridSurface.SetPointElevation(new GridLocation(row, col), newElevation);
gridSurface.RaisePoints(locations, deltaElevation);

// Delete points
gridSurface.DeletePoint(new GridLocation(row, col));
gridSurface.DeletePoints(locationCollection);
```

## Sampling Elevations

```csharp
// Sample elevations along a line between two points
Point3dCollection pts = tinSurface.SampleElevations(pt1, pt2);

// Sample elevations along a curve entity
Point3dCollection pts = tinSurface.SampleElevations(curveObjectId);
```

## Surface Operations

```csharp
// Raise entire surface by a delta
oSurface.RaiseSurface(deltaElevation);

// Paste another surface onto this one
oSurface.PasteSurface(otherSurfaceId);

// Simplify surface (reduce triangles)
SurfaceSimplifyOptions opts = new SurfaceSimplifyOptions();
oSurface.SimplifySurface(opts);

// Minimize flat areas
SurfaceMinimizeFlatAreaOptions flatOpts = new SurfaceMinimizeFlatAreaOptions();
oSurface.MinimizeFlatAreas(flatOpts);

// Access operation history
SurfaceOperationCollection ops = oSurface.Operations;
```

## Exporting Surfaces

### Export to DEM

```csharp
// Basic export
oSurface.ExportToDEM(
    @"path\to\output.dem",
    "coordinateSystemCode",
    gridSpacing: 10.0,
    ExportDetermineElevationType.SampleSurfaceAtGridPoint);

// With custom null elevation
oSurface.ExportToDEM(
    @"path\to\output.dem",
    "coordinateSystemCode",
    gridSpacing: 10.0,
    ExportDetermineElevationType.Average,
    useCustomNullElevationation: true,
    customNullElevation: -9999.0f);
```

### ExportDetermineElevationType Values
- `SampleSurfaceAtGridPoint` - use the elevation at each grid point
- `Average` - average surrounding elevations

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

## 3D Solids from TIN Surface

```csharp
// Create solids at a fixed depth below the surface
ObjectIdCollection solidIds = tinSurface.CreateSolidsAtDepth(depth, "LayerName", penIndex);

// Create solids down to a fixed elevation
ObjectIdCollection solidIds = tinSurface.CreateSolidsAtFixedElevation(elevation, "LayerName", penIndex);

// Create solids between this surface and another surface
ObjectIdCollection solidIds = tinSurface.CreateSolidsAtSurface(bottomSurfaceId, "LayerName", penIndex);

// Each method has a ToFile variant that writes to a file instead
ObjectIdCollection solidIds = tinSurface.CreateSolidsAtDepthToFile(
    depth, "LayerName", penIndex, ref fileName);
```

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
- Surface must be rebuilt after boundary changes via API
- Wall breaklines cannot create perfectly vertical walls in TIN surfaces
- Contour altitude uses z-value of the FIRST point only, regardless of other vertices
- `CreateFromLandXML()` 3-parameter overload is deprecated since Civil 2022; use the 4-parameter overload specifying the LandXML surface name

## Related Skills

- `c3d-root-objects` - Accessing surfaces through CivilDocument
- `c3d-profiles` - Surface profiles along alignments
- `c3d-corridors` - Corridor surfaces
