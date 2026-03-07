---
name: c3d-intersections
description: Intersection objects, curb returns, corridor intersection geometry, intersection labels, approach roads, intersection styles
---

# Civil 3D Intersections

Use this skill when querying intersection objects, curb returns, corridor intersection geometry, or intersection labels.

## API Limitations

Intersection creation in Civil 3D is **wizard-driven** — there is no `Intersection.Create()` in the managed .NET API. The Intersection Wizard in the UI handles creation, including curb return generation, corridor region splitting, and approach road configuration. The .NET API provides **read access** to existing intersection objects and their properties.

## Accessing Intersections

Intersections are accessed through `CivilDocument`. Each intersection is an `Intersection` entity in the drawing database.

```csharp
CivilDocument doc = CivilApplication.ActiveDocument;

using (Transaction ts = db.TransactionManager.StartTransaction())
{
    ObjectIdCollection intIds = doc.GetIntersectionIds();
    foreach (ObjectId intId in intIds)
    {
        Intersection ix = ts.GetObject(intId, OpenMode.ForRead) as Intersection;
        ed.WriteMessage("Intersection: {0}, Location: ({1:F2}, {2:F2})\n",
            ix.Name, ix.Location.X, ix.Location.Y);
    }
    ts.Commit();
}
```

## Intersection Properties

- Name (string, get/set) — display name
- Description (string, get/set) — user description
- StyleId (ObjectId, get/set) — intersection display style
- Location (Point2d, get) — 2D point where alignments cross
- RoadwayAlignmentId (ObjectId, get) — main road alignment
- CorridorId (ObjectId, get) — parent corridor (if created within a corridor)

```csharp
Intersection ix = ts.GetObject(intId, OpenMode.ForRead) as Intersection;

// Identity
string name = ix.Name;
ObjectId styleId = ix.StyleId;

// Location — the 2D point where alignments cross
Point2d location = ix.Location;

// Road references
ObjectId mainRoadId = ix.RoadwayAlignmentId;
ObjectIdCollection approachIds = ix.GetApproachIds();
ObjectIdCollection curbReturnIds = ix.GetCurbReturnIds();

// Corridor reference
ObjectId corridorId = ix.CorridorId;
```

### Modifying Properties

```csharp
Intersection ix = ts.GetObject(intId, OpenMode.ForWrite) as Intersection;

ix.Name = "Main St & 1st Ave";
ix.Description = "Signalized 4-way intersection";
ix.StyleId = newStyleId;
```

## Creating Intersections

Intersection creation is **not available** through the managed .NET API. Use the Intersection Wizard via `SendStringToExecute`:

```csharp
// Opens the interactive Intersection Wizard
Document acadDoc = Application.DocumentManager.MdiActiveDocument;
acadDoc.SendStringToExecute("CREATEINTERSECTION ", true, false, false);
```

The wizard requires:
1. A main road alignment
2. One or more approach alignments that geometrically cross the main road
3. A crossing point selection
4. Curb return parameters (radius, widening, etc.)

### Finding the Crossing Point of Two Alignments

To compute where two alignments cross (useful for pre-validation):

```csharp
Alignment mainAlign = ts.GetObject(mainAlignId, OpenMode.ForRead) as Alignment;
Alignment approachAlign = ts.GetObject(approachAlignId, OpenMode.ForRead) as Alignment;

// Entity.IntersectWith works on the visual representation
Point3dCollection crossingPts = new Point3dCollection();
mainAlign.IntersectWith(approachAlign,
    Intersect.OnBothOperands, crossingPts,
    IntPtr.Zero, IntPtr.Zero);

if (crossingPts.Count > 0)
{
    Point2d crossPt = new Point2d(crossingPts[0].X, crossingPts[0].Y);
    ed.WriteMessage("Crossing at: ({0:F2}, {1:F2})\n", crossPt.X, crossPt.Y);
}
```

> **Note:** `Entity.IntersectWith` works on the visual representation and may not account for vertical geometry. Use `Alignment.GetStationAtPoint` to verify the result.

## Curb Returns

Curb returns are the fillet arcs connecting the edge of pavement between the main road and approach road at an intersection. They are child objects created by the Intersection Wizard.

```csharp
Intersection ix = ts.GetObject(intId, OpenMode.ForRead) as Intersection;
ObjectIdCollection curbReturnIds = ix.GetCurbReturnIds();

foreach (ObjectId crId in curbReturnIds)
{
    CurbReturn cr = ts.GetObject(crId, OpenMode.ForRead) as CurbReturn;
    ed.WriteMessage("Curb return: {0}\n", cr.Name);
}
```

### Curb Return Properties

Curb return properties (radius, widening, fillet type) are configured during creation through the wizard. The .NET API provides read access to the resulting alignment and profile objects.

- Name (string, get) — curb return display name
- AlignmentId (ObjectId, get) — the curb return alignment entity
- ProfileId (ObjectId, get) — profile along the curb return

```csharp
CurbReturn cr = ts.GetObject(crId, OpenMode.ForRead) as CurbReturn;
ObjectId crAlignmentId = cr.AlignmentId;
ObjectId crProfileId = cr.ProfileId;

// Access the curb return as an alignment
Alignment crAlign = ts.GetObject(crAlignmentId, OpenMode.ForRead) as Alignment;
ed.WriteMessage("Curb return alignment: {0}, Length: {1:F2}\n",
    crAlign.Name, crAlign.Length);
```

> **Note:** Curb return alignments are child objects of the intersection. They do not appear in the main alignment collection and cannot be independently reparented.

## Intersection Corridor Integration

Intersections and corridors are tightly linked. When an intersection is created within a corridor, Civil 3D automatically generates curb return alignments/profiles and corridor regions for the intersection area.

### Accessing Corridor Intersection Regions

```csharp
Corridor corridor = ts.GetObject(corridorId, OpenMode.ForRead) as Corridor;

foreach (Baseline bl in corridor.Baselines)
{
    foreach (BaselineRegion region in bl.BaselineRegions)
    {
        // Intersection regions are typically named with the intersection name
        ed.WriteMessage("Region: {0}, Start: {1:F2}, End: {2:F2}\n",
            region.Name, region.StartStation, region.EndStation);

        ObjectId assemblyId = region.AssemblyId;
    }
}
```

### Rebuilding After Changes

```csharp
Corridor corridor = ts.GetObject(corridorId, OpenMode.ForWrite) as Corridor;
corridor.Rebuild();
```

### Corridor Surfaces

Intersection corridors contribute to the overall corridor surface:

```csharp
Corridor corridor = ts.GetObject(corridorId, OpenMode.ForRead) as Corridor;

foreach (CorridorSurface cSurf in corridor.CorridorSurfaces)
{
    ed.WriteMessage("Corridor surface: {0}\n", cSurf.Name);
    ObjectId surfId = cSurf.SurfaceId;
}
```

## Approach Roads

Approach roads are the alignments connecting to the main road. An intersection can have multiple approaches (e.g., a 4-way intersection has one main road plus three approaches, or two roads crossing creates a main road plus one approach).

```csharp
Intersection ix = ts.GetObject(intId, OpenMode.ForRead) as Intersection;

// Main road
Alignment mainRoad = ts.GetObject(ix.RoadwayAlignmentId, OpenMode.ForRead) as Alignment;
ed.WriteMessage("Main road: {0}\n", mainRoad.Name);

// Approach roads
ObjectIdCollection approachIds = ix.GetApproachIds();
foreach (ObjectId appId in approachIds)
{
    Alignment approach = ts.GetObject(appId, OpenMode.ForRead) as Alignment;
    ed.WriteMessage("  Approach: {0}\n", approach.Name);
}
```

> **Note:** `GetApproachIds()` returns only approach alignments. The main road is accessed via `RoadwayAlignmentId` — it is not included in the approach collection.

## Intersection Styles and Labels

### Styles

```csharp
// Assign a style to an intersection
Intersection ix = ts.GetObject(intId, OpenMode.ForWrite) as Intersection;
ix.StyleId = doc.Styles.IntersectionStyles["Standard"];
```

### Labels

Intersection labels display name, station on roads, coordinates, and angles between roads.

```csharp
// Set the label style on the intersection
Intersection ix = ts.GetObject(intId, OpenMode.ForWrite) as Intersection;
ix.LabelStyleId = labelStyleId;
```

### Common Label Property Fields

| Property Field | Description |
|----------------|-------------|
| Intersection Name | Name of the intersection object |
| Main Road Name | Name of the main road alignment |
| Main Road Station | Station on the main road at the crossing |
| Approach Road Name | Name of the approach alignment |
| Approach Road Station | Station on the approach road at the crossing |
| Intersection Easting | X coordinate of the intersection point |
| Intersection Northing | Y coordinate of the intersection point |
| Intersection Angle | Angle between the two alignments |

## Gotchas

- **No .NET creation API.** Intersections cannot be created programmatically. Use the `CREATEINTERSECTION` wizard command or `SendStringToExecute`. This is confirmed by Autodesk community forums.
- **Curb return IDs may be empty before corridor rebuild.** After creating an intersection, curb return geometry is not fully generated until the corridor is rebuilt.
- **Approach road direction matters.** The direction (start to end) of the approach alignment affects which side is "left" and "right" for curb returns and offset alignments.
- **Modifying intersection properties requires corridor rebuild.** Changes to curb returns or approach roads don't immediately update the corridor geometry.
- **Multiple intersections on the same alignment.** A single main road can have multiple intersections. Watch for overlapping corridor regions when intersections are close together.
- **GetApproachIds() excludes the main road.** The main road is accessed via `RoadwayAlignmentId`, not from the approach collection.
- **Style assignment requires ForWrite.** Setting `StyleId` or `LabelStyleId` outside a transaction or on a read-only object throws.
- **Intersection deletion cascades.** Deleting an intersection erases its curb return alignments, profiles, and associated corridor regions.
- **Curb return alignments are not standalone.** They are child objects of the intersection, not in the main alignment collection.
- **Intersection regions use special assemblies.** Swapping assemblies without understanding intersection subassembly requirements can produce invalid geometry.

## Related Skills

- `c3d-alignments` — main and approach road alignments
- `c3d-corridors` — corridor integration with intersections
- `c3d-profiles` — profile views at intersections
- `c3d-label-styles` — general label style configuration
- `c3d-root-objects` — CivilDocument access and transaction patterns
