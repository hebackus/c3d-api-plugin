---
name: c3d-featurelines
description: Feature lines - grading/standalone FeatureLine (DBObject) and corridor CorridorFeatureLine (computed), creation, elevation management, export
---

# Civil 3D Feature Lines

Use this skill when working with feature lines - creating standalone/grading feature lines, managing elevations and geometry, accessing corridor feature lines, or exporting corridor feature lines to other object types.

## Two Types of Feature Lines

Civil 3D has two distinct feature line types that share a name but differ fundamentally:

| Aspect | `FeatureLine` (Grading) | `CorridorFeatureLine` (Corridor) |
|--------|------------------------|----------------------------------|
| Base class | `Feature` : `Entity` (DBObject) | Corridor sub-object (not a DBObject) |
| Persistence | Stored in drawing, has ObjectId | Computed on corridor rebuild |
| Creation | `FeatureLine.Create()` from polyline | Automatic from assembly point codes |
| Visibility | Prospector > Sites > Feature Lines | Corridor > Baselines > Feature Lines |
| Editing | Direct point/elevation editing | Read-only (change assembly/corridor) |
| Namespace | `Autodesk.Civil.DatabaseServices` | `Autodesk.Civil.DatabaseServices` |

## Accessing Grading Feature Lines

```csharp
CivilDocument doc = CivilApplication.ActiveDocument;

// Siteless feature lines (not associated with any site)
ObjectIdCollection sitelessFLs = doc.GetSitelessFeatureLineIds();

// Feature lines within a specific site
foreach (ObjectId siteId in doc.GetSiteIds())
{
    Site site = ts.GetObject(siteId, OpenMode.ForRead) as Site;
    ObjectIdCollection siteFLs = site.GetFeatureLineIds();
    foreach (ObjectId flId in siteFLs)
    {
        FeatureLine fl = ts.GetObject(flId, OpenMode.ForRead) as FeatureLine;
        ed.WriteMessage("Feature Line: {0}, Length2D: {1:F2}\n",
            fl.Name, fl.Length2D);
    }
}
```

## Creating Feature Lines

Feature lines are created from existing geometry: `Line`, `Arc`, `Polyline`, `Polyline2d`, or `Polyline3d`.

```csharp
// Create from an existing polyline (siteless)
ObjectId flId = FeatureLine.Create("My Feature Line", polylineId);

// Create from an existing polyline (assigned to a site)
ObjectId flId = FeatureLine.Create("My Feature Line", polylineId, siteId);
```

### Practical Workflow: Draw Then Create

```csharp
// 1. Create a polyline in the drawing
using (Polyline pline = new Polyline())
{
    pline.AddVertexAt(0, new Point2d(0, 0), 0, 0, 0);
    pline.AddVertexAt(1, new Point2d(100, 0), 0, 0, 0);
    pline.AddVertexAt(2, new Point2d(200, 50), 0, 0, 0);

    BlockTableRecord btr = ts.GetObject(db.CurrentSpaceId,
        OpenMode.ForWrite) as BlockTableRecord;
    ObjectId plineId = btr.AppendEntity(pline);
    ts.AddNewlyCreatedDBObject(pline, true);

    // 2. Create feature line from the polyline
    ObjectId flId = FeatureLine.Create("Centerline FL", plineId);
}
```

## Properties

```csharp
FeatureLine fl = ts.GetObject(flId, OpenMode.ForRead) as FeatureLine;

// Geometry measurements
double len2d = fl.Length2D;           // 2D (plan) length
double len3d = fl.Length3D;           // 3D length accounting for elevation changes

// Grade info
double maxGrade = fl.MaxGrade;       // Maximum grade along the feature line
double minGrade = fl.MinGrade;       // Minimum grade along the feature line

// Elevation range
double maxElev = fl.MaxElevation;    // Highest point elevation
double minElev = fl.MinElevation;    // Lowest point elevation

// Point counts
int totalPts = fl.PointsCount;           // Total vertex count
int piPts = fl.PIPointsCount;            // PI (intersection) point count
int elevPts = fl.ElevationPointsCount;   // Elevation point count
int curves = fl.CurvesCount;             // Number of curve segments

// Associations
ObjectId siteId = fl.SiteId;                  // Site containing this FL (Null if siteless)
ObjectId surfId = fl.RelativeSurfaceId;       // Reference surface for relative elevations
fl.RelativeSurfaceId = newSurfaceId;          // Set reference surface

// Style (note: StyleId is set-only, use StyleName to read)
string styleName = fl.StyleName;
fl.StyleId = newStyleId;
fl.StyleName = "New Style";
```

## Getting Points

```csharp
// Get PI points (vertices that define the alignment path)
Point3dCollection piPoints = fl.GetPoints(FeatureLinePointType.PIPoint);

// Get elevation points (intermediate grade break points)
Point3dCollection elevPoints = fl.GetPoints(FeatureLinePointType.ElevationPoint);

// Get all points (PI + elevation points combined)
Point3dCollection allPoints = fl.GetPoints(FeatureLinePointType.AllPoints);

foreach (Point3d pt in allPoints)
{
    ed.WriteMessage("  ({0:F2}, {1:F2}, {2:F2})\n", pt.X, pt.Y, pt.Z);
}
```

## Elevation Management

### Set Point Elevation by Index

```csharp
FeatureLine fl = ts.GetObject(flId, OpenMode.ForWrite) as FeatureLine;

// Set elevation of the first point to 100.0
fl.SetPointElevation(0, 100.0);

// Set elevation of the last point
fl.SetPointElevation(fl.PointsCount - 1, 105.0);
```

### Assign Elevations from Surface

```csharp
// Drape feature line onto a surface
// bIncIntermediate = true inserts grade break points where FL crosses surface TIN edges
fl.AssignElevationsFromSurface(surfaceId, false);

// With intermediate grade breaks (more accurate but adds many points)
fl.AssignElevationsFromSurface(surfaceId, true);
```

### Relative Elevations

```csharp
// Check if a point's elevation is relative to a surface
bool isRelative = fl.IsElevationRelativeToSurface(point);

// Get relative elevation (offset from surface)
double relElev = fl.GetPointRelativeElevation(point);

// Set a point's elevation relative to a surface
// relative=true: elevation is offset from surface; false: absolute elevation
fl.SetPointRelativeElevation(point, true, 2.5);  // 2.5 above surface
```

## PI and Elevation Point Manipulation

Points are identified by `Point3d` coordinates, not by index.

### Elevation Points

```csharp
FeatureLine fl = ts.GetObject(flId, OpenMode.ForWrite) as FeatureLine;

// Insert a single elevation point
fl.InsertElevationPoint(new Point3d(50, 0, 102.0));

// Insert multiple elevation points at once
Point3dCollection pts = new Point3dCollection();
pts.Add(new Point3d(25, 0, 101.0));
pts.Add(new Point3d(75, 0, 103.0));
fl.InsertElevationPoints(pts);

// Delete a single elevation point
fl.DeleteElevationPoint(new Point3d(50, 0, 102.0));

// Delete multiple elevation points
fl.DeleteElevationPoints(pts);
```

### PI Points

```csharp
// Insert a new PI point (changes the horizontal path)
fl.InsertPIPoint(new Point3d(150, 25, 104.0));

// Delete a PI point
fl.DeletePIPoint(new Point3d(150, 25, 104.0));
```

## Grade and Geometry Analysis

All analysis methods take a `Point3d` that must lie on the feature line.

```csharp
Point3dCollection points = fl.GetPoints(FeatureLinePointType.AllPoints);
Point3d pt = points[1]; // second point

// Grade approaching this point (from previous point)
double gradeIn = fl.GetGradeInAtPoint(pt);

// Grade leaving this point (toward next point)
double gradeOut = fl.GetGradeOutAtPoint(pt);

// Deflection angle at this point (radians)
double deflection = fl.GetDeflectionAngleAtPoint(pt);

// 3D distance from start to this point
double dist3d = fl.Get3dDistanceAtPoint(pt);
```

## Segment Bulge and Curves

Bulge and curve operations use segment index (0-based).

```csharp
FeatureLine fl = ts.GetObject(flId, OpenMode.ForWrite) as FeatureLine;

// Get bulge of segment at index (0 = straight, nonzero = arc)
double bulge = fl.GetBulge(0);

// Set bulge of a segment (parameter named "bugle" in API — typo)
fl.SetBulge(0, 0.5);

// Get curve radius at a segment index (Civil 3D 2022.1+)
double radius = fl.GetCurveRadius(1);

// Set curve radius at a segment index (Civil 3D 2022.1+)
fl.SetCurveRadius(1, 50.0);
```

## Extending Feature Lines

```csharp
FeatureLine fl = ts.GetObject(flId, OpenMode.ForWrite) as FeatureLine;

// Extend with a fixed-length line from the start
fl.ExtendWithFixedLine(true, 25.0);   // extendFromStart=true, length=25

// Extend with a fixed-length line from the end
fl.ExtendWithFixedLine(false, 50.0);  // extendFromStart=false, length=50

// Extend to a target point (line)
fl.ExtendWithFixedLine(false, new Point3d(300, 0, 106.0));

// Extend with a curve through a second point to a target point
fl.ExtendWithFixedCurve(false, new Point3d(250, 10, 105.0),
    new Point3d(300, 0, 106.0));

// Extend with a curve to a target point (auto-tangent)
fl.ExtendWithFixedCurve(false, new Point3d(300, 0, 106.0));
```

## Site Management

Feature lines can live in a named site or be siteless. Sites enforce topology interactions between feature lines, alignments, and parcels within the same site.

```csharp
// Create a new site
ObjectId siteId = Site.Create(doc, "Grading Site");

// Get feature lines in a site
Site site = ts.GetObject(siteId, OpenMode.ForRead) as Site;
ObjectIdCollection flIds = site.GetFeatureLineIds();

// Move a feature line to a site (static method)
FeatureLine.MoveToSite(flId, siteId);

// Move a feature line out of any site (siteless)
FeatureLine.MoveToNoneSite(flId);
```

## Styles

```csharp
// Access feature line style collection
FeatureLineStyleCollection styles = doc.Styles.FeatureLineStyles;

// Create a new style
ObjectId styleId = styles.Add("My FL Style");
FeatureLineStyle style = ts.GetObject(styleId, OpenMode.ForWrite) as FeatureLineStyle;

// Display styles (plan and model views)
DisplayStyle planStyle = style.GetFeatureLineDisplayStylePlan();
DisplayStyle modelStyle = style.GetFeatureLineDisplayStyleModel();

// Profile view display styles (by component type)
DisplayStyle flProfile = style.GetDisplayStyleProfile(
    FeatureLineDisplayStyleProfileType.FeatureLine);
DisplayStyle beginVertex = style.GetDisplayStyleProfile(
    FeatureLineDisplayStyleProfileType.BeginningVertex);
DisplayStyle internalVertex = style.GetDisplayStyleProfile(
    FeatureLineDisplayStyleProfileType.InternalVertex);
DisplayStyle endVertex = style.GetDisplayStyleProfile(
    FeatureLineDisplayStyleProfileType.EndingVertex);

// Section marker display
DisplayStyle sectionMarker = style.GetSectionMarkerDisplayStyleSection();

// Marker styles for profile view vertices
style.ProfileBeginningVertexMarkerStyleId = markerStyleId;
style.ProfileInternalVertexMarkerStyleId = markerStyleId;
style.ProfileEndingVertexMarkerStyleId = markerStyleId;

// Section marker style
style.SectionMarkerStyleId = markerStyleId;

// Apply style to a feature line
FeatureLine fl = ts.GetObject(flId, OpenMode.ForWrite) as FeatureLine;
fl.StyleId = styleId;
```

## Corridor Feature Lines

Corridor feature lines are computed results connecting assembly points that share the same code name along a baseline. They are **not** DBObjects and cannot be edited directly.

### Accessing via Baseline

```csharp
Corridor corridor = ts.GetObject(corridorId, OpenMode.ForRead) as Corridor;

foreach (Baseline baseline in corridor.Baselines)
{
    // Main baseline feature lines
    BaselineFeatureLines mainBFL = baseline.MainBaselineFeatureLines;

    // Get all code names
    string[] codes = mainBFL.CodeNames();

    // Iterate by code
    foreach (FeatureLineCollection flCol in mainBFL.FeatureLineCollectionMap)
    {
        foreach (CorridorFeatureLine cfl in flCol)
        {
            ed.WriteMessage("Code: {0}, Points: {1}\n",
                cfl.CodeName, cfl.FeatureLinePoints.Count);
        }
    }

    // Access by code name directly
    FeatureLineCollection topFLs = mainBFL.FeatureLineCollectionMap["Top"];
    CorridorFeatureLine firstTop = topFLs[0];

    // Offset baseline feature lines
    foreach (BaselineFeatureLines obfl in baseline.OffsetBaselineFeatureLinesCol)
    {
        foreach (FeatureLineCollection flCol in obfl.FeatureLineCollectionMap)
        {
            foreach (CorridorFeatureLine cfl in flCol)
            {
                ed.WriteMessage("Offset FL: {0}\n", cfl.CodeName);
            }
        }
    }
}
```

### FeatureLineCollectionMap

```csharp
FeatureLineCollectionMap map = mainBFL.FeatureLineCollectionMap;

// Get all available code names
string[] codeNames = map.CodeNames();

// Access by code name
FeatureLineCollection flCol = map["ETW"];

// Access by index
FeatureLineCollection flCol2 = map[0];

// Count of code groups
int codeCount = map.Count;
```

### FeatureLineCollection Properties

```csharp
FeatureLineCollection flCol = map["Top"];

// Connect direction for this code's feature lines
FeatureLineConnectDirectionType dir = flCol.ConnectDirection;
flCol.ConnectDirection = FeatureLineConnectDirectionType.Outward;

// Whether to connect extra points between stations
bool connectExtra = flCol.IsConnectExtraPoints;
flCol.IsConnectExtraPoints = true;

// Code info (code name, connection, pay items)
FeatureLineCodeInfo codeInfo = flCol.FeatureLineCodeInfo;
string codeName = codeInfo.CodeName;
bool isConnected = codeInfo.IsConnected;
```

### FeatureLinePoint (Corridor)

```csharp
CorridorFeatureLine cfl = flCol[0];

foreach (FeatureLinePoint flPt in cfl.FeatureLinePoints)
{
    // 3D coordinates
    Point3d xyz = flPt.XYZ;

    // Station along baseline
    double station = flPt.Station;

    // Offset from baseline
    double offset = flPt.Offset;

    // Whether this is a break point (region boundary, etc.)
    bool isBreak = flPt.IsBreak;

    ed.WriteMessage("  Sta {0:F2}, Offset {1:F2}, Elev {2:F2}, Break: {3}\n",
        station, offset, xyz.Z, isBreak);
}
```

### Corridor Feature Line Style

```csharp
CorridorFeatureLine cfl = flCol[0];

// Get/set style (unlike grading FeatureLine, StyleId has both getter and setter)
ObjectId styleId = cfl.StyleId;
string styleName = cfl.StyleName;
cfl.StyleId = newStyleId;
cfl.StyleName = "New Style";

// Get parent corridor
ObjectId corrId = cfl.CorridorId;
```

## Exporting Corridor Feature Lines

Corridor feature lines can be exported to persistent drawing objects.

### Export as Polyline3d

```csharp
CorridorFeatureLine cfl = flCol[0];

// Export as Polyline3d collection (one per region, since Civil 3D 2014)
ObjectIdCollection pline3dIds = cfl.ExportAsPolyline3dCollection();
```

### Export as Grading Feature Line

```csharp
// Full control over export
GradingSmoothOption smoothOpt = new GradingSmoothOption(
    false,  // needSmooth (note: param named "isSoomth" in API)
    0.0,    // arcInclusionDistance
    0.0,    // weedingDistance
    0.0);   // horizDeviation

ObjectId gradingFLId = cfl.ExportAsGradingFeatureLine(
    siteId,             // destination site
    true,               // isDynamic (updates when corridor rebuilds)
    "Exported ETW",     // feature line name
    layerId,            // layer
    featureLineStyleId, // style
    smoothOpt);         // smoothing options

// Minimal overload (default name, layer, style)
ObjectId gradingFLId2 = cfl.ExportAsGradingFeatureLine(siteId, false);
```

### Export as Alignment

```csharp
ObjectId alignId = cfl.ExportAsAlignment(
    "ETW Alignment",         // alignment name
    siteId,                  // site (ObjectId.Null for siteless)
    layerId,                 // layer
    alignmentStyleId,        // alignment style
    labelSetId,              // label set style
    AlignmentType.Centerline // alignment type
);
```

### Export as Profile

```csharp
ObjectId profileId = cfl.ExportAsProfile(
    "ETW Profile",    // profile name
    alignmentId,      // parent alignment
    layerId,          // layer
    profileStyleId,   // profile style
    labelSetId        // profile label set style
);
```

## Enums

### FeatureLinePointType

Used with `FeatureLine.GetPoints()`:

| Value | Description |
|-------|-------------|
| `PIPoint` | PI (point of intersection) vertices that define the horizontal path |
| `ElevationPoint` | Intermediate elevation/grade break points |
| `AllPoints` | All points (PI + elevation combined) |

### FeatureLineConnectDirectionType

Used with `FeatureLineCollection.ConnectDirection`:

| Value | Description |
|-------|-------------|
| `Inward` | Connect feature line points inward toward baseline |
| `Outward` | Connect feature line points outward from baseline |

### FeatureLineDisplayStyleProfileType

Used with `FeatureLineStyle.GetDisplayStyleProfile()`:

| Value | Int | Description |
|-------|-----|-------------|
| `FeatureLine` | 0 | The feature line itself in profile view |
| `BeginningVertex` | 2 | Starting vertex marker |
| `InternalVertex` | 3 | Internal vertex markers |
| `EndingVertex` | 4 | Ending vertex marker |

Note: Values are non-sequential (0, 2, 3, 4 - no value 1).

### GradingSmoothOption

Struct used when exporting corridor feature lines as grading feature lines:

| Property | Type | Description |
|----------|------|-------------|
| `NeedSmooth` | `bool` | Whether to apply smoothing |
| `ArcInclusionDistance` | `double` | Arc inclusion distance for smoothing |
| `WeedingDistance` | `double` | Point weeding distance |
| `HorizDeviation` | `double` | Horizontal deviation tolerance |

## Gotchas

**Point manipulation uses Point3d, not index.** `InsertElevationPoint`, `DeleteElevationPoint`, `InsertPIPoint`, `DeletePIPoint` all take `Point3d` coordinates. Only `SetPointElevation` uses an integer index.

**`StyleId` has no getter on grading `FeatureLine`.** Use `StyleName` to read the current style. `CorridorFeatureLine.StyleId` has both getter and setter.

**`SetBulge` parameter is named "bugle" in the API.** This is a typo in the Civil 3D API source. The method works correctly despite the misspelling.

**`GradingSmoothOption` constructor parameter is named "isSoomth".** Another API typo. Use `NeedSmooth` property for clarity.

**No managed API to draw a feature line from scratch.** `FeatureLine.Create()` requires an existing `Line`, `Arc`, `Polyline`, `Polyline2d`, or `Polyline3d` as input. To create a feature line from arbitrary points, first create a polyline, then call `Create()`.

**`AssignElevationsFromSurface` with grade breaks inserts many points.** When `bIncIntermediate=true`, the method inserts elevation points at every TIN edge crossing. This can add hundreds of points on complex surfaces. Use `false` for simple draping.

**Site topology interactions.** Feature lines in a site interact topologically with alignments and parcels in the same site. Moving a feature line into a site may split parcels or create unexpected topology. Use siteless feature lines to avoid this.

**`FeatureLineDisplayStyleProfileType` enum is non-sequential.** Values are 0, 2, 3, 4 (no value 1). Do not iterate with a simple integer loop - use the named enum values.

## Related Skills

- `c3d-corridors` - Corridors that generate corridor feature lines
- `c3d-alignments` - Alignments used as corridor baselines; feature lines can export as alignments
- `c3d-profiles` - Feature lines can export as profiles
- `c3d-surfaces` - Surfaces used for elevation assignment and relative elevations
