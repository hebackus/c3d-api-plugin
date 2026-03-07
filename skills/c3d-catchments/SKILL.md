---
name: c3d-catchments
description: Catchment areas, flow paths, watershed delineation, drainage analysis, catchment properties, catchment labels
---

# Civil 3D Catchments

Use this skill when working with catchment areas, flow paths, watershed delineation, or drainage analysis in Civil 3D.

## Catchment Overview

Catchments in Civil 3D represent drainage areas on a surface where water flows to a common discharge point. They are fundamental to stormwater and hydrology analysis, linking surface terrain data to pipe network design. Each catchment is defined by a boundary polygon, a reference surface, and a discharge point where collected runoff exits the catchment area.

Catchments are typically derived from surface analysis (watershed delineation) or created manually by drawing boundaries. They store hydrological properties such as area, runoff coefficient, rainfall intensity, and time of concentration for use in the rational method and other drainage calculations.

The .NET API for catchments is more limited than the interactive UI. Many creation and analysis operations must be performed through commands rather than direct API calls.

## Accessing Catchments

### CivilDocument and the Catchment Collection

Catchments are accessed through `CivilDocument` and its site collections. Catchments belong to a `Site`, which groups related drainage objects.

```csharp
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.Civil;
using Autodesk.Civil.DatabaseServices;

// Access catchments through CivilDocument sites
Document acadDoc = Application.DocumentManager.MdiActiveDocument;
Database db = acadDoc.Database;
CivilDocument doc = CivilDocument.GetCivilDocument(db);

using (Transaction ts = db.TransactionManager.StartTransaction())
{
    // Iterate sites to find catchments
    ObjectIdCollection siteIds = doc.GetSiteIds();
    foreach (ObjectId siteId in siteIds)
    {
        Site site = ts.GetObject(siteId, OpenMode.ForRead) as Site;
        if (site == null) continue;

        ObjectIdCollection catchmentIds = site.GetCatchmentIds();
        foreach (ObjectId catchId in catchmentIds)
        {
            Catchment catchment = ts.GetObject(catchId, OpenMode.ForRead) as Catchment;
            if (catchment == null) continue;

            ed.WriteMessage($"\nCatchment: {catchment.Name}, Area: {catchment.Area:F2}");
        }
    }
    ts.Commit();
}
```

### Finding a Specific Catchment

```csharp
using (Transaction ts = db.TransactionManager.StartTransaction())
{
    ObjectIdCollection siteIds = doc.GetSiteIds();
    foreach (ObjectId siteId in siteIds)
    {
        Site site = ts.GetObject(siteId, OpenMode.ForRead) as Site;
        ObjectIdCollection catchmentIds = site.GetCatchmentIds();

        foreach (ObjectId catchId in catchmentIds)
        {
            Catchment c = ts.GetObject(catchId, OpenMode.ForRead) as Catchment;
            if (c != null && c.Name == "Catchment - (1)")
            {
                // Found the target catchment
                ProcessCatchment(c);
                break;
            }
        }
    }
    ts.Commit();
}
```

## Catchment Properties

- Name (string, get/set) — catchment display name
- Area (double, get) — computed area in square drawing units
- Perimeter (double, get) — boundary perimeter length
- SurfaceId (ObjectId, get) — reference surface for flow analysis
- RunoffCoefficient (double, get/set) — dimensionless C value for rational method
- RainfallIntensity (double, get/set) — design storm intensity (in/hr or mm/hr)
- TimeOfConcentration (double, get/set) — Tc in minutes
- DischargePoint (Point2d, get) — discharge location

### Reading Properties

```csharp
using (Transaction ts = db.TransactionManager.StartTransaction())
{
    Catchment catchment = ts.GetObject(catchmentId, OpenMode.ForRead) as Catchment;

    // Geometric properties
    string name = catchment.Name;
    double area = catchment.Area;                   // Square feet/meters depending on drawing units
    double perimeter = catchment.Perimeter;         // Linear units

    // Reference surface
    ObjectId surfaceId = catchment.SurfaceId;
    TinSurface surface = ts.GetObject(surfaceId, OpenMode.ForRead) as TinSurface;

    // Hydrology properties (read/write when opened ForWrite)
    double runoffCoeff = catchment.RunoffCoefficient;
    double rainfall = catchment.RainfallIntensity;     // inches/hour or mm/hour
    double toc = catchment.TimeOfConcentration;         // minutes

    // Discharge point
    Point2d discharge = catchment.DischargePoint;

    ed.WriteMessage($"\nCatchment: {name}");
    ed.WriteMessage($"\n  Area: {area:F2} sq ft");
    ed.WriteMessage($"\n  Perimeter: {perimeter:F2} ft");
    ed.WriteMessage($"\n  Runoff Coeff: {runoffCoeff:F3}");
    ed.WriteMessage($"\n  Rainfall: {rainfall:F2} in/hr");
    ed.WriteMessage($"\n  Tc: {toc:F2} min");
    ed.WriteMessage($"\n  Discharge: ({discharge.X:F2}, {discharge.Y:F2})");

    ts.Commit();
}
```

### Modifying Hydrology Properties

```csharp
using (Transaction ts = db.TransactionManager.StartTransaction())
{
    Catchment catchment = ts.GetObject(catchmentId, OpenMode.ForWrite) as Catchment;

    catchment.RunoffCoefficient = 0.65;
    catchment.RainfallIntensity = 4.5;       // in/hr for a design storm
    catchment.TimeOfConcentration = 15.0;    // minutes

    ts.Commit();
}
```

### Computing Peak Runoff (Rational Method)

The rational method formula is Q = C x I x A, where Q is peak runoff (cfs), C is the runoff coefficient, I is rainfall intensity (in/hr), and A is area (acres). Convert `Catchment.Area` from sq ft to acres by dividing by 43,560.

## Creating Catchments

### Limitations of the .NET API

Direct catchment creation through the .NET API is limited. The primary creation workflows (watershed delineation from surface analysis, catchment from object) are driven by interactive commands. For programmatic creation, use `SendStringToExecute` to invoke the built-in commands.

### Using Interactive Commands Programmatically

```csharp
// Invoke the CREATECATCHMENTFROMOBJECT command
// This requires user interaction to pick objects
Document acadDoc = Application.DocumentManager.MdiActiveDocument;
acadDoc.SendStringToExecute("CREATECATCHMENTFROMOBJECT\n", true, false, false);

// For watershed delineation from a surface
acadDoc.SendStringToExecute("CREATEWATERDROP\n", true, false, false);
```

### Creating a Catchment from a Closed Polyline Boundary

If the API supports `Catchment.Create` in your version, it generally requires a site, a surface, and a boundary:

```csharp
// Note: availability depends on Civil 3D version and API exposure.
// Check Autodesk.Civil.DatabaseServices.Catchment for static Create methods.
// If unavailable, use SendStringToExecute with CREATECATCHMENTFROMOBJECT.

using (Transaction ts = db.TransactionManager.StartTransaction())
{
    // Get site and surface references
    ObjectId siteId = doc.GetSiteIds()[0];
    ObjectId surfaceId = /* your surface ObjectId */;

    // If Catchment.Create is available:
    // ObjectId catchmentId = Catchment.Create(doc, siteId, surfaceId, boundaryPolylineId);

    ts.Commit();
}
```

## Interactive-Only Operations

Several catchment-related operations have no .NET API and must use commands:

```csharp
Document acadDoc = Application.DocumentManager.MdiActiveDocument;

// Water drop analysis — traces flow paths across a surface
acadDoc.SendStringToExecute("CREATEWATERDROP\n", true, false, false);

// Watershed delineation — identifies drainage basins on a surface
acadDoc.SendStringToExecute("ANALYZEWATERSHED\n", true, false, false);
```

After watershed analysis, catchments created from the results are accessible through the site collection as shown in the Accessing Catchments section.

## Catchment Groups

Catchments are organized within Sites. A site acts as a grouping mechanism, and multiple catchments within the same site share topology rules.

### Iterating Catchment Groups by Site

```csharp
using (Transaction ts = db.TransactionManager.StartTransaction())
{
    ObjectIdCollection siteIds = doc.GetSiteIds();
    foreach (ObjectId siteId in siteIds)
    {
        Site site = ts.GetObject(siteId, OpenMode.ForRead) as Site;
        ObjectIdCollection catchmentIds = site.GetCatchmentIds();

        if (catchmentIds.Count == 0) continue;

        ed.WriteMessage($"\nSite: {site.Name} ({catchmentIds.Count} catchments)");

        double totalArea = 0;
        foreach (ObjectId cId in catchmentIds)
        {
            Catchment c = ts.GetObject(cId, OpenMode.ForRead) as Catchment;
            if (c != null)
            {
                totalArea += c.Area;
                ed.WriteMessage($"\n  {c.Name}: {c.Area:F2} sq ft");
            }
        }
        ed.WriteMessage($"\n  Total area: {totalArea:F2} sq ft ({totalArea / 43560.0:F2} acres)");
    }
    ts.Commit();
}
```

## Hydrology Calculations

### Composite Runoff Coefficient

When a catchment has multiple land use types, compute a weighted runoff coefficient:

```csharp
// Weighted C value for a composite catchment
// C3D stores a single RunoffCoefficient per catchment,
// so composite values must be computed externally and assigned.

double[] areas = { 20000, 15000, 8000 };        // sub-area sq ft
double[] coefficients = { 0.35, 0.65, 0.90 };   // grass, pavement, roof

double weightedC = 0;
double totalArea = 0;
for (int i = 0; i < areas.Length; i++)
{
    weightedC += areas[i] * coefficients[i];
    totalArea += areas[i];
}
weightedC /= totalArea;

using (Transaction ts = db.TransactionManager.StartTransaction())
{
    Catchment catchment = ts.GetObject(catchmentId, OpenMode.ForWrite) as Catchment;
    catchment.RunoffCoefficient = weightedC;
    ts.Commit();
}
```

### Summarizing Multiple Catchments for a Pipe Network

```csharp
using (Transaction ts = db.TransactionManager.StartTransaction())
{
    // Gather all catchments contributing to a storm network
    Site site = ts.GetObject(targetSiteId, OpenMode.ForRead) as Site;
    ObjectIdCollection catchmentIds = site.GetCatchmentIds();

    double totalQ = 0;
    foreach (ObjectId cId in catchmentIds)
    {
        Catchment c = ts.GetObject(cId, OpenMode.ForRead) as Catchment;
        if (c == null) continue;

        double areaAcres = c.Area / 43560.0;
        double q = c.RunoffCoefficient * c.RainfallIntensity * areaAcres;
        totalQ += q;

        ed.WriteMessage($"\n  {c.Name}: Q = {q:F2} cfs");
    }
    ed.WriteMessage($"\nTotal design flow: {totalQ:F2} cfs");

    ts.Commit();
}
```

## Catchment Labels

### Adding Catchment Labels

Catchment labels display area, runoff, and other properties directly on the drawing. Label placement is typically handled through the Annotate ribbon or via commands:

```csharp
// Add catchment area label via command
acadDoc.SendStringToExecute("ADDCATCHMENTLABEL\n", true, false, false);
```

### Enumerating Catchment Label Styles

```csharp
using (Transaction ts = db.TransactionManager.StartTransaction())
{
    // Access catchment label styles from the document
    ObjectIdCollection styleIds = doc.Styles.LabelStyles
        .CatchmentLabelStyles.AreaLabelStyles.GetDescendantIds();

    foreach (ObjectId styleId in styleIds)
    {
        LabelStyle style = ts.GetObject(styleId, OpenMode.ForRead) as LabelStyle;
        if (style != null)
        {
            ed.WriteMessage($"\nCatchment label style: {style.Name}");
        }
    }
    ts.Commit();
}
```

### Catchment Label Property Fields

Common property fields available in catchment labels:
- `Catchment Area` -- the computed area of the catchment boundary
- `Catchment Perimeter` -- boundary perimeter length
- `Runoff Coefficient` -- the C value
- `Rainfall Intensity` -- design storm intensity
- `Time of Concentration` -- Tc in minutes
- `Peak Runoff` -- computed Q value (rational method)
- `Catchment Name` -- the catchment object name

## Catchment Styles

### Accessing and Assigning Catchment Styles

```csharp
using (Transaction ts = db.TransactionManager.StartTransaction())
{
    // List available catchment styles
    ObjectIdCollection styleIds = doc.Styles.CatchmentStyles;
    foreach (ObjectId styleId in styleIds)
    {
        CatchmentStyle style = ts.GetObject(styleId, OpenMode.ForRead) as CatchmentStyle;
        if (style != null)
            ed.WriteMessage($"\nCatchment style: {style.Name}");
    }

    // Assign a style to a catchment
    Catchment catchment = ts.GetObject(catchmentId, OpenMode.ForWrite) as Catchment;
    // catchment.StyleId = targetStyleId;

    ts.Commit();
}
```

### Style Display Properties

Catchment styles control the visual representation of the catchment boundary, fill pattern, and flow path display. Style configuration is generally done through the UI (Edit Catchment Style dialog) since the style component display properties have limited .NET API write access.

## Gotchas

- **Catchment creation is primarily interactive.** The .NET API does not provide robust `Catchment.Create` methods in most versions. Use `SendStringToExecute` to invoke creation commands when automating.
- **Catchments require a Site.** You cannot create orphan catchments; they must belong to a Site. If no site exists, one must be created first.
- **Surface dependency is critical.** Catchments reference a surface for elevation and flow analysis. If the surface is deleted or rebuilt, catchment data may become invalid or require regeneration.
- **Area units follow drawing settings.** `Catchment.Area` returns values in the drawing's current square units (sq ft or sq m). Always check `DrawingUnits` before performing calculations.
- **Rational method assumes consistent units.** The formula Q = CIA expects C (dimensionless), I (in/hr), and A (acres) to produce Q in cfs. Convert area from sq ft to acres (divide by 43560) before computing.
- **Watershed delineation has no direct .NET API.** Surface watershed analysis must be run through the UI or via command strings. Results are read-only after generation.
- **Flow path geometry may not be directly accessible.** The longest flow path used for Tc calculations is sometimes stored internally and not exposed as a standard polyline entity through the API.
- **`GetCatchmentIds()` returns only catchments in that specific site.** If catchments are spread across multiple sites, you must iterate all sites to find them all.
- **Time of Concentration is user-specified, not auto-calculated.** Civil 3D stores the Tc value you assign but does not automatically compute it from flow path geometry via the .NET API.
- **Label style hierarchy uses `GetDescendantIds()`.** Like other Civil 3D label styles, catchment label styles can be nested in subcategories. Always use `GetDescendantIds()` instead of direct iteration to get all styles.
- **Catchment property changes require `OpenMode.ForWrite`.** Reading properties works with `ForRead`, but modifying `RunoffCoefficient`, `RainfallIntensity`, or `TimeOfConcentration` requires opening the catchment `ForWrite` within a transaction.
- **COM/interop alternatives exist for some operations.** If the managed .NET API is insufficient, some catchment operations can be accessed through the Civil 3D COM API, though this is less common in modern development.

## Related Skills

- `c3d-surfaces` -- surfaces that drive catchment delineation and flow analysis
- `c3d-pipe-networks` -- storm pipe networks that receive catchment runoff at discharge points
- `c3d-label-styles` -- general label style configuration and management
- `c3d-root-objects` -- CivilDocument access and transaction patterns
