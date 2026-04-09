---
name: acad-dimensions
description: Dimensions — aligned, rotated, arc, radial, angular, ordinate, text overrides
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

### Radial Dimension

```csharp
RadialDimension dim = new RadialDimension(
    new Point3d(50, 50, 0),    // center point
    new Point3d(100, 50, 0),   // chord point (on circle)
    10.0,                       // leader length
    "",                         // dimension text
    db.Dimstyle);
```

### Diametric Dimension

```csharp
DiametricDimension dim = new DiametricDimension(
    new Point3d(100, 50, 0),   // chord point (near side)
    new Point3d(0, 50, 0),     // far chord point (opposite side)
    10.0,                       // leader length
    "",                         // dimension text
    db.Dimstyle);
```

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

### Ordinate Dimension

```csharp
OrdinateDimension dim = new OrdinateDimension(
    true,                       // true = X axis, false = Y axis
    new Point3d(100, 50, 0),   // defining point
    new Point3d(100, 80, 0),   // leader end point
    "",                         // dimension text
    db.Dimstyle);
```

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

## Related Skills

- `acad-geometry` — Point3d coordinates for dimension definition points
- `acad-mtext` — MText formatting in dimension text overrides
- `acad-layers` — layer assignment for dimension entities
