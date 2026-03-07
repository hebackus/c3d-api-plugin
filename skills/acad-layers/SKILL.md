---
name: acad-layers
description: Layer table, layer records, properties, creation, states, filters, color and linetype assignment
---

# AutoCAD Layers

Use this skill when creating, reading, or modifying layers — accessing the layer table, setting layer properties (color, linetype, frozen, locked, off), managing layer states, and filtering layers.

## Layer Table Access

```csharp
Database db = doc.Database;
using (Transaction tr = db.TransactionManager.StartTransaction())
{
    LayerTable lt = (LayerTable)tr.GetObject(db.LayerTableId, OpenMode.ForRead);

    // Check if a layer exists (case-insensitive)
    bool exists = lt.Has("MyLayer");

    // Get layer by name
    ObjectId layerId = lt["MyLayer"];
    LayerTableRecord layer = (LayerTableRecord)tr.GetObject(layerId, OpenMode.ForRead);

    // Get current layer
    LayerTableRecord current = (LayerTableRecord)tr.GetObject(db.Clayer, OpenMode.ForRead);

    tr.Commit();
}
```

### Enumerating All Layers

```csharp
LayerTable lt = (LayerTable)tr.GetObject(db.LayerTableId, OpenMode.ForRead);
List<string> names = new List<string>();

foreach (ObjectId id in lt)
{
    LayerTableRecord layer = (LayerTableRecord)tr.GetObject(id, OpenMode.ForRead);
    if (layer.IsDependent) continue;  // skip xref layers
    if (layer.IsLocked) continue;     // skip locked layers
    names.Add(layer.Name);
}

names.Sort(StringComparer.OrdinalIgnoreCase);
```

## Creating Layers

### Basic Layer Creation

```csharp
private static void EnsureLayerExists(LayerTable lt, Transaction tr, string layerName)
{
    if (string.IsNullOrWhiteSpace(layerName) || layerName == "0")
        return;

    if (!lt.Has(layerName))
    {
        lt.UpgradeOpen();  // must upgrade the TABLE, not the record
        LayerTableRecord newLayer = new LayerTableRecord
        {
            Name = layerName
        };
        lt.Add(newLayer);
        tr.AddNewlyCreatedDBObject(newLayer, true);
    }
}
```

### Layer with Full Properties

```csharp
lt.UpgradeOpen();
LayerTableRecord layer = new LayerTableRecord
{
    Name = "C-ROAD-CURB",
    Color = Color.FromColorIndex(ColorMethod.ByAci, 3),  // green
    LinetypeObjectId = GetLinetypeId(tr, db, "CONTINUOUS"),
    LineWeight = LineWeight.LineWeight030,
    IsPlottable = true,
    Description = "Road curb lines"
};
lt.Add(layer);
tr.AddNewlyCreatedDBObject(layer, true);
```

### Looking Up a Linetype

```csharp
private static ObjectId GetLinetypeId(Transaction tr, Database db, string name)
{
    LinetypeTable ltt = (LinetypeTable)tr.GetObject(db.LinetypeTableId, OpenMode.ForRead);
    if (ltt.Has(name))
        return ltt[name];
    return db.ContinuousLinetype;  // fallback
}
```

## LayerTableRecord Properties

- `Name` (string, get/set) — layer name (max 255 chars)
- `Color` (Color, get/set) — layer color (ACI, TrueColor, or color book)
- `LinetypeObjectId` (ObjectId, get/set) — assigned linetype
- `LineWeight` (LineWeight, get/set) — line weight enum
- `IsOff` (bool, get/set) — layer visibility off
- `IsFrozen` (bool, get/set) — layer frozen (not regenerated)
- `IsLocked` (bool, get/set) — layer locked (visible but uneditable)
- `IsPlottable` (bool, get/set) — include in plot output
- `IsReconciled` (bool, get/set) — reconciled (new layer notification cleared)
- `IsHidden` (bool, get/set) — hidden in layer manager
- `ViewportVisibilityDefault` (bool, get/set) — default visibility in new viewports
- `PlotStyleName` (string, get/set) — named plot style
- `Description` (string, get/set) — layer description
- `Transparency` (Transparency, get/set) — layer transparency
- `IsDependent` (bool, get-only) — true if xref-dependent (read-only layer)
- `IsResolved` (bool, get-only) — true if xref resolved
- `ObjectId` (ObjectId, get-only) — database identity

## Color Assignment

### ACI (AutoCAD Color Index)

```csharp
// Standard ACI color (1-255)
layer.Color = Color.FromColorIndex(ColorMethod.ByAci, 1);  // red

// ByLayer (index 256) and ByBlock (index 0)
entity.ColorIndex = 256;  // ByLayer
entity.ColorIndex = 0;    // ByBlock
```

### True Color (RGB)

```csharp
layer.Color = Color.FromRgb(128, 64, 0);

// Read back
byte r = layer.Color.Red;
byte g = layer.Color.Green;
byte b = layer.Color.Blue;
```

### Color Book

```csharp
layer.Color = Color.FromNames("PANTONE+ Solid Coated", "PANTONE 185 C");
```

## LineWeight Values

Common `LineWeight` enum values:
- `LineWeight.ByLayer` (-1), `LineWeight.ByBlock` (-2), `LineWeight.ByLineWeightDefault` (-3)
- `LineWeight.LineWeight000` (0.00mm), `LineWeight.LineWeight013` (0.13mm)
- `LineWeight.LineWeight025` (0.25mm), `LineWeight.LineWeight030` (0.30mm)
- `LineWeight.LineWeight050` (0.50mm), `LineWeight.LineWeight100` (1.00mm)

## Transparency

```csharp
// Set transparency (0 = opaque, 90 = maximum transparency)
// AutoCAD limits transparency to 0–90, not 0–100
layer.Transparency = new Transparency(50);  // 50% transparent

// Read back
int percent = (int)(layer.Transparency.Alpha / 255.0 * 100.0);
```

## Reading Layer Properties

```csharp
private static bool IsLayerUsable(string layerName, Transaction tr, Database db, out string message)
{
    message = string.Empty;
    LayerTable lt = (LayerTable)tr.GetObject(db.LayerTableId, OpenMode.ForRead);

    if (!lt.Has(layerName))
    {
        message = $"Layer '{layerName}' was not found.";
        return false;
    }

    LayerTableRecord layer = (LayerTableRecord)tr.GetObject(lt[layerName], OpenMode.ForRead);

    if (layer.IsDependent)
    {
        message = $"Layer '{layerName}' is xref-dependent.";
        return false;
    }
    if (layer.IsLocked)
    {
        message = $"Layer '{layerName}' is locked.";
        return false;
    }

    return true;
}
```

## Modifying Layer Properties

```csharp
LayerTableRecord layer = (LayerTableRecord)tr.GetObject(lt[layerName], OpenMode.ForRead);
layer.UpgradeOpen();  // switch to ForWrite

layer.IsLocked = false;
layer.IsFrozen = false;
layer.IsOff = false;
layer.Color = Color.FromColorIndex(ColorMethod.ByAci, 7);
```

### Setting the Current Layer

```csharp
// Set by ObjectId
db.Clayer = lt["MyLayer"];

// Verify
string currentName = ((LayerTableRecord)tr.GetObject(db.Clayer, OpenMode.ForRead)).Name;
```

## Deleting and Purging Layers

```csharp
// Erase a layer (fails if layer has entities or is current/0/xref)
LayerTableRecord layer = (LayerTableRecord)tr.GetObject(lt[layerName], OpenMode.ForWrite);
layer.Erase(true);

// Check purgeable layers
ObjectIdCollection layerIds = new ObjectIdCollection();
foreach (ObjectId id in lt)
    layerIds.Add(id);

db.Purge(layerIds);  // removes non-purgeable IDs from the collection

foreach (ObjectId id in layerIds)
{
    LayerTableRecord purgeableLayer = (LayerTableRecord)tr.GetObject(id, OpenMode.ForWrite);
    purgeableLayer.Erase(true);
}
```

## Layer Filters

```csharp
// Access the layer filter tree
LayerFilterTree filterTree = db.LayerFilters;
LayerFilterCollection filters = filterTree.Root.NestedFilters;

foreach (LayerFilter filter in filters)
{
    ed.WriteMessage($"\nFilter: {filter.Name}, Expression: {filter.FilterExpression}");
}

// Create a new filter
LayerFilter newFilter = new LayerFilter();
newFilter.Name = "Road Layers";
newFilter.FilterExpression = "NAME==\"C-ROAD-*\"";
filterTree.Root.NestedFilters.Add(newFilter);
db.LayerFilters = filterTree;  // save back
```

## Layer States

```csharp
LayerStateManager lsm = db.LayerStateManager;

// Save current layer states
lsm.SaveLayerState("DesignFreeze", LayerStateMasks.Color | LayerStateMasks.On | LayerStateMasks.Frozen);

// Restore
lsm.RestoreLayerState("DesignFreeze", ObjectId.Null,
    0,  // no viewport
    LayerStateMasks.Color | LayerStateMasks.On | LayerStateMasks.Frozen);

// Check existence
bool exists = lsm.HasLayerState("DesignFreeze");

// Delete
lsm.DeleteLayerState("DesignFreeze");

// Export/import .las files
lsm.ExportLayerState("DesignFreeze", @"C:\Temp\DesignFreeze.las");
lsm.ImportLayerState(@"C:\Temp\DesignFreeze.las");
```

### LayerStateMasks Flags

- `LayerStateMasks.On`, `Frozen`, `Locked`, `Color`, `Linetype`, `LineWeight`
- `LayerStateMasks.PlotStyle`, `Plot`, `NewViewport`, `Transparency`
- Combine with `|` operator

## Gotchas

- Layer `"0"` cannot be deleted, renamed, or frozen — it is always present
- Must call `UpgradeOpen()` on the **LayerTable** before `Add()`, not on individual records
- `IsDependent = true` means xref-dependent layer — cannot modify properties
- Setting `IsFrozen = true` on the current layer throws an exception
- `Color.FromColorIndex` uses `ColorMethod.ByAci`; ByLayer = index 256, ByBlock = index 0
- `LayerTable.Has()` is case-insensitive
- `db.Clayer` requires an ObjectId, not a name string — use `lt["name"]` to convert
- Layer names cannot contain: `< > / \ " : ; ? * | = '`
- Transparency range is 0–90 (AutoCAD limitation), not 0–100
- Viewport-specific overrides (VP Freeze, VP Color) require the viewport override API, not direct layer properties
- Erasing a layer that has entities on it throws — move or erase the entities first

## Related Skills

- `acad-blocks` — entities within blocks inherit layer properties
- `acad-polylines` — polylines and other entities reference layers via the Layer property
- `acad-editor-input` — selection filters can filter entities by DxfCode.LayerName (8)
