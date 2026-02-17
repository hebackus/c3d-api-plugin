---
name: c3d-custom-subassemblies
description: Custom subassembly design in VB.NET - naming, parameters, superelevation, CorridorState, targets, SATemplate pattern, and tool catalog
---

# Custom Subassemblies Using .NET

Use this skill when creating custom subassembly components for corridors in Civil 3D.

## Overview

Custom subassemblies are written in VB.NET (the supported and preferred method). They define cross-sectional shapes that are placed along corridor baselines.

## Naming Conventions

- No spaces or special characters
- PascalCase with uppercase first letter per word
- Group by component type as prefix: `LaneBasic`, `ShoulderExtended`, `CurbTypeA`
- For fixed-dimension variants, create separate subassemblies (e.g., `CurbTypeA` through `CurbTypeE`) rather than one with many parameters

## Attachment Methodology

Most subassemblies have a single attachment point extending in one direction. Special cases:

| Category | Behavior |
|----------|----------|
| **Medians** | Insert left and right simultaneously about a centerline. Attachment point may not be on the median surface (e.g., above a depressed median ditch). |
| **Components Joining Two Roadways** | Need two attachment points - normal attachment on one side, marked point attachment on the other. |
| **Rehabilitation/Overlay** | Calculations based on existing roadway section shape rather than design centerline. |

## Input Parameter Types

| Parameter | Description |
|-----------|-------------|
| **Widths** | Horizontal distance between two points. Positive values extend in insertion direction (left/right). Candidates for alignment targeting. |
| **Offsets** | Horizontal distance from corridor baseline. Positive = right, negative = left. |
| **% Slopes** | Rise-to-run ratio. Unitless (-0.05) or percent (-5%). Use same convention across catalog. |
| **Ratio Slopes** | Run-to-rise ratio (e.g., 4:1). May be signed or unsigned depending on context. |
| **Point/Link/Shape Codes** | Usually hard-coded for consistency. Exception: generic link subassemblies where user assigns codes. |

**Design guidance:** Generally, widths, depths, and slopes should be variable (not fixed). Provide default values usable in most situations.

## Superelevation Behavior

Key considerations:
- Where is the superelevation pivot point?
- How does it relate to the Profile Grade Line (PGL)?

Common pivot/PGL combinations:
- Both at crown of road
- Both at inside edge-of-traveled-way (divided road)
- Both at one edge-of-traveled-way (undivided road)
- Pivot at inside edge, PGL at centerline
- On divided crowned roads: PGL at crown points, pivot at inside ETW
- On divided uncrowned: both above median at centerline

Special superelevation behaviors:
- **Broken Back Subbase** - break point in subbase on high side
- **Shoulder Breakover** - maximum slope difference between lane and shoulder
- **Curbs-and-Gutters** - high-side gutter behavior changes in superelevation

## Target Mapping (Civil 3D 2013+)

Subassemblies can target object types beyond alignments/profiles:

### Parameter Types

Replace old types with new target types:

| Old | New | Description |
|-----|-----|-------------|
| `ParamLogicalNameType.Alignment` | `ParamLogicalNameType.OffsetTarget` | Alignments, feature lines, survey figures, polylines |
| `ParamLogicalNameType.Alignment` | `ParamLogicalNameType.OffsetTargetPipe` | Pipe network offset targets |
| `ParamLogicalNameType.Profile` | `ParamLogicalNameType.ElevationTarget` | Profiles, feature lines, survey figures, 3D polylines |
| `ParamLogicalNameType.Profile` | `ParamLogicalNameType.ElevationTargetPipe` | Pipe network elevation targets |

### Target Collections in CorridorState

```vb
' Get target collections
Dim oParamsOffsetTarget As ParamOffsetTargetCollection
oParamsOffsetTarget = corridorState.ParamsOffsetTarget

Dim oParamsElevationTarget As ParamElevationTargetCollection
' (replaces ParamsAlignment and ParamsProfile)
```

### Target Objects

```vb
' Declare targets as objects (not IDs)
Dim offsetTarget As WidthOffsetTarget
offsetTarget = Nothing

Dim elevationTarget As SlopeElevationTarget
elevationTarget = Nothing
```

### Getting Elevation from Target

```vb
' Get elevation directly from elevation target
Try
    dOffsetElev = elevationTarget.GetElevation( _
        oCurrentAlignmentId, _
        corridorState.CurrentStation, _
        Utilities.GetSide(vSide))
Catch
    Utilities.RecordWarning(corridorState, _
        CorridorError.LogicalNameNotFound, _
        "TargetHA", "BasicLaneTransition")
    dOffsetElev = corridorState.CurrentElevation + vWidth * vSlope
End Try
```

### CalcAlignmentOffsetToThisAlignment Changes

This utility method now:
- Calculates offset from alignment to offset target
- Returns XY coordinate (not station value) at the perpendicular point

## CorridorState Object

The `CorridorState` object provides access to the current corridor processing state:

```vb
corridorState.CurrentStation        ' Current station being processed
corridorState.CurrentElevation      ' Current elevation at station
corridorState.ParamsLong            ' Long parameters collection
corridorState.ParamsDouble          ' Double parameters collection
corridorState.ParamsString          ' String parameters collection
corridorState.ParamsOffsetTarget    ' Offset target parameters
corridorState.ParamsElevationTarget ' Elevation target parameters
```

## SATemplate Pattern

The SATemplate (SubAssembly Template) pattern is the standard structure for custom subassembly code:

1. Define input parameters
2. Read current corridor state
3. Calculate geometry based on parameters and targets
4. Create points, links, and shapes with appropriate codes
5. Handle errors with `Utilities.RecordWarning()`

## Support Files

| File | Purpose |
|------|---------|
| `CodesSpecific` | Defines point, link, and shape codes used by the subassembly |
| `Utilities` | Helper methods for common calculations |

Key utility methods:
- `Utilities.GetSide()` - determine left/right side
- `Utilities.RecordWarning()` - log corridor processing warnings

## Tool Catalog

Custom subassemblies are distributed via tool catalogs.

### ATC File Format

The Autodesk Tool Catalog (`.atc`) file is an XML file defining:
- Categories and subcategories
- Individual tools (subassemblies)
- Parameters, descriptions, and help references

### Cover Page

The catalog cover page provides:
- Catalog name and description
- Version information
- Publisher information

### Registry File

Associates the tool catalog with Civil 3D so it appears in the tool palette.

### PKT Package Export

Package subassemblies for distribution:
1. Compile the VB.NET assembly
2. Create the ATC catalog file
3. Create registry entries
4. Export as PKT package

## Gotchas

- Custom subassemblies MUST be written in VB.NET (currently supported and preferred method)
- Always handle the case where targets are not found (use Try/Catch)
- Use `Utilities.RecordWarning()` instead of throwing exceptions to avoid crashing corridor processing
- Point, link, and shape codes should be consistent across all subassemblies in a catalog
- Consider both normal crown and superelevation conditions
- `CalcAlignmentOffsetToThisAlignment()` behavior changed in 2013 - returns coordinates, not station
- The `.NET` toolbox execution type requires static methods with explicit document locking

## Related Skills

- `c3d-corridors` - Corridor structure, baselines, assemblies
- `c3d-alignments` - Alignments and superelevation
- `c3d-profiles` - Profiles used as corridor baselines
