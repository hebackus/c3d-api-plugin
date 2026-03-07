---
name: c3d-survey
description: Survey database, survey figures, survey points, survey networks, equipment databases, linework processing, figure prefixes
---

# Civil 3D Survey

Use this skill when working with survey databases, figures, points, networks, equipment, or linework processing in Civil 3D.

## API Limitations — Read This First

The Civil 3D Survey subsystem is one of the **least-exposed** areas in the .NET API. Many operations that are routine in the UI (importing field books, running least squares adjustments, editing equipment databases) have **no direct .NET API entry point**. The survey database lives outside the drawing in a separate SQLite-based file structure, and most manipulation goes through the `Autodesk.Civil.DatabaseServices` survey classes or falls back to `SendStringToExecute` for command-line-only operations.

The primary .NET namespace is `Autodesk.Civil.DatabaseServices` — survey classes live alongside other Civil 3D objects but have a distinctly different access pattern because the survey database is external to the DWG.

## Survey Database Access

### Opening the Survey Database

The survey database is a folder-based database separate from the drawing. Access it through `CivilDocument`:

```csharp
using Autodesk.Civil;
using Autodesk.Civil.DatabaseServices;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;

// Get the survey database collection for the current document
var doc = CivilDocument.GetCivilDocument(
    Application.DocumentManager.MdiActiveDocument.Database);

// The SurveyDatabases property gives access to all survey databases
// associated with the current drawing
SurveyDatabaseCollection surveyDbs = doc.SurveyDatabases;
```

### Enumerating Survey Databases

```csharp
using (Transaction ts = doc.Database.TransactionManager.StartTransaction())
{
    foreach (string dbName in surveyDbs)
    {
        ed.WriteMessage($"\nSurvey database: {dbName}");
    }
    ts.Commit();
}
```

### Database Location

Survey databases are stored in a project folder, typically:
`C:\Civil 3D Projects\<ProjectName>\Survey\Survey Databases\<DatabaseName>\`

The database location is configured in the drawing settings under Survey > Survey Database. You can read the current database path but changing it programmatically requires `SendStringToExecute`.

```csharp
// Get the current survey database (if one is set as current)
string currentDbName = surveyDbs.GetCurrentDatabaseName();
if (!string.IsNullOrEmpty(currentDbName))
{
    ed.WriteMessage($"\nCurrent survey DB: {currentDbName}");
}
```

## Survey Points

Survey points in the survey database are distinct from COGO points (`CogoPoint`). Survey points live in the survey database and can be imported into the drawing as COGO points.

### Reading Survey Points

```csharp
// Access points through the survey database
// Note: Direct enumeration of survey points requires the database be open
// The .NET API exposes limited read access to survey point properties

// Survey points have these core properties:
// - PointNumber (int)
// - Easting (double) — X coordinate
// - Northing (double) — Y coordinate
// - Elevation (double) — Z coordinate
// - RawDescription (string) — field description
// - FullDescription (string) — expanded description after desc key processing
```

### Importing Survey Points to Drawing

The most reliable way to get survey points into a drawing as COGO points is through commands:

```csharp
// Import survey points as COGO points via command
// This is necessary because the .NET API does not expose a direct
// "import survey points to drawing" method
string cmd = "SURVEYIMPORTPOINTS\n";
Application.DocumentManager.MdiActiveDocument
    .SendStringToExecute(cmd, true, false, false);
```

### Creating COGO Points from Survey Data Programmatically

If you have the coordinate data, create COGO points directly:

```csharp
using (Transaction ts = db.TransactionManager.StartTransaction())
{
    CogoPointCollection cogoPts = CivilDocument.GetCivilDocument(db).CogoPoints;

    // Add a point with survey-sourced coordinates
    ObjectId ptId = cogoPts.Add(easting, northing, elevation);
    CogoPoint pt = ptId.GetObject(OpenMode.ForWrite) as CogoPoint;
    pt.PointNumber = surveyPointNumber;
    pt.RawDescription = rawDescription;

    ts.Commit();
}
```

## Survey Figures

Figures are polyline-like objects in the survey database that represent field-surveyed linework (edges of pavement, building corners, fences, etc.). They can be promoted to the drawing as feature lines or 3D polylines.

### Figure Prefixes

Figure prefixes control automatic behavior when figures are created from field codes. A prefix database maps name prefixes to:

- **Breakline status** — whether the figure acts as a surface breakline
- **Layer assignment** — which layer the figure goes to when inserted in the drawing
- **Style** — which figure style to apply
- **Lot line** — whether it defines a parcel lot line

```csharp
// Figure prefix databases are managed through the Survey settings
// in the UI. The .NET API provides read access but modification
// is limited. Access figure prefix settings via:
//   Survey Tab > User Settings > Figure Prefix Database

// To programmatically set up figure prefixes, use SendStringToExecute
// with the EDITFIGUREPREFIXDATABASE command
string cmd = "EDITFIGUREPREFIXDATABASE\n";
Application.DocumentManager.MdiActiveDocument
    .SendStringToExecute(cmd, true, false, false);
```

### Figure Styles

Figure styles control the display of survey figures (color, linetype, layer). Figure style configuration is managed through the Settings tab in the Toolspace under `Survey > Figure Prefix Databases`. The .NET API does not expose a `FigureStyle` class or a direct `FigureStyleIds` collection — figure style assignment is done through figure prefix database settings in the UI.

### Accessing Figures in the Drawing

Once figures are inserted into the drawing, they become Civil 3D entities:

```csharp
using (Transaction ts = db.TransactionManager.StartTransaction())
{
    // Figures inserted into the drawing appear as Feature objects
    // in the survey database or as AutoCAD entities (3D polylines)
    // depending on how they were imported.

    // To find survey figures in model space, look for entities
    // on survey-related layers (typically "V-SURV-FIGR-*")
    var bt = ts.GetObject(db.BlockTableId, OpenMode.ForRead) as BlockTable;
    var ms = ts.GetObject(bt[BlockTableRecord.ModelSpace],
        OpenMode.ForRead) as BlockTableRecord;

    foreach (ObjectId entId in ms)
    {
        Entity ent = ts.GetObject(entId, OpenMode.ForRead) as Entity;
        if (ent.Layer.StartsWith("V-SURV", StringComparison.OrdinalIgnoreCase))
        {
            ed.WriteMessage($"\nSurvey entity: {ent.GetType().Name} on {ent.Layer}");
        }
    }

    ts.Commit();
}
```

## Survey Networks

Survey networks contain the raw observations (angles, distances) from field surveys. They support least squares adjustment for coordinate computation.

### Network Concepts

A survey network consists of:
- **Setups** — instrument positions (occupied points)
- **Observations** — measurements taken from each setup (angles, distances, directions)
- **Control points** — known coordinates used as fixed references
- **Adjusted coordinates** — computed positions after least squares processing

### Accessing Networks

```csharp
// Survey networks are managed within the survey database.
// The .NET API provides limited direct access to network data.
// Most network operations (creating networks, adding observations,
// running adjustments) are command-driven.

// List networks via command
string cmd = "SURVEYNETWORKMANAGER\n";
Application.DocumentManager.MdiActiveDocument
    .SendStringToExecute(cmd, true, false, false);
```

### Least Squares Adjustment

Least squares adjustment is **UI/command only** — there is no .NET API for running adjustments programmatically:

```csharp
// Run network adjustment via command line
// The SURVEYNETWORKADJUST command opens the adjustment dialog
string cmd = "_SURVEYNETWORKADJUST\n";
Application.DocumentManager.MdiActiveDocument
    .SendStringToExecute(cmd, true, false, false);
```

## Equipment Databases

Equipment databases store instrument and prism settings used during surveying. Each equipment entry defines:

- **Instrument settings** — EDM accuracy, angular accuracy, centering error
- **Prism constants** — offset values for different prism types
- **Target settings** — prism height, target height defaults

### Accessing Equipment Settings

```csharp
// Equipment databases are XML files stored in the Survey folder:
// C:\Civil 3D Projects\<Project>\Survey\Equipment Databases\

// The .NET API does not expose direct equipment database manipulation.
// Use the command interface:
string cmd = "EDITEQUIPMENTDATABASE\n";
Application.DocumentManager.MdiActiveDocument
    .SendStringToExecute(cmd, true, false, false);

// Equipment settings affect how raw observations are processed
// into coordinates. The prism constant offsets are applied during
// coordinate computation in the survey database.
```

## Importing Survey Data

### Field Book Files (.fbk)

Field book files contain raw survey observations. Import is command-driven:

```csharp
// Import a field book file into the current survey database
// This is command-only — no .NET API method exists
string fbkPath = @"C:\SurveyData\fieldbook.fbk";
string cmd = $"_IMPORTSURVEYDATA\n\"{fbkPath}\"\n";
Application.DocumentManager.MdiActiveDocument
    .SendStringToExecute(cmd, true, false, false);
```

### Point Files (.csv, .txt, .pnezd)

For point file import, you can either use the command or parse and create COGO points directly:

```csharp
// Option 1: Command-based import (respects survey database settings)
string cmd = "IMPORTSURVEYDATA\n";
Application.DocumentManager.MdiActiveDocument
    .SendStringToExecute(cmd, true, false, false);

// Option 2: Direct COGO point creation (bypasses survey database)
// Parse the file yourself and add points to the drawing
using (Transaction ts = db.TransactionManager.StartTransaction())
{
    var doc = CivilDocument.GetCivilDocument(db);
    CogoPointCollection pts = doc.CogoPoints;

    // Read CSV: PointNumber, Northing, Easting, Elevation, Description
    foreach (string line in File.ReadLines(csvPath))
    {
        string[] parts = line.Split(',');
        if (parts.Length < 5) continue;

        uint ptNum = uint.Parse(parts[0].Trim());
        double northing = double.Parse(parts[1].Trim());
        double easting = double.Parse(parts[2].Trim());
        double elev = double.Parse(parts[3].Trim());
        string desc = parts[4].Trim();

        ObjectId ptId = pts.Add(
            new Point3d(easting, northing, elev), desc);
        CogoPoint pt = ptId.GetObject(OpenMode.ForWrite) as CogoPoint;
        pt.PointNumber = ptNum;
    }

    ts.Commit();
}
```

### LandXML Import

```csharp
// LandXML import/export is command-driven
// Import:
string xmlPath = @"C:\SurveyData\survey.xml";
string cmd = $"_LANDXMLIN\n\"{xmlPath}\"\n";
Application.DocumentManager.MdiActiveDocument
    .SendStringToExecute(cmd, true, false, false);

// Export:
string exportCmd = "_LANDXMLOUT\n";
Application.DocumentManager.MdiActiveDocument
    .SendStringToExecute(exportCmd, true, false, false);
```

## Linework Processing

Linework processing (also called "figure processing" or "code processing") converts field codes embedded in point descriptions into figures (lines connecting surveyed points).

### Description Key Sets and Code Sets

Description keys map raw descriptions to expanded descriptions, layers, symbols, and figure connections:

```csharp
using (Transaction ts = db.TransactionManager.StartTransaction())
{
    var doc = CivilDocument.GetCivilDocument(db);

    // Access description key sets via static method
    var dkSets = PointDescriptionKeySetCollection.GetPointDescriptionKeySets(db);

    foreach (ObjectId setId in dkSets)
    {
        var dkSet = ts.GetObject(setId, OpenMode.ForRead)
            as DescriptionKeySet;
        ed.WriteMessage($"\nDesc key set: {dkSet.Name}");

        // Enumerate keys within the set
        foreach (ObjectId keyId in dkSet)
        {
            var key = ts.GetObject(keyId, OpenMode.ForRead)
                as DescriptionKey;
            ed.WriteMessage($"\n  Key: {key.Code} -> Layer: {key.Layer}");
        }
    }

    ts.Commit();
}
```

### Processing Linework from Field Codes

Linework code processing interprets special codes in point descriptions to create, close, and curve figures:

```csharp
// Common linework codes (Autodesk default code set):
// B  = Begin figure
// E  = End figure
// C  = Close figure
// PC = Start curve
// PT = End curve
// .S = Side shot (no linework)
//
// Example field descriptions:
// "EP B"     -> Begin "EP" (Edge of Pavement) figure
// "EP"       -> Continue EP figure
// "EP C"     -> Close EP figure
// "TC B PC"  -> Begin "TC" (Top of Curb) figure, start curve

// Linework processing is triggered automatically during field book import
// if enabled in the survey database settings, or manually:
string cmd = "PROCESSLINEWORK\n";
Application.DocumentManager.MdiActiveDocument
    .SendStringToExecute(cmd, true, false, false);
```

### Figure Creation from Processed Codes

After linework processing, figures exist in the survey database. To get them into the drawing:

```csharp
// Insert all figures from the survey database into the drawing
string cmd = "SURVEYINSERTFIGURES\n";
Application.DocumentManager.MdiActiveDocument
    .SendStringToExecute(cmd, true, false, false);

// Figures become 3D polylines or feature lines in the drawing,
// depending on the figure prefix database settings.
```

## Survey Queries and Filtering

After survey points are imported as COGO points, query and filter them using the standard `CogoPointCollection` and `PointGroup` APIs. See the `c3d-points` skill for comprehensive coverage of COGO point querying by description, location, and point group membership.

## Gotchas

- **Survey database is external to the DWG.** Unlike COGO points, survey data lives in a folder-based database outside the drawing file. You cannot access survey observations purely through the drawing database.
- **Most survey operations are command-only.** Field book import, network adjustment, equipment editing, and linework processing have no .NET API methods. Use `SendStringToExecute` for these operations.
- **Survey points vs. COGO points are different objects.** Survey points exist in the survey database; COGO points exist in the drawing. Importing survey points creates COGO points, but they are separate entities after import. Edits to one do not propagate to the other.
- **Figure prefix database is not writable via .NET.** You can read figure prefix settings but cannot add or modify prefixes programmatically. Use the `EDITFIGUREPREFIXDATABASE` command instead.
- **Survey database must be set as current before operations.** Many survey commands fail silently or error if no survey database is set as the current database for the drawing.
- **LandXML import can create duplicate points.** If you import LandXML data that overlaps with existing survey or COGO points, duplicates are created. There is no automatic merge — you must handle deduplication yourself.
- **Linework processing codes are case-sensitive in some configurations.** The default Autodesk code set treats "B" and "b" the same, but custom code sets may not. Always verify with the active code set.
- **`SendStringToExecute` is asynchronous.** The command string is queued and executes after your .NET code returns. You cannot read results immediately. Use `Application.Idle` events or `CommandEnded` events to process results after command completion.
- **Survey figure insertion honors the active coordinate system.** If the drawing coordinate system differs from the survey database coordinate system, figures may appear in the wrong location. Verify coordinate system settings match before inserting figures.
- **The `SurveyDatabaseCollection` may be empty.** If no survey database has been created or associated with the drawing, the collection is empty. Always check before attempting to access a database.
- **Equipment database XML files are version-specific.** Equipment databases created in one Civil 3D version may not load correctly in another. Do not manually edit the XML files.
- **Network adjustment results are stored in the survey database, not the drawing.** After running least squares adjustment, updated coordinates exist only in the survey database until you explicitly update or re-import the points into the drawing.

## Related Skills

- `c3d-points` — COGO points created from survey data
- `c3d-surfaces` — surfaces created from survey figures and points
- `c3d-alignments` — alignments from survey figure data
- `c3d-root-objects` — CivilDocument access and transaction patterns
