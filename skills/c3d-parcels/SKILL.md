---
name: c3d-parcels
description: Sites, parcels, parcel topology, subdivision, parcel segments, parcel labels, renumbering, parcel styles
---

# Civil 3D Parcels

Use this skill when creating, modifying, or querying parcels and sites, working with parcel segments and topology, or configuring parcel styles and labels.

## Sites

Sites are containers that enforce topology between parcels and alignments. All parcels must belong to a site.

```csharp
CivilDocument doc = CivilApplication.ActiveDocument;

// Get all sites
ObjectIdCollection siteIds = doc.GetSiteIds();
foreach (ObjectId siteId in siteIds)
{
    Site site = ts.GetObject(siteId, OpenMode.ForRead) as Site;
    ed.WriteMessage("Site: {0}\n", site.Name);

    // Get parcels in this site
    ObjectIdCollection parcelIds = site.GetParcelIds();
    ed.WriteMessage("  Parcels: {0}\n", parcelIds.Count);

    // Get alignments in this site
    ObjectIdCollection alignIds = site.GetAlignmentIds();
    ed.WriteMessage("  Alignments: {0}\n", alignIds.Count);

    // Get feature lines in this site
    ObjectIdCollection flIds = site.GetFeatureLineIds();
    ed.WriteMessage("  Feature Lines: {0}\n", flIds.Count);
}
```

### Site Properties and Methods

- Name (string, get/set) — display name of the site
- Description (string, get/set) — user description

Key methods:

- GetParcelIds() → ObjectIdCollection — all parcels in the site
- GetAlignmentIds() → ObjectIdCollection — all alignments in the site
- GetFeatureLineIds() → ObjectIdCollection — all feature lines in the site

### Creating a Site

```csharp
// Create a new site by name
ObjectId siteId = Site.Create(doc, "My Subdivision");
Site site = ts.GetObject(siteId, OpenMode.ForWrite) as Site;
site.Description = "Phase 1 residential lots";
```

## Accessing Parcels

```csharp
// Through a site
Site site = ts.GetObject(siteId, OpenMode.ForRead) as Site;
ObjectIdCollection parcelIds = site.GetParcelIds();

foreach (ObjectId parcelId in parcelIds)
{
    Parcel parcel = ts.GetObject(parcelId, OpenMode.ForRead) as Parcel;
    ed.WriteMessage("Parcel: {0}, Number: {1}, Area: {2:F2}\n",
        parcel.Name, parcel.Number, parcel.Area);
}
```

## Parcel Properties

- Name (string, get/set) — parcel display name (e.g., "Lot 15A")
- Number (int, get/set) — integer lot number
- Area (double, get) — computed area in square drawing units
- Perimeter (double, get) — computed perimeter length
- Address (string, get/set) — street address
- TaxId (string, get/set) — tax parcel identifier
- LandUse (string, get/set) — land use classification
- StyleId (ObjectId, get/set) — parcel display style
- SiteId (ObjectId, get) — parent site
- IsEnclosingParcel (bool, get) — true if this is the remainder/parent parcel
- Centroid (Point3d, get) — computed center point of the parcel
- Segments (ParcelSegmentCollection, get) — boundary segments

```csharp
Parcel parcel = ts.GetObject(parcelId, OpenMode.ForWrite) as Parcel;

// Read properties
double area      = parcel.Area;       // square feet/meters (drawing units)
double perimeter = parcel.Perimeter;

// Set writable properties
parcel.Name    = "Lot 15";
parcel.Number  = 15;
parcel.Address = "123 Main St";
parcel.TaxId   = "R-2026-0015";
parcel.LandUse = "Residential";
parcel.StyleId = parcelStyleId;
```

## Creating Parcels from Objects

```csharp
// Create parcels from AutoCAD entities (lines, arcs, polylines)
// Entities must form closed boundaries within the site
ObjectIdCollection entityIds = new ObjectIdCollection();
entityIds.Add(polylineId1);
entityIds.Add(polylineId2);

Site site = ts.GetObject(siteId, OpenMode.ForWrite) as Site;
site.CreateParcelsFromObjects(entityIds, parcelStyleId, labelStyleId);
```

## Subdivision

Layout tools create parcels using subdivision algorithms. Civil 3D supports three modes:

- **Frontage** — subdivides a parent parcel along a frontage line (road alignment), constrained by minimum width and area
- **Sliding Angle** — sweeps lot lines at a specified angle from the frontage, constrained by minimum area/frontage and side (left or right)
- **Free Form** — manually defined boundaries within a parent parcel

**Note:** Subdivision methods are primarily interactive (wizard-driven in the Civil 3D UI). The .NET API supports creation from existing geometry via `CreateParcelsFromObjects`. For complex subdivision scenarios, use `SendStringToExecute` to invoke built-in subdivision commands.

## Parcel Segments

Parcel boundaries are composed of `ParcelSegment` objects (lines and curves):

```csharp
Parcel parcel = ts.GetObject(parcelId, OpenMode.ForRead) as Parcel;

int segmentCount = parcel.Segments.Count;
foreach (ParcelSegment segment in parcel.Segments)
{
    ed.WriteMessage("Segment: Start=({0:F2},{1:F2}), End=({2:F2},{3:F2})\n",
        segment.StartPoint.X, segment.StartPoint.Y,
        segment.EndPoint.X, segment.EndPoint.Y);

    if (segment.IsCurve)
    {
        ed.WriteMessage("  Curve: Radius={0:F2}, ArcLength={1:F2}\n",
            segment.Radius, segment.Length);
    }
    else
    {
        ed.WriteMessage("  Line: Bearing={0}, Length={1:F2}\n",
            segment.Direction, segment.Length);
    }
}
```

### Segment Properties

- StartPoint (Point2d, get) — segment start coordinate
- EndPoint (Point2d, get) — segment end coordinate
- Length (double, get) — segment length (arc length for curves)
- Direction (double, get) — bearing in radians from north, clockwise positive
- IsCurve (bool, get) — true if arc segment, false if line
- Radius (double, get) — arc radius (valid when IsCurve is true)
- CenterPoint (Point2d, get) — arc center (valid when IsCurve is true)
- IsClockwise (bool, get) — arc direction (valid when IsCurve is true)

## Parcel Topology

Parcels in a site maintain topological relationships. When boundaries are shared, modifying one parcel automatically updates its neighbors.

### Adjacency and Parent/Child

```csharp
Parcel parcel = ts.GetObject(parcelId, OpenMode.ForRead) as Parcel;

// Check if this parcel is an enclosing (parent) parcel
bool isEnclosing = parcel.IsEnclosingParcel;

// Get the site to discover all parcels and their relationships
Site site = ts.GetObject(parcel.SiteId, OpenMode.ForRead) as Site;
ObjectIdCollection allParcelIds = site.GetParcelIds();

// Typically the largest parcel is the "remainder" or parent lot
// Child lots are carved from it via subdivision
// The enclosing parcel updates automatically as child lots are created
```

### Right-of-Way

Right-of-way (ROW) parcels are created when alignments pass through a site. The alignment splits the site into parcels, and the ROW parcel represents the road corridor.

```csharp
// When an alignment is added to a site, it automatically creates
// ROW parcels by splitting existing parcels along the alignment
// ROW width is controlled by alignment offset parameters

// Check parcel style to identify ROW parcels
Parcel parcel = ts.GetObject(parcelId, OpenMode.ForRead) as Parcel;
ParcelStyle style = ts.GetObject(parcel.StyleId, OpenMode.ForRead) as ParcelStyle;
string styleName = style.Name; // e.g., "Right Of Way" or "ROW"
```

## Parcel Styles

```csharp
// Create a parcel style
ObjectId styleId = doc.Styles.ParcelStyles.Add("Residential Lot");
ParcelStyle style = ts.GetObject(styleId, OpenMode.ForWrite) as ParcelStyle;

// Display settings - plan view
style.GetDisplayStylePlan(ParcelDisplayStyleType.ParcelSegment).Color =
    Color.FromColorIndex(ColorMethod.ByAci, 3); // green
style.GetDisplayStylePlan(ParcelDisplayStyleType.ParcelSegment).Lineweight =
    LineWeight.LineWeight040;

// Fill display
style.GetDisplayStylePlan(ParcelDisplayStyleType.ParcelAreaFill).Visible = true;
style.GetDisplayStylePlan(ParcelDisplayStyleType.ParcelAreaFill).Color =
    Color.FromRgb(200, 255, 200); // light green fill

// Assign to parcel
parcel.StyleId = styleId;

// Access existing styles
ObjectId existingStyleId = doc.Styles.ParcelStyles["Standard"];
```

## Parcel Labels

### Label Style Hierarchy

```csharp
var parcelLabelStyles = doc.Styles.LabelStyles.ParcelLabelStyles;

// Area labels (placed inside the parcel)
var areaLabelStyles = parcelLabelStyles.AreaLabelStyles;

// Segment labels (placed along boundaries)
var lineLabelStyles = parcelLabelStyles.LineLabelStyles;
var curveLabelStyles = parcelLabelStyles.CurveLabelStyles;
```

### Creating Labels

```csharp
// Area label (placed at parcel centroid)
Point2d labelLocation = new Point2d(parcel.Centroid.X, parcel.Centroid.Y);
ObjectId areaLabelId = ParcelLabel.Create(
    parcelId, areaLabelStyleId, labelLocation);

// Line segment label
ObjectId lineLabelId = ParcelSegmentLabel.Create(
    parcelId, segmentIndex, lineLabelStyleId);

// Curve segment label
ObjectId curveLabelId = ParcelSegmentLabel.Create(
    parcelId, segmentIndex, curveLabelStyleId);

// Get existing labels
ObjectIdCollection existingLabels = parcel.GetAvailableLabelIds();

// Change label style
Label label = ts.GetObject(areaLabelId, OpenMode.ForWrite) as Label;
label.StyleId = newLabelStyleId;
```

### Common Parcel Label Property Fields

Area labels:
```
<[Parcel Name(CP)]>
<[Parcel Number]>
<[Parcel Area(Usf|P0|RN|AP|Sn|OF)]>
<[Parcel Perimeter(Uft|P2|RN|AP|Sn|OF)]>
<[Parcel Address(CP)]>
<[Tax ID(CP)]>
```

Segment labels (line):
```
<[Segment Bearing(Udir|P0|B4)]>
<[Segment Length(Uft|P2|RN|AP|Sn|OF)]>
```

Segment labels (curve):
```
<[Segment Arc Length(Uft|P2|RN|AP|Sn|OF)]>
<[Segment Radius(Uft|P2|RN|AP|Sn|OF)]>
<[Segment Delta Angle(Udeg|P4)]>
<[Segment Chord Length(Uft|P2|RN|AP|Sn|OF)]>
<[Segment Chord Bearing(Udir|P0|B4)]>
```

## Renumbering

```csharp
// Renumber parcels sequentially
Site site = ts.GetObject(siteId, OpenMode.ForRead) as Site;
ObjectIdCollection parcelIds = site.GetParcelIds();

int lotNumber = 1;
foreach (ObjectId pid in parcelIds)
{
    Parcel p = ts.GetObject(pid, OpenMode.ForWrite) as Parcel;

    // Skip ROW or enclosing parcels
    if (p.IsEnclosingParcel) continue;

    p.Number = lotNumber;
    p.Name = string.Format("Lot {0}", lotNumber);
    lotNumber++;
}
```

**Note:** `GetParcelIds()` does not guarantee any specific ordering. For specific ordering (e.g., clockwise around a cul-de-sac), sort parcels by centroid angle or frontage station before renumbering.

## Parcel Analysis

### Area and Frontage Checks

```csharp
double minArea = 7500.0;  // minimum 7,500 sq ft

Site site = ts.GetObject(siteId, OpenMode.ForRead) as Site;
foreach (ObjectId pid in site.GetParcelIds())
{
    Parcel p = ts.GetObject(pid, OpenMode.ForRead) as Parcel;
    if (p.IsEnclosingParcel) continue;

    if (p.Area < minArea)
        ed.WriteMessage("WARNING: {0} area {1:F0} sf < minimum {2:F0}\n",
            p.Name, p.Area, minArea);
}
```

### Summary Statistics

```csharp
double totalArea = 0, minLot = double.MaxValue, maxLot = double.MinValue;
int lotCount = 0;

foreach (ObjectId pid in parcelIds)
{
    Parcel p = ts.GetObject(pid, OpenMode.ForRead) as Parcel;
    if (p.IsEnclosingParcel) continue;
    totalArea += p.Area;
    minLot = Math.Min(minLot, p.Area);
    maxLot = Math.Max(maxLot, p.Area);
    lotCount++;
}

ed.WriteMessage("Lots: {0}, Min: {1:F0} sf, Max: {2:F0} sf, Avg: {3:F0} sf\n",
    lotCount, minLot, maxLot, totalArea / lotCount);
```

## Enumerating All Parcels

```csharp
// Enumerate all parcels across all sites
ObjectIdCollection siteIds = doc.GetSiteIds();
foreach (ObjectId siteId in siteIds)
{
    Site site = ts.GetObject(siteId, OpenMode.ForRead) as Site;
    foreach (ObjectId parcelId in site.GetParcelIds())
    {
        Parcel parcel = ts.GetObject(parcelId, OpenMode.ForRead) as Parcel;
        ed.WriteMessage("[{0}] {1}: {2:F0} sq ft\n",
            site.Name, parcel.Name, parcel.Area);
    }
}
```

## Gotchas

- All parcels must belong to a site — there is no "siteless" parcel concept (unlike siteless alignments)
- Adding an alignment to a site automatically splits existing parcels, creating ROW parcels
- Parcel topology is enforced within a site — editing one boundary updates adjacent parcels
- `Parcel.Area` and `Parcel.Perimeter` are read-only computed properties based on segment geometry
- `ParcelSegment.Direction` is in radians measured from north (not east), clockwise positive
- Subdivision methods (frontage, sliding angle) are interactive — the .NET API primarily supports creation from existing geometry via `CreateParcelsFromObjects`
- `GetParcelIds()` does not guarantee any specific ordering — sort manually for renumbering
- The enclosing (remainder) parcel updates automatically as child lots are created or deleted
- Parcel `Number` is an integer property, not a string — use `Name` for alphanumeric identifiers like "Lot 15A"
- Modifying parcel segments directly is limited — use site topology operations or recreate from objects
- When a site contains both parcels and alignments, deleting an alignment merges the parcels it previously split
- `ParcelSegment` curve properties (`Radius`, `CenterPoint`, `IsClockwise`) throw if accessed on a line segment — check `IsCurve` first

## Related Skills

- `c3d-alignments` — alignments within sites and their relationship to parcel topology
- `c3d-surfaces` — surface-based grading and elevation data for parcel design
- `c3d-label-styles` — general label style creation and configuration
- `c3d-root-objects` — CivilDocument access, `GetSiteIds()`, and transaction patterns
