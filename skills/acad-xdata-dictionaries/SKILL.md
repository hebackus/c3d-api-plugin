---
name: acad-xdata-dictionaries
description: XData reading and writing, RegAppTable registration, ResultBuffer construction, Named Object Dictionary, Extension Dictionaries, XRecord storage, DBDictionary operations, choosing between XData vs XRecord vs Extension Dictionary
---

# XData and Dictionaries

Use this skill when you need to attach custom data to entities or store application-level data in a drawing. Covers XData (extended entity data), the Named Object Dictionary (NOD), Extension Dictionaries, XRecords, and DBDictionary operations.

## XData (Extended Entity Data)

XData attaches lightweight key-value data directly to any `DBObject`. Each application registers a name and gets up to 16 KB of storage per entity.

### Registering an Application Name

Before writing XData, the application name must exist in the `RegAppTable`.

```csharp
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Runtime;

public static void EnsureRegApp(Database db, Transaction tr, string appName)
{
    RegAppTable rat = (RegAppTable)tr.GetObject(
        db.RegAppTableId, OpenMode.ForRead);

    if (!rat.Has(appName))
    {
        rat.UpgradeOpen();
        RegAppTableRecord record = new RegAppTableRecord();
        record.Name = appName;
        rat.Add(record);
        tr.AddNewlyCreatedDBObject(record, true);
    }
}
```

### Writing XData

XData is stored as a `ResultBuffer` attached via `Entity.XData`. The buffer must start with `DxfCode.ExtendedDataRegAppName`.

```csharp
public static void WriteXData(Entity ent, Transaction tr,
    string appName, string value, double number)
{
    ent.UpgradeOpen();

    ResultBuffer rb = new ResultBuffer(
        new TypedValue((int)DxfCode.ExtendedDataRegAppName, appName),
        new TypedValue((int)DxfCode.ExtendedDataAsciiString, value),
        new TypedValue((int)DxfCode.ExtendedDataReal, number),
        new TypedValue((int)DxfCode.ExtendedDataInteger32, 42)
    );

    ent.XData = rb;
    rb.Dispose();
}
```

### Reading XData

Use `GetXDataForApplication` to retrieve XData for a specific application name.

```csharp
public static void ReadXData(Entity ent, string appName)
{
    ResultBuffer rb = ent.GetXDataForApplication(appName);
    if (rb == null)
        return;

    TypedValue[] values = rb.AsArray();
    // values[0] is always the RegAppName entry
    for (int i = 1; i < values.Length; i++)
    {
        TypedValue tv = values[i];
        short typeCode = tv.TypeCode;
        object val = tv.Value;

        switch (typeCode)
        {
            case (int)DxfCode.ExtendedDataAsciiString:
                string s = (string)val;
                break;
            case (int)DxfCode.ExtendedDataReal:
                double d = (double)val;
                break;
            case (int)DxfCode.ExtendedDataInteger32:
                int n = (int)val;
                break;
        }
    }

    rb.Dispose();
}
```

### XData TypedValue Codes

Common `DxfCode.ExtendedData*` constants for XData entries:

- `ExtendedDataRegAppName` (1001) — application name, must be first entry
- `ExtendedDataAsciiString` (1000) — string value, max 255 characters per entry
- `ExtendedDataReal` (1040) — double-precision floating point
- `ExtendedDataInteger16` (1070) — 16-bit integer
- `ExtendedDataInteger32` (1071) — 32-bit integer
- `ExtendedDataControlString` (1002) — open `"{"` or close `"}"` for grouping
- `ExtendedDataWorldSpacePosition` (1011) — 3D point (Point3d)
- `ExtendedDataWorldSpaceDisp` (1012) — 3D displacement vector
- `ExtendedDataWorldDirection` (1013) — 3D direction vector
- `ExtendedDataDist` (1041) — distance (scaled with drawing)
- `ExtendedDataScale` (1042) — scale factor (scaled with drawing)
- `ExtendedDataHandle` (1005) — soft-pointer entity handle
- `ExtendedDataBinaryChunk` (1004) — binary data as byte array
- `ExtendedDataLayerName` (1003) — layer name reference

### Grouping with Control Strings

Use control strings to create nested structures within XData.

```csharp
ResultBuffer rb = new ResultBuffer(
    new TypedValue((int)DxfCode.ExtendedDataRegAppName, "MY_APP"),
    new TypedValue((int)DxfCode.ExtendedDataAsciiString, "header"),
    new TypedValue((int)DxfCode.ExtendedDataControlString, "{"),
    new TypedValue((int)DxfCode.ExtendedDataAsciiString, "key1"),
    new TypedValue((int)DxfCode.ExtendedDataReal, 3.14),
    new TypedValue((int)DxfCode.ExtendedDataAsciiString, "key2"),
    new TypedValue((int)DxfCode.ExtendedDataInteger32, 99),
    new TypedValue((int)DxfCode.ExtendedDataControlString, "}"),
    new TypedValue((int)DxfCode.ExtendedDataAsciiString, "footer")
);
```

## Named Object Dictionary (NOD)

The NOD is a drawing-level `DBDictionary` for storing application data not tied to a specific entity. Access it via `Database.NamedObjectDictionaryId`.

```csharp
public static void WriteToNOD(Database db, Transaction tr,
    string dictName, string key, string value)
{
    DBDictionary nod = (DBDictionary)tr.GetObject(
        db.NamedObjectDictionaryId, OpenMode.ForRead);

    DBDictionary appDict;
    if (nod.Contains(dictName))
    {
        appDict = (DBDictionary)tr.GetObject(
            nod.GetAt(dictName), OpenMode.ForWrite);
    }
    else
    {
        nod.UpgradeOpen();
        appDict = new DBDictionary();
        nod.SetAt(dictName, appDict);
        tr.AddNewlyCreatedDBObject(appDict, true);
    }

    Xrecord xrec = new Xrecord();
    xrec.Data = new ResultBuffer(
        new TypedValue((int)DxfCode.Text, value)
    );
    appDict.SetAt(key, xrec);
    tr.AddNewlyCreatedDBObject(xrec, true);
}
```

### Reading from the NOD

```csharp
public static string ReadFromNOD(Database db, Transaction tr,
    string dictName, string key)
{
    DBDictionary nod = (DBDictionary)tr.GetObject(
        db.NamedObjectDictionaryId, OpenMode.ForRead);

    if (!nod.Contains(dictName))
        return null;

    DBDictionary appDict = (DBDictionary)tr.GetObject(
        nod.GetAt(dictName), OpenMode.ForRead);

    if (!appDict.Contains(key))
        return null;

    Xrecord xrec = (Xrecord)tr.GetObject(
        appDict.GetAt(key), OpenMode.ForRead);

    TypedValue[] values = xrec.Data.AsArray();
    return (string)values[0].Value;
}
```

## Extension Dictionaries

An Extension Dictionary is a `DBDictionary` attached to a specific entity. Use it when you need structured or large data storage per entity.

### Creating and Writing

```csharp
public static void WriteExtensionData(Entity ent, Transaction tr,
    string dictName, string key, ResultBuffer data)
{
    // Ensure the entity has an extension dictionary
    if (ent.ExtensionDictionary == ObjectId.Null)
    {
        ent.UpgradeOpen();
        ent.CreateExtensionDictionary();
    }

    DBDictionary extDict = (DBDictionary)tr.GetObject(
        ent.ExtensionDictionary, OpenMode.ForRead);

    DBDictionary appDict;
    if (extDict.Contains(dictName))
    {
        appDict = (DBDictionary)tr.GetObject(
            extDict.GetAt(dictName), OpenMode.ForWrite);
    }
    else
    {
        extDict.UpgradeOpen();
        appDict = new DBDictionary();
        extDict.SetAt(dictName, appDict);
        tr.AddNewlyCreatedDBObject(appDict, true);
    }

    Xrecord xrec;
    if (appDict.Contains(key))
    {
        xrec = (Xrecord)tr.GetObject(
            appDict.GetAt(key), OpenMode.ForWrite);
    }
    else
    {
        xrec = new Xrecord();
        appDict.SetAt(key, xrec);
        tr.AddNewlyCreatedDBObject(xrec, true);
    }

    xrec.Data = data;
}
```

### Reading from an Extension Dictionary

```csharp
public static ResultBuffer ReadExtensionData(Entity ent, Transaction tr,
    string dictName, string key)
{
    if (ent.ExtensionDictionary == ObjectId.Null)
        return null;

    DBDictionary extDict = (DBDictionary)tr.GetObject(
        ent.ExtensionDictionary, OpenMode.ForRead);

    if (!extDict.Contains(dictName))
        return null;

    DBDictionary appDict = (DBDictionary)tr.GetObject(
        extDict.GetAt(dictName), OpenMode.ForRead);

    if (!appDict.Contains(key))
        return null;

    Xrecord xrec = (Xrecord)tr.GetObject(
        appDict.GetAt(key), OpenMode.ForRead);

    return xrec.Data;
}
```

## XRecord

An `Xrecord` stores a `ResultBuffer` inside a `DBDictionary`. It has no size limit (unlike XData's 16 KB cap) and supports any `DxfCode` values.

### XRecord Properties and Methods

- `Data` (ResultBuffer, get/set) — the stored data payload
- `XlateReferences` (XlateType, get/set) — controls how ObjectId references translate during copy/merge operations

### Storing Complex Data in an XRecord

```csharp
public static void StoreComplexRecord(DBDictionary dict, Transaction tr,
    string key, string name, double[] coordinates)
{
    List<TypedValue> values = new List<TypedValue>();
    values.Add(new TypedValue((int)DxfCode.Text, name));
    values.Add(new TypedValue((int)DxfCode.Int32, coordinates.Length));
    foreach (double coord in coordinates)
    {
        values.Add(new TypedValue((int)DxfCode.Real, coord));
    }

    Xrecord xrec = new Xrecord();
    xrec.Data = new ResultBuffer(values.ToArray());
    dict.SetAt(key, xrec);
    tr.AddNewlyCreatedDBObject(xrec, true);
}
```

## DBDictionary Operations

`DBDictionary` is the container for XRecords and nested dictionaries. Both the NOD and Extension Dictionaries are `DBDictionary` instances.

### Key Methods

- `Contains(string key)` -> bool — check if a key exists
- `GetAt(string key)` -> ObjectId — get the ObjectId for a key
- `SetAt(string key, DBObject obj)` -> ObjectId — add or replace an entry
- `Remove(string key)` — remove an entry by key
- `Remove(ObjectId id)` — remove an entry by ObjectId
- `Count` (int, get) — number of entries

### Iterating a Dictionary

```csharp
public static void IterateDictionary(DBDictionary dict, Transaction tr)
{
    foreach (DBDictionaryEntry entry in dict)
    {
        string key = entry.Key;
        ObjectId valueId = entry.Value;

        DBObject obj = tr.GetObject(valueId, OpenMode.ForRead);
        if (obj is Xrecord xrec)
        {
            ResultBuffer data = xrec.Data;
            // process data...
        }
        else if (obj is DBDictionary nestedDict)
        {
            // recurse into nested dictionary
            IterateDictionary(nestedDict, tr);
        }
    }
}
```

### Searching for a Key Safely

```csharp
public static ObjectId TryGetDictEntry(DBDictionary dict, string key)
{
    if (dict.Contains(key))
        return dict.GetAt(key);
    return ObjectId.Null;
}
```

### Creating Nested Dictionaries

```csharp
public static DBDictionary GetOrCreateNestedDict(
    DBDictionary parent, Transaction tr, string name)
{
    if (parent.Contains(name))
    {
        return (DBDictionary)tr.GetObject(
            parent.GetAt(name), OpenMode.ForWrite);
    }

    parent.UpgradeOpen();
    DBDictionary child = new DBDictionary();
    parent.SetAt(name, child);
    tr.AddNewlyCreatedDBObject(child, true);
    return child;
}
```

## ResultBuffer Construction and Parsing

`ResultBuffer` is a collection of `TypedValue` entries used by both XData and XRecords. Construction and parsing patterns differ between the two contexts.

### Building a ResultBuffer

```csharp
// From explicit TypedValue arguments
ResultBuffer rb1 = new ResultBuffer(
    new TypedValue((int)DxfCode.Text, "hello"),
    new TypedValue((int)DxfCode.Real, 3.14),
    new TypedValue((int)DxfCode.Int32, 42)
);

// From a list (useful for dynamic data)
List<TypedValue> tvList = new List<TypedValue>();
tvList.Add(new TypedValue((int)DxfCode.Text, "name"));
tvList.Add(new TypedValue((int)DxfCode.Int32, items.Count));
foreach (var item in items)
    tvList.Add(new TypedValue((int)DxfCode.Text, item));
ResultBuffer rb2 = new ResultBuffer(tvList.ToArray());
```

### Parsing a ResultBuffer

```csharp
public static void ParseResultBuffer(ResultBuffer rb)
{
    if (rb == null)
        return;

    TypedValue[] values = rb.AsArray();
    for (int i = 0; i < values.Length; i++)
    {
        short code = values[i].TypeCode;
        object val = values[i].Value;

        // DxfCode.Text = 1, DxfCode.Real = 40, DxfCode.Int32 = 90
        // XData codes start at 1000+
        // Cast val based on the code
    }
}
```

### Common DxfCode Values for XRecords

XRecords accept standard DXF codes (unlike XData which requires 1000+ codes):

- `DxfCode.Text` (1) — string
- `DxfCode.Real` (40) — double
- `DxfCode.Int16` (70) — short
- `DxfCode.Int32` (90) — int
- `DxfCode.Bool` (290) — bool
- `DxfCode.SoftPointerId` (330) — soft-pointer ObjectId
- `DxfCode.HardPointerId` (340) — hard-pointer ObjectId
- `DxfCode.SoftOwnershipId` (360) — soft-ownership ObjectId
- `DxfCode.HardOwnershipId` (360) — hard-ownership ObjectId

## Choosing Between XData, XRecord, and Extension Dictionary

| Criteria | XData | XRecord (NOD) | XRecord (Extension Dict) |
|---|---|---|---|
| **Attached to** | Any entity | Drawing-level | Specific entity |
| **Size limit** | 16 KB per app | No limit | No limit |
| **Structure** | Flat list | Dictionary hierarchy | Dictionary hierarchy |
| **Survives WBLOCK** | Yes (with entity) | Only if referenced | Yes (with entity) |
| **Copied with entity** | Yes | No | Yes |
| **Performance** | Fast read/write | Moderate | Moderate |
| **Use when** | Small flags, tags, status values | App settings, drawing metadata | Large or structured per-entity data |

### Decision Guide

Use **XData** when:
- Data is small (under a few KB) and flat
- You need data to travel with the entity on copy/move
- You want the simplest read/write pattern
- Storing flags, status codes, or short identifiers

Use **XRecords in the NOD** when:
- Data is drawing-wide, not tied to a specific entity
- Storing application settings or configuration
- You need hierarchical key-value storage
- Data should persist even if entities are deleted

Use **XRecords in an Extension Dictionary** when:
- Data is tied to a specific entity but exceeds 16 KB
- You need structured or hierarchical per-entity storage
- Multiple applications store independent data on the same entity
- You need named keys for different data categories

## Gotchas

- XData's 16 KB limit is per registered application name per entity. Exceeding it throws an `eXdataSizeExceeded` exception with no partial write.
- The first `TypedValue` in an XData `ResultBuffer` must always be `DxfCode.ExtendedDataRegAppName`. Omitting it causes a silent failure or exception.
- `Entity.XData` setter replaces all XData for that application name. To append, read existing XData first, merge, then write back.
- `GetXDataForApplication` returns `null` (not an empty `ResultBuffer`) when no XData exists for the given app name. Always null-check.
- XData control strings (`"{"` and `"}"`) must be balanced. Unbalanced braces corrupt the XData structure.
- XData string entries (`ExtendedDataAsciiString`) are limited to 255 characters each. Split longer strings across multiple entries.
- `Xrecord.Data` can be `null` if the XRecord was created but never assigned data. Always null-check before calling `AsArray()`.
- `DBDictionary.GetAt` throws `Autodesk.AutoCAD.Runtime.Exception` if the key does not exist. Always check `Contains` first or catch the exception.
- `SetAt` on a `DBDictionary` with an existing key replaces the entry but does not erase the old object. The old object becomes orphaned unless you erase it explicitly.
- Extension dictionaries are created lazily. `Entity.ExtensionDictionary` returns `ObjectId.Null` until you call `CreateExtensionDictionary()`.
- When copying entities between drawings, XData handles (`ExtendedDataHandle`) are not automatically translated. Use `IdMapping` from deep clone operations to remap them.
- `ResultBuffer` implements `IDisposable`. Dispose it when you are done to avoid native memory leaks, especially in loops.
- XRecord `DxfCode.SoftPointerId` references are translated during deep clone; `DxfCode.HardPointerId` references are not. Choose the right pointer type based on whether the referenced entity should be included in copy operations.
- Do not store `ObjectId` values directly in XData. ObjectIds are session-specific. Use entity handles (`DxfCode.ExtendedDataHandle` for XData or `DxfCode.SoftPointerId` for XRecords) which persist across sessions.

## Related Skills

- `acad-blocks` — block references commonly use extension dictionaries for per-instance custom data
- `acad-fields` — field expressions can reference XData and dictionary values for dynamic text
- `c3d-root-objects` — Civil 3D stores style, label, and network data in drawing dictionaries accessed through the NOD
