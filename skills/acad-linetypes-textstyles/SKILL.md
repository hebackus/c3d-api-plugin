---
name: acad-linetypes-textstyles
description: LinetypeTable, LinetypeTableRecord, loading linetypes from .lin files, linetype properties, simple and complex linetypes, LTSCALE system variables, TextStyleTable, TextStyleTableRecord, creating text styles, TrueType vs SHX fonts, SHX shapes for complex linetypes
---

# AutoCAD Linetypes and Text Styles

Use this skill when creating, loading, or modifying linetypes and text styles — accessing linetype and text style tables, loading linetypes from .lin files, configuring linetype scale variables, creating text styles with TrueType or SHX fonts, and setting up complex linetypes that embed text or shape elements.

## Linetype Table Access

```csharp
Database db = doc.Database;
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    LinetypeTable ltt = (LinetypeTable)tr.GetObject(db.LinetypeTableId, OpenMode.ForRead);

    // Check if a linetype exists (case-insensitive)
    bool exists = ltt.Has("DASHED");

    // Get linetype by name
    ObjectId ltId = ltt["DASHED"];
    LinetypeTableRecord ltr = (LinetypeTableRecord)tr.GetObject(ltId, OpenMode.ForRead);

    // Enumerate all linetypes
    foreach (ObjectId id in ltt)
    {
        LinetypeTableRecord rec = (LinetypeTableRecord)tr.GetObject(id, OpenMode.ForRead);
        if (rec.IsDependent) continue;  // skip xref linetypes
        ed.WriteMessage($"\n{rec.Name}: {rec.AsciiDescription}");
    }

    tr.Commit();
}
```

## System Linetypes

Three linetypes are always present and cannot be deleted:

```csharp
ObjectId byLayerId = db.ByLayerLinetype;       // entities inherit from layer
ObjectId byBlockId = db.ByBlockLinetype;       // entities inherit from block reference
ObjectId continuousId = db.ContinuousLinetype; // solid unbroken line

// Current entity linetype (CELTYPE sysvar)
ObjectId currentId = db.Celtype;
db.Celtype = ltt["HIDDEN"];  // set current linetype for new entities
```

## Loading Linetypes from .lin Files

```csharp
// Load a single linetype by name from a .lin file
db.LoadLineTypeFile("HIDDEN", "acad.lin");
db.LoadLineTypeFile("HIDDEN2", "acadiso.lin");  // metric
db.LoadLineTypeFile("MY_LINETYPE", @"C:\Standards\custom.lin");  // custom file
```

### Safe Load with Existence Check

```csharp
private static ObjectId EnsureLinetypeLoaded(
    Database db, Transaction tr, string linetypeName, string linFile = "acad.lin")
{
    LinetypeTable ltt = (LinetypeTable)tr.GetObject(db.LinetypeTableId, OpenMode.ForRead);
    if (ltt.Has(linetypeName))
        return ltt[linetypeName];

    try
    {
        db.LoadLineTypeFile(linetypeName, linFile);
    }
    catch (Autodesk.AutoCAD.Runtime.Exception ex)
        when (ex.ErrorStatus == ErrorStatus.FilerError)
    {
        return db.ContinuousLinetype;  // .lin file not found
    }
    catch (Autodesk.AutoCAD.Runtime.Exception ex)
        when (ex.ErrorStatus == ErrorStatus.DuplicateKey)
    {
        // Already loaded (race condition)
    }

    ltt = (LinetypeTable)tr.GetObject(db.LinetypeTableId, OpenMode.ForRead);
    return ltt.Has(linetypeName) ? ltt[linetypeName] : db.ContinuousLinetype;
}
```

## LinetypeTableRecord Properties

- `Name` (string, get/set) — linetype name
- `AsciiDescription` (string, get/set) — description shown in linetype dialog (e.g., "Hidden __ __ __")
- `PatternLength` (double, get-only) — total length of one pattern repeat
- `NumDashes` (int, get-only) — number of dash elements in the pattern
- `IsScaledToFit` (bool, get/set) — whether the pattern scales to fit the entity length
- `Comments` (string, get/set) — additional comments
- `IsDependent` (bool, get-only) — true if xref-dependent
- `IsResolved` (bool, get-only) — true if xref resolved

### Reading Dash Pattern Elements

```csharp
for (int i = 0; i < ltr.NumDashes; i++)
{
    double dashLength = ltr.DashLengthAt(i);      // positive=dash, negative=gap, zero=dot
    int shapeNumber = ltr.ShapeNumberAt(i);        // 0 for simple dashes; nonzero for shape elements
    ObjectId shapeStyleId = ltr.ShapeStyleAt(i);   // text style or shape-file style
    string textAt = ltr.TextAt(i);                 // non-empty for text elements
    double shapeScale = ltr.ShapeScaleAt(i);
    double shapeRotation = ltr.ShapeRotationAt(i);
    Vector2d shapeOffset = ltr.ShapeOffsetAt(i);
    bool ucsOriented = ltr.ShapeIsUcsOrientedAt(i);
}
```

## Simple vs Complex Linetypes

### Simple Linetypes

Simple linetypes contain only dashes, gaps, and dots — defined purely by numeric values:

```
;; .lin file definition
*DASHED,Dashed __ __ __ __
A,.5,-.25
```

All dash elements have `ShapeNumberAt(i) == 0` and `TextAt(i) == ""`.

### Complex Linetypes — Text Elements

Complex linetypes embed text characters within the dash-gap pattern. The text element references a text style.

```
*HOT_WATER_SUPPLY,Hot water supply ----HW----HW----
A,.5,-.2,["HW",STANDARD,S=.1,R=0.0,X=-0.1,Y=-.05],-.2
```

Text elements appear as dash entries where `TextAt(i)` returns a non-empty string. `ShapeStyleAt(i)` returns the text style ObjectId used for rendering.

### Complex Linetypes — Shape Elements

Shape elements reference SHX shapes via a text style with `IsShapeFile = true`:

```
*FENCELINE1,Fenceline circle ----0-----0----0-----0----
A,.25,-.1,[CIRC1,ltypeshp.shx,x=-.1,s=.1],-.1,1
```

Shape elements have `ShapeNumberAt(i) != 0`. `ShapeStyleAt(i)` returns the shape-file text style ObjectId.

## Creating Linetypes Programmatically

```csharp
LinetypeTable ltt = (LinetypeTable)tr.GetObject(db.LinetypeTableId, OpenMode.ForWrite);

LinetypeTableRecord ltr = new LinetypeTableRecord();
ltr.Name = "MY_DASH_DOT";
ltr.AsciiDescription = "Custom dash dot __.__.__";
ltr.NumDashes = 4;
ltr.SetDashLengthAt(0, 0.5);    // dash (positive)
ltr.SetDashLengthAt(1, -0.25);  // gap (negative)
ltr.SetDashLengthAt(2, 0.0);    // dot (zero)
ltr.SetDashLengthAt(3, -0.25);  // gap

ltt.Add(ltr);
tr.AddNewlyCreatedDBObject(ltr, true);
```

### Complex Linetype with Text

```csharp
LinetypeTableRecord ltr = new LinetypeTableRecord();
ltr.Name = "GAS_LINE";
ltr.AsciiDescription = "Gas line ----GAS----GAS----";
ltr.NumDashes = 3;

ltr.SetDashLengthAt(0, 0.75);                                    // dash
ltr.SetDashLengthAt(1, -0.45);                                   // gap (holds text)
ltr.SetTextAt(1, "GAS");
ltr.SetShapeStyleAt(1, tst["STANDARD"]);                         // text style
ltr.SetShapeScaleAt(1, 0.1);
ltr.SetShapeRotationAt(1, 0.0);
ltr.SetShapeOffsetAt(1, new Vector2d(-0.1, -0.05));
ltr.SetShapeIsUcsOrientedAt(1, false);
ltr.SetDashLengthAt(2, -0.2);                                    // trailing gap

ltt.UpgradeOpen();
ltt.Add(ltr);
tr.AddNewlyCreatedDBObject(ltr, true);
```

## Linetype Scale System Variables

### LTSCALE — Global Linetype Scale

```csharp
double ltscale = db.Ltscale;   // read
db.Ltscale = 1.0;              // set (also: Application.SetSystemVariable("LTSCALE", 1.0))
```

### CELTSCALE — Current Entity Linetype Scale

```csharp
double celtscale = db.Celtscale;  // read
db.Celtscale = 0.5;               // new entities get LinetypeScale = 0.5

// Per-entity override (baked at creation from CELTSCALE, editable after)
entity.LinetypeScale = 2.0;
```

### PSLTSCALE — Paper Space Linetype Scale

```csharp
// 1 = scale linetypes in viewports to match paper space appearance
// 0 = display at model space scale
Application.SetSystemVariable("PSLTSCALE", (short)1);
```

**Effective scale** for an entity = `LTSCALE * Entity.LinetypeScale`
(CELTSCALE is baked into `Entity.LinetypeScale` at creation time.)

## Assigning Linetypes to Entities

```csharp
Line line = new Line(pt1, pt2);
line.LinetypeId = ltt["HIDDEN"];         // specific linetype
line.LinetypeId = db.ByLayerLinetype;    // inherit from layer (default)
line.LinetypeId = db.ByBlockLinetype;    // inherit from block reference
line.LinetypeScale = 0.5;               // per-entity scale
```

## TextStyleTable Access

```csharp
TextStyleTable tst = (TextStyleTable)tr.GetObject(db.TextStyleTableId, OpenMode.ForRead);

bool exists = tst.Has("MyStyle");
ObjectId styleId = tst["MyStyle"];
TextStyleTableRecord style = (TextStyleTableRecord)tr.GetObject(styleId, OpenMode.ForRead);

// Current text style
ObjectId currentStyleId = db.Textstyle;
db.Textstyle = tst["STANDARD"];  // set current

// Enumerate (skip xref and shape-file styles)
foreach (ObjectId id in tst)
{
    TextStyleTableRecord rec = (TextStyleTableRecord)tr.GetObject(id, OpenMode.ForRead);
    if (rec.IsDependent || rec.IsShapeFile) continue;
    ed.WriteMessage($"\n{rec.Name}: {rec.FileName}");
}
```

## Creating Text Styles

### TrueType Font Style

```csharp
TextStyleTable tst = (TextStyleTable)tr.GetObject(db.TextStyleTableId, OpenMode.ForWrite);

TextStyleTableRecord style = new TextStyleTableRecord();
style.Name = "ARIAL_NARROW";
style.FileName = "arialn.ttf";
style.BigFontFileName = "";
style.TextSize = 0.0;           // 0 = variable height (set per entity)
style.XScale = 1.0;             // width factor
style.ObliquingAngle = 0.0;
style.IsVertical = false;

ObjectId styleId = tst.Add(style);
tr.AddNewlyCreatedDBObject(style, true);

// Alternative: use FontDescriptor for TrueType
style.Font = new FontDescriptor("Arial Narrow", false, false, 0, 0);
//                               typeface        bold   italic charset pitch
```

### SHX Font Style

```csharp
TextStyleTableRecord style = new TextStyleTableRecord();
style.Name = "ROMANS_STYLE";
style.FileName = "romans.shx";
style.BigFontFileName = "";            // set for CJK (e.g., "bigfont.shx")
style.TextSize = 2.5;                 // fixed height
style.XScale = 0.8;
style.ObliquingAngle = 0.2618;        // ~15 degrees

tst.UpgradeOpen();
tst.Add(style);
tr.AddNewlyCreatedDBObject(style, true);
```

## TextStyleTableRecord Properties

- `Name` (string, get/set) — style name (inherited from SymbolTableRecord)
- `FileName` (string, get/set) — font file (.ttf for TrueType, .shx for SHX)
- `BigFontFileName` (string, get/set) — big font file for CJK/extended character sets
- `Font` (FontDescriptor, get/set) — TrueType descriptor (typeface, bold, italic, charset, pitch)
- `TextSize` (double, get/set) — fixed text size (0.0 = variable, set per entity)
- `PriorSize` (double, get/set) — last-used height when TextSize is 0
- `XScale` (double, get/set) — width factor (1.0 = normal)
- `ObliquingAngle` (double, get/set) — oblique angle in radians (positive = forward lean)
- `IsVertical` (bool, get/set) — vertical text direction
- `IsShapeFile` (bool, get/set) — true if this record represents a .shx shape file (not a user text style)
- `FlagBits` (byte, get/set) — bit 2 = vertical, bit 4 = shape file; prefer `IsVertical`/`IsShapeFile`

### Detecting Font Type

```csharp
FontDescriptor fd = style.Font;
bool isTrueType = !string.IsNullOrEmpty(fd.TypeFace);
bool isShx = style.FileName.EndsWith(".shx", StringComparison.OrdinalIgnoreCase);

// TrueType: fd.TypeFace = "Arial", fd.Bold, fd.Italic, fd.CharacterSet, fd.PitchAndFamily
// SHX: fd.TypeFace is empty, FileName is the .shx path
```

## TrueType vs SHX Fonts

| Aspect | TrueType (.ttf) | SHX (.shx) |
|--------|-----------------|-------------|
| Rendering | Filled outlines | Stroke-based vectors |
| PDF export | Embedded as fonts | Converted to geometry |
| Big fonts | Not supported | Supported via BigFontFileName |
| Performance | Slower for many entities | Faster for many entities |
| Font property | Populated TypeFace | Empty TypeFace |

Common SHX: `txt.shx`, `simplex.shx`, `romans.shx`, `complex.shx`, `monotxt.shx`, `isocp.shx`

## Loading SHX Shapes for Complex Linetypes

Complex linetypes that embed shapes need a text style with `IsShapeFile = true`:

```csharp
private static ObjectId EnsureShapeFileStyle(
    Database db, Transaction tr, string shxFileName)
{
    TextStyleTable tst = (TextStyleTable)tr.GetObject(
        db.TextStyleTableId, OpenMode.ForRead);

    // Check if a matching shape-file style already exists
    foreach (ObjectId id in tst)
    {
        TextStyleTableRecord existing = (TextStyleTableRecord)tr.GetObject(
            id, OpenMode.ForRead);
        if (existing.IsShapeFile &&
            existing.FileName.Equals(shxFileName, StringComparison.OrdinalIgnoreCase))
            return id;
    }

    // Create new shape-file style
    tst.UpgradeOpen();
    TextStyleTableRecord shapeStyle = new TextStyleTableRecord();
    shapeStyle.Name = Path.GetFileNameWithoutExtension(shxFileName).ToUpperInvariant();
    shapeStyle.FileName = shxFileName;   // e.g., "ltypeshp.shx"
    shapeStyle.IsShapeFile = true;
    shapeStyle.TextSize = 0.0;

    ObjectId newId = tst.Add(shapeStyle);
    tr.AddNewlyCreatedDBObject(shapeStyle, true);
    return newId;
}
```

Standard shape files: `ltypeshp.shx` (circles, boxes, diamonds), `gdt.shx` (GD&T symbols).

## Gotchas

- `db.LoadLineTypeFile()` throws if the name is not in the .lin file — always try/catch; also throws `DuplicateKey` if already loaded
- System linetypes (ByLayer, ByBlock, Continuous) cannot be deleted, renamed, or modified
- `LinetypeTable.Has()` is case-insensitive
- `PatternLength` is read-only — computed from sum of absolute dash lengths
- `NumDashes` must be set before `SetDashLengthAt()` — it allocates the internal array
- Dot elements use dash length of exactly `0.0` (not a small positive number)
- Complex text elements require the referenced text style to exist — missing style = text won't render
- Complex shape elements require a text style with `IsShapeFile = true` — not a regular text style
- Shape-file text styles appear in TextStyleTable but are hidden from user-facing style list
- `FileName` accepts just the file name (`arial.ttf`, `romans.shx`) — AutoCAD resolves from its fonts/support paths
- `TextSize = 0.0` means variable height — non-zero forces all entities to that fixed height
- `ObliquingAngle` is in radians, not degrees
- The STANDARD text style always exists and cannot be deleted, but can be modified
- `db.Textstyle` (lowercase 's') is the current text style ObjectId — not `TextStyleTableId`
- PSLTSCALE only takes effect after `REGEN` in each viewport
- `Entity.LinetypeScale` incorporates CELTSCALE from creation — changing CELTSCALE later does not update existing entities

## Related Skills

- `acad-layers` — linetype assignment on layers via LinetypeObjectId property
- `acad-mtext` — text style usage in MText and DBText entities
- `acad-dimensions` — dimension styles reference text styles for dimension text formatting
- `acad-polylines` — linetypes applied to polylines; linetype generation (PLINEGEN) across vertices
