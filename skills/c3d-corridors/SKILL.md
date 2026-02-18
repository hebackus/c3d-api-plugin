---
name: c3d-corridors
description: Corridors, baselines, baseline regions, assemblies, subassemblies, feature lines, corridor surfaces, and styles
---

# Civil 3D Corridors

Use this skill when working with corridors - creating, listing, accessing baselines, assemblies, feature lines, corridor surfaces, and styles.

## Corridor Overview

A corridor represents a path (road, trail, railroad). Its geometry is defined by:
- **Baseline** = alignment (horizontal) + profile (vertical) = 3D centerline
- **Assemblies** = cross-sectional shapes placed at stations along baselines
- **Feature lines** = connecting common points in assemblies along the baseline
- **Corridor surfaces** = surfaces representing the finished roadway

## Creating Corridors

```csharp
CivilDocument doc = CivilApplication.ActiveDocument;

// Create an empty corridor
ObjectId corridorId = doc.CorridorCollection.Add("My Corridor");

// Create with baseline from alignment + profile
ObjectId corridorId2 = doc.CorridorCollection.Add(
    "Road Corridor",       // corridor name
    "Centerline",          // baseline name
    alignmentId,           // alignment ObjectId
    profileId);            // profile ObjectId

// Create with baseline, region, and assembly in one call
ObjectId corridorId3 = doc.CorridorCollection.Add(
    "Full Corridor",       // corridor name
    "Centerline",          // baseline name
    alignmentId,           // alignment ObjectId
    profileId,             // profile ObjectId
    "Region 1",            // baseline region name
    assemblyId);           // assembly ObjectId

// Create from a feature line
ObjectId corridorId4 = doc.CorridorCollection.Add(
    "FL Corridor",         // corridor name
    "Baseline",            // baseline name
    featureLineId);        // feature line ObjectId

// Rebuild all corridors
doc.CorridorCollection.RebuildAll();
```

## Listing Corridors

```csharp
CivilDocument doc = CivilApplication.ActiveDocument;

foreach (ObjectId objId in doc.CorridorCollection)
{
    Corridor corridor = ts.GetObject(objId, OpenMode.ForRead) as Corridor;
    ed.WriteMessage("Corridor: {0}, Max triangle side: {1}\n",
        corridor.Name, corridor.MaximumTriangleSideLength);
}
```

## Corridor Properties and Methods

```csharp
Corridor corridor = ts.GetObject(corridorId, OpenMode.ForWrite) as Corridor;

// Check if corridor needs rebuilding
bool outOfDate = corridor.IsOutOfDate;

// Control automatic rebuilding
corridor.RebuildAutomatic = true;

// Manually rebuild
corridor.Rebuild();

// Get/set code set style
corridor.CodeSetStyleId = newCodeSetStyleId;
corridor.CodeSetStyleName = "My Code Set Style";

// Get/set max triangle side length
corridor.MaximumTriangleSideLength = 50.0;

// Region lock mode
corridor.RegionLockMode = CorridorRegionLockType.LockAllRegions;

// Get all point/link/shape codes used in the corridor
string[] pointCodes = corridor.GetPointCodes();
string[] linkCodes = corridor.GetLinkCodes();
string[] shapeCodes = corridor.GetShapeCodes();

// Get/set subassembly targets (surfaces, alignments, profiles)
SubassemblyTargetInfoCollection targets = corridor.GetTargets();
corridor.SetTargets(targets);

// Export corridor solids to 3D solids
ExportCorridorSolidsParams solidParams = new ExportCorridorSolidsParams();
ObjectIdCollection solidIds = corridor.ExportSolids(solidParams, db);

// Export feature lines as COGO points
ObjectId pointGroupId = corridor.ExportFeatureLinesAsCogoPoints(
    "Corridor Points", codes);
```

## Corridor Ambient Settings

```csharp
SettingsCorridor corridorSettings =
    doc.Settings.GetFeatureSettings<SettingsCorridor>() as SettingsCorridor;

// Name format templates
corridorSettings.NameFormat.Corridor.Value =
    "Corridor <[Next Counter(CP)]> (<[Corridor First Assembly(CP)]>)";

// Default styles
corridorSettings.Styles.Alignment.Value = alignmentStyleName;
```

### Name Format Property Fields

| Format | Available Fields |
|--------|-----------------|
| Corridor | `<[Corridor First Assembly(CP)]>`, `<[Corridor First Baseline(CP)]>`, `<[Corridor First Profile(CP)]>`, `<[Next Counter(CP)]>` |
| Corridor Surface | `<[Corridor Name(CP)]>`, `<[Next Corridor Surface Counter(CP)]>` |
| Profile From Feature Line | `<[Next Counter(CP)]>` |
| Alignment From Feature Line | `<[Corridor Baseline Name(CP)]>`, `<[Corridor Feature Code(CP)]>`, `<[Corridor Name(CP)]>`, `<[Next Counter(CP)]>`, `<[Profile Type]>` |

## Baselines

A baseline = alignment + profile. A corridor can have multiple baselines (e.g., for intersections).

### Reading Baselines

```csharp
foreach (Baseline baseline in corridor.Baselines)
{
    Alignment align = ts.GetObject(baseline.AlignmentId, OpenMode.ForRead) as Alignment;
    Profile profile = ts.GetObject(baseline.ProfileId, OpenMode.ForRead) as Profile;

    ed.WriteMessage("Baseline - Alignment: {0}, Profile: {1}\n",
        align.Name, profile.Name);
    ed.WriteMessage("  Start: {0}, End: {1}\n",
        baseline.StartStation, baseline.EndStation);
}
```

### Adding and Removing Baselines

```csharp
Corridor corridor = ts.GetObject(corridorId, OpenMode.ForWrite) as Corridor;

// Add baseline from alignment + profile (by ObjectId)
Baseline newBaseline = corridor.Baselines.Add(
    "Second Baseline", alignmentId, profileId);

// Add baseline from alignment + profile (by name)
Baseline newBaseline2 = corridor.Baselines.Add(
    "Third Baseline", "Alignment - (2)", "Profile - (1)");

// Add baseline from a feature line
Baseline flBaseline = corridor.Baselines.Add(
    "FL Baseline", featureLineId);

// Remove a baseline
corridor.Baselines.Remove(newBaseline);
corridor.Baselines.Remove("Third Baseline");
corridor.Baselines.RemoveAt(0);

// Access baselines by index, name, or GUID
Baseline bl = corridor.Baselines[0];
Baseline bl2 = corridor.Baselines["Centerline"];
```

## Baseline Regions

Each baseline has regions, each with its own assembly (cross-section shape).

### Reading Regions

```csharp
foreach (BaselineRegion region in baseline.BaselineRegions)
{
    ed.WriteMessage("Region: {0}, Start {1}, End {2}\n",
        region.Name, region.StartStation, region.EndStation);
}
```

### Creating and Modifying Regions

```csharp
// Add a region with assembly and station range
BaselineRegion newRegion = baseline.BaselineRegions.Add(
    "Region 1", assemblyId, 0.0, 500.0);

// Add a region with assembly (by name), full baseline extent
BaselineRegion newRegion2 = baseline.BaselineRegions.Add(
    "Region 2", "Assembly - (1)");

// Modify region properties
newRegion.StartStation = 100.0;
newRegion.EndStation = 400.0;
newRegion.AssemblyId = differentAssemblyId;
newRegion.Name = "Modified Region";

// Split a region at a station (returns the new second region)
BaselineRegion secondHalf = newRegion.Split(250.0);

// Match region settings from another region
newRegion.Match(sourceRegion, RegionMatchType.All);

// Merge consecutive regions
newRegion.Merge(firstRegion, lastRegion);

// Remove regions
baseline.BaselineRegions.Remove(newRegion);
baseline.BaselineRegions.Remove("Region 2");
baseline.BaselineRegions.RemoveAt(0);

// Get/set subassembly targets per region
SubassemblyTargetInfoCollection regionTargets = newRegion.GetTargets();
newRegion.SetTargets(regionTargets);

// Export region solids
ObjectIdCollection solids = newRegion.ExportSolids(
    solidParams, startStation, endStation, targetDb);
```

### Stations in Regions

```csharp
// Get all stations in a region
double[] stations = region.SortedStations();

// Add a station
double midStation = region.StartStation +
    ((region.EndStation - region.StartStation) / 2);
region.AddStation(midStation, "New Station");

// Delete a station (with optional tolerance)
region.DeleteStation(region.StartStation);

// Get added stations
double[] addedStations = region.AdditionalStations();

// Clear all added stations
region.ClearAdditionalStations();

// Get overridden stations
OverriddenStationInfo[] overridden = region.GetOverriddenStations();

// Remove a specific overridden station
region.RemoveOverriddenStation(150.0);
```

## Offset Baselines

Secondary baselines offset from the main baseline within a region:

```csharp
foreach (BaseBaseline ob in region.OffsetBaselines)
{
    switch (ob.BaselineType)
    {
        case CorridorBaselineType.OffsetBaseline:
            OffsetBaseline offb = (OffsetBaseline)ob;
            // Variable offset from main baseline
            var startOffset = offb.GetOffsetElevationFromMainBaselineStation(
                offb.StartStationOnMainBaseline);
            // startOffset.X = horizontal offset, startOffset.Y = vertical offset
            break;

        case CorridorBaselineType.HardcodedOffsetBaseline:
            HardcodedOffsetBaseline hob = (HardcodedOffsetBaseline)ob;
            // Constant offset
            // hob.OffsetElevationFromMainBaseline.X/Y
            break;
    }
}
```


## Assemblies

An assembly defines the cross-section template used along a corridor baseline.

### Creating Assemblies

```csharp
CivilDocument doc = CivilApplication.ActiveDocument;

// Create a new assembly at a location
ObjectId assemblyId = doc.AssemblyCollection.Add(
    "My Assembly",
    AssemblyType.Other,
    new Point3d(0, 0, 0));

// Create with explicit style and code set style
ObjectId assemblyId2 = doc.AssemblyCollection.Add(
    "Styled Assembly",
    AssemblyType.Other,
    new Point3d(100, 0, 0),
    assemblyStyleId,
    codeSetStyleId);

// Import assembly from another drawing's database
ObjectId imported = doc.AssemblyCollection.ImportAssembly(
    "Imported Assembly",
    sourceDatabase,
    "Source Assembly Name",
    new Point3d(200, 0, 0));

// Import assembly from an ATC (tool catalog) file
ObjectId fromCatalog = doc.AssemblyCollection.ImportAssembly(
    "Catalog Assembly",
    @"C:\path\to\catalog.atc",
    itemId,
    new Point3d(300, 0, 0));
```

### Modifying Assemblies

```csharp
Assembly assembly = ts.GetObject(assemblyId, OpenMode.ForWrite) as Assembly;

// Set properties
assembly.Location = new Point3d(50, 50, 0);
assembly.Type = AssemblyType.Other;
assembly.CodeSetStyleId = newCodeSetStyleId;

// Add a subassembly (auto-placed)
AssemblyGroup group = assembly.AddSubassembly(subassemblyId);

// Add a subassembly at a specific hook point
assembly.AddSubassembly(subassemblyId, hookPoint);

// Replace one subassembly with another
assembly.ReplaceSubassembly(newSubassemblyId, targetSubassemblyId);

// Insert before/after existing subassemblies
assembly.InsertSubassemblyBefore(newSubassemblyId, targetSubassemblyId);
assembly.InsertSubassemblyAfter(newSubassemblyId, hookPoint);

// Copy a subassembly (auto-placed or at hook point)
AssemblyGroup copiedGroup = assembly.CopySubassembly(sourceSubassemblyId);
ObjectId copiedId = assembly.CopySubassembly(sourceSubassemblyId, hookPoint);

// Mirror a subassembly
AssemblyGroup mirroredGroup = assembly.MirrorSubassembly(sourceSubassemblyId);
ObjectId mirroredId = assembly.MirrorSubassembly(sourceSubassemblyId, hookPoint);

// Access assembly groups
AssemblyGroupCollection groups = assembly.Groups;

// Get offset baseline names
string[] offsetNames = assembly.GetOffsetBaselineNames();
```

### Applied Assemblies (Corridor Results)

When an assembly is placed along a corridor, it becomes an `AppliedAssembly` containing `CalculatedShape`, `CalculatedLink`, and `CalculatedPoint`.

```csharp
foreach (AppliedAssembly appliedAsm in region.AppliedAssemblies)
{
    ed.WriteMessage("Assembly - Shapes: {0}, Links: {1}, Points: {2}\n",
        appliedAsm.Shapes.Count, appliedAsm.Links.Count, appliedAsm.Points.Count);

    // Point positions (station, offset, elevation to baseline)
    foreach (CalculatedPoint point in appliedAsm.Points)
    {
        ed.WriteMessage("  Point: Station {0}, Offset {1}, Elev {2}\n",
            point.StationOffsetElevationToBaseline.X,
            point.StationOffsetElevationToBaseline.Y,
            point.StationOffsetElevationToBaseline.Z);
    }
}
```

### Applied Subassemblies

```csharp
foreach (AppliedSubassembly appliedSub in appliedAsm.GetAppliedSubassemblies())
{
    ed.WriteMessage("Subassembly origin: Station {0}, Offset {1}, Elev {2}\n",
        appliedSub.OriginStationOffsetElevationToBaseline.X,
        appliedSub.OriginStationOffsetElevationToBaseline.Y,
        appliedSub.OriginStationOffsetElevationToBaseline.Z);

    // Get archetype subassembly info
    Subassembly sub = ts.GetObject(appliedSub.SubassemblyId,
        OpenMode.ForRead) as Subassembly;
    ed.WriteMessage("  Template: {0}\n", sub.Name);
}
```

### Calculated Elements Structure

```
AppliedAssembly
+-- Shapes (CalculatedShape)
|     +-- Links (collection of CalculatedLink)
+-- Links (CalculatedLink)
|     +-- Points (collection of CalculatedPoint)
+-- Points (CalculatedPoint)
|     +-- StationOffsetElevationToBaseline (Point3d: X=station, Y=offset, Z=elevation)
|     +-- CorridorCodes (string[])
+-- AppliedSubassemblies
      +-- (each has its own Shapes, Links, Points)
```

## Feature Lines

Feature lines connect related points (sharing a common code) along the baseline.

### Along Main Baseline

```csharp
foreach (FeatureLineCollection flCol in
    baseline.MainBaselineFeatureLines.FeatureLineCollectionMap)
{
    foreach (FeatureLine fl in flCol)
    {
        ed.WriteMessage("Feature line code: {0}\n", fl.CodeName);
        foreach (FeatureLinePoint flPoint in fl.FeatureLinePoints)
        {
            ed.WriteMessage("  Point: {0}, {1}, {2}\n",
                flPoint.XYZ.X, flPoint.XYZ.Y, flPoint.XYZ.Z);
        }
    }
}
```

### Along Offset Baselines

```csharp
foreach (BaselineFeatureLines bfl in baseline.OffsetBaselineFeatureLinesCol)
{
    foreach (FeatureLineCollection flCol in bfl.FeatureLineCollectionMap)
    {
        foreach (FeatureLine fl in flCol)
        {
            ed.WriteMessage("Offset feature line: {0}\n", fl.CodeName);
        }
    }
}
```

Offset baselines also have `RelatedOffsetBaselineFeatureLines` for direct access.

## Corridor Surfaces

### Reading Corridor Surfaces

```csharp
foreach (CorridorSurface cSurface in corridor.CorridorSurfaces)
{
    ed.WriteMessage("Surface: {0}\n", cSurface.Name);

    // Point codes that make up the surface
    string[] pointCodes = cSurface.PointCodes();
    foreach (string code in pointCodes)
        ed.WriteMessage("  Code: {0}\n", code);
}
```

### Creating and Managing Corridor Surfaces

```csharp
Corridor corridor = ts.GetObject(corridorId, OpenMode.ForWrite) as Corridor;

// Create a corridor surface
CorridorSurface newSurface = corridor.CorridorSurfaces.Add("Top Surface");

// Create with a surface style
CorridorSurface styledSurface = corridor.CorridorSurfaces.Add(
    "Datum Surface", surfaceStyleId);

// Add link codes to define what builds the surface
newSurface.AddLinkCode("Top", true);    // true = add as breakline
newSurface.AddLinkCode("Datum", false);

// Add feature line codes
newSurface.AddFeatureLineCode("Top");

// Remove codes
newSurface.RemoveLinkCode("Datum");
newSurface.RemoveFeatureLineCode("Top");

// Check/set link code as breakline
bool isBreak = newSurface.IsLinkCodeAsBreakLine("Top");
newSurface.SetLinkCodeAsBreakLine("Top", true);

// Query the surface
string[] linkCodes = newSurface.LinkCodes();
string[] featureCodes = newSurface.FeatureLineCodes();

// Set surface properties
newSurface.Name = "Renamed Surface";
newSurface.Description = "Top of corridor";
newSurface.SurfaceStyleId = surfaceStyleId;
newSurface.RenderMaterialId = materialId;
newSurface.OverhangCorrection = OverhangCorrectionType.None;
newSurface.IsBuild = true;

// Get the underlying TIN surface ObjectId
ObjectId tinSurfaceId = newSurface.SurfaceId;

// Find elevation at a point
double elev = newSurface.FindElevationAtXY(1000.0, 2000.0);

// Sample elevations along a line
Point3dCollection samples = newSurface.GetSampleElevations(
    startX, startY, endX, endY);

// Remove a corridor surface
corridor.CorridorSurfaces.Remove("Top Surface");
corridor.CorridorSurfaces.RemoveAt(0);
```

### Surface Boundaries

```csharp
CorridorSurfaceBoundaryCollection boundaries = cSurface.Boundaries;

// Add corridor extents boundary (automatic)
CorridorSurfaceBoundary extentsBoundary =
    boundaries.AddCorridorExtentsBoundary("Extents");

// Add boundary from a feature line code
CorridorSurfaceBoundary flBoundary =
    boundaries.Add("Daylight Boundary", "Daylight");

// Add boundary from a polyline
CorridorSurfaceBoundary polyBoundary =
    boundaries.Add("Custom Boundary", polylineId);

// Add boundary from points
Point3dCollection pts = new Point3dCollection();
pts.Add(new Point3d(0, 0, 0));
pts.Add(new Point3d(100, 0, 0));
pts.Add(new Point3d(100, 50, 0));
CorridorSurfaceBoundary ptsBoundary =
    boundaries.Add("Points Boundary", pts);

// Set boundary type
flBoundary.BoundaryType = CorridorSurfaceBoundaryType.OutsideBoundary;

// Read boundary info
foreach (CorridorSurfaceBoundary boundary in boundaries)
{
    string type = boundary.BoundaryType ==
        CorridorSurfaceBoundaryType.InsideBoundary ? "Inner" : "Outer";
    ed.WriteMessage("  {0} Boundary: {1}\n", type, boundary.Name);

    Point3d[] points = boundary.PolygonPoints();
    ed.WriteMessage("  Points: {0}\n", points.Length);

    // Feature line components
    foreach (FeatureLineComponent flc in boundary.FeatureLineComponents)
    {
        ed.WriteMessage("    Code: {0}, Start: {1}, End: {2}\n",
            flc.FeatureLine.CodeName,
            flc.StartStation, flc.EndStation);
    }
}

// Remove boundaries
boundaries.Remove("Custom Boundary");
boundaries.RemoveAt(0);
```

### Surface Masks

```csharp
CorridorSurfaceMaskCollection masks = cSurface.Masks;

// Add mask from a feature line code
CorridorSurfaceMask flMask = masks.Add("Median Mask", "Median");

// Add mask from a polyline
CorridorSurfaceMask polyMask = masks.Add("Custom Mask", polylineId);

// Add mask from points
CorridorSurfaceMask ptsMask = masks.Add("Points Mask", pointCollection);

// Remove masks
masks.Remove("Median Mask");
masks.RemoveAt(0);
```

## Styles

### Assembly Style

```csharp
ObjectId styleId = doc.Styles.AssemblyStyles.Add("My Assembly Style");
AssemblyStyle style = ts.GetObject(styleId, OpenMode.ForWrite) as AssemblyStyle;

ObjectId markerId = style.MarkerStyleAtMainBaselineId;
MarkerStyle marker = ts.GetObject(markerId, OpenMode.ForWrite) as MarkerStyle;
marker.CustomMarkerStyle = CustomMarkerType.CustomMarkerX;
```

### Link Style

```csharp
ObjectId linkStyleId = doc.Styles.LinkStyles.Add("My Link Style");
LinkStyle linkStyle = ts.GetObject(linkStyleId, OpenMode.ForWrite) as LinkStyle;
linkStyle.LinkDisplayStylePlan.Color = Color.FromColorIndex(ColorMethod.ByAci, 80);
```

### Shape Style

```csharp
ObjectId shapeStyleId = doc.Styles.ShapeStyles.Add("My Shape Style");
ShapeStyle shapeStyle = ts.GetObject(shapeStyleId, OpenMode.ForWrite) as ShapeStyle;
shapeStyle.AreaFillDisplayStylePlan.Color = Color.FromColorIndex(ColorMethod.ByAci, 50);
shapeStyle.BorderDisplayStylePlan.Color = Color.FromColorIndex(ColorMethod.ByAci, 30);
```

### Code Set Styles (Roadway Style Sets)

Maps corridor codes to link/shape styles:

```csharp
ObjectId cssId = doc.Styles.CodeSetStyles.Add("My Style Set");
CodeSetStyle css = ts.GetObject(cssId, OpenMode.ForWrite) as CodeSetStyle;
css.Add("TOP", doc.Styles.LinkStyles["My Link Style"]);
css.Add("BASE", doc.Styles.ShapeStyles["My Shape Style"]);

// Get current active style set
ObjectId currentId = CodeSetStyle.GetCurrentStyleSetId();

// Set code set style on a corridor
corridor.CodeSetStyleId = cssId;
corridor.CodeSetStyleName = "My Style Set";
```

## Gotchas

These are the most common pitfalls when working with corridors in the .NET API:

**Feature line polyline creation requires COM.** The .NET API provides no method to create a corridor feature line from a polyline. Use the COM interface `IAeccLandFeatureLine.AddFromPolyline()` instead. The managed `CorridorFeatureLine` class only supports reading feature lines and exporting them (to polyline, grading feature line, alignment, or profile).

**Cut/fill volume computation requires COM.** `CorridorSurface` exposes no managed method to compute cut/fill volumes between a corridor surface and a reference surface. Use COM API to access volume computation.

**Offset baselines require COM.** There is no managed API method to create offset baselines on a corridor. You can read existing offset baselines via `region.OffsetBaselines` and cast to `OffsetBaseline` or `HardcodedOffsetBaseline`, but creation must go through COM.

## .NET API Limitations Summary

| Feature | Supported? |
|---------|-----------|
| Create corridors | Yes |
| List/read corridors | Yes |
| Rebuild corridors | Yes |
| Add/remove baselines | Yes |
| Create/modify regions | Yes |
| Split/match/merge regions | Yes |
| Create/modify assemblies | Yes |
| Import assemblies | Yes |
| Add/delete stations | Yes |
| Read feature lines | Yes |
| Create feature lines from polylines | No (use COM) |
| Create/modify corridor surfaces | Yes |
| Add/remove boundaries | Yes |
| Add/remove masks | Yes |
| Query surface elevations | Yes |
| Export solids | Yes |
| Get/set targets | Yes |
| Set CodeSetStyle on corridor | Yes |
| Create offset baselines | No (use COM) |
| Compute cut/fill | No (use COM) |
| Create/modify styles | Yes |

## Related Skills

- `c3d-alignments` - Alignments used as corridor baselines
- `c3d-profiles` - Profiles used as corridor baselines
- `c3d-surfaces` - Surface objects vs corridor surfaces
- `c3d-custom-subassemblies` - Creating custom subassembly code
