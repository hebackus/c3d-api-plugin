---
name: acad-dimensions
description: Dimensions - aligned, rotated, arc, radial, diametric, angular, ordinate - creation, text overrides, and dimension styles
---

# AutoCAD Dimensions

Use this skill when creating or modifying dimension objects - linear, aligned, angular, radial, diametric, arc, and ordinate dimensions, plus dimension styles.

## Dimension Class Hierarchy

```
Dimension (abstract base)
├── AlignedDimension
├── RotatedDimension
├── ArcDimension
├── DiametricDimension
├── RadialDimension
├── LineAngularDimension2
├── Point3AngularDimension
└── OrdinateDimension
```

## Creating Dimensions

### Aligned Dimension

```csharp
AlignedDimension dim = new AlignedDimension(
    new Point3d(0, 0, 0),      // first extension line point
    new Point3d(100, 0, 0),    // second extension line point
    new Point3d(50, 20, 0),    // dimension line position
    "",                         // dimension text (empty = measurement)
    db.Dimstyle);              // dimension style ObjectId

btr.AppendEntity(dim);
tr.AddNewlyCreatedDBObject(dim, true);
```

Properties: `XLine1Point`, `XLine2Point`, `DimLinePoint` (Point3d, get/set), `Oblique` (double, get/set)

### Rotated Dimension

```csharp
RotatedDimension dim = new RotatedDimension(
    0.0,                        // rotation angle (radians)
    new Point3d(0, 0, 0),      // first extension line point
    new Point3d(100, 50, 0),   // second extension line point
    new Point3d(50, 70, 0),    // dimension line position
    "",                         // dimension text
    db.Dimstyle);
```

Properties: `XLine1Point`, `XLine2Point`, `DimLinePoint`, `Rotation`, `Oblique` (all get/set)

### Arc Dimension

```csharp
ArcDimension dim = new ArcDimension(
    new Point3d(50, 50, 0),    // center point
    new Point3d(100, 50, 0),   // first extension line point
    new Point3d(50, 100, 0),   // second extension line point
    new Point3d(80, 80, 0),    // arc point (dimension position)
    "",                         // dimension text
    db.Dimstyle);
```

Properties: `CenterPoint`, `XLine1Point`, `XLine2Point`, `ArcPoint` (Point3d, get/set), `Leader1Point`, `Leader2Point` (Point3d, get/set), `ArcStartParam`, `ArcEndParam` (double, get/set), `ArcSymbolType` (int, get/set), `IsPartial` (bool, get/set), `HasLeader` (bool, get/set)

### Radial Dimension

```csharp
RadialDimension dim = new RadialDimension(
    new Point3d(50, 50, 0),    // center point
    new Point3d(100, 50, 0),   // chord point (on circle)
    10.0,                       // leader length
    "",                         // dimension text
    db.Dimstyle);
```

Properties: `Center`, `ChordPoint` (Point3d, get/set), `LeaderLength` (double, get/set)

### Diametric Dimension

```csharp
DiametricDimension dim = new DiametricDimension(
    new Point3d(100, 50, 0),   // chord point (near side)
    new Point3d(0, 50, 0),     // far chord point (opposite side)
    10.0,                       // leader length
    "",                         // dimension text
    db.Dimstyle);
```

Properties: `ChordPoint`, `FarChordPoint` (Point3d, get/set), `LeaderLength` (double, get/set)

### Angular Dimension (2-Line)

```csharp
LineAngularDimension2 dim = new LineAngularDimension2(
    new Point3d(0, 0, 0),      // first line start
    new Point3d(100, 0, 0),    // first line end
    new Point3d(0, 0, 0),      // second line start
    new Point3d(0, 100, 0),    // second line end
    new Point3d(30, 30, 0),    // arc point (dimension position)
    "",                         // dimension text
    db.Dimstyle);
```

Properties: `XLine1Start`, `XLine1End`, `XLine2Start`, `XLine2End`, `ArcPoint` (all Point3d, get/set)

### Angular Dimension (3-Point)

```csharp
Point3AngularDimension dim = new Point3AngularDimension(
    new Point3d(50, 50, 0),    // center point (vertex)
    new Point3d(100, 50, 0),   // first point on angle
    new Point3d(50, 100, 0),   // second point on angle
    new Point3d(80, 80, 0),    // arc point (dimension position)
    "",                         // dimension text
    db.Dimstyle);
```

Properties: `CenterPoint`, `XLine1Point`, `XLine2Point`, `ArcPoint` (all Point3d, get/set)

### Ordinate Dimension

```csharp
OrdinateDimension dim = new OrdinateDimension(
    true,                       // true = X axis, false = Y axis
    new Point3d(100, 50, 0),   // defining point
    new Point3d(100, 80, 0),   // leader end point
    "",                         // dimension text
    db.Dimstyle);
```

Properties: `UsingXAxis` (bool, get/set), `UsingYAxis` (bool, get-only), `Origin` (Point3d, get/set), `DefiningPoint` (Point3d, get/set), `LeaderEndPoint` (Point3d, get/set)

## Dimension Base Properties (on all dimension types)

**Text:**
- `DimensionText` (string, get/set) - override text ("" = show measurement, "<>" = include measurement in custom text)
- `Prefix` (string, get/set) - text prefix
- `Suffix` (string, get/set) - text suffix
- `TextPosition` (Point3d, get/set) - text position
- `TextRotation` (double, get/set) - text rotation in radians
- `TextAttachment` (AttachmentPoint, get/set)
- `UsingDefaultTextPosition` (bool, get/set)
- `Measurement` (double, get-only) - the measured value

**Style:**
- `DimensionStyle` (ObjectId, get/set)
- `DimensionStyleName` (string, get/set)
- `TextStyleId` (ObjectId, get/set) - Dimtxsty equivalent

**Geometry:**
- `Normal` (Vector3d, get/set)
- `Elevation` (double, get/set)
- `HorizontalRotation` (double, get/set)
- `DimBlockPosition` (Point3d, get-only)
- `DimBlockId` (ObjectId, get/set)
- `DynamicDimension` (bool, get/set)

**Dimension variable overrides (per-entity):**
These override the dimension style for this specific dimension. Most commonly used:

- `Dimasz` (double) - arrow size
- `Dimtxt` (double) - text height
- `Dimscale` (double) - overall scale factor
- `Dimgap` (double) - gap between text and dimension line
- `Dimexe` (double) - extension line extension
- `Dimexo` (double) - extension line offset from origin
- `Dimdle` (double) - dimension line extension past extension lines
- `Dimdli` (double) - dimension line increment for baseline dimensions
- `Dimclrd` (Color) - dimension line color
- `Dimclre` (Color) - extension line color
- `Dimclrt` (Color) - text color
- `Dimse1` (bool) - suppress first extension line
- `Dimse2` (bool) - suppress second extension line
- `Dimsd1` (bool) - suppress first dimension line segment
- `Dimsd2` (bool) - suppress second dimension line segment
- `Dimtih` (bool) - text inside horizontal
- `Dimtoh` (bool) - text outside horizontal
- `Dimtix` (bool) - force text inside extension lines
- `Dimtofl` (bool) - force dimension line between extension lines
- `Dimupt` (bool) - user-positioned text
- `Dimblk` (ObjectId) - default arrow block
- `Dimblk1` (ObjectId) - first arrow block
- `Dimblk2` (ObjectId) - second arrow block
- `Dimsah` (bool) - separate arrow heads
- `Dimtol` (bool) - show tolerances
- `Dimlim` (bool) - show limits
- `Dimtp` (double) - plus tolerance
- `Dimtm` (double) - minus tolerance
- `Dimdec` (int) - primary decimal places
- `Dimlfac` (double) - linear scale factor
- `Dimrnd` (double) - rounding increment
- `Dimpost` (string) - primary units suffix
- `Dimapost` (string) - alternate units suffix
- `Dimalt` (bool) - alternate units on
- `Dimaltf` (double) - alternate units scale factor
- `Dimaltd` (int) - alternate units decimal places
- `Dimlunit` (int) - linear unit format
- `Dimaunit` (int) - angular unit format
- `Dimadec` (int) - angular decimal places
- `Dimdsep` (char) - decimal separator
- `Dimfrac` (int) - fraction format
- `DimfxlenOn` (bool) - fixed extension line length on
- `Dimfxlen` (double) - fixed extension line length
- `Dimtfill` (int) - text background fill mode
- `Dimtfillclr` (Color) - text background fill color
- `Dimlwd` (LineWeight) - dimension line weight
- `Dimlwe` (LineWeight) - extension line weight
- `Dimltype` (ObjectId) - dimension line linetype
- `Dimltex1` (ObjectId) - extension line 1 linetype
- `Dimltex2` (ObjectId) - extension line 2 linetype
- `Dimtmove` (int) - text movement rule
- `Dimjust` (int) - text justification
- `Dimtad` (int) - text above/below dimension line
- `Dimtvp` (double) - text vertical position

## Methods

- `SetDimstyleData(DimStyleTableRecord)` - apply style to dimension
- `GetDimstyleData()` -> `DimStyleTableRecord` - get effective style
- `RecomputeDimensionBlock(bool forceUpdate)` - regenerate dimension graphics
- `GenerateLayout()` - generate layout geometry
- `FormatMeasurement(double measurement, string dimensionText)` -> string
- `RemoveTextField()` - remove text field
- `FieldToMText(MText)` - convert field to MText
- `FieldFromMText(MText)` - extract field from MText

## Dimension Styles

```csharp
DimStyleTable dst = (DimStyleTable)tr.GetObject(
    db.DimStyleTableId, OpenMode.ForWrite);

DimStyleTableRecord dstr = new DimStyleTableRecord();
dstr.Name = "MyDimStyle";

// Text settings
dstr.Dimtxt = 2.5;           // text height
dstr.Dimtxsty = textStyleId;  // text style
dstr.Dimgap = 1.0;           // text gap
dstr.Dimtad = 1;             // text above (0=centered, 1=above)

// Arrow settings
dstr.Dimasz = 2.5;           // arrow size
dstr.Dimtsz = 0.0;           // tick size (0 = use arrows)

// Line settings
dstr.Dimexe = 1.25;          // extension line extension
dstr.Dimexo = 0.625;         // extension line offset

// Scale
dstr.Dimscale = 1.0;         // overall scale

// Units
dstr.Dimdec = 2;             // decimal places
dstr.Dimlunit = 2;           // decimal (2=Decimal, 4=Architectural)

ObjectId styleId = dst.Add(dstr);
tr.AddNewlyCreatedDBObject(dstr, true);

// Apply style to a dimension
dim.DimensionStyle = styleId;
```

**DimStyleTableRecord** has all the same Dim* properties as the Dimension base class, plus:
- `Name` (inherited from SymbolTableRecord)
- `Dimtxsty` (ObjectId) - text style (same as `TextStyleId` on Dimension)
- `Dimtsz` (double) - tick mark size
- `IsModifiedForRecompute` (bool, get-only)
- `GetArrowId(DimArrowFlag whichArrow)` -> ObjectId

## Gotchas

- Empty string `""` for `DimensionText` shows the measured value; use `"<>"` to embed the measurement within custom text (e.g., `"Length: <> mm"`)
- All Dim* properties on a Dimension entity are **per-entity overrides** - they only take effect when they differ from the dimension style
- Use `SetDimstyleData()` to apply all dim variable overrides from a style at once; individual property sets only override specific variables
- `Measurement` is read-only and computed from geometry points - move the points to change the measurement
- `RecomputeDimensionBlock(true)` must be called after changing geometry points programmatically for the visual to update
- Angular dimensions measure the angle on the side where `ArcPoint` is placed - the arc point determines which of the four possible angles is measured
- `DimStyleTableRecord.Dimtxsty` is the text style; `Dimension.TextStyleId` is the same thing but with a friendlier name
- `Dimblk` sets both arrows; use `Dimblk1`/`Dimblk2` with `Dimsah = true` for separate arrow heads
- Ordinate dimensions: `UsingXAxis = true` measures X coordinates, `UsingXAxis = false` measures Y coordinates
- `GetDimstyleData()` returns a **temporary** `DimStyleTableRecord` not owned by the database — call `Dispose()` on it after use to avoid memory leaks: `using (var tmp = dim.GetDimstyleData()) { ... }`
- `DimStyleTableRecord.CopyFrom(sourceDstr)` copies all dim variable values but **overwrites the `Name` property** — reassign `dstr.Name` immediately after calling `CopyFrom()`
