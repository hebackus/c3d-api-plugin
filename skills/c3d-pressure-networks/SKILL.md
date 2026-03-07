---
name: c3d-pressure-networks
description: Pressure pipes, fittings, appurtenances, pressure parts lists, design checks, pressure network creation, pressure network labels
---

# Civil 3D Pressure Networks

Use this skill when creating, modifying, or querying pressure pipe networks, fittings, appurtenances, or pressure parts lists.

## Overview

Pressure pipe networks represent pressurized utility systems such as water distribution, fire protection, gas, and irrigation lines. Unlike gravity networks (which rely on slope and invert elevations), pressure networks are defined by operating pressure, pipe material ratings, and connection fittings. Pressure networks have three part categories — pipes, fittings, and appurtenances — compared to gravity networks which have pipes and structures.

Key differences from gravity networks:
- Pipes have pressure ratings and material specifications rather than slope-driven inverts
- Connections use fittings (tees, bends, crosses) instead of structures (manholes, catch basins)
- Appurtenances (valves, hydrants, meters) have no gravity equivalent
- Parts lists are separate: pressure parts list vs gravity parts list
- Label style collections use three separate accessor methods, not a single hierarchy

## Accessing Pressure Networks

### Enumerating Networks

```csharp
CivilDocument doc = CivilApplication.ActiveDocument;

// Get all pressure network IDs — note the method name includes "PressurePipe"
ObjectIdCollection networkIds = doc.GetPressurePipeNetworkIds();

foreach (ObjectId netId in networkIds)
{
    PressurePipeNetwork pn = ts.GetObject(netId, OpenMode.ForRead) as PressurePipeNetwork;
    ed.WriteMessage($"\nNetwork: {pn.Name}");

    ObjectIdCollection pipeIds = pn.GetPipeIds();
    ObjectIdCollection fittingIds = pn.GetFittingIds();
    ObjectIdCollection appurtIds = pn.GetAppurtenanceIds();
    ed.WriteMessage($"  Pipes: {pipeIds.Count}, Fittings: {fittingIds.Count}, " +
                    $"Appurtenances: {appurtIds.Count}");
}
```

### Opening a Specific Network by Name

```csharp
ObjectIdCollection networkIds = doc.GetPressurePipeNetworkIds();
foreach (ObjectId netId in networkIds)
{
    PressurePipeNetwork pn = ts.GetObject(netId, OpenMode.ForRead) as PressurePipeNetwork;
    if (pn.Name == targetName)
    {
        ProcessNetwork(pn, ts);
        break;
    }
}
```

## Pressure Network Properties

- Name (string, get/set) — network display name
- Description (string, get/set) — user description
- PartsListId (ObjectId, get/set) — pressure parts list governing available sizes
- ReferenceAlignmentId (ObjectId, get/set) — alignment for station/offset reporting; may be `ObjectId.Null`
- ReferenceSurfaceId (ObjectId, get/set) — surface for cover depth calculations; may be `ObjectId.Null`

```csharp
PressurePipeNetwork pn = ts.GetObject(netId, OpenMode.ForRead) as PressurePipeNetwork;

string name = pn.Name;
ObjectId partsListId = pn.PartsListId;
ObjectId refAlignmentId = pn.ReferenceAlignmentId;
ObjectId refSurfaceId = pn.ReferenceSurfaceId;
```

## Pressure Pipes

### PressurePipe Properties

- Name (string, get/set) — pipe display name
- Length (double, get) — pipe centerline length
- InnerDiameter (double, get) — inside diameter
- OuterDiameter (double, get) — outside diameter
- Material (string, get) — pipe material description
- StartPoint (Point3d, get/set) — start coordinate
- EndPoint (Point3d, get/set) — end coordinate
- Slope (double, get) — rise/run ratio
- PressureRating (double, get) — maximum operating pressure
- StartConnection (ObjectId, get) — fitting/appurtenance at start
- EndConnection (ObjectId, get) — fitting/appurtenance at end

```csharp
ObjectIdCollection pipeIds = pn.GetPipeIds();

foreach (ObjectId pipeId in pipeIds)
{
    PressurePipe pipe = ts.GetObject(pipeId, OpenMode.ForRead) as PressurePipe;

    ed.WriteMessage($"\n  Pipe: {pipe.Name}, Length={pipe.Length:F2}, " +
                    $"ID={pipe.InnerDiameter:F2}, Material={pipe.Material}, " +
                    $"Rating={pipe.PressureRating:F0} psi");
}
```

## Fittings

Fittings are connection points where pipes meet — tees, bends, crosses, reducers, and couplings.

```csharp
ObjectIdCollection fittingIds = pn.GetFittingIds();

foreach (ObjectId fId in fittingIds)
{
    PressureFitting fitting = ts.GetObject(fId, OpenMode.ForRead) as PressureFitting;

    string fittingType = fitting.FittingType;
    Point3d location = fitting.Location;
    ObjectIdCollection connectedPipes = fitting.GetConnectedPipeIds();
    string partDesc = fitting.PartDescription;

    ed.WriteMessage($"\n  Fitting: {fitting.Name}, Type={fittingType}, " +
                    $"Connections={connectedPipes.Count}");
}
```

### Fitting Types

- **Bend** — two-port, changes direction at a specified angle
- **Tee** — three-port, branch connection
- **Cross** — four-port, intersection
- **Reducer** — two-port, transitions between pipe sizes
- **Coupling** — two-port, joins pipes of the same size

## Appurtenances

Appurtenances are inline or terminal devices — valves, hydrants, meters, blowoffs, and similar functional devices.

```csharp
ObjectIdCollection appIds = pn.GetAppurtenanceIds();

foreach (ObjectId aId in appIds)
{
    PressureAppurtenance app = ts.GetObject(aId, OpenMode.ForRead) as PressureAppurtenance;

    string appType = app.AppurtenanceType;
    Point3d location = app.Location;

    ed.WriteMessage($"\n  Appurtenance: {app.Name}, Type={appType}");
}
```

### Fitting vs Appurtenance Distinction

Both are point objects in the network. The key difference:
- **Fittings** are structural connections — they exist to join pipes (tees, bends, crosses)
- **Appurtenances** are functional devices — they exist to control or measure flow (valves, hydrants)

In the API, both have `Location` and connection properties, but their part families and label style collections are separate.

## Design Checks

### Cover Depth

```csharp
// Cover depth is calculated relative to the reference surface
PressurePipeNetwork pn = ts.GetObject(netId, OpenMode.ForRead) as PressurePipeNetwork;

if (pn.ReferenceSurfaceId != ObjectId.Null)
{
    foreach (ObjectId pipeId in pn.GetPipeIds())
    {
        PressurePipe pipe = ts.GetObject(pipeId, OpenMode.ForRead) as PressurePipe;
        // Cover depth = surface elevation - pipe crown elevation
    }
}
```

### Deflection Angle Checks

Deflection angles at fittings are validated against the maximum allowable angle for the fitting type and size. Bends have defined maximum deflection; pipes arriving at a fitting exceeding the rated angle trigger a design check violation.

### Pipe Length Constraints

Design checks can enforce minimum and maximum pipe lengths based on material and size specifications from the parts list.

## Pressure Network Labels

### Label Style Hierarchy

Pressure network label styles use **three separate accessor methods** on the label styles root — one each for pipes, fittings, and appurtenances:

```csharp
var labelStylesRoot = doc.Styles.LabelStyles;

// 1. Pipe label styles — has PlanProfileLabelStyles and CrossingSectionLabelStyles
var pipeLabelStyles = labelStylesRoot.GetPressurePipeLabelStyles();
var pipePlanProfileStyles = pipeLabelStyles.PlanProfileLabelStyles;
var pipeSectionStyles = pipeLabelStyles.CrossingSectionLabelStyles;

// 2. Fitting label styles — has a flat LabelStyles collection
var fittingLabelStyles = labelStylesRoot.GetPressureFittingLabelStyles();
var fittingStyles = fittingLabelStyles.LabelStyles;

// 3. Appurtenance label styles — has a flat LabelStyles collection
var appLabelStyles = labelStylesRoot.GetPressureAppurtenanceLabelStyles();
var appStyles = appLabelStyles.LabelStyles;
```

### Enumerating All Styles Including Nested

```csharp
// Use GetDescendantIds() to get ALL styles including those in subcategories
var pipeLabelStyles = labelStylesRoot.GetPressurePipeLabelStyles();
ObjectIdCollection allPipePlanStyles =
    pipeLabelStyles.PlanProfileLabelStyles.GetDescendantIds();

foreach (ObjectId styleId in allPipePlanStyles)
{
    LabelStyle style = ts.GetObject(styleId, OpenMode.ForRead) as LabelStyle;
    ed.WriteMessage($"\n  Pipe style: {style.Name}");
}

// Same pattern for fittings and appurtenances
var fittingLabelStyles = labelStylesRoot.GetPressureFittingLabelStyles();
ObjectIdCollection allFittingStyles =
    fittingLabelStyles.LabelStyles.GetDescendantIds();
```

### Adding Labels — Pipes (Plan View)

```csharp
// PressurePipeLabel.Create(pipeId, ratio, styleId)
// ratio: 0.0 = start, 0.5 = midpoint, 1.0 = end
foreach (ObjectId pipeId in pn.GetPipeIds())
{
    ObjectIdCollection existing = PressurePipeLabel.GetAvailableLabelIds(pipeId);
    if (existing.Count == 0)
    {
        ObjectId labelId = PressurePipeLabel.Create(pipeId, 0.5, pipePlanStyleId);
    }
}
```

### Adding Labels — Fittings and Appurtenances (Plan View)

```csharp
// PressureFittingLabel.Create(fittingId, styleId, ratio, direction)
foreach (ObjectId fId in pn.GetFittingIds())
{
    ObjectIdCollection existing = PressureFittingLabel.GetAvailableLabelIds(fId);
    if (existing.Count == 0)
    {
        ObjectId labelId = PressureFittingLabel.Create(
            fId, fittingPlanStyleId, 0.5, new Vector3d(1, 0, 0));
    }
}

// PressureAppurtenanceLabel.Create — same signature as fittings
foreach (ObjectId aId in pn.GetAppurtenanceIds())
{
    ObjectIdCollection existing = PressureAppurtenanceLabel.GetAvailableLabelIds(aId);
    if (existing.Count == 0)
    {
        ObjectId labelId = PressureAppurtenanceLabel.Create(
            aId, appPlanStyleId, 0.5, new Vector3d(1, 0, 0));
    }
}
```

### Common Pressure Label Property Fields

| Property Field | Description |
|----------------|-------------|
| Pressure Pipe Length | Pipe centerline length |
| Pressure Pipe Inner Diameter | Inside diameter |
| Pressure Pipe Outer Diameter | Outside diameter |
| Pressure Pipe Material | Material description |
| Pressure Pipe Slope | Pipe slope |
| Pressure Rating | Maximum operating pressure |
| Fitting Type | Tee, bend, cross, etc. |
| Appurtenance Type | Valve, hydrant, etc. |
| Cover Depth | Depth below reference surface |
| Station | Station along reference alignment |
| Offset | Offset from reference alignment |

## Gotchas

- **Class name is `PressurePipeNetwork`, not `PressureNetwork`.** The gravity class is `Network`; the pressure class is `PressurePipeNetwork`. Don't confuse the two — casting between them fails.

- **Document method is `GetPressurePipeNetworkIds()`.** Not `GetPressureNetworkIds()`. The naming follows the class name convention.

- **Label style hierarchy uses three separate method calls.** `GetPressurePipeLabelStyles()`, `GetPressureFittingLabelStyles()`, and `GetPressureAppurtenanceLabelStyles()` — each returns a different object with different sub-properties.

- **Pipe label styles have `PlanProfileLabelStyles` (combined).** Not separate plan and profile collections. Section styles are at `CrossingSectionLabelStyles` (note the "Crossing" prefix).

- **Fitting and appurtenance styles use a flat `LabelStyles` property.** Not split by view type like pipes. The same collection is used for all views.

- **`PressurePipeLabel.Create` signature is `(pipeId, ratio, styleId)`.** Ratio comes before styleId, unlike some gravity label methods.

- **`PressureFittingLabel.Create` requires 4 parameters.** `(fittingId, styleId, ratio, directionVector)` — the `Vector3d` direction parameter controls label placement angle.

- **Use `GetDescendantIds()` for all style enumeration.** Iterating with `foreach` only yields direct children. Always use `GetDescendantIds()` to retrieve nested styles.

- **Three label categories, not two.** Pressure networks require separate label style selections for pipes, fittings, and appurtenances. Forgetting appurtenance labels is a common oversight.

- **Parts list compatibility.** A pressure parts list is not interchangeable with a gravity parts list. Verify the type before assignment.

- **Null reference alignment/surface.** `ReferenceAlignmentId` and `ReferenceSurfaceId` can be `ObjectId.Null`. Always check before using them for station/offset or cover depth calculations.

- **Check existing labels before creating.** Use `PressurePipeLabel.GetAvailableLabelIds()` (and the fitting/appurtenance equivalents) to avoid duplicate labels.

- **Profile view labels use crossing syntax.** Pressure pipes appear in profile views as crossings. Use `ProfileView.GetPressureNetworkPartsInGraph()` to find parts visible in a specific profile view.

- **Transaction scope for modifications.** Adding pipes, fittings, and appurtenances must occur within the same transaction or in the correct order. Adding a pipe that references an uncommitted fitting will fail.

## Related Skills

- `c3d-pipe-networks` — gravity pipe networks (complementary skill covering pipes, structures, and gravity-specific labeling)
- `c3d-alignments` — reference alignments for pressure network layout and station/offset reporting
- `c3d-surfaces` — reference surfaces for cover depth checks and vertical placement
- `c3d-profiles` — profile views showing pressure network crossings and vertical relationships
- `c3d-label-styles` — general label style configuration, text components, and expression usage
- `c3d-root-objects` — CivilDocument access, transaction patterns, and document-level collections
