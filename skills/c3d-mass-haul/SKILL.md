---
name: c3d-mass-haul
description: Mass haul diagrams, free haul, overhaul, borrow pits, waste sites, earthwork balance lines, mass haul views
---

# Civil 3D Mass Haul

Use this skill when working with mass haul diagrams, earthwork balance lines, free haul and overhaul distances, or borrow/waste site management.

## Overview

Mass haul diagrams visualize cumulative earthwork volumes along an alignment, showing where material must be moved from cut zones to fill zones. The diagram plots cumulative volume (y-axis) against station (x-axis), producing a curve whose slope indicates cut (rising) or fill (falling) regions.

Key relationships:
- **Alignment** — defines the horizontal path along which earthwork is measured
- **Sample line group** — provides the cross-section sampling stations
- **Material list** — defines cut/fill material definitions with swell/shrinkage factors
- **Corridor** — the design model whose surfaces generate cut and fill volumes

## API Limitations

Mass haul diagrams are primarily created through the **Mass Haul Diagram wizard** (command `CreateMassHaulDiagram`). The managed .NET API does not provide a `MassHaulDiagram.Create()` method. The API surface for reading existing mass haul data is also limited compared to other Civil 3D objects. Many operations require the wizard UI or report generation commands.

> **Note:** The `MassHaulView` and `MassHaulDiagram` classes may have limited property exposure depending on your Civil 3D version. Verify available members against the Object Browser for your target version.

## Accessing Mass Haul Views

Mass haul views are graphical entities in model space. Find them by iterating the block table record:

```csharp
using (Transaction ts = db.TransactionManager.StartTransaction())
{
    BlockTableRecord btr = (BlockTableRecord)ts.GetObject(
        SymbolUtilityServices.GetBlockModelSpaceId(db), OpenMode.ForRead);

    foreach (ObjectId id in btr)
    {
        Entity ent = (Entity)ts.GetObject(id, OpenMode.ForRead);
        if (ent is MassHaulView mhView)
        {
            ed.WriteMessage($"\nMass Haul View: {mhView.Name}");
        }
    }

    ts.Commit();
}
```

## Creating Mass Haul Diagrams

Creation is **wizard-driven only**:

```csharp
// Trigger the built-in mass haul creation wizard
Application.DocumentManager.MdiActiveDocument.SendStringToExecute(
    "CreateMassHaulDiagram ", true, false, false);
```

The wizard requires:
1. An alignment with a corridor
2. Sample lines crossing the corridor
3. A computed material list (quantity takeoff materials)

There is no silent/automated creation path through the managed .NET API.

## Mass Haul Concepts

### Balance Lines

Balance lines on a mass haul diagram indicate stations where cumulative cut equals cumulative fill. They define segments where material can be balanced internally:

- A **balance line** is a horizontal line intersecting the mass haul curve at two or more points
- Material between intersection points can be balanced within the segment
- The **free haul zone** is the portion within the free haul distance of each balance point
- Material moved beyond the free haul distance incurs **overhaul** costs

### Free Haul and Overhaul

- **Free haul** — maximum distance material can be transported at no additional cost (included in base excavation price)
- **Overhaul** — cost of moving material beyond the free haul distance: volume x excess distance x unit cost

Overhaul is computed from the mass haul diagram:
- **Overhaul volume** = volume of material moved beyond free haul distance
- **Overhaul distance** = average haul distance minus free haul distance

### Borrow Pits and Waste Sites

When a project cannot balance cut and fill internally:
- **Borrow pits** — external material sources
- **Waste sites** — external material disposal locations

These are configured in the mass haul wizard with station location, capacity, and description. The .NET API does not expose creation or modification of borrow/waste sites.

### Cumulative Volume Curve

The mass haul curve plots cumulative volume vs. station:
- **Rising segments** — net cut (material surplus)
- **Falling segments** — net fill (material deficit)
- **Peaks** — transitions from cut to fill
- **Valleys** — transitions from fill to cut
- **Zero crossings** relative to a balance line — balance points

## Material Lists

Material lists define the cut and fill surfaces and are essential inputs to mass haul computation.

### Structure

A material list references:
- **Quantity takeoff criteria** defining material types
- **Cut surface** (typically existing ground)
- **Fill surface** (typically corridor datum or design surface)
- **Swell factor** — volume increase when excavated (e.g., 1.20 = 20% swell)
- **Shrinkage factor** — volume decrease when compacted (e.g., 0.95 = 5% shrinkage)

### Accessing Material Lists via Sample Line Groups

```csharp
using (Transaction ts = db.TransactionManager.StartTransaction())
{
    SampleLineGroup slg = (SampleLineGroup)ts.GetObject(
        sampleLineGroupId, OpenMode.ForRead);

    // Access material lists through the sample line group
    // See c3d-quantity-takeoff skill for detailed material list access
    ed.WriteMessage($"\nSample line group: {slg.Name}");

    ts.Commit();
}
```

### Swell and Shrinkage

Swell and shrinkage factors directly impact the mass haul curve:
```
Adjusted Cut Volume  = Raw Cut Volume x Swell Factor
Adjusted Fill Volume = Raw Fill Volume x Shrinkage Factor
```

These factors are set in the material list definition. The `c3d-quantity-takeoff` skill documents `FillFactor` as a multiplier.

## Volume Data from Sample Lines

```csharp
using (Transaction ts = db.TransactionManager.StartTransaction())
{
    SampleLineGroup slg = (SampleLineGroup)ts.GetObject(
        sampleLineGroupId, OpenMode.ForRead);

    ObjectIdCollection sampleLineIds = slg.GetSampleLineIds();

    foreach (ObjectId slId in sampleLineIds)
    {
        SampleLine sl = (SampleLine)ts.GetObject(slId, OpenMode.ForRead);
        ed.WriteMessage($"\nStation: {sl.Station:F2}");
        // Volume data is computed via quantity takeoff at each station
        // The mass haul diagram aggregates these into a cumulative curve
    }

    ts.Commit();
}
```

### Volume Reports

For detailed per-station volume data, use built-in reporting:

```csharp
Application.DocumentManager.MdiActiveDocument.SendStringToExecute(
    "GenerateQuantitiesReport ", true, false, false);
```

## Gotchas

- **No .NET creation API.** Mass haul diagrams cannot be created programmatically. Use the `CreateMassHaulDiagram` wizard command.
- **Material list dependency.** A mass haul diagram requires a computed material list. If the material list is out of date, the diagram shows stale data.
- **Swell/shrinkage are multiplicative.** Forgetting to account for these factors will produce incorrect mass haul curves and shift balance points.
- **Free haul distance uses drawing units.** Feet or meters depending on the drawing. Mixing units produces nonsensical overhaul calculations.
- **Balance lines are visual, not queryable.** The .NET API does not expose individual balance line intersection stations.
- **Sample lines must exist first.** If sample lines don't cover the full corridor extent, the mass haul diagram only reflects the sampled range.
- **Corridor rebuild required.** If the corridor design changes, rebuild the corridor and recompute material volumes before the mass haul diagram reflects updates.
- **Multiple material lists.** A sample line group can have multiple material lists. Ensure you reference the correct one.
- **MassHaulView vs MassHaulDiagram.** The `MassHaulView` is the graphical container in the drawing. The `MassHaulDiagram` is the data object. A view can display multiple diagrams.
- **Most properties are read-only.** Structural changes (adding sites, changing materials) require the wizard. Write access is limited.
- **Report export for analysis.** For cost optimization or haul distance matrices, export via `GenerateQuantitiesReport` or XML reports rather than extracting through the object model.

## Related Skills

- `c3d-surfaces` — existing ground and design surfaces for volume computation
- `c3d-profiles` — profiles that define cut/fill relationships along alignments
- `c3d-corridors` — corridors that generate the earthwork volumes feeding mass haul
- `c3d-sample-lines` — sample line groups that provide cross-section stations
- `c3d-quantity-takeoff` — quantity takeoff for material volumes and material lists
- `c3d-root-objects` — CivilDocument access and transaction patterns
