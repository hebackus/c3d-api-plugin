---
name: c3d-grading
description: Grading groups, grading objects, grading criteria, feature line grading, daylight projections, volume calculation, and grading styles
---

# Civil 3D Grading

Use this skill when working with grading objects - creating grading groups, defining grading criteria, projecting feature lines to surfaces or elevations, computing daylight lines, and calculating grading volumes.

## Grading Object Model

```
Site
├── GradingGroup              - Container for related grading objects
│   ├── Grading               - Single grading projection from a footprint
│   └── Surface (automatic)   - TIN surface generated from grading objects
└── FeatureLine               - 3D polyline used as grading footprint
```

A **Grading** projects outward (or inward) from a **FeatureLine** footprint toward a target (surface, distance, elevation, or relative elevation) using a slope defined in a **GradingCriteria**. Gradings are organized into **GradingGroups**, which can automatically generate a TIN surface.

## Namespace References

```csharp
using Autodesk.Civil.ApplicationServices;
using Autodesk.Civil.DatabaseServices;
using Autodesk.Civil.DatabaseServices.Styles;
```

GradingCriteria and GradingCriteriaSet live in `Autodesk.Civil.DatabaseServices.Styles`. All other grading classes live in `Autodesk.Civil.DatabaseServices`.

## Accessing Grading Groups

```csharp
CivilDocument doc = CivilApplication.ActiveDocument;

// Get all grading group ObjectIds in the drawing
ObjectIdCollection gradingGroupIds = doc.GetGradingGroupIds();

foreach (ObjectId ggId in gradingGroupIds)
{
    GradingGroup gg = ts.GetObject(ggId, OpenMode.ForRead) as GradingGroup;
    ed.WriteMessage("Grading Group: {0}, Surface: {1}\n",
        gg.Name, gg.AutomaticSurfaceCreation ? "Auto" : "None");
}
```

## GradingGroup Properties

- Name (string, get/set) — group display name
- SiteId (ObjectId, get) — parent site
- SurfaceId (ObjectId, get) — associated TIN surface (if automatic surface creation is enabled)
- AutomaticSurfaceCreation (bool, get/set) — whether to auto-create a TIN surface from grading objects
- VolumeBaselineSurfaceId (ObjectId, get/set) — base surface for volume computation
- StyleId (ObjectId, get/set) — grading group style

## GradingGroup Methods

- GetGradingIds() → ObjectIdCollection — all grading ObjectIds in the group
- Update() → void — rebuild grading group and regenerate surface

## Creating a Grading Group

```csharp
CivilDocument doc = CivilApplication.ActiveDocument;

// Grading groups belong to a site - get or create a site first
ObjectId siteId = doc.GetSiteIds()[0];  // use existing site
Site site = ts.GetObject(siteId, OpenMode.ForWrite) as Site;

// Create a new grading group
ObjectId ggId = GradingGroup.Create(site.Id, "Parking Lot Grading");
GradingGroup gg = ts.GetObject(ggId, OpenMode.ForWrite) as GradingGroup;

// Enable automatic surface creation
gg.AutomaticSurfaceCreation = true;

// Set a volume baseline surface for cut/fill computation
gg.VolumeBaselineSurfaceId = existingSurfaceId;
```

## Feature Lines

Feature lines are 3D polylines that serve as grading footprints. They belong to a site and can have per-vertex elevations.

### Creating Feature Lines

```csharp
// Create from an existing polyline, arc, line, or 3D polyline
ObjectId flId = FeatureLine.Create(
    "MyFeatureLine",       // name
    polylineId,            // source entity ObjectId
    siteId);               // site ObjectId

// Create from a set of points
Point3dCollection points = new Point3dCollection();
points.Add(new Point3d(0, 0, 100));
points.Add(new Point3d(100, 0, 100));
points.Add(new Point3d(100, 100, 100));
points.Add(new Point3d(0, 100, 100));
ObjectId flId = FeatureLine.Create("Footprint", points, siteId);
```

### FeatureLine Properties

- Name (string, get/set) — display name
- SiteId (ObjectId, get) — parent site
- MaxElevation (double, get) — highest vertex elevation
- MinElevation (double, get) — lowest vertex elevation
- Length2D (double, get) — planimetric length
- Length3D (double, get) — 3D length including elevation changes
- StyleId (ObjectId, get/set) — feature line style

### FeatureLine Elevation Methods

```csharp
FeatureLine fl = ts.GetObject(flId, OpenMode.ForWrite) as FeatureLine;

// Set all vertex elevations from a surface
fl.SetElevationsFromSurface(surfaceId);

// Assign a constant elevation to the entire feature line
fl.AssignElevationsToVertices(105.0);

// Get the elevation at a specific station along the feature line
double elev = fl.GetElevationAtStation(50.0);

// Insert an elevation point at a station
fl.InsertElevationPoint(75.0);  // station

// Get all points (geometry + elevation points)
Point3dCollection pts = fl.GetPoints(FeatureLinePointType.AllPoints);

// Get only PI (geometry) points
Point3dCollection piPts = fl.GetPoints(FeatureLinePointType.PIPoint);

// Get only elevation points
Point3dCollection elevPts = fl.GetPoints(FeatureLinePointType.ElevationPoint);

// Set elevation at a specific point
fl.SetPointElevation(pointIndex, 102.5);

// Raise/lower entire feature line by a delta
fl.RaiseElevations(2.0);   // raise by 2 feet
fl.RaiseElevations(-1.5);  // lower by 1.5 feet
```

### FeatureLinePointType Values
- `AllPoints` — all geometry and elevation points
- `PIPoint` — point of intersection (geometry vertices)
- `ElevationPoint` — manually inserted elevation points

## Grading Criteria

Grading criteria define the projection rule: target type, slope format, cut/fill slopes, and search order. They are style objects stored in criteria sets.

### GradingCriteria Properties

- Target (GradingTargetType, get/set) — projection target type (must be set before CutSlope/FillSlope)
- SearchOrder (GradingSearchOrderType, get/set) — cut-first or fill-first
- Slope (double, get/set) — slope value when Target is Distance or Elevation
- CutSlope (double, get/set) — slope for cut condition (when Target is Surface)
- FillSlope (double, get/set) — slope for fill condition (when Target is Surface)
- SlopeFormatType (GradingSlopeFormatType, get/set) — how slope values are expressed
- Distance (double, get/set) — target distance (when Target is Distance)
- RelativeElevation (double, get/set) — elevation offset (when Target is RelativeElevation)
- InteriorCornerOverlap (GradingInteriorCornerOverlapType, get/set) — interior corner handling

### GradingTargetType Values
- `Surface` — project to a target surface (daylight)
- `Distance` — project a fixed horizontal distance
- `Elevation` — project to an absolute elevation
- `RelativeElevation` — project to an elevation relative to the footprint

### GradingSlopeFormatType Values
- `Grade` -- slope as a percentage (e.g., 2.0 = 2%)
- `SlopeRatio` -- slope as a ratio (e.g., 3.0 = 3:1)
- `RiseRun` -- slope as rise over run

### GradingSearchOrderType Values
- `CutFirst` -- test for cut condition before fill
- `FillFirst` -- test for fill condition before cut

### Accessing and Configuring Criteria

```csharp
CivilDocument doc = CivilApplication.ActiveDocument;

// Access grading criteria sets from styles
ObjectIdCollection criteriaSetIds = doc.Styles.GradingCriteriaSetStyles;
GradingCriteriaSet criteriaSet = ts.GetObject(
    criteriaSetIds[0], OpenMode.ForRead) as GradingCriteriaSet;

// Iterate criteria in the set
foreach (ObjectId criteriaId in criteriaSet)
{
    GradingCriteria criteria = ts.GetObject(
        criteriaId, OpenMode.ForRead) as GradingCriteria;
    ed.WriteMessage("Criteria: {0}, Target: {1}\n",
        criteria.Name, criteria.Target);
}
```

### Creating Grading Criteria

```csharp
// Get or create a criteria set
ObjectId csId = doc.Styles.GradingCriteriaSetStyles.Add("Site Criteria");
GradingCriteriaSet criteriaSet = ts.GetObject(csId, OpenMode.ForWrite) as GradingCriteriaSet;

// Add a new criteria to the set
ObjectId critId = criteriaSet.Add("3:1 to Surface");
GradingCriteria criteria = ts.GetObject(critId, OpenMode.ForWrite) as GradingCriteria;

// Configure as daylight to surface with 3:1 slopes
// IMPORTANT: Set Target first, before CutSlope/FillSlope
criteria.Target = GradingTargetType.Surface;
criteria.SearchOrder = GradingSearchOrderType.CutFirst;
criteria.SlopeFormatType = GradingSlopeFormatType.SlopeRatio;
criteria.CutSlope = 3.0;   // 3:1 cut
criteria.FillSlope = 3.0;  // 3:1 fill
```

### Distance-Based Criteria

```csharp
ObjectId critId = criteriaSet.Add("10ft at 2%");
GradingCriteria criteria = ts.GetObject(critId, OpenMode.ForWrite) as GradingCriteria;

criteria.Target = GradingTargetType.Distance;
criteria.SlopeFormatType = GradingSlopeFormatType.Grade;
criteria.Slope = -2.0;      // 2% downward grade
criteria.Distance = 10.0;   // 10-foot projection
```

### Relative Elevation Criteria

```csharp
ObjectId critId = criteriaSet.Add("Drop 3ft at 4:1");
GradingCriteria criteria = ts.GetObject(critId, OpenMode.ForWrite) as GradingCriteria;

criteria.Target = GradingTargetType.RelativeElevation;
criteria.SlopeFormatType = GradingSlopeFormatType.SlopeRatio;
criteria.Slope = 4.0;              // 4:1
criteria.RelativeElevation = -3.0; // 3 feet below footprint
```

## Creating Gradings

A grading projects from a feature line footprint using a grading criteria.

```csharp
// Create a grading in a grading group from a feature line
Grading grading = Grading.Create(
    gradingGroupId,    // parent grading group ObjectId
    featureLineId,     // footprint feature line ObjectId
    criteriaId,        // grading criteria ObjectId
    targetSurfaceId,   // target surface (for daylight; ObjectId.Null for non-surface targets)
    true);             // grade to exterior (true) or interior (false)
```

### Grading Properties

- GradingGroupId (ObjectId, get) -- parent grading group
- FeatureLineId (ObjectId, get) -- footprint feature line
- GradingCriteriaId (ObjectId, get/set) -- the criteria used for projection
- TargetSurfaceId (ObjectId, get/set) -- target surface for daylight grading
- IsExterior (bool, get) -- whether grading projects outward

### Updating Gradings

```csharp
Grading grading = ts.GetObject(gradingId, OpenMode.ForWrite) as Grading;

// Change criteria
grading.GradingCriteriaId = newCriteriaId;

// Change target surface
grading.TargetSurfaceId = newSurfaceId;

// Rebuild the grading group after changes
GradingGroup gg = ts.GetObject(grading.GradingGroupId, OpenMode.ForWrite) as GradingGroup;
gg.Update();
```

## Daylight Grading (Surface Target)

Daylight grading projects from a feature line to an existing ground surface. The projection follows cut and fill slopes until it intersects the target surface.

```csharp
// 1. Create or access the existing ground surface
ObjectId existingGroundId = doc.GetSurfaceIds()[0];

// 2. Create a feature line for the design edge (e.g., top of slope)
Point3dCollection pts = new Point3dCollection();
pts.Add(new Point3d(1000, 1000, 105));
pts.Add(new Point3d(1200, 1000, 105));
pts.Add(new Point3d(1200, 1200, 105));
ObjectId flId = FeatureLine.Create("Design Edge", pts, siteId);

// 3. Set up daylight criteria (2:1 cut, 3:1 fill)
ObjectId csId = doc.Styles.GradingCriteriaSetStyles.Add("Daylight Set");
GradingCriteriaSet cs = ts.GetObject(csId, OpenMode.ForWrite) as GradingCriteriaSet;
ObjectId critId = cs.Add("Daylight 2:1/3:1");
GradingCriteria crit = ts.GetObject(critId, OpenMode.ForWrite) as GradingCriteria;
crit.Target = GradingTargetType.Surface;
crit.SearchOrder = GradingSearchOrderType.CutFirst;
crit.SlopeFormatType = GradingSlopeFormatType.SlopeRatio;
crit.CutSlope = 2.0;
crit.FillSlope = 3.0;

// 4. Create grading group and grading
ObjectId ggId = GradingGroup.Create(siteId, "Daylight Grading");
GradingGroup gg = ts.GetObject(ggId, OpenMode.ForWrite) as GradingGroup;
gg.AutomaticSurfaceCreation = true;

Grading grading = Grading.Create(ggId, flId, critId, existingGroundId, true);

// 5. Rebuild
gg.Update();
```

## Volume Calculation

### Volume via Grading Group

When a grading group has `AutomaticSurfaceCreation` enabled and a `VolumeBaselineSurfaceId` set, Civil 3D computes cut/fill volumes between the grading surface and the baseline surface.

```csharp
GradingGroup gg = ts.GetObject(ggId, OpenMode.ForRead) as GradingGroup;

// Ensure volume baseline is set
if (gg.VolumeBaselineSurfaceId != ObjectId.Null)
{
    // Access the grading group's auto-generated surface
    ObjectId gradingSurfaceId = gg.SurfaceId;

    // Create a TIN volume surface for precise computation
    ObjectId volSurfId = TinVolumeSurface.Create(
        "Grading Volumes",
        gg.VolumeBaselineSurfaceId,   // base (existing ground)
        gradingSurfaceId,              // comparison (grading surface)
        doc.Styles.SurfaceStyles[0]);

    TinVolumeSurface volSurf = ts.GetObject(
        volSurfId, OpenMode.ForRead) as TinVolumeSurface;
    VolumeSurfaceProperties volProps = volSurf.GetVolumeProperties();

    ed.WriteMessage("Cut: {0:F2} cu.yd, Fill: {1:F2} cu.yd, Net: {2:F2} cu.yd\n",
        volProps.AdjustedCutVolume / 27.0,
        volProps.AdjustedFillVolume / 27.0,
        volProps.AdjustedNetVolume / 27.0);
}
```

### Bounded Volume on Any Surface

```csharp
// Calculate volumes within a polygon region
TinSurface surface = ts.GetObject(surfaceId, OpenMode.ForRead) as TinSurface;

Point3dCollection boundary = new Point3dCollection();
boundary.Add(new Point3d(x1, y1, 0));
boundary.Add(new Point3d(x2, y2, 0));
boundary.Add(new Point3d(x3, y3, 0));

SurfaceVolumeInfo volInfo = surface.GetBoundedVolumes(boundary, datumElevation);
ed.WriteMessage("Cut: {0:F2}, Fill: {1:F2}\n", volInfo.Cut, volInfo.Fill);
```

### Volume Surface with Cut/Fill Factors

```csharp
TinVolumeSurface volSurf = ts.GetObject(volSurfId, OpenMode.ForWrite) as TinVolumeSurface;
volSurf.CutFactor = 1.0;    // no swell
volSurf.FillFactor = 1.15;  // 15% compaction factor
VolumeSurfaceProperties props = volSurf.GetVolumeProperties();
// props.AdjustedCutVolume, AdjustedFillVolume reflect factors
```

## Gotchas

- **Set Target before slopes.** You must set `GradingCriteria.Target` before accessing `CutSlope`, `FillSlope`, or `Slope`. Setting slopes before target causes unexpected behavior or exceptions.
- **Grading groups require a site.** Unlike corridors, grading groups and feature lines must belong to a `Site`. You cannot create them without a valid site.
- **Call Update() after changes.** After modifying grading criteria, feature line elevations, or adding/removing gradings, call `GradingGroup.Update()` to rebuild the surface.
- **Feature line elevation assignment order matters.** `SetElevationsFromSurface()` overwrites all vertex elevations. If you need to override specific vertices afterward, call `SetPointElevation()` after the surface assignment.
- **Volume units are cubic feet (imperial).** The API returns volume values in cubic drawing units. Divide by 27 to convert cubic feet to cubic yards.
- **Interior vs exterior grading.** The `isExterior` parameter in `Grading.Create()` controls projection direction. Exterior projects outward from the footprint; interior projects inward (e.g., pond or ditch).
- **Overlapping gradings in a group.** When multiple gradings in the same group overlap, the surface generation resolves conflicts. Ensure footprints do not create contradictory projections.
- **Grading creation may require COM for older versions.** Some older Civil 3D versions have limited .NET grading creation support. If `Grading.Create()` is unavailable, use the COM `IAeccGradingGroup` interface as a fallback.

## Related Skills

- `c3d-surfaces` -- TIN surfaces, volume surfaces, and bounded volume queries
- `c3d-corridors` -- Corridor feature lines and corridor surfaces
- `c3d-alignments` -- Alignments that can define grading footprint geometry
- `c3d-root-objects` -- CivilDocument, sites, and top-level object access
