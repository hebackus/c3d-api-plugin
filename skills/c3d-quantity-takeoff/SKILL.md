---
name: c3d-quantity-takeoff
description: Quantity takeoff criteria, pay items, material computation, earthwork volumes, quantity reports, QTO manager integration
---

# Civil 3D Quantity Takeoff

Use this skill when working with quantity takeoff (QTO) - computing material volumes, assigning pay items, defining QTO criteria, generating quantity reports, or calculating earthwork cut/fill volumes.

## Quantity Takeoff Overview

Quantity takeoff in Civil 3D connects design objects to cost estimation:
- **QTO Criteria** = rules mapping corridor shapes/surfaces to material definitions
- **Material Lists** = computed volumes per sample line group from corridor cross-sections
- **Pay Items** = cost line items (from .csv pay item files) assigned to Civil 3D objects
- **Quantity Reports** = XML-based summary or detailed reports of pay item quantities

## QTO Criteria and Material Lists

### Loading QTO Criteria into a Sample Line Group

Material computation starts by importing QTO criteria into a sample line group. The criteria define which corridor shapes and surfaces produce material volumes.

```csharp
CivilDocument doc = CivilApplication.ActiveDocument;

// Get the sample line group
SampleLineGroup slg = ts.GetObject(slgId, OpenMode.ForWrite) as SampleLineGroup;

// Access the material lists collection
QTOMaterialListCollection materialLists = slg.MaterialLists;

// Import criteria from a QuantityTakeoffCriteria object
// Requires a QTOCriteriaNameMapping to map criteria names to drawing objects
QTOCriteriaNameMapping nameMapping = new QTOCriteriaNameMapping();
materialLists.ImportCriteria(materialLists, nameMapping);
```

### Reading Material Lists

```csharp
SampleLineGroup slg = ts.GetObject(slgId, OpenMode.ForRead) as SampleLineGroup;
QTOMaterialListCollection materialLists = slg.MaterialLists;

foreach (QTOMaterialList matList in materialLists)
{
    ed.WriteMessage("Material list: {0}\n", matList.Name);

    foreach (QTOMaterial material in matList)
    {
        ed.WriteMessage("  Material: {0}\n", material.Name);

        // Access subcriteria (surface-to-surface or shape-based definitions)
        QTOMaterialSubcriteriaCollection subcriteria = material.Subcriteria;
        foreach (QTOMaterialSubcriteria sub in subcriteria)
        {
            ed.WriteMessage("    Subcriteria: {0}\n", sub.Name);
        }
    }
}
```

### Material Sections per Sample Line

Each sample line can return a material section containing computed areas at that station.

```csharp
SampleLine sl = ts.GetObject(slId, OpenMode.ForRead) as SampleLine;

// GetMaterialSectionId exposes material lists and material GUID
ObjectId materialSectionId = sl.GetMaterialSectionId();
```

## QTO Material Class Hierarchy

```
SampleLineGroup
  └── MaterialLists (QTOMaterialListCollection)
        └── QTOMaterialList
              └── QTOMaterial
                    ├── Name — material name (e.g., "Earthwork", "Pavement")
                    ├── Subcriteria (QTOMaterialSubcriteriaCollection)
                    │     └── QTOMaterialSubcriteria
                    │           └── QTOMaterialItem (surface or shape reference)
                    └── QuantityTakeoffResult — computed volume/area results
```

## Earthwork Volume Computation

### Volume Surfaces (Cut/Fill Between Two Surfaces)

The most common earthwork calculation compares an existing ground surface to a proposed design surface.

```csharp
// Create a TIN volume surface between existing and proposed
ObjectId volSurfaceId = TinVolumeSurface.Create(
    "EW - Cut-Fill",
    existingGroundId,    // base surface (existing ground)
    proposedSurfaceId,   // comparison surface (finished grade)
    surfaceStyleId);

TinVolumeSurface volSurface =
    ts.GetObject(volSurfaceId, OpenMode.ForWrite) as TinVolumeSurface;

// Set shrinkage/swell factors
volSurface.CutFactor = 1.0;     // no adjustment for cut
volSurface.FillFactor = 1.20;   // 20% swell factor for fill

// Read computed volumes
VolumeSurfaceProperties volProps = volSurface.GetVolumeProperties();
ed.WriteMessage("Cut:  {0:F2} cu.yd.\n", volProps.AdjustedCutVolume);
ed.WriteMessage("Fill: {0:F2} cu.yd.\n", volProps.AdjustedFillVolume);
ed.WriteMessage("Net:  {0:F2} cu.yd.\n", volProps.AdjustedNetVolume);
```

### Bounded Volumes (Within a Polygon Region)

Calculate cut/fill within a specific area boundary on any surface.

```csharp
CivSurface oSurface = ts.GetObject(surfaceId, OpenMode.ForRead) as CivSurface;

Point3dCollection polygon = new Point3dCollection();
polygon.Add(new Point3d(1000, 2000, 0));
polygon.Add(new Point3d(1200, 2000, 0));
polygon.Add(new Point3d(1200, 2200, 0));
polygon.Add(new Point3d(1000, 2200, 0));

// Volume relative to a datum elevation
SurfaceVolumeInfo volInfo = oSurface.GetBoundedVolumes(polygon, datumElevation: 100.0);
ed.WriteMessage("Cut: {0:F2}, Fill: {1:F2}, Net: {2:F2}\n",
    volInfo.Cut, volInfo.Fill, volInfo.Net);
```

### Grid Volume Surface

For regular-grid earthwork computations:

```csharp
ObjectId gridVolId = GridVolumeSurface.Create(
    "Grid EW Volume",
    existingGridId,      // base grid surface
    proposedGridId,      // comparison grid surface
    spacingX: 10.0,
    spacingY: 10.0,
    orientation: 0.0,
    surfaceStyleId);
```

## Generating Quantity Reports

### XML Report Generation

```csharp
// Create report generation parameters
QTOGenerateDetail detail = new QTOGenerateDetail();
// Configure detail parameters (alignment extent, summary vs. detailed, etc.)

// Generate the XML report
string xmlReport = GenerateXMLReport(detail);

// Transform XML to another format (CSV, HTML) using XSLT
string outputPath = @"C:\Reports\quantities.html";
string xslPath = @"C:\Program Files\Autodesk\AutoCAD 2026\C3D\Quantity Takeoff\xsl\QuantitySummary.xsl";
TransformXMLReport(xmlReport, xslPath, outputPath);
```

### Sample Line Group Quantity Report

```csharp
SampleLineGroup slg = ts.GetObject(slgId, OpenMode.ForRead) as SampleLineGroup;

// Generate quantities report for the group
slg.ReportQuantities();
```

## Pay Items

### Pay Item File Structure

Pay item data is stored in CSV files with item numbers, descriptions, units, and unit prices. Civil 3D loads these through the QTO Manager. A categorization XML file groups pay items into logical categories.

```
Pay Item Files:
  PayItems_2026.csv           — item number, description, unit, price
  Categories_2026.xml         — categorization of pay items into groups
  Formulas.xml                — quantity computation formulas
```

### Assigning Pay Items to Objects

Pay items are assigned to Civil 3D objects through the QTO Manager or programmatically. Once assigned, the object's quantity (length, area, volume, count) is associated with the pay item for reporting.

```csharp
// Pay items can be assigned via code set styles for corridor objects
// The code set style maps corridor codes to pay items automatically
Corridor corridor = ts.GetObject(corridorId, OpenMode.ForRead) as Corridor;
ObjectId codeSetId = corridor.CodeSetStyleId;

// For pipe networks, pay items are assigned through the parts list
// Each part definition can reference a pay item number
```

### Reading Pay Item Assignments

```csharp
// Access QTO pay item file paths and formats from settings
// Pay item files, paths, and formats are available through the API
CivilDocument doc = CivilApplication.ActiveDocument;

// The QTO settings provide access to pay item file configuration
// including the active pay item list path and categorization file
```

## Corridor Material Volumes via Solids Export

An alternative approach to material computation exports corridor solids, which carry all property set data including baseline info and stations.

```csharp
Corridor corridor = ts.GetObject(corridorId, OpenMode.ForWrite) as Corridor;

// Export corridor regions as 3D solids
ExportCorridorSolidsParams solidParams = new ExportCorridorSolidsParams();
// solidParams properties control dynamic linking, layer placement, etc.

ObjectIdCollection solidIds = corridor.ExportSolids(solidParams, db);

// Each solid retains corridor property set data:
// - Baseline name and station range
// - Shape code and material type
// - Volume of the solid
// Solids update automatically if created with dynamic corridor link
```

### Region-Level Solid Export

```csharp
BaselineRegion region = corridor.Baselines[0].BaselineRegions[0];

ObjectIdCollection regionSolids = region.ExportSolids(
    solidParams,
    region.StartStation,
    region.EndStation,
    db);
```

## Surface-to-Surface Volume (Without Volume Surface)

For quick volume checks without creating a persistent volume surface, use TIN surface solid creation methods.

```csharp
TinSurface tinSurface = ts.GetObject(surfaceId, OpenMode.ForRead) as TinSurface;

// Create solids between this surface and another surface
ObjectIdCollection solidIds = tinSurface.CreateSolidsAtSurface(
    bottomSurfaceId, "V-EARTHWORK", penIndex: 1);

// Create solids at a fixed depth below the surface
ObjectIdCollection depthSolids = tinSurface.CreateSolidsAtDepth(
    depth: 2.0, "V-SUBBASE", penIndex: 2);

// Create solids down to a fixed elevation
ObjectIdCollection elevSolids = tinSurface.CreateSolidsAtFixedElevation(
    elevation: 95.0, "V-EXCAVATION", penIndex: 3);
```

## Volume Surface Properties

- CutFactor (double, get/set) -- multiplier applied to cut volumes (1.0 = no adjustment)
- FillFactor (double, get/set) -- multiplier applied to fill volumes (accounts for swell/shrinkage)
- GetVolumeProperties() -> VolumeSurfaceProperties -- computed volume results

### VolumeSurfaceProperties Fields

- UnadjustedCutVolume (double, get) -- raw cut volume before factor
- UnadjustedFillVolume (double, get) -- raw fill volume before factor
- UnadjustedNetVolume (double, get) -- raw net volume (cut minus fill)
- AdjustedCutVolume (double, get) -- cut volume after CutFactor applied
- AdjustedFillVolume (double, get) -- fill volume after FillFactor applied
- AdjustedNetVolume (double, get) -- net volume after factors applied
- BaseSurface (ObjectId, get) -- the base (existing) surface
- ComparisonSurface (ObjectId, get) -- the comparison (proposed) surface

### SurfaceVolumeInfo Fields

- Cut (double, get) -- cut volume within the bounded region
- Fill (double, get) -- fill volume within the bounded region
- Net (double, get) -- net volume within the bounded region

## QTO Material Classes

- QTOMaterialListCollection -- collection of material lists on a SampleLineGroup
- QTOMaterialList -- a named material list containing material definitions
- QTOMaterial -- a single material definition (e.g., "Earthwork", "Pavement")
- QTOMaterialSubcriteriaCollection -- subcriteria defining material extents
- QTOMaterialSubcriteria -- a subcriteria entry (surface pair or corridor shape)
- QTOMaterialItem -- reference to a surface or shape used in the subcriteria
- QuantityTakeoffResult -- computed quantity result for a material

## QTO Report Methods

- GenerateXMLReport(QTOGenerateDetail) -> string -- generates summary or detailed XML report
- TransformXMLReport(string xml, string xslPath, string outputPath) -- transforms XML report to CSV/HTML via XSLT
- SampleLineGroup.ReportQuantities() -> void -- generates quantities report for a group of sample lines

## Gotchas

- **Material computation requires sample lines.** You cannot compute corridor material volumes without first creating a sample line group along the alignment. The sample lines define the cross-section stations where areas are calculated and volumes interpolated.

- **QTOMaterialListCollection.ImportCriteria requires two arguments.** The API reference may show only one parameter, but the actual method requires both the QTOMaterialListCollection and a QTOCriteriaNameMapping object that maps criteria names to drawing surface/shape names.

- **Volume surface factors are multiplicative, not additive.** A FillFactor of 1.20 means 120% of the raw fill volume (20% swell), not an additional 0.20 added to each measurement.

- **GetGeneralProperties() on volume surfaces is expensive.** Call once and cache the result rather than querying repeatedly in a loop.

- **Corridor cut/fill volume computation requires COM.** The managed .NET API does not expose a direct method on CorridorSurface to compute cut/fill between a corridor surface and a reference surface. Use volume surfaces or export solids instead.

- **Pay item assignments use external CSV files.** The pay item database is not stored in the drawing; it is loaded from external .csv files. Changes to the pay item file affect all drawings referencing it.

- **Report generation does not support selection extents.** GenerateXMLReport() does not support Sheet and Selection Extent scope or reporting for selected pay items only with station/offset data.

- **Rebuild surface before querying volumes.** If the base or comparison surface has been modified, the volume surface must be rebuilt before GetVolumeProperties() returns accurate results.

## Related Skills

- `c3d-corridors` -- Corridor objects whose shapes and surfaces feed material computation
- `c3d-surfaces` -- TIN/Grid/Volume surfaces used for earthwork cut/fill calculations
- `c3d-profiles` -- Profile data along alignments used in cross-section volume analysis
- `c3d-root-objects` -- CivilDocument access to surface collections and settings
- `c3d-mass-haul` -- Mass haul diagrams derived from material list volumes
