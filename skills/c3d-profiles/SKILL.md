---
name: c3d-profiles
description: Profile creation (from surface, by layout, from feature line, offset), profile views, PVIs, profile entities, band sets, and styles
---

# Civil 3D Profiles and Profile Views

Use this skill when creating profiles from surfaces, building layout profiles with entities, creating profile views, or working with profile styles.

## Profile Overview

Profiles are the vertical analogue to alignments. Together, an alignment and profile represent a 3D path.

## Accessing Profiles

```csharp
ObjectIdCollection profileIds = alignment.GetProfileIds();
foreach (ObjectId profileId in profileIds)
{
    Profile profile = ts.GetObject(profileId, OpenMode.ForRead) as Profile;
    ed.WriteMessage("Profile: {0}\n", profile.Name);
}
```

## Profile Properties

```csharp
Profile profile = ts.GetObject(profileId, OpenMode.ForRead) as Profile;

// Read-only properties
double startSta = profile.StartingStation;
double endSta = profile.EndingStation;
double len = profile.Length;
double minElev = profile.ElevationMin;
double maxElev = profile.ElevationMax;
ProfileType pType = profile.ProfileType;
ObjectId alignId = profile.AlignmentId;
string dataSource = profile.DataSourceName;
double offset = profile.Offset;

// Query elevation and grade at any station
double elev = profile.ElevationAt(1000.0);
double grade = profile.GradeAt(1000.0);
```

## Creating a Profile from a Surface

Derives elevation data from a surface along an alignment path:

```csharp
// ObjectId-based overload (preferred)
ObjectId profileId = Profile.CreateFromSurface(
    "My Profile", alignId, surfaceId, layerId, styleId, labelSetId);

// With offset and station range
ObjectId profileId = Profile.CreateFromSurface(
    "My Profile", alignId, surfaceId, layerId, styleId, labelSetId,
    offset: 10.0, sampleStart: 0.0, sampleEnd: 500.0);

// String name-based overload
ObjectId profileId = Profile.CreateFromSurface(
    "My Profile", doc, "Alignment Name", "Surface Name",
    "Layer Name", "Style Name", "Label Set Name");
```

## Creating a Profile by Layout (Entity-Based)

Creates an empty profile, then defines shape with entities:

```csharp
// ObjectId-based overload (preferred)
ObjectId profileId = Profile.CreateByLayout(
    "My Profile", alignId, layerId, styleId, labelSetId);

// String name-based overload
ObjectId profileId = Profile.CreateByLayout(
    "My Profile", doc, "Alignment Name", "Layer Name",
    "Style Name", "Label Set Name");

Profile oProfile = ts.GetObject(profileId, OpenMode.ForWrite) as Profile;
```

## Creating a Profile from a Feature Line

Extracts profile data from a corridor feature line:

```csharp
ObjectId profileId = Profile.CreateFromFeatureLine(
    "My Profile", corridorFeatureLine, alignId, layerId, styleId, labelSetId);
```

## Creating a Static Copy of a Profile

Creates a static (non-dynamic) finished ground profile from an existing profile:

```csharp
// ObjectId-based
ObjectId profileId = Profile.CreateStaticFGFromProfile(
    "Static Copy", srcProfileId, layerId, styleId, labelSetId);

// String name-based
ObjectId profileId = Profile.CreateStaticFGFromProfile(
    "Static Copy", doc, "Source Profile", "Layer Name",
    "Style Name", "Label Set Name");
```

## Creating an Offset Profile

Creates a profile on an offset alignment with a constant slope from the parent profile:

```csharp
// ObjectId-based
ObjectId profileId = parentProfile.CreateOffsetProfileBySlope(
    "Offset Profile", offsetAlignmentId, profileStyleId, slope: 0.02);

// String name-based
ObjectId profileId = parentProfile.CreateOffsetProfileBySlope(
    "Offset Profile", "Offset Alignment Name", "Style Name", slope: 0.02);
```

### Offset Profile Parameters

```csharp
// Access the offset parameters for station-based slope control
Profile.OffsetProfileParameters offsetParams = profile.OffsetParameters;
ObjectId parentProfileId = offsetParams.ParentProfileId;
ObjectId parentAlignId = offsetParams.ParentAlignmentId;

// Define variable slopes at specific stations
offsetParams.Stations = new List<Profile.OffsetProfileParametersStation>
{
    new Profile.OffsetProfileParametersStation(0.0, 0.02, "Start"),
    new Profile.OffsetProfileParametersStation(500.0, 0.04, "Steeper section"),
};
```

## Adding Profile Entities

Profile entities define the geometry of layout profiles. Coordinates use (station, elevation) as `Point2d`.

### Fixed Tangents (Straight Lines)

```csharp
// Fixed tangent between two points
Point2d startPoint = new Point2d(alignment.StartingStation, -40);
Point2d endPoint = new Point2d(758.2, -70);
ProfileTangent tangent1 = oProfile.Entities.AddFixedTangent(startPoint, endPoint);

// Fixed tangent specifying insertion after a previous entity
ProfileTangent tangent = oProfile.Entities.AddFixedTangentWithPreviousEntity(
    prevEntity.EntityId, startPoint, endPoint);
```

### Floating and Free Tangents

```csharp
// Floating tangent - attaches to an entity end and passes through a point
ProfileTangent floatTan = oProfile.Entities.AddFloatingTangent(
    entityId, passPoint, EntityAttachType.End);

// Free tangent - connects two existing entities
ProfileTangent freeTan = oProfile.Entities.AddFreeTangent(
    prevEntityId, nextEntityId);
```

### Symmetric Parabolic Curves

```csharp
// Free symmetric parabola by length (connects two entities)
oProfile.Entities.AddFreeSymmetricParabolaByLength(
    tangent1.EntityId, tangent2.EntityId,
    VerticalCurveType.Sag, 900.1, preferFlat: true);

// Free symmetric parabola by K value
oProfile.Entities.AddFreeSymmetricParabolaByK(
    prevEntityId, nextEntityId, VerticalCurveType.Crest, k: 50.0);

// Free symmetric parabola by radius
oProfile.Entities.AddFreeSymmetricParabolaByRadius(
    prevEntityId, nextEntityId, VerticalCurveType.Sag, radius: 1000.0);

// Free symmetric parabola at a PVI
oProfile.Entities.AddFreeSymmetricParabolaByPVIAndCurveLength(pvi, curveLength: 200.0);
oProfile.Entities.AddFreeSymmetricParabolaByPVIAndK(pvi, k: 50.0);
oProfile.Entities.AddFreeSymmetricParabolaByPVIAndThroughPoint(pvi, passPoint);

// Fixed symmetric parabola by three points
oProfile.Entities.AddFixedSymmetricParabolaByThreePoints(pt1, pt2, pt3);

// Fixed symmetric parabola by two points and constraint
oProfile.Entities.AddFixedSymmetricParabolaByTwoPointsAndK(pt1, pt2, VerticalCurveType.Sag, k);
oProfile.Entities.AddFixedSymmetricParabolaByTwoPointsAndRadius(pt1, pt2, VerticalCurveType.Sag, radius);
oProfile.Entities.AddFixedSymmetricParabolaByTwoPointsAndStartGrade(pt1, pt2, startGrade);
oProfile.Entities.AddFixedSymmetricParabolaByTwoPointsAndEndGrade(pt1, pt2, endGrade);
oProfile.Entities.AddFixedSymmetricParabolaByEntityEndAndThroughPoint(entityId, passPoint);

// Floating symmetric parabola (attaches to an existing entity)
oProfile.Entities.AddFloatingSymmetricParabolaByThroughPointAndK(entityId, passPoint, k, attachType);
oProfile.Entities.AddFloatingSymmetricParabolaByThroughPointAndRadius(entityId, passPoint, radius, attachType);
oProfile.Entities.AddFloatingSymmetricParabolaByThroughPointAndGrade(entityId, passPoint, grade, attachType);
```

### Asymmetric Parabolic Curves

```csharp
// Free asymmetric parabola at a PVI with two different lengths
oProfile.Entities.AddFreeAsymmetricParabolaByPVIAndLengths(pvi, length1, length2);
```

### Circular Curves

```csharp
// Free circular curve at a PVI
oProfile.Entities.AddFreeCircularCurveByPVIAndRadius(pvi, radius);
oProfile.Entities.AddFreeCircularCurveByPVIAndLength(pvi, length);
oProfile.Entities.AddFreeCircularCurveByPVIAndThroughPoint(pvi, passPoint);
```

### Managing Entities

```csharp
// Iterate entities
foreach (ProfileEntity entity in oProfile.Entities)
{
    ed.WriteMessage("Entity type: {0}\n", entity.EntityType);
}

// Access by index or ID
ProfileEntity ent = oProfile.Entities[0];
ProfileEntity entById = oProfile.Entities.EntityAtId(entityId);
uint first = oProfile.Entities.FirstEntity;
uint last = oProfile.Entities.LastEntity;

// Remove entities
oProfile.Entities.Remove(entity);
oProfile.Entities.RemoveAt(index);
oProfile.Entities.Clear();
```

## Points of Vertical Intersection (PVIs)

The intersection point of two adjacent tangents:

```csharp
// Find PVI closest to station 1000, elevation -70
ProfilePVI pvi = oProfile.PVIs.GetPVIAt(1000, -70);
ed.WriteMessage("PVI at station: {0}\n", pvi.RawStation);

// Add a plain PVI (sharp point, no vertical curve)
ProfilePVI newPvi = oProfile.PVIs.AddPVI(607.4, -64.3);
newPvi.Elevation -= 2.0; // Adjust elevation

// Add PVI with a vertical curve already attached
ProfilePVI arcPvi = oProfile.PVIs.AddPVIArc(station, elevation, radius);
ProfilePVI symPvi = oProfile.PVIs.AddPVISymParabola(station, elevation, curveLength);
ProfilePVI asymPvi = oProfile.PVIs.AddPVIAsymParabola(station, elevation, tangentLen1, tangentLen2);

// Remove PVI (multiple overloads)
oProfile.PVIs.RemoveAt(station, elevation);   // by closest station+elevation
oProfile.PVIs.RemoveAt(index);                // by index
oProfile.PVIs.Remove(pvi);                    // by object reference
```

### PVI Properties

```csharp
ProfilePVI pvi = oProfile.PVIs[0];
double station = pvi.RawStation;        // use RawStation (Station is deprecated since Civil 2024)
double elevation = pvi.Elevation;
double gradeIn = pvi.GradeIn;
double gradeOut = pvi.GradeOut;
ProfileEntityType pviType = pvi.PVIType;
uint entityBefore = pvi.EntityBefore;
uint entityAfter = pvi.EntityAfter;
ProfileEntity vertCurve = pvi.VerticalCurve;

// Sight distance properties
double stopping = pvi.StoppingSightDistance;
double passing = pvi.PassingSightDistance;
double headlight = pvi.HeadlightSightDistance;
```

**Note:** PVIs are identified by station+elevation (no name/ID). `GetPVIAt` and `RemoveAt(station, elevation)` find the CLOSEST match.

## Profile Views

### Creating a Single Profile View

```csharp
Point3d insertionPoint = new Point3d(100, 100, 0);

// Minimal overload (uses default styles)
ObjectId profileViewId = ProfileView.Create(alignId, insertionPoint);

// With name, band set, and style
ObjectId profileViewId = ProfileView.Create(
    alignId, insertionPoint, "New Profile View",
    bandSetStyleId, profileViewStyleId);

// With split options
ObjectId profileViewId = ProfileView.Create(
    alignId, insertionPoint, "New Profile View",
    bandSetStyleId, profileViewStyleId, splitOptions);
```

### Creating Stacked Profile Views

Returns multiple profile view IDs for stacked display:

```csharp
// Stacked views
ObjectIdCollection pvIds = ProfileView.Create(
    alignId, insertionPoint, stackedOptions);

// Stacked with name and band set
ObjectIdCollection pvIds = ProfileView.Create(
    alignId, insertionPoint, "Profile View",
    bandSetStyleId, stackedOptions);

// Stacked with split options
ObjectIdCollection pvIds = ProfileView.Create(
    alignId, insertionPoint, "Profile View",
    bandSetStyleId, stackedOptions, splitOptions);
```

### Creating Multiple Profile Views (Station-Range Segments)

Splits the alignment into multiple profile views by station range:

```csharp
// Minimal
ObjectIdCollection pvIds = ProfileView.CreateMultiple(
    alignId, insertionPoint, multipleOptions);

// With name, band set, style, split, and datum
ObjectIdCollection pvIds = ProfileView.CreateMultiple(
    alignId, insertionPoint, "Profile View",
    bandSetStyleId, profileViewStyleId,
    multipleOptions, splitOptions, datumType);

// With stacked and multiple combined
ObjectIdCollection pvIds = ProfileView.CreateMultiple(
    alignId, insertionPoint, stackedOptions, multipleOptions);
```

### Profile View Properties

```csharp
ProfileView pv = ts.GetObject(pvId, OpenMode.ForWrite) as ProfileView;

// Alignment info
ObjectId alignId = pv.AlignmentId;
string alignName = pv.AlignmentName;

// Station range
StationRangeType staMode = pv.StationRangeMode;
double staStart = pv.StationStart;
double staEnd = pv.StationEnd;

// Elevation range
ElevationRangeType elevMode = pv.ElevationRangeMode;
double elevMin = pv.ElevationMin;
double elevMax = pv.ElevationMax;

// Split profile view
pv.SplitProfileView = true;
pv.SplitHeight = 5.0;
pv.SplitStationMode = SplitStationType.Manual;
```

### Coordinate Conversion

Convert between drawing XY coordinates and station/elevation:

```csharp
double station = 0, elevation = 0;
bool found = pv.FindStationAndElevationAtXY(x, y, ref station, ref elevation);

double x = 0, y = 0;
bool found = pv.FindXYAtStationAndElevation(station, elevation, ref x, ref y);
```

### Getting Profiles and Labels in a Profile View

```csharp
// Available label collections
ObjectIdCollection pvLabels = pv.GetProfileViewLabelIds();
ObjectIdCollection pipeLabels = pv.GetAvailablePipeProfileLabelIds();
ObjectIdCollection spanLabels = pv.GetAvailableSpanningPipeProfileLabelIds();
ObjectIdCollection structLabels = pv.GetAvailableStructureProfileLabelIds();
ObjectIdCollection pressureParts = pv.GetPressureNetworkPartsInGraph();
```

### Profile View Band Sets

Bands display tabular data below or above the profile view (station, elevation, cut/fill, etc.):

```csharp
ProfileView pv = ts.GetObject(pvId, OpenMode.ForWrite) as ProfileView;
ProfileViewBandSet bandSet = pv.Bands;

// Get current band items
ProfileViewBandItemCollection topBands = bandSet.GetTopBandItems();
ProfileViewBandItemCollection bottomBands = bandSet.GetBottomBandItems();

// Modify band items
foreach (ProfileViewBandItem band in bottomBands)
{
    band.Profile1Id = profileId;
    band.Profile2Id = existingGroundProfileId;
    band.AlignmentId;  // read-only, set at creation
}

// Apply modified band items back
bandSet.SetBottomBandItems(bottomBands);
bandSet.SetTopBandItems(topBands);

// Create a new band item collection
ProfileViewBandItemCollection newBands = new ProfileViewBandItemCollection(
    pvId, BandLocationType.Bottom);
```

### Profile View Overrides

```csharp
// Profile display overrides in this view
ProfileOverrideCollection overrides = pv.GraphOverrides;

// Pipe and structure overrides
PipeOverrideCollection pipeOverrides = pv.PipeOverrides;
StructureOverrideCollection structOverrides = pv.StructureOverrides;

// Hatch areas between profiles
ProfileHatchAreaCollection hatchAreas = pv.HatchAreas;
```

## Profile View Styles

```csharp
ObjectId pvStyleId = doc.Styles.ProfileViewStyles.Add("New Style");
ProfileViewStyle pvStyle = ts.GetObject(pvStyleId, OpenMode.ForWrite)
    as ProfileViewStyle;
```

Style components:
- **Axes:** `BottomAxis`, `TopAxis`, `LeftAxis`, `RightAxis` (all `AxisStyle` type)
- **Graph:** `GraphStyle` - overall graph appearance
- **Grid lines:** `GetDisplayStylePlan(ProfileViewDisplayStyleType type)` — e.g. `GridAtHGP` for horizontal geometry point grid lines, `GridHorizontalMajor`/`GridHorizontalMinor`/`GridVerticalMajor`/`GridVerticalMinor` for regular grid

### Axis Style Properties

Each axis style controls:
- Axis line display style
- Tick marks and text along the axis
- Title annotation

```csharp
AxisStyle bottomAxis = pvStyle.BottomAxis;
```

## Profile Styles

```csharp
ObjectId styleId = doc.Styles.ProfileStyles.Add("My Profile Style");
ProfileStyle style = ts.GetObject(styleId, OpenMode.ForWrite) as ProfileStyle;

// Display style types for profiles
style.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.Arrow).Visible = true;
style.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.Line).Color =
    Color.FromColorIndex(ColorMethod.ByAci, 50); // yellow
style.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.Curve).Color =
    Color.FromColorIndex(ColorMethod.ByAci, 80); // green
style.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.SymmetricalParabola).Color =
    Color.FromColorIndex(ColorMethod.ByAci, 81);
style.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.AsymmetricalParabola).Color =
    Color.FromColorIndex(ColorMethod.ByAci, 83);

// Extension styles (grey)
style.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.LineExtension).Color =
    Color.FromColorIndex(ColorMethod.ByAci, 251);
style.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.ParabolicCurveExtension).Color =
    Color.FromColorIndex(ColorMethod.ByAci, 251);
```

### ProfileDisplayStyleProfileType Enum Values

- `Arrow` - direction arrows
- `Line` - straight segments
- `LineExtension` - line extensions beyond profile
- `Curve` - curved segments
- `ParabolicCurveExtension` - parabola extensions
- `SymmetricalParabola` - symmetric parabolic curves
- `AsymmetricalParabola` - asymmetric parabolic curves

## Gotchas

- `CreateByLayout` creates a profile with NO elevation data - must add entities or PVIs
- Profile entity points use `Point2d(station, elevation)` coordinates (the `Point3d` overloads are deprecated since Civil 2011)
- PVIs have no unique ID - identified by closest station+elevation match
- Use `RawStation` on PVI objects (`Station` is deprecated since Civil 2024)
- Profile styles should set both Profile and Model (3D) display properties
- Named styles must exist in the document or calls will fail
- `ProfileView.Create(CivilDocument, ...)` overloads are deprecated since Civil 2013; use the `Create(ObjectId alignmentId, ...)` overloads instead

## Related Skills

- `c3d-alignments` - Alignments that profiles are based on
- `c3d-surfaces` - Surface profiles (`CreateFromSurface`)
- `c3d-corridors` - Corridors use alignment+profile as baselines
- `c3d-label-styles` - Profile label styles
