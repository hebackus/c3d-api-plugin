---
name: c3d-alignments
description: Alignment creation, entities, stations, station equations, design speeds, superelevation, and alignment styles
---

# Civil 3D Alignments

Use this skill when creating, modifying, or querying alignments, working with stations, or configuring superelevation.

## Alignment Collections

```csharp
// All alignments (siteless + sited)
ObjectIdCollection allAlignments = doc.GetAlignmentIds();

// Only siteless alignments
ObjectIdCollection sitelessAlignments = doc.GetSitelessAlignmentIds();
```

## Creating Alignments

### Empty Alignment (no geometry)

```csharp
// Overload 1: By name strings (pass "" for siteless)
ObjectId alignId = Alignment.Create(doc, "New Alignment",
    "",             // site name ("" = siteless)
    "0",            // layer name
    "Basic",        // alignment style name
    "AllLabels"     // label set style name
);

// Overload 2: By ObjectIds (pass ObjectId.Null for siteless)
ObjectId alignId = Alignment.Create(doc, "New Alignment",
    ObjectId.Null,  // siteId (Null = siteless)
    layerId,        // ObjectId of layer
    styleId,        // ObjectId of alignment style
    labelSetId      // ObjectId of label set style
);

// Overload 3: By ObjectIds with explicit AlignmentType
ObjectId alignId = Alignment.Create(doc, "New Alignment",
    ObjectId.Null, layerId, styleId, labelSetId,
    AlignmentType.Centerline
);
```

### From Polyline

```csharp
PromptEntityOptions opt = new PromptEntityOptions("\nSelect a polyline");
opt.SetRejectMessage("\nObject must be a polyline.");
opt.AddAllowedClass(typeof(Polyline), false);
PromptEntityResult res = ed.GetEntity(opt);

PolylineOptions plops = new PolylineOptions();
plops.AddCurvesBetweenTangents = true;
plops.EraseExistingEntities = true;
plops.PlineId = res.ObjectId;

// String overload
ObjectId alignId = Alignment.Create(doc, plops,
    "New Alignment", "MySite", "0", "Standard", "Standard");

// ObjectId overload
ObjectId alignId = Alignment.Create(doc, plops,
    "New Alignment", siteId, layerId, styleId, labelSetId);
```

### From Corridor Feature Line

```csharp
ObjectId alignId = Alignment.Create(corridorFeatureLine,
    "FL Alignment", siteId, layerId, styleId, labelSetId,
    AlignmentType.Centerline);
```

### Offset Alignment (static methods)

The instance method `CreateOffsetAlignment(double)` is deprecated since Civil 3D 2010. Use the static overloads instead:

```csharp
// By name strings (full station range)
ObjectId offsetId = Alignment.CreateOffsetAlignment(db,
    "Offset Align",       // new alignment name
    "Parent Alignment",   // parent alignment name
    10.0,                 // offset distance (positive = right)
    "Standard"            // style name
);

// By name strings (partial station range)
ObjectId offsetId = Alignment.CreateOffsetAlignment(db,
    "Offset Align", "Parent Alignment", 10.0, "Standard",
    100.0, 500.0          // startStation, endStation
);

// By ObjectIds (full station range)
ObjectId offsetId = Alignment.CreateOffsetAlignment(
    "Offset Align", parentAlignId, 10.0, styleId);

// By ObjectIds (partial station range)
ObjectId offsetId = Alignment.CreateOffsetAlignment(
    "Offset Align", parentAlignId, 10.0, styleId, 100.0, 500.0);
```

### Connected Alignment

```csharp
ObjectId connectedId = Alignment.CreateConnectedAlignment(
    "Connected Align", siteId, layerId, styleId, labelSetId,
    connectedAlignmentParams);

// Check if an alignment is connected
bool isConnected = align.IsConnectedAlignment;
ConnectedAlignmentInfo info = align.ConnectedAlignmentInfo;
```

### Site Operations

```csharp
// Copy to a named site
align.CopyToSite("MySite");

// Copy by site ObjectId
align.CopyToSite(siteId);

// Copy within the same site
align.CopyToSameSite();
```

## Alignment Entities

Entities are lines, curves, and spirals that form the alignment path. The collection supports fixed, floating, and free constraint types.

### Iterating Entities

```csharp
AlignmentEntityCollection entities = align.Entities;

foreach (AlignmentEntity ae in align.Entities)
{
    switch (ae.EntityType)
    {
        case AlignmentEntityType.Arc:
            AlignmentArc myArc = ae as AlignmentArc;
            ed.WriteMessage("Arc R={0}, L={1}\n", myArc.Radius, myArc.Length);
            break;
        case AlignmentEntityType.Line:
            AlignmentLine myLine = ae as AlignmentLine;
            ed.WriteMessage("Line dir={0}\n", myLine.Direction);
            break;
        case AlignmentEntityType.Spiral:
            AlignmentSpiral mySpiral = ae as AlignmentSpiral;
            ed.WriteMessage("Spiral A={0}\n", mySpiral.A);
            break;
        // Also: SpiralCurve, SpiralSpiral, SpiralCurveSpiralCurveSpiral, etc.
    }
}
```

### Accessing Entities

```csharp
AlignmentEntity entity = entities.EntityAtId(entityId);     // by entity ID
AlignmentEntity entity = entities.GetEntityByOrder(index);   // by draw order
AlignmentEntity entity = entities.EntityAtStation(rawStation); // by station
int first = entities.FirstEntity;  // ID of first entity
int last  = entities.LastEntity;   // ID of last entity
```

### Adding Fixed Entities (defined by coordinates)

```csharp
// Fixed lines
AlignmentLine line = entities.AddFixedLine(startPoint, endPoint);
AlignmentLine line = entities.AddFixedLine(prevEntityId, startPoint, endPoint);
AlignmentLine line = entities.AddFixedLine(prevEntityId, distance);

// Fixed curves (many overloads)
AlignmentArc arc = entities.AddFixedCurve(prevEntityId, startPt, midPt, endPt);
AlignmentArc arc = entities.AddFixedCurve(pt1, pt2, radius, isClockwise);
AlignmentArc arc = entities.AddFixedCurve(centerPt, passThroughPt, isClockwise);
AlignmentArc arc = entities.AddFixedCurve(centerPt, radius, isClockwise);
AlignmentArc arc = entities.AddFixedCurve(pt1, dirAtPt1, radius, isClockwise);
AlignmentArc arc = entities.AddFixedCurve(pt1, dirAtPt1, pt2);
AlignmentArc arc = entities.AddFixedCurve(pt1, pt2, dirAtPt2);

// Fixed spirals
AlignmentSpiral sp = entities.AddFixedSpiral(prevId, startRadius, endRadius, length, spiralDef);
AlignmentSpiral sp = entities.AddFixedSpiral(prevId, radius, length, spiralCurveType, spiralDef);
AlignmentSpiral sp = entities.AddFixedSpiral(prevId, startPt, piPt, endPt, spiralDef);
```

### Adding Floating Entities (attached to one neighbor)

```csharp
// Floating lines
AlignmentLine line = entities.AddFloatingLine(prevEntityId, length);
AlignmentLine line = entities.AddFloatingLine(prevEntityId, passThroughPt);
AlignmentLine line = entities.AddFloatingLine(length, nextEntityId);

// Floating curves
AlignmentArc arc = entities.AddFloatingCurve(prevEntityId, passThroughPt);
AlignmentArc arc = entities.AddFloatingCurve(prevEntityId, radius, paramValue,
    paramType, isClockwise);
```

### Adding Free Entities (constrained to two neighbors)

```csharp
// Free line between two entities
AlignmentLine line = entities.AddFreeLine(prevEntityId, nextEntityId);

// Free curve between two entities
AlignmentArc arc = entities.AddFreeCurve(prevEntityId, nextEntityId,
    passThroughPt);
AlignmentArc arc = entities.AddFreeCurve(prevEntityId, nextEntityId,
    paramValue, paramType, isGreaterThan180, curveType);

// Free spiral-curve-spiral
AlignmentSCS scs = entities.AddFreeSCS(prevEntityId, nextEntityId,
    sp1Param, sp2Param, spType, radius, isGreaterThan180, spiralDef);
```

### Removing Entities

```csharp
entities.Remove(entity);
entities.RemoveAt(index);
entities.Clear();
```

## Stations

### Station Equations

```csharp
StationEquation eq = align.StationEquations.Add(
    80,     // rawStationBack: raw station value at the equation point (distance from start)
    0,      // stationAhead: station value assigned going ahead past the equation
    StationEquationType.Increasing
);
```

### Station Sets

`StationTypes` is a flags enum (note the plural). Common values: `All`, `Major`, `Minor`, `GeometryPoint`, `Equation`, `SuperTransPoint`.

```csharp
// Get all stations with major=100, minor=20
Station[] stations = align.GetStationSet(StationTypes.All, 100, 20);
foreach (Station s in stations)
{
    ed.WriteMessage("Station {0}, Type: {1}, Location: ({2},{3})\n",
        s.RawStation, s.StationType, s.Location.X, s.Location.Y);
}

// Major stations only, single interval
Station[] majors = align.GetStationSet(StationTypes.Major, 100);

// Geometry points only (no interval needed)
Station[] geoPts = align.GetStationSet(StationTypes.GeometryPoint);

// Custom range with major=50, minor=10
Station[] ranged = align.GetStationSet(StationTypes.All, 50, 10, 100.0, 500.0);
```

### Point Location from Station

```csharp
// Simple version: station + offset -> easting + northing
double easting, northing;
align.PointLocation(station, offset, ref easting, ref northing);

// With tolerance and bearing
double bearing;
align.PointLocation(station, offset, tolerance,
    ref easting, ref northing, ref bearing);
```

**Tolerance note:** Determines which entity the point is on. A large tolerance may place the point on an earlier entity. Note parameter order is easting, northing (X, Y).

### Station/Offset from Point (inverse of PointLocation)

```csharp
// Simple version: easting + northing -> station + offset
double station, offset;
align.StationOffset(easting, northing, ref station, ref offset);

// With tolerance
align.StationOffset(easting, northing, tolerance, ref station, ref offset);

// Accept out-of-range points (beyond alignment start/end)
bool outOfRange;
align.StationOffsetAcceptOutOfRange(easting, northing,
    ref station, ref offset, ref outOfRange);

// With tolerance + out-of-range
align.StationOffsetAcceptOutOfRange(easting, northing, tolerance,
    ref station, ref offset, ref outOfRange);
```

### Instantaneous Radius at Station

```csharp
// Get the radius at a specific raw station value
// Returns double.PositiveInfinity for tangent segments
double radius = align.GetInstantaneousRadius(rawStation);
```

### Reverse Alignment Direction

```csharp
// Reverses the direction of the alignment geometry
align.Reverse();
```

### Distance to Another Alignment

```csharp
double distToOther, stationOnOther;
align.DistanceToAlignment(stationOnThis, otherAlignment,
    ref distToOther, ref stationOnOther);

// With explicit side
align.DistanceToAlignment(stationOnThis, otherAlignment,
    AlignmentSide.Left, ref distToOther, ref stationOnOther);
```

## Design Speeds

```csharp
DesignSpeed ds = align.DesignSpeeds.Add(0, 45);    // station 0+00, 45 mph
ds.Comment = "Straightaway";

ds = align.DesignSpeeds.Add(430, 30);               // station 4+30
ds.Comment = "Start of curve";

align.UseDesignSpeed = true; // Enable speed-based design
```

**Note:** `GetDesignSpeed()` requires a "raw" station value (without station equation modifications).

## Superelevation

Superelevation is divided into curves, each containing transition regions with critical stations.

```csharp
// Access superelevation curves
if (align.SuperelevationCurves.Count < 1)
{
    ed.WriteMessage("Must calculate superelevation data first.\n");
    return;
}

foreach (SuperelevationCurve sec in align.SuperelevationCurves)
{
    ed.WriteMessage("Curve: {0}, Start: {1}, End: {2}\n",
        sec.Name, sec.StartStation, sec.EndStation);

    foreach (SuperelevationCriticalStation sest in sec.CriticalStations)
    {
        ed.WriteMessage("  Station: {0}, Type: {1}, Region: {2}\n",
            sest.Station, sest.StationType, sest.TransitionRegionType);

        // Get slope for each cross segment type
        foreach (int i in Enum.GetValues(typeof(SuperelevationCrossSegmentType)))
        {
            try
            {
                double slope = sest.GetSlope(
                    (SuperelevationCrossSegmentType)i);
                ed.WriteMessage("    Slope: {0}, Segment: {1}\n", slope,
                    Enum.GetName(typeof(SuperelevationCrossSegmentType), i));
            }
            catch (InvalidOperationException) { } // Invalid segment type for this station
        }
    }
}
```

**Key properties:**
- `Alignment.SuperelevationCurves` - collection of SE curves
- `Alignment.SuperelevationCriticalStations` - all critical stations across all curves
- `SuperelevationCriticalStationCollection.GetCriticalStationAt()` - access individual stations

**API Change Note (Civil 3D 2013+):** `SuperelevationData` property and `SuperElevationAtStation()` method were removed. Use `SuperelevationCurves` and `SuperelevationCriticalStations` instead.

## Alignment Styles

```csharp
ObjectId styleId = doc.Styles.AlignmentStyles.Add("My Alignment Style");
AlignmentStyle style = ts.GetObject(styleId, OpenMode.ForWrite) as AlignmentStyle;

// Hide direction arrows
style.GetDisplayStylePlan(AlignmentDisplayStyleType.Arrow).Visible = false;

// Show curves in violet
style.GetDisplayStylePlan(AlignmentDisplayStyleType.Curve).Color =
    Color.FromColorIndex(ColorMethod.ByAci, 200);

// Show lines in blue
style.GetDisplayStylePlan(AlignmentDisplayStyleType.Line).Color =
    Color.FromColorIndex(ColorMethod.ByAci, 160);

// Assign to alignment
align.StyleId = style.Id;
```

## Alignment Label Styles

Labels are set via `LabelSet` when creating an alignment, or through `LabelSetStyles`:

```csharp
// Label set styles
var labelSetStyles = doc.Styles.LabelSetStyles.AlignmentLabelSetStyles;

// AlignmentLabelSetItem types:
// LabelStyleType.AlignmentMajorStation
// LabelStyleType.AlignmentMinorStation

// Minor stations must reference a parent major station AlignmentLabelSetItem
```

### Alignment Label Property Fields

Major/minor stations:
```
<[Station Value(Uft|FS|P0|RN|AP|Sn|TP|B2|EN|W0|OF)]>
<[Northing(Uft|P4|RN|AP|Sn|OF)]>
<[Design Speed(P3|RN|AP|Sn|OF)]>
<[Alignment Name(CP)]>
```

Additional fields for specific label types:
- Minor stations: `<[Offset From Major Station(...)]>`
- Geometry points: `<[Geometry Point Text(CP)]>`, `<[Geometry Point Entity Before/After Data(CP)]>`
- Design speeds: `<[Design Speed Before(...)]>`
- Station equations: `<[Station Ahead(...)]>`, `<[Station Back(...)]>`, `<[Increase/Decrease(CP)]>`

## Related Queries

```csharp
// Get profile views for this alignment
ObjectIdCollection pvIds = align.GetProfileViewIds();

// Get sample line groups
ObjectIdCollection slgIds = align.GetSampleLineGroupIds();

// Get profiles
ObjectIdCollection profileIds = align.GetProfileIds();

// Get superelevation views
ObjectIdCollection seViewIds = align.GetSuperelevationViewIds();

// Get child offset alignments
ObjectIdCollection offsetIds = align.GetChildOffsetAlignmentIds();
ObjectIdCollection dynamicOnly = align.GetChildOffsetAlignmentIds(true); // only dynamic-update offsets

// Get label group IDs
ObjectIdCollection labelGroupIds = align.GetAlignmentLabelGroupIds();
ObjectIdCollection labelIds = align.GetAlignmentLabelIds();

// Export to polyline
ObjectId plineId = align.GetPolyline();

// Import a label set
align.ImportLabelSet("My Label Set");
align.ImportLabelSet(labelSetStyleId);

// Get station string with equations applied
string stationStr = align.GetStationStringWithEquations(rawStation);

// Get next unique alignment name
string uniqueName = Alignment.GetNextUniqueName("MyAlignment");
```

## Useful Properties

```csharp
// Alignment geometry range
double start  = align.StartingStation;
double end    = align.EndingStation;
double endEq  = align.EndingStationWithEquations;
double length = align.Length;

// Reference point (station origin)
Point2d refPt     = align.ReferencePoint;
double refStation  = align.ReferencePointStation;

// Site info
string siteName = align.SiteName;
bool isSiteless = align.IsSiteless;

// Offset alignment info
bool isOffset = align.IsOffsetAlignment;
OffsetAlignmentInfo oaInfo = align.OffsetAlignmentInfo;

// Type and creation mode
AlignmentType aType = align.AlignmentType;
AlignmentCreationType cMode = align.CreationMode;

// Cross slope at station (superelevation)
double slope = align.GetCrossSlopeAtStation(station,
    SuperelevationCrossSegmentType.InsideLane, true);
```

## Gotchas

- `Create()` string overload fails if the named styles don't exist in the document
- Offset alignment does NOT inherit station labels, equations, or design speeds
- Station equations modify station values - some methods need "raw" stations (use `GetStationStringWithEquations()` for display)
- Superelevation curves must be calculated before accessing (manually or via wizard)
- `GetSlope()` throws `InvalidOperationException` for invalid segment types - catch silently
- `PointLocation` and `StationOffset` parameter order is easting, northing (X, Y), not northing, easting
- `GetInstantaneousRadius()` requires a raw station value
- The instance method `CreateOffsetAlignment(double)` is deprecated since Civil 3D 2010; use the static overloads
- `StationTypes` is a flags enum (plural) - use `StationTypes.All`, not `StationType.All`

## Related Skills

- `c3d-profiles` - Profiles along alignments
- `c3d-label-styles` - General label style creation
- `c3d-corridors` - Corridors use alignments as baselines
