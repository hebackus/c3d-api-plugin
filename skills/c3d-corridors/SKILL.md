---
name: c3d-corridors
description: Corridors, baselines, baseline regions, assemblies, subassemblies, feature lines, corridor surfaces, and styles
---

# Civil 3D Corridors

Use this skill when working with corridors - listing, accessing baselines, assemblies, feature lines, corridor surfaces, and styles.

## Corridor Overview

A corridor represents a path (road, trail, railroad). Its geometry is defined by:
- **Baseline** = alignment (horizontal) + profile (vertical) = 3D centerline
- **Assemblies** = cross-sectional shapes placed at stations along baselines
- **Feature lines** = connecting common points in assemblies along the baseline
- **Corridor surfaces** = surfaces representing the finished roadway

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

**Limitation:** You CANNOT create new corridors via the .NET API.

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

**Limitation:** You CANNOT add baselines to corridors via the .NET API.

## Baseline Regions

Each baseline has regions, each with its own assembly (cross-section shape).

```csharp
foreach (BaselineRegion region in baseline.BaselineRegions)
{
    ed.WriteMessage("Region: Start {0}, End {1}\n",
        region.StartStation, region.EndStation);
}
```

**Limitation:** Cannot create or modify baseline regions via .NET API.

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
var addedStations = region.GetAdditionalStation;

// Clear all added stations
region.ClearAdditionalStations();
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

**Limitation:** Cannot create offset baselines via .NET API.

## Assemblies and Applied Assemblies

An assembly defines the cross-section template. When placed along a corridor, it becomes an `AppliedAssembly` containing `CalculatedShape`, `CalculatedLink`, and `CalculatedPoint`.

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

**Limitation:** Cannot create or modify assemblies via .NET API.

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
├── Shapes (CalculatedShape)
│     └── Links (collection of CalculatedLink)
├── Links (CalculatedLink)
│     └── Points (collection of CalculatedPoint)
├── Points (CalculatedPoint)
│     ├── StationOffsetElevationToBaseline (Point3d: X=station, Y=offset, Z=elevation)
│     └── CorridorCodes (string[])
└── AppliedSubassemblies
      └── (each has its own Shapes, Links, Points)
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

**Limitation:** Creating feature lines from polylines is NOT supported in .NET. Use COM `IAeccLandFeatureLine.AddFromPolyline()`.

## Corridor Surfaces

```csharp
foreach (CorridorSurface cSurface in corridor.CorridorSurfaces)
{
    ed.WriteMessage("Surface: {0}\n", cSurface.Name);

    // Point codes that make up the surface
    string[] pointCodes = cSurface.PointCodes();
    foreach (string code in pointCodes)
        ed.WriteMessage("  Code: {0}\n", code);

    // Surface boundaries
    foreach (CorridorSurfaceBoundary boundary in cSurface.Boundaries)
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
}
```

**Limitations:**
- Cannot create corridor surfaces via .NET API
- Cannot modify corridor boundaries or masks via .NET API
- Cut/fill computation is NOT exposed in .NET - use COM API

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
```

**Note:** Link and shape styles are used with CodeSetStyles, not directly with link/shape objects.

## .NET API Limitations Summary

| Feature | Supported? |
|---------|-----------|
| List/read corridors | Yes |
| Create corridors | No |
| Add baselines | No |
| Create/modify regions | No |
| Create/modify assemblies | No |
| Add/delete stations | Yes |
| Read feature lines | Yes |
| Create feature lines from polylines | No (use COM) |
| Read corridor surfaces | Yes |
| Create/modify corridor surfaces | No |
| Create/modify boundaries/masks | No |
| Compute cut/fill | No (use COM) |
| Set CodeSetStyle as active | No (can read current) |
| Create/modify styles | Yes |

## Related Skills

- `c3d-alignments` - Alignments used as corridor baselines
- `c3d-profiles` - Profiles used as corridor baselines
- `c3d-surfaces` - Surface objects vs corridor surfaces
- `c3d-custom-subassemblies` - Creating custom subassembly code
