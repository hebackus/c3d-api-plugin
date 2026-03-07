---
name: c3d-superelevation
description: Superelevation design, attainment methods, transition tables, cross slope, pivot points, lane configurations, superelevation views
---

# Civil 3D Superelevation

Use this skill when reading superelevation data, querying cross slopes at stations, working with critical stations, or understanding superelevation's relationship to corridors and subassemblies.

## Superelevation Overview

Superelevation is the banking of a roadway through horizontal curves to counteract centrifugal force. In Civil 3D, superelevation data is attached to an **Alignment** and consumed by a **Corridor** to shape cross sections through curves.

The workflow is:
1. **Alignment** defines the horizontal geometry (curves where superelevation applies)
2. **Superelevation wizard** (UI) calculates transition stations and cross slopes
3. **Superelevation data** is stored on the alignment as curves with critical stations
4. **Corridor** reads superelevation data via superelevation-aware subassemblies
5. **Subassemblies** adjust lane/shoulder slopes at each station based on the data

Key relationships:
- Superelevation is a **property of alignments**, not corridors
- Corridors **consume** superelevation data through their baseline alignment
- The superelevation wizard is a **UI operation** — the .NET API is for reading computed results

**API Change Note (Civil 3D 2013+):** The `SuperelevationData` property and `SuperElevationAtStation()` method were removed. Use `SuperelevationCurves` and `SuperelevationCriticalStations` instead.

## Accessing Superelevation Data

Superelevation data lives on the `Alignment` object, organized as a collection of `SuperelevationCurve` objects, each containing critical stations.

```csharp
Alignment align = ts.GetObject(alignmentId, OpenMode.ForRead) as Alignment;

// Check if superelevation has been calculated
if (align.SuperelevationCurves.Count < 1)
{
    ed.WriteMessage("Must calculate superelevation data first.\n");
    return;
}

// Iterate superelevation curves
foreach (SuperelevationCurve sec in align.SuperelevationCurves)
{
    ed.WriteMessage("Curve: {0}, Start: {1:F2}, End: {2:F2}\n",
        sec.Name, sec.StartStation, sec.EndStation);

    // Each curve has its own critical stations
    foreach (SuperelevationCriticalStation sest in sec.CriticalStations)
    {
        ed.WriteMessage("  Station: {0:F2}, Type: {1}, Region: {2}\n",
            sest.Station, sest.StationType, sest.TransitionRegionType);

        // Get slope for each cross segment type
        foreach (int i in Enum.GetValues(typeof(SuperelevationCrossSegmentType)))
        {
            try
            {
                double slope = sest.GetSlope((SuperelevationCrossSegmentType)i);
                ed.WriteMessage("    {0}: {1:F4}\n",
                    Enum.GetName(typeof(SuperelevationCrossSegmentType), i), slope);
            }
            catch (InvalidOperationException) { }  // Invalid segment for this station
        }
    }
}
```

### Key Access Properties

- `Alignment.SuperelevationCurves` — collection of `SuperelevationCurve` objects
- `Alignment.SuperelevationCriticalStations` — all critical stations across all curves (flat collection)
- `SuperelevationCriticalStationCollection.GetCriticalStationAt()` — access individual stations

## Cross Slope at a Station

The `Alignment.GetCrossSlopeAtStation()` method returns the slope for a specific cross segment type at any station.

```csharp
Alignment align = ts.GetObject(alignmentId, OpenMode.ForRead) as Alignment;
double station = 500.0;

// SuperelevationCrossSegmentType values:
//   LeftOutShoulderCrossSlope, LeftOutLaneCrossSlope,
//   LeftInShoulderCrossSlope,  LeftInLaneCrossSlope,
//   RightInLaneCrossSlope,     RightInShoulderCrossSlope,
//   RightOutLaneCrossSlope,    RightOutShoulderCrossSlope

double leftInLane = align.GetCrossSlopeAtStation(
    station, SuperelevationCrossSegmentType.LeftInLaneCrossSlope, true);
double rightInLane = align.GetCrossSlopeAtStation(
    station, SuperelevationCrossSegmentType.RightInLaneCrossSlope, true);

ed.WriteMessage($"\nAt sta {station:F2}: Left={leftInLane:F4}, Right={rightInLane:F4}");
```

### Reading All Cross Slopes at a Station

```csharp
double station = 500.0;

foreach (int i in Enum.GetValues(typeof(SuperelevationCrossSegmentType)))
{
    try
    {
        var segType = (SuperelevationCrossSegmentType)i;
        double slope = align.GetCrossSlopeAtStation(station, segType, true);
        ed.WriteMessage($"\n  {segType}: {slope:F4}");
    }
    catch (InvalidOperationException) { }
}
```

## Critical Stations

Critical stations mark key points in the superelevation transition. Each curve generates a set of these stations.

### SuperelevationCriticalStation Properties

- Station (double, get) — station value on the alignment
- StationType (enum, get) — type of critical station (see below)
- TransitionRegionType (enum, get) — which transition region this belongs to
- GetSlope(SuperelevationCrossSegmentType) → double — cross slope for a specific segment

### Station Types

The `StationType` property identifies where in the transition this station falls:
- **BeginNormalCrown** — start of transition (still at normal crown)
- **LevelCrown** — cross slope passes through 0% (level)
- **EndNormalCrown** — adverse crown fully removed
- **BeginFullSuper** — full superelevation rate achieved
- **EndFullSuper** — full superelevation rate ends
- **BeginNormalCrownReturn** — returning to normal crown
- **EndNormalCrownReturn** — back to normal crown

Typical sequence for a right curve:
```
BeginNormalCrown → LevelCrown → EndNormalCrown →
  BeginFullSuper → [through curve] → EndFullSuper →
  EndNormalCrown(return) → LevelCrown(return) → BeginNormalCrownReturn
```

### Iterating All Critical Stations

```csharp
// Flat collection across all curves
foreach (SuperelevationCriticalStation sest in align.SuperelevationCriticalStations)
{
    ed.WriteMessage($"\n  Sta {sest.Station,10:F2}  Type: {sest.StationType,-25}");
}
```

### Runoff and Runout

- **Runoff length** — distance from adverse crown removed to full superelevation
- **Runout length** — distance from normal crown to adverse crown removed

These are derived from the critical station positions:
```csharp
// Calculate from station differences between critical station types
double runoutLength = endNormalCrownStation - beginNormalCrownStation;
double runoffLength = beginFullSuperStation - endNormalCrownStation;
```

## Attainment Methods

Attainment methods control how the roadway transitions from normal crown to full superelevation. These are configured through the superelevation wizard UI.

- **AASHTO methods** — use design tables based on speed, radius, and eMax to compute runoff and runout lengths
- **Planar** — entire cross section rotates as a plane about the pivot point
- **Linear with runoff** — separate runoff and runout lengths calculated linearly

> **Note:** Attainment method, eMax, design speed, pivot method, lane counts, and lane widths are all configured through the superelevation wizard. The .NET API does not expose these as writable properties. They are embedded in the computed critical station data.

## Pivot Points

The pivot point determines which element remains fixed while lanes rotate:

- **Crown pivot** — rotates about the crown point (center of road). Most common for undivided roads.
- **Center pivot** — rotates both sides equally about the centerline. Profile grade maintained at center.
- **Edge pivot** — holds one edge of pavement fixed. Useful for curbed sections where one gutter must maintain grade.

## Transition Tables

The superelevation wizard uses transition tables mapping design speed + curve radius + eMax to required superelevation rate, runoff length, and runout length. These tables are based on AASHTO or agency-specific criteria.

The .NET API reads the computed results but does not expose the lookup tables. Custom tables are configured through:
- `Settings > Alignment > Superelevation > Attainment` in Civil 3D settings
- XML-based superelevation table files that Civil 3D can import

## Applying Superelevation to Corridors

Corridors consume superelevation data automatically when they reference an alignment that has superelevation defined. The key is using **superelevation-aware subassemblies**.

### Superelevation-Aware Subassemblies

Common built-in subassemblies that read superelevation:
- `LaneSuperelevationAOR` — lane with superelevation axis of rotation
- `LaneOutsideSuperAOR` — outside lane during superelevation
- `LaneInsideSuper` — inside lane during superelevation
- `ShoulderExtendAll` — shoulder that follows superelevation
- `ShoulderSubbase` — shoulder subbase with superelevation support

These subassemblies have target parameters that read slope values from the alignment's superelevation data at each corridor station. In corridor properties, set the target to "Superelevation" for these parameters.

### Rebuilding After Changes

```csharp
// After changing superelevation on the alignment, rebuild the corridor
Corridor corridor = ts.GetObject(corridorId, OpenMode.ForWrite) as Corridor;
corridor.Rebuild();
```

### Verifying Superelevation on a Corridor Baseline

```csharp
Corridor corridor = ts.GetObject(corridorId, OpenMode.ForRead) as Corridor;

foreach (Baseline bl in corridor.Baselines)
{
    Alignment blAlign = ts.GetObject(bl.AlignmentId, OpenMode.ForRead) as Alignment;
    bool hasSE = blAlign.SuperelevationCurves.Count > 0;
    ed.WriteMessage($"\nBaseline '{bl.Name}' has superelevation: {hasSE}");
}
```

## Exporting Superelevation Data

```csharp
// Export superelevation data for reporting
var report = new System.Text.StringBuilder();
report.AppendLine("Station,Type,Region");

foreach (SuperelevationCriticalStation sest in align.SuperelevationCriticalStations)
{
    var line = $"{sest.Station:F2},{sest.StationType},{sest.TransitionRegionType}";

    // Append all available slopes
    foreach (int i in Enum.GetValues(typeof(SuperelevationCrossSegmentType)))
    {
        try
        {
            double slope = sest.GetSlope((SuperelevationCrossSegmentType)i);
            line += $",{slope:F4}";
        }
        catch (InvalidOperationException)
        {
            line += ",";
        }
    }
    report.AppendLine(line);
}

ed.WriteMessage($"\n{report}");
```

## Creating Superelevation

Superelevation creation is a **UI wizard operation**. The .NET API does not expose creation methods. Use `SendStringToExecute` to invoke the wizard:

```csharp
Document acadDoc = Application.DocumentManager.MdiActiveDocument;
// Opens the interactive superelevation wizard — not fully automatable
acadDoc.SendStringToExecute("SUPERELEVATION ", true, false, false);
```

## Gotchas

- **`SuperelevationData` was removed in Civil 3D 2013.** Use `SuperelevationCurves` and `SuperelevationCriticalStations` instead. Code referencing the old API will not compile.
- **Slopes are decimals, not percentages.** A -2% slope is stored as `-0.02`. Format with `:P` or multiply by 100 for display.
- **`GetSlope()` throws `InvalidOperationException` for invalid segment types.** Not all cross segment types are valid at every critical station. Always wrap in try/catch.
- **`GetCrossSlopeAtStation()` third parameter is `adjustForSide`.** Pass `true` to automatically adjust the sign based on which side of the alignment the segment is on.
- **Superelevation requires curves.** Tangent-only alignments have no superelevation data. The wizard only generates transitions for circular and spiral curves.
- **Critical stations depend on attainment method.** Changing the method changes the number and position of critical stations. Always re-read after wizard changes.
- **Corridor rebuild required.** After modifying superelevation on an alignment, call `corridor.Rebuild()` for the corridor to reflect changes.
- **Subassembly must be superelevation-aware.** Standard subassemblies like `BasicLane` ignore superelevation data. Use `LaneSuperelevationAOR` or similar.
- **Left/right is relative to alignment direction.** "Left inside" means the inside lane on the left side when traveling in the alignment direction. On a right curve, the left side is the outside.
- **Spiral curves affect transitions.** When spirals are present, superelevation transitions distribute along the spiral length rather than extending into the tangent.
- **Creation and configuration are wizard-only.** Attainment method, eMax, design speed, pivot method, lane configuration — none of these have writable .NET API properties.

## Related Skills

- `c3d-alignments` — alignments that host superelevation data (includes superelevation code examples)
- `c3d-corridors` — corridors that consume superelevation for cross-section shaping
- `c3d-profiles` — profile relationship with superelevation design
- `c3d-custom-subassemblies` — subassemblies that read superelevation parameters
- `c3d-root-objects` — CivilDocument access and transaction patterns
