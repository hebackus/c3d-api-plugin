---
name: c3d-profiles
description: Profile creation (from surface and by layout), profile views, PVIs, profile styles, and profile view styles
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

## Creating a Profile from a Surface

Derives elevation data from a surface along an alignment path:

```csharp
ObjectId alignId = ed.GetEntity(opt).ObjectId;
Alignment oAlignment = ts.GetObject(alignId, OpenMode.ForRead) as Alignment;
ObjectId layerId = oAlignment.LayerId;

ObjectId surfaceId = doc.GetSurfaceIds()[0];
ObjectId styleId = doc.Styles.ProfileStyles[0];
ObjectId labelSetId = doc.Styles.LabelSetStyles.ProfileLabelSetStyles[0];

ObjectId profileId = Profile.CreateFromSurface(
    "My Profile", alignId, surfaceId, layerId, styleId, labelSetId);
ts.Commit();
```

## Creating a Profile by Layout (Entity-Based)

Creates an empty profile, then defines shape with entities:

```csharp
ObjectId styleId = doc.Styles.ProfileStyles["Standard"];
ObjectId labelSetId = doc.Styles.LabelSetStyles.ProfileLabelSetStyles["Standard"];

ObjectId profileId = Profile.CreateByLayout(
    "My Profile", alignId, layerId, styleId, labelSetId);

Profile oProfile = ts.GetObject(profileId, OpenMode.ForRead) as Profile;
```

### Adding Entities

```csharp
// Fixed tangent (straight line between two points)
// Points are (station, elevation, 0)
Point3d startPoint = new Point3d(alignment.StartingStation, -40, 0);
Point3d endPoint = new Point3d(758.2, -70, 0);
ProfileTangent tangent1 = oProfile.Entities.AddFixedTangent(startPoint, endPoint);

startPoint = new Point3d(1508.2, -60.0, 0);
endPoint = new Point3d(alignment.EndingStation, -4.0, 0);
ProfileTangent tangent2 = oProfile.Entities.AddFixedTangent(startPoint, endPoint);

// Symmetric parabola connecting two tangents (sag curve)
oProfile.Entities.AddFreeSymmetricParabolaByLength(
    tangent1.EntityId, tangent2.EntityId,
    VerticalCurveType.Sag, 900.1, true);
```

### Entity Types

The `ProfileEntityCollection` supports:
- `AddFixedTangent()` - straight segments
- `AddFreeSymmetricParabolaByLength()` - symmetric parabolic curves
- Asymmetric parabolas and other curve types

## Points of Vertical Intersection (PVIs)

The intersection point of two adjacent tangents:

```csharp
// Find PVI closest to station 1000, elevation -70
ProfilePVI pvi = oProfile.PVIs.GetPVIAt(1000, -70);
ed.WriteMessage("PVI at station: {0}\n", pvi.Station);

// Add a new PVI
ProfilePVI newPvi = oProfile.PVIs.AddPVI(607.4, -64.3);
newPvi.Elevation -= 2.0; // Adjust elevation

// Remove PVI
oProfile.PVIs.RemoveAt(station, elevation);
```

**Note:** PVIs are identified by station+elevation (no name/ID). `GetPVIAt` and `RemoveAt` find the CLOSEST match.

## Profile Views

### Creating a Profile View

```csharp
Point3d insertionPoint = new Point3d(100, 100, 0);

ObjectId bandSetStyleId = doc.Styles.ProfileViewBandSetStyles["Standard"];
// Fallback if named style doesn't exist:
if (bandSetStyleId == null)
    bandSetStyleId = doc.Styles.ProfileViewBandSetStyles[0];

ObjectId profileViewId = ProfileView.Create(
    doc, "New Profile View", bandSetStyleId, alignId, insertionPoint);
ts.Commit();
```

Two overloads: one takes ObjectIds, the other takes string names for band set style and alignment.

### Getting Profiles in a Profile View

```csharp
ProfileView pv = ts.GetObject(pvId, OpenMode.ForRead) as ProfileView;
ObjectIdCollection profileIds = pv.GetProfileIds();
```

### Profile View Styles

```csharp
ObjectId pvStyleId = doc.Styles.ProfileViewStyles.Add("New Style");
ProfileViewStyle pvStyle = ts.GetObject(pvStyleId, OpenMode.ForRead)
    as ProfileViewStyle;
```

Style components:
- **Axes:** `BottomAxis`, `TopAxis`, `LeftAxis`, `RightAxis` (all `AxisStyle` type)
- **Graph:** `GraphStyle` - overall graph appearance
- **Grid lines:** `GetDisplayStylePlan()` for horizontal geometry point grid lines

### Axis Style Properties

Each axis style controls:
- Axis line display style
- Tick marks and text along the axis
- Title annotation

```csharp
// Access axis style
AxisStyle bottomAxis = pvStyle.BottomAxis;
// Configure axis display, ticks, titles...
```

## Profile Styles

```csharp
ObjectId styleId = doc.Styles.ProfileStyles.Add("My Profile Style");
ProfileStyle style = ts.GetObject(styleId, OpenMode.ForRead) as ProfileStyle;

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

- `CreateByLayout` creates a profile with NO elevation data - must add entities
- Profile entity points use (station, elevation, 0) coordinates
- PVIs have no unique ID - identified by closest station+elevation match
- Profile styles should set both Profile and Model (3D) display properties
- `Create()` for ProfileView requires a valid band set style
- Named styles must exist in the document or calls will fail

## Related Skills

- `c3d-alignments` - Alignments that profiles are based on
- `c3d-surfaces` - Surface profiles (`CreateFromSurface`)
- `c3d-corridors` - Corridors use alignment+profile as baselines
- `c3d-label-styles` - Profile label styles
