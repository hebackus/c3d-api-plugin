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
// By ObjectIds (pass ObjectId.Null for siteless)
ObjectId alignId = Alignment.Create(doc, "New Alignment",
    ObjectId.Null,  // site (Null = siteless)
    "0",            // layer name
    "Basic",        // alignment style name
    "AllLabels"     // label set style name
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

ObjectId alignId = Alignment.Create(doc, plops,
    "New Alignment", "0", "Standard", "Standard");
```

### Offset Alignment

```csharp
Alignment align = ts.GetObject(alignId, OpenMode.ForRead) as Alignment;
ObjectId offsetAlignId = align.CreateOffsetAlignment(10.0); // offset distance
// Inherits name (with number suffix) and style, but NOT station labels/equations/design speeds
```

### Site Operations

```csharp
// Move to site
align.CopyToSite(siteId);

// Copy as siteless (from sited)
align.CopyToSite(ObjectId.Null);  // or pass ""
```

## Alignment Entities

Entities are lines, curves, and spirals that form the alignment path.

```csharp
// Entity collection
AlignmentEntityCollection entities = align.Entities;

// Add a fixed curve
AlignmentArc arc = align.Entities.AddFixedCurve(
    previousEntityId, startPoint, middlePoint, endPoint);

// Iterate and determine types
foreach (AlignmentEntity ae in align.Entities)
{
    switch (ae.EntityType)
    {
        case AlignmentEntityType.Arc:
            AlignmentArc myArc = ae as AlignmentArc;
            ed.WriteMessage("Arc length: {0}\n", myArc.Length);
            break;
        case AlignmentEntityType.Spiral:
            AlignmentSpiral mySpiral = ae as AlignmentSpiral;
            break;
        // Also: Tangent, SpiralCurve, SpiralSpiral, etc.
    }
}
```

Each entity has `EntityId` and knows its before/after entities. Access by ID:
```csharp
AlignmentEntity entity = entities.EntityAtId(entityId);
```

## Stations

### Station Equations

```csharp
StationEquation eq = align.StationEquations.Add(
    80,     // location (distance from start)
    0,      // new station number basis
    StationEquationType.Increasing
);
```

### Station Sets

```csharp
// Get all stations with major=100, minor=20
Station[] stations = align.GetStationSet(StationType.All, 100, 20);
foreach (Station s in stations)
{
    ed.WriteMessage("Station {0}, Type: {1}, Location: {2}\n",
        s.RawStation, s.StnType, s.Location);
}
```

### Point Location from Station

```csharp
// Simple version: station + offset -> northing + easting
double northing, easting;
align.PointLocation(station, offset, ref northing, ref easting);

// With tolerance and bearing
double bearing;
align.PointLocation(station, offset, tolerance,
    ref northing, ref easting, ref bearing);
```

**Tolerance note:** Determines which entity the point is on. A large tolerance may place the point on an earlier entity.

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
                    (SuperelevationCrossSegmentType)i, false);
                ed.WriteMessage("    Slope: {0}, Segment: {1}\n", slope,
                    Enum.GetName(typeof(SuperelevationCrossSegmentType), i));
            }
            catch (InvalidOperationException) { } // Invalid segment type
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
```

## Gotchas

- `Create()` fails if the named styles don't exist in the document
- Offset alignment does NOT inherit station labels, equations, or design speeds
- Station equations modify station values - some methods need "raw" stations
- Superelevation curves must be calculated before accessing (manually or via wizard)
- `GetSlope()` throws `InvalidOperationException` for invalid segment types - catch silently
- `PointLocation` tolerance affects which entity returns the point

## Related Skills

- `c3d-profiles` - Profiles along alignments
- `c3d-label-styles` - General label style creation
- `c3d-corridors` - Corridors use alignments as baselines
