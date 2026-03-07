---
name: acad-editor-input
description: Editor prompts (point, entity, selection, string, keyword, angle, double, integer, distance), selection filters, TypedValue, prompt options
---

# AutoCAD Editor Input

Use this skill when prompting users for input — picking points, selecting entities, building selection sets with filters, getting string/keyword/numeric input, and handling prompt results.

## Editor Access

```csharp
Document doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
Editor ed = doc.Editor;
```

The `Editor` class lives in `Autodesk.AutoCAD.EditorInput`. All prompt methods return a result object with a `Status` property — always check it before accessing `Value`.

## Point Input

### GetPoint

```csharp
// Simple point pick
PromptPointResult result = ed.GetPoint("\nPick insertion point: ");
if (result.Status != PromptStatus.OK) return;
Point3d point = result.Value;  // WCS coordinates
```

### PromptPointOptions

```csharp
PromptPointOptions ppo = new PromptPointOptions("\nPick second point: ")
{
    BasePoint = firstPoint,    // rubber-band line from this point
    UseBasePoint = true,
    AllowNone = true           // pressing Enter returns PromptStatus.None
};
PromptPointResult result = ed.GetPoint(ppo);
```

### GetCorner

```csharp
// Pick opposite corner of a rectangle (rubber-band box from base)
PromptCornerOptions pco = new PromptCornerOptions("\nPick opposite corner: ", basePoint);
PromptPointResult result = ed.GetCorner(pco);
```

## Entity Selection

### GetEntity

```csharp
PromptEntityOptions peo = new PromptEntityOptions("\nSelect a polyline: ");
peo.SetRejectMessage("\nEntity must be a polyline.");
peo.AddAllowedClass(typeof(Polyline), true);  // true = exact match only
PromptEntityResult per = ed.GetEntity(peo);
if (per.Status != PromptStatus.OK) return;

ObjectId entityId = per.ObjectId;
Point3d pickedPoint = per.PickedPoint;  // point where user clicked (UCS)
```

### Multiple Allowed Types

```csharp
PromptEntityOptions peo = new PromptEntityOptions("\nSelect line or polyline: ");
peo.SetRejectMessage("\nMust be a line or polyline.");
peo.AddAllowedClass(typeof(Line), true);
peo.AddAllowedClass(typeof(Polyline), true);
```

### GetNestedEntity

```csharp
// Select entity inside a block reference
PromptNestedEntityOptions pneo = new PromptNestedEntityOptions("\nSelect nested entity: ");
PromptNestedEntityResult pner = ed.GetNestedEntity(pneo);
if (pner.Status == PromptStatus.OK)
{
    ObjectId nestedId = pner.ObjectId;
    ObjectId[] containers = pner.GetContainers();  // block refs from outer to inner
    Matrix3d transform = pner.Transform;  // cumulative transform to WCS
}
```

## Selection Sets

### Interactive Selection

```csharp
PromptSelectionOptions pso = new PromptSelectionOptions
{
    MessageForAdding = "\nSelect objects: ",
    MessageForRemoval = "\nRemove objects: ",
    AllowDuplicates = false
};

PromptSelectionResult psr = ed.GetSelection(pso);
if (psr.Status != PromptStatus.OK) return;

SelectionSet ss = psr.Value;
ObjectId[] ids = ss.GetObjectIds();

foreach (ObjectId id in ids)
{
    Entity ent = (Entity)tr.GetObject(id, OpenMode.ForRead);
    // process entity
}
```

### Selection with Filter

```csharp
TypedValue[] filterValues = new TypedValue[]
{
    new TypedValue((int)DxfCode.Start, "LINE,LWPOLYLINE,POLYLINE,ARC,AECC_FEATURE_LINE")
};
SelectionFilter filter = new SelectionFilter(filterValues);

PromptSelectionOptions pso = new PromptSelectionOptions();
pso.MessageForAdding = "\nSelect line/polyline/arc/feature line objects: ";

PromptSelectionResult psr = ed.GetSelection(pso, filter);
if (psr.Status != PromptStatus.OK) return;

int count = psr.Value.Count;
```

### Non-Interactive Selection

```csharp
// Select all matching entities in the drawing
PromptSelectionResult psr = ed.SelectAll(filter);

// Select by window (only fully enclosed)
PromptSelectionResult psr = ed.SelectWindow(corner1, corner2, filter);

// Select by crossing window (touching or enclosed)
PromptSelectionResult psr = ed.SelectCrossingWindow(corner1, corner2, filter);

// Select by fence (polyline crossing)
Point3dCollection fencePoints = new Point3dCollection { pt1, pt2, pt3 };
PromptSelectionResult psr = ed.SelectFence(fencePoints, filter);

// Select at a specific point
PromptSelectionResult psr = ed.SelectAtPoint(point, filter);
```

### Iterating SelectedObjects

```csharp
foreach (SelectedObject selObj in psr.Value)
{
    if (selObj == null) continue;
    ObjectId id = selObj.ObjectId;
    // selObj.SelectionMethod tells how it was selected
}
```

## SelectionFilter and TypedValue

### Simple Filter by Entity Type

```csharp
// Single type
SelectionFilter filter = new SelectionFilter(
    new TypedValue[] { new TypedValue((int)DxfCode.Start, "LWPOLYLINE") }
);

// Multiple types (comma-separated in one value)
SelectionFilter filter = new SelectionFilter(
    new TypedValue[] { new TypedValue((int)DxfCode.Start, "LINE,ARC,LWPOLYLINE") }
);
```

### Filter by Layer

```csharp
SelectionFilter filter = new SelectionFilter(
    new TypedValue[] { new TypedValue((int)DxfCode.LayerName, "C-ROAD-*") }
);
```

### Compound Filters (AND / OR)

```csharp
// Type AND layer
SelectionFilter filter = new SelectionFilter(new TypedValue[]
{
    new TypedValue((int)DxfCode.Operator, "<and"),
    new TypedValue((int)DxfCode.Start, "LWPOLYLINE"),
    new TypedValue((int)DxfCode.LayerName, "C-ROAD-*"),
    new TypedValue((int)DxfCode.Operator, "and>")
});

// Type1 OR Type2 (on specific layer)
SelectionFilter filter = new SelectionFilter(new TypedValue[]
{
    new TypedValue((int)DxfCode.Operator, "<and"),
        new TypedValue((int)DxfCode.Operator, "<or"),
            new TypedValue((int)DxfCode.Start, "LINE"),
            new TypedValue((int)DxfCode.Start, "LWPOLYLINE"),
        new TypedValue((int)DxfCode.Operator, "or>"),
        new TypedValue((int)DxfCode.LayerName, "C-ROAD-*"),
    new TypedValue((int)DxfCode.Operator, "and>")
});
```

### Common DxfCode Constants

| DxfCode | Value | Filters by |
|---------|-------|------------|
| `DxfCode.Start` | 0 | DXF entity type name |
| `DxfCode.Text` | 1 | Text content |
| `DxfCode.BlockName` | 2 | Block name (for INSERT) |
| `DxfCode.Handle` | 5 | Entity handle |
| `DxfCode.LayerName` | 8 | Layer name |
| `DxfCode.LinetypeName` | 6 | Linetype name |
| `DxfCode.Color` | 62 | ACI color index |
| `DxfCode.ClassName` | 100 | Managed class name (AcDb*) |
| `DxfCode.Operator` | -4 | Compound filter operator |

### Operator Strings

- `"<and"` / `"and>"` — all conditions must match
- `"<or"` / `"or>"` — any condition matches
- `"<not"` / `"not>"` — negate condition
- `"<xor"` / `"xor>"` — exactly one matches

### Comparison Operators (for numeric DxfCodes)

Use with `DxfCode.Operator`:
- `"<"`, `">"`, `"<="`, `">="`, `"!="`, `"="` — compare numeric group codes
- `"*"` — wildcard match for string group codes

## Angle Input

```csharp
PromptAngleOptions pao = new PromptAngleOptions("\nSpecify rotation angle <0>: ")
{
    BasePoint = insertionPoint,
    UseBasePoint = true,        // rubber-band angle indicator
    AllowNone = true            // Enter accepts default
};

PromptDoubleResult result = ed.GetAngle(pao);
double radians = result.Status == PromptStatus.OK ? result.Value : 0.0;
double degrees = radians * 180.0 / Math.PI;
```

## Numeric Input

### GetDouble

```csharp
PromptDoubleOptions pdo = new PromptDoubleOptions("\nEnter scale factor <1.0>: ")
{
    DefaultValue = 1.0,
    UseDefaultValue = true,
    AllowNegative = false,
    AllowZero = false,
    AllowNone = true
};
PromptDoubleResult result = ed.GetDouble(pdo);
```

### GetInteger

```csharp
PromptIntegerOptions pio = new PromptIntegerOptions("\nEnter count <5>: ")
{
    DefaultValue = 5,
    UseDefaultValue = true,
    LowerLimit = 1,
    UpperLimit = 100
};
PromptIntegerResult result = ed.GetInteger(pio);
```

### GetDistance

```csharp
PromptDistanceOptions pdist = new PromptDistanceOptions("\nSpecify offset distance: ")
{
    BasePoint = startPoint,
    UseBasePoint = true,      // rubber-band from base
    AllowNegative = false,
    AllowZero = false
};
PromptDoubleResult result = ed.GetDistance(pdist);
```

## String and Keyword Input

### GetString

```csharp
PromptStringOptions pstro = new PromptStringOptions("\nEnter layer name: ")
{
    AllowSpaces = true,
    DefaultValue = "0",
    UseDefaultValue = true
};
PromptResult result = ed.GetString(pstro);
if (result.Status == PromptStatus.OK)
    string text = result.StringResult;
```

### Keywords

```csharp
PromptKeywordOptions pko = new PromptKeywordOptions("\nSelect option [Yes/No/All]: ", "Yes No All");
pko.AllowNone = false;
pko.AllowArbitraryInput = false;

PromptResult result = ed.GetKeywords(pko);
if (result.Status == PromptStatus.OK)
{
    switch (result.StringResult)
    {
        case "Yes": /* ... */ break;
        case "No":  /* ... */ break;
        case "All": /* ... */ break;
    }
}
```

### Keywords on Other Prompts

```csharp
// Add keywords to a point prompt
PromptPointOptions ppo = new PromptPointOptions("\nPick point or [Exit/Undo]: ", "Exit Undo");
PromptPointResult result = ed.GetPoint(ppo);

if (result.Status == PromptStatus.Keyword)
{
    string keyword = result.StringResult;
    // handle keyword
}
else if (result.Status == PromptStatus.OK)
{
    Point3d point = result.Value;
    // handle point
}
```

## PromptStatus Values

| Status | Meaning |
|--------|---------|
| `OK` | User provided valid input |
| `Cancel` | User pressed Escape |
| `None` | User pressed Enter with AllowNone = true |
| `Keyword` | User entered a keyword |
| `Error` | Input error |
| `Modeless` | Modeless operation |
| `Other` | Other result |

Always check `Status` before accessing `Value` — `Value` is undefined when Status is not OK.

## Writing Messages

```csharp
// Output to command line
ed.WriteMessage("\nProcessed {0} entities.", count);
ed.WriteMessage($"\nError: {ex.Message}");

// Note: \n prefix to start on a new line (not \r\n)
```

## Gotchas

- `GetAngle` returns **radians**, not degrees — multiply by `180.0 / Math.PI` for degrees
- `GetPoint` returns **WCS** coordinates — use `ed.CurrentUserCoordinateSystem` for UCS conversion
- `GetEntity` `PickedPoint` is in **UCS**, not WCS
- `PromptSelectionResult.Value` is **null** when Status is not OK — always check Status first
- `AddAllowedClass` second parameter (`exactMatch`): `true` = exact type only, `false` = includes derived types
- TypedValue array order matters in compound filters — operator tags must wrap their operands
- DXF name `"LWPOLYLINE"` = `Polyline` class (lightweight); `"POLYLINE"` = `Polyline2d` or `Polyline3d`
- Multiple entity types in one filter: comma-separate in a single TypedValue `"LINE,ARC,LWPOLYLINE"`
- `Keywords.Add` has overloads — `(globalName, localName, displayName)` for localization support
- `GetSelection` during a modeless command needs `CommandFlags.UsePickSet` or explicit user pick
- Wildcard patterns in string filters use AutoCAD wildcards (`*`, `?`, `#`, `@`, `.`, `~`), not regex
- `SelectAll` with no filter returns everything including entities on frozen/locked layers

## Related Skills

- `acad-layers` — selection filters can filter by DxfCode.LayerName (8)
- `acad-polylines` — common selection target; use DxfCode.Start `"LWPOLYLINE"` or `"POLYLINE"`
- `acad-geometry` — GetPoint returns Point3d; geometry types used throughout prompts
- `acad-blocks` — GetEntity can select block references; filter with DxfCode.Start `"INSERT"`
