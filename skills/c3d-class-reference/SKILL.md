---
name: c3d-class-reference
description: Quick reference for Civil 3D .NET API classes - instant class lookups
---

# Civil 3D .NET API Class Reference

**Quick lookup for 959 classes across 19 namespaces**

## When to Use This Skill

- Looking for a specific class name
- Checking what classes exist in a namespace
- Finding the right type for a task
- Exploring available API surface

## Core Namespaces (384 classes)

### Autodesk.Civil.DatabaseServices

**Main Civil 3D objects** - Alignments, Surfaces, Profiles, Pipe Networks, etc.

**Key Classes:**
- `Alignment` - Horizontal/vertical alignments
- `Surface` - TIN/Grid/Volume surfaces
- `TinSurface`, `GridSurface`, `TinVolumeSurface`
- `Profile` - Vertical profiles
- `ProfileView` - Profile view drawings
- `Network` - Gravity pipe networks
- `PressurePipeNetwork` - Pressure pipe networks
- `Pipe`, `Structure` - Gravity network parts
- `PressurePipe`, `PressureFitting`, `PressureAppurtenance` - Pressure parts
- `Corridor` - Corridor models
- `Assembly` - Assembly definitions
- `Subassembly` - Subassembly components
- `FeatureLine` - Feature line objects
- `CogoPoint` - Survey/COGO points
- `PointGroup` - Point group collections
- `Catchment` - Catchment areas
- `Parcel` - Parcel objects
- `SampleLine`, `SampleLineGroup` - Cross sections

**Label Classes:**
- `AlignmentLabel`, `SurfaceLabel`, `ProfileLabel`
- `PipeLabel`, `StructureLabel`
- `GeneralNoteLabel`, `CurveLabel`, `LineLabel`

### Autodesk.Civil.DatabaseServices.Styles (163 classes)

**Styles for all Civil 3D objects**

**Key Styles:**
- `AlignmentStyle`, `ProfileStyle`, `SurfaceStyle`
- `PipeStyle`, `StructureStyle`
- `CorridorStyle`, `AssemblyStyle`
- `LabelStyle`, `LabelStyleComponent`
- `MarkerStyle`, `ProfileViewStyle`

### Autodesk.Civil (241 classes)

**Core types, enumerations, exceptions**

**Key Types:**
- `CivilException` - Base exception type
- `Property*` classes - For accessing object properties
- Enumerations for all option types
- `Constant` - API constants

### Autodesk.Civil.Settings (86 classes)

**Drawing and object settings**

**Key Classes:**
- `SettingsRoot` - Root settings access
- `SettingsAlignment`, `SettingsSurface`, `SettingsProfile`
- `SettingsPipeNetwork`, `SettingsCorridor`
- `SettingsDrawing` - Drawing-level settings

### Autodesk.Civil.ApplicationServices (1 class)

- `CivilApplication` - Main application object

## Common Patterns

### Get CivilDocument
```csharp
using Autodesk.Civil.ApplicationServices;

CivilDocument civilDoc = CivilApplication.ActiveDocument;
```

### Access Collections
```csharp
using Autodesk.Civil.DatabaseServices;

ObjectIdCollection alignmentIds = civilDoc.GetAlignmentIds();
ObjectIdCollection surfaceIds = civilDoc.GetSurfaceIds();
ObjectIdCollection networkIds = civilDoc.GetPipeNetworkIds();
ObjectIdCollection pressureNetworkIds = civilDoc.GetPressurePipeNetworkIds();
```

### Open Objects
```csharp
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    Alignment align = tr.GetObject(alignmentId, OpenMode.ForRead) as Alignment;
    Surface surf = tr.GetObject(surfaceId, OpenMode.ForRead) as Surface;

    tr.Commit();
}
```

## Full Class Index

See [`CLASS_INDEX.md`](../../api-reference/CLASS_INDEX.md) for complete listing of all 959 types.

## Related Skills

- `/c3d-api:c3d-project-setup` - Setting up .NET project for Civil 3D development
- `/c3d-api:c3d-root-objects` - CivilApplication, CivilDocument, settings hierarchy
- `/c3d-api:c3d-alignments` - Alignment creation, entities, geometry
- `/c3d-api:c3d-surfaces` - Surface creation, editing, data extraction
- `/c3d-api:c3d-profiles` - Profile layout, PVIs, profile views
- `/c3d-api:c3d-pipe-networks` - Gravity and pressure pipe network objects
- `/c3d-api:c3d-corridors` - Corridor creation, baselines, regions
- `/c3d-api:c3d-points` - CogoPoint, PointGroup, UDP access
- `/c3d-api:c3d-label-styles` - LabelStyle, components, hierarchy
- `/c3d-api:c3d-custom-subassemblies` - Subassembly SDK, CorridorState, geometry callbacks
