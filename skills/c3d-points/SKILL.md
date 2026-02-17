---
name: c3d-points
description: COGO points, point groups, user-defined properties (UDPs), point styles, label styles, description keys, and bulk editing
---

# Civil 3D Points

Use this skill when working with COGO points - creating, querying, grouping, styling, or using description keys.

## Points Collection

All points are in `CivilDocument.CogoPoints` (`CogoPointCollection`):

```csharp
CogoPointCollection cogoPoints = doc.CogoPoints;

// Add individual point
ObjectId pointId = cogoPoints.Add(new Point3d(4958, 4079, 200));

// Add multiple points
Point3d[] pts = { new Point3d(4927, 3887, 150), new Point3d(5101, 3660, 250) };
cogoPoints.Add(new Point3dCollection(pts));

// Add with description
cogoPoints.Add(new Point3d(100, 200, 225), "GRND");

// Iterate
foreach (ObjectId pointId in cogoPoints)
{
    CogoPoint pt = pointId.GetObject(OpenMode.ForRead) as CogoPoint;
    ed.WriteMessage("Point #{0}: Elev={1}\n", pt.PointNumber, pt.Elevation);
}

// Remove by point number
cogoPoints.Remove(779);
```

## CogoPoint Properties

```csharp
CogoPoint pt = pointId.GetObject(OpenMode.ForWrite) as CogoPoint;

// Settable properties
pt.PointName = "point1";
pt.RawDescription = "Point description";
pt.PointNumber = 100;    // Throws if number already exists
pt.Renumber(100);        // Uses conflict resolution settings

// Read-only
string fullDesc = pt.FullDescription;  // Read-only after creation
Point3d location = pt.Location;        // Read-only, use Easting/Northing/Elevation

// Position (read/write)
double easting = pt.Easting;
double northing = pt.Northing;
double elevation = pt.Elevation;

// Grid coordinates
double gridE = pt.GridEasting;
double gridN = pt.GridNorthing;

// Geographic coordinates
double lat = pt.Latitude;
double lon = pt.Longitude;

// Project points
if (pt.IsProjectPoint)
{
    bool checkedOut = pt.IsCheckedOut;
    int version = pt.ProjectVersion;
}

// Override values (read-only, set by PointGroup)
// pt.ElevationOverride, pt.FullDescriptionOverride
// pt.LabelStyleIdOverride, pt.StyleIdOverride
```

## Bulk Editing

`CogoPointCollection` provides bulk methods with three overloads each:
1. Single point by ObjectId
2. All points in list to single value
3. All points in list to corresponding values

```csharp
// Set elevation offset for all points
cogoPoints.SetElevationByOffset(cogoPoints, 3.00);

// Set raw description for all points
cogoPoints.SetRawDescription(cogoPoints, "NEW_DESC");

// Set full description format ($* = same as raw description)
cogoPoints.SetDescriptionFormat(cogoPoints, "$*");

// Also available: SetPointNumber, SetStyleId, SetLabelStyleId, etc.
```

## Point Groups

Point groups define subsets of points. All groups in `doc.PointGroups`.

```csharp
// Create
ObjectId pgId = doc.PointGroups.Add("My Point Group");
PointGroup pg = pgId.GetObject(OpenMode.ForWrite) as PointGroup;

// Special group: all points
ObjectId allPtsId = doc.PointGroups.AllPointGroupsId;

// Check membership
if (pg.ContainsPoint(cogoPoint.PointNumber))
    ed.WriteMessage("Point is in group\n");

// Override elevations for all points in group
pg.ElevationOverride.FixedElevation = 100;
pg.ElevationOverride.ActiveOverrideType = PointGroupOverrideType.FixedValue;
pg.IsElevationOverriden = true;
```

### Standard Queries

Match points by descriptions, elevations, names, numbers:

```csharp
StandardPointGroupQuery query = new StandardPointGroupQuery();
query.IncludeElevations = "100-200";        // Range
query.IncludeFullDescriptions = "FLO*";     // Wildcard
query.IncludeNumbers = ">2200";             // Greater than
query.ExcludeElevations = "150-155";
query.ExcludeNames = "BRKL";
query.UseCaseSensitiveMatch = true;

pg.SetQuery(query);
pg.Update();  // Apply the query

ed.WriteMessage("Selected: {0} points\nQuery: {1}\n",
    pg.PointsCount, query.QueryString);
// Output query: (FullDescription='FLO*' OR PointElevation=100-200 OR
//   PointNumber>2200) AND NOT(Name='BRKL' OR PointElevation=150-155)
```

**Include/Exclude property values:**
- Single number: `"110.01"`
- Range: `"1-100"`
- Greater/less than: `">200"`, `"<-100"`
- Multiple (comma-separated): `"<-100,1-100,110.01,>200"`
- Wildcards in descriptions/names: `"IP*"`, `"?X*"`

All `Include*` properties are ORed; all `Exclude*` properties are ORed. Final query = (Includes) AND NOT (Excludes).

### Custom Queries

For nested queries not expressible with StandardQuery:

```csharp
CustomPointGroupQuery customQuery = new CustomPointGroupQuery();
customQuery.QueryString =
    "(RawDescription='GR*') AND (PointElevation>=100 AND PointElevation<=300)";
pg.SetQuery(customQuery);
pg.Update();
```

Operators: `=`, `>`, `<`, `>=`, `<=`, `AND`, `OR`, `NOT`, parentheses for grouping.

### Pending Changes

```csharp
PointGroupChangeInfo changes = pg.GetPendingChanges();
ed.WriteMessage("To add: {0}, To remove: {1}\n",
    changes.PointsToAdd.Length, changes.PointsToRemove.Length);
pg.Update(); // Apply pending changes
```

Changes are registered when points matching the query are added/removed, NOT when the query itself changes.

## User-Defined Properties (UDPs)

UDPs attach custom data to points, organized in classifications:

```csharp
// Create classification
UDPClassification udpClass = doc.PointUDPClassifications.Add("Example");

// Create UDP (integer with bounds)
AttributeTypeInfoInt attrInfo = new AttributeTypeInfoInt("Int UDP");
attrInfo.DefaultValue = 15;
attrInfo.UpperBoundValue = 20;
attrInfo.LowerBoundValue = 10;
UDP udp = udpClass.CreateUDP(attrInfo);

// Assign classification to point group
PointGroup pg = pgId.GetObject(OpenMode.ForWrite) as PointGroup;
pg.UseCustomClassification("Example");
```

### UDP Types

| Type | Class | Extra Properties |
|------|-------|-----------------|
| Integer | `UDPInteger` | `UpperBoundValue`, `LowerBoundValue`, `*Inclusive` |
| Double | `UDPDouble` | `UpperBoundValue`, `LowerBoundValue`, `*Inclusive` |
| String | `UDPString` | (none) |
| Boolean | `UDPBoolean` | (none) |
| Enumeration | `UDPEnumeration` | `GetEnumValues()` |

### AttributeTypeInfo Classes

- `AttributeTypeInfoInt` - integer with bounds
- `AttributeTypeInfoDouble` - double with bounds
- `AttributeTypeInfoString` - string
- `AttributeTypeInfoBool` - boolean
- `AttributeTypeInfoEnum` - enumeration

`CreateUDP()` accepts an optional GUID parameter to create identical UDPs across drawings.

### Listing UDPs

```csharp
foreach (UDPClassification udpClass in doc.PointUDPClassifications)
{
    foreach (UDP udp in udpClass.UDPs)
    {
        ed.WriteMessage("UDP: {0}, GUID: {1}, Default: {2}\n",
            udp.Name, udp.Guid, udp.DefaultValue);
    }
}
```

## Point Styles

```csharp
ObjectId styleId = doc.Styles.PointStyles.Add("My Point Style");
PointStyle style = styleId.GetObject(OpenMode.ForWrite) as PointStyle;

// Marker type
style.MarkerType = PointMarkerDisplayType.UseCustomMarker;
style.CustomMarkerStyle = CustomMarkerType.CustomMarkerPlus;
style.CustomMarkerSuperimposeStyle = CustomMarkerSuperimposeType.Square;

// For symbol markers
style.MarkerSymbolName = "BLOCK_NAME"; // AutoCAD block in drawing

// Assign to point
cogoPoint.StyleId = styleId;
```

Display settings accessed via `GetDisplay*()`, `GetLabelDisplay*()`, `GetMarkerDisplay*()` methods for Model, Plan, Profile, or Section views.

## Point Label Styles

```csharp
// Access via
var labelStyles = doc.Styles.LabelStyles.PointLabelStyles;

// Assign to point
cogoPoint.LabelStyleId = labelStyleId;
```

### Point Label Property Fields

```
<[Name(CP)]>
<[Point Number]>
<[Northing(Uft|P4|RN|AP|Sn|OF)]>
<[Easting(Uft|P4|RN|AP|Sn|OF)]>
<[Raw Description(CP)]>
<[Full Description(CP)]>
<[Point Elevation(Uft|P3|RN|AP|Sn|OF)]>
<[Latitude(Udeg|FDMSdSp|P6|RN|DPSn|CU|AP|OF)]>
<[Longitude(Udeg|FDMSdSp|P6|RN|DPSn|CU|AP|OF)]>
<[Grid Northing(Uft|P4|RN|AP|Sn|OF)]>
<[Grid Easting(Uft|P4|RN|AP|Sn|OF)]>
<[Scale Factor(P3|RN|AP|OF)]>
<[Convergence(Udeg|FDMSdSp|P6|RN|AP|OF)]>
<[Survey Point]>
```

## Description Keys

Automatically apply styles and settings to points by matching descriptions:

```csharp
// Create key set
ObjectId keySetId = PointDescriptionKeySetCollection
    .GetPointDescriptionKeySets(acaddoc.Database)
    .Add("My Key Set");
PointDescriptionKeySet keySet = keySetId.GetObject(OpenMode.ForWrite)
    as PointDescriptionKeySet;

// Create key matching "GRND*"
ObjectId keyId = keySet.Add("GRND*");
PointDescriptionKey key = keyId.GetObject(OpenMode.ForWrite) as PointDescriptionKey;

// Apply style and label style
key.StyleId = pointStyleId;
key.ApplyStyleId = true;
key.LabelStyleId = labelStyleId;
key.ApplyLabelStyleId = true;

// Scale from description parameter
key.ApplyDrawingScale = false;
key.ScaleParameter = 1;
key.ApplyScaleParameter = true;
key.ApplyScaleXY = true;

// Fixed rotation
key.FixedMarkerRotation = 0.785398163; // radians (45 degrees)
key.RotationDirection = RotationDirType.Clockwise;
key.ApplyFixedMarkerRotation = true;

// Set search order (priority)
var allKeySets = PointDescriptionKeySetCollection
    .GetPointDescriptionKeySets(acaddoc.Database);
ObjectIdCollection searchOrder = allKeySets.SearchOrder;
// Rearrange searchOrder as needed
allKeySets.SearchOrder = searchOrder;

// Apply to point group
pointGroup.ApplyDescriptionKeys();
```

Wildcards `?` and `*` are supported in the `Code` property.

## Using Points with TIN Surfaces

```csharp
// Add point group to surface
TinSurface surface = ...;
// surface.PointGroupsDefinition - collection exists but adding is NOT supported via API
```

## Gotchas

- `PointNumber` setter throws if number exists; use `Renumber()` for conflict resolution
- `FullDescription` is read-only after point creation
- `Location` is read-only; modify via `Easting`, `Northing`, `Elevation`
- Accessing `IsCheckedOut`/`ProjectVersion` on non-project points throws
- Point group overrides take precedence over individual point settings
- `StandardPointGroupQuery` ORs all includes and ORs all excludes
- Pending changes aren't registered when the query itself changes, only when matching points are added/removed
- Adding point groups to TIN surfaces is NOT supported via .NET API
- Description key search order determines priority when multiple keys match

## Related Skills

- `c3d-label-styles` - Point label style creation
- `c3d-surfaces` - Points as surface data
- `c3d-root-objects` - Accessing point collections
