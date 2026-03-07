---
name: acad-database-operations
description: Database cloning (WblockCloneObjects, DeepCloneObjects), IdMapping, side databases, Insert, Wblock, ReadDwgFile, SaveAs, Purge, Audit, WorkingDatabase context switching
---

# AutoCAD Database Operations

Use this skill when copying objects between databases, processing external .dwg files, importing blocks, purging unused records, or working with side databases outside the active document.

## WblockCloneObjects -- Copying Between Databases

`WblockCloneObjects` copies objects from one database to another. This is the primary mechanism for importing entities, symbol table records, or any named objects across drawings.

```csharp
public static void CopyEntitiesBetweenDatabases(
    Database sourceDb, Database destDb, ObjectIdCollection sourceIds)
{
    using (Transaction tr = sourceDb.TransactionManager.StartTransaction())
    {
        ObjectId destModelSpaceId = SymbolUtilityServices.GetBlockModelSpaceId(destDb);
        IdMapping idMap = new IdMapping();

        sourceDb.WblockCloneObjects(
            sourceIds,           // objects to copy
            destModelSpaceId,    // owner in destination database
            idMap,               // receives old-to-new ObjectId mapping
            DuplicateRecordCloning.Ignore,  // how to handle name collisions
            false);              // deferTranslation -- false for immediate resolution

        tr.Commit();
    }
}
```

### Cloning Symbol Table Records

For symbol table records (layers, text styles, etc.), the destination owner is the corresponding symbol table in the target database.

```csharp
public static void CopyLayersBetweenDatabases(Database sourceDb, Database destDb)
{
    using (Transaction tr = sourceDb.TransactionManager.StartTransaction())
    {
        LayerTable srcLt = (LayerTable)tr.GetObject(sourceDb.LayerTableId, OpenMode.ForRead);

        ObjectIdCollection layerIds = new ObjectIdCollection();
        foreach (ObjectId layerId in srcLt)
        {
            LayerTableRecord ltr = (LayerTableRecord)tr.GetObject(layerId, OpenMode.ForRead);
            if (ltr.Name != "0")
                layerIds.Add(layerId);
        }

        IdMapping idMap = new IdMapping();
        sourceDb.WblockCloneObjects(
            layerIds, destDb.LayerTableId, idMap,
            DuplicateRecordCloning.Ignore, false);

        tr.Commit();
    }
}
```

## DeepCloneObjects -- Copying Within the Same Database

`DeepCloneObjects` copies objects within a single database. It cannot cross database boundaries.

```csharp
public static ObjectIdCollection DuplicateEntities(
    Database db, ObjectIdCollection sourceIds, ObjectId ownerId)
{
    IdMapping idMap = new IdMapping();
    db.DeepCloneObjects(sourceIds, ownerId, idMap, false);

    ObjectIdCollection newIds = new ObjectIdCollection();
    foreach (IdPair pair in idMap)
    {
        if (pair.IsCloned && pair.IsPrimary)
            newIds.Add(pair.Value);
    }
    return newIds;
}
```

The destination owner can be any container -- model space, paper space, or a `BlockTableRecord` for cloning entities into a block definition.

## DuplicateRecordCloning Enum

Controls how name collisions are resolved when cloning named objects (layers, block definitions, text styles, etc.).

| Value | Behavior |
|-------|----------|
| `NotApplicable` | No duplicate handling (used for unnamed objects) |
| `Ignore` | Keep the existing destination record; skip the source record |
| `Replace` | Overwrite the destination record with the source record |
| `XrefMangleName` | Rename using xref-style convention (`BlockName$0$SymbolName`) |
| `MangleName` | Rename with a numeric suffix to avoid collision (`SymbolName_1`) |

`Ignore` is the safe default for imports. `Replace` forces source definitions onto the destination. `XrefMangleName` preserves both, matching bind-style naming.

## IdMapping and IdPair

`IdMapping` tracks the correspondence between source and destination ObjectIds after a clone operation.

```csharp
public static ObjectId TranslateId(IdMapping idMap, ObjectId sourceId)
{
    if (idMap.Contains(sourceId))
    {
        IdPair pair = idMap[sourceId];
        if (pair.IsCloned)
            return pair.Value;
    }
    return ObjectId.Null;
}

// Iterate all mapped pairs
foreach (IdPair pair in idMap)
{
    ObjectId sourceId = pair.Key;      // original ObjectId
    ObjectId destId   = pair.Value;    // new ObjectId in destination
    bool cloned  = pair.IsCloned;      // true if actually cloned
    bool primary = pair.IsPrimary;     // true if top-level requested object
    bool owner   = pair.IsOwnerXlated; // true if owner was translated
}
```

ObjectIds are database-specific -- an ObjectId from one database is meaningless in another. Always use `IdMapping` from clone operations to translate between databases.

## Database.Insert -- Importing a Drawing as a Block

`Insert` reads an entire .dwg file and creates a block definition from it.

```csharp
public static ObjectId InsertDrawingAsBlock(
    Database db, string dwgPath, string blockName)
{
    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        ObjectId blockId = db.Insert(
            blockName,  // name for the new block definition
            dwgPath,    // path to the .dwg file
            false);     // preserveSourceDatabase -- false to allow cleanup

        BlockTableRecord modelSpace = (BlockTableRecord)tr.GetObject(
            SymbolUtilityServices.GetBlockModelSpaceId(db), OpenMode.ForWrite);

        BlockReference blockRef = new BlockReference(Point3d.Origin, blockId);
        modelSpace.AppendEntity(blockRef);
        tr.AddNewlyCreatedDBObject(blockRef, true);

        tr.Commit();
        return blockId;
    }
}
```

To merge file content directly, insert as a block reference then call `ExplodeToOwnerSpace()` and erase the reference.

## Database.Wblock -- Writing Objects to a New File

`Wblock` exports objects or the entire database to a new .dwg file.

```csharp
// Wblock selected objects
using (Database newDb = db.Wblock(objectIds, Point3d.Origin))
    newDb.SaveAs(outputPath, DwgVersion.Current);

// Wblock entire database (clean copy, strips unused objects)
using (Database newDb = db.Wblock())
    newDb.SaveAs(outputPath, DwgVersion.Current);

// Wblock a single block definition (contents become model space)
using (Database newDb = db.Wblock(blockDefId))
    newDb.SaveAs(outputPath, DwgVersion.Current);
```

## ReadDwgFile and SaveAs

### Reading a .dwg File into a Side Database

```csharp
public static void ProcessExternalDrawing(string dwgPath)
{
    using (Database sideDb = new Database(false, true))
    {
        sideDb.ReadDwgFile(dwgPath, FileOpenMode.OpenForReadAndAllShare, true, null);
        // Parameters: path, fileMode, allowCPConversion, password

        using (Transaction tr = sideDb.TransactionManager.StartTransaction())
        {
            BlockTableRecord modelSpace = (BlockTableRecord)tr.GetObject(
                SymbolUtilityServices.GetBlockModelSpaceId(sideDb), OpenMode.ForRead);

            foreach (ObjectId entId in modelSpace)
            {
                Entity ent = (Entity)tr.GetObject(entId, OpenMode.ForRead);
                // Process entity...
            }
            tr.Commit();
        }
    }
}
```

### SaveAs Version Values

- `DwgVersion.Current` -- same version as the running AutoCAD
- `DwgVersion.AC1032` -- AutoCAD 2018-2025 format
- `DwgVersion.AC1027` -- AutoCAD 2013-2017 format
- `DwgVersion.AC1024` -- AutoCAD 2010-2012 format

Call `sideDb.CloseInput(true)` after `ReadDwgFile` to release the file lock while keeping the database usable in memory.

## Side Database Pattern

A "side database" is a `Database` created independently of any open document -- essential for batch processing, file inspection, or migrating objects without opening the drawing in the editor.

```csharp
public static void BatchImportBlocks(string[] dwgPaths, Database activeDb)
{
    foreach (string path in dwgPaths)
    {
        using (Database sideDb = new Database(false, true))
        {
            sideDb.ReadDwgFile(path, FileOpenMode.OpenForReadAndAllShare, true, null);

            using (Transaction tr = sideDb.TransactionManager.StartTransaction())
            {
                BlockTable bt = (BlockTable)tr.GetObject(sideDb.BlockTableId, OpenMode.ForRead);
                ObjectIdCollection blockIds = new ObjectIdCollection();

                foreach (ObjectId btrId in bt)
                {
                    BlockTableRecord btr = (BlockTableRecord)tr.GetObject(
                        btrId, OpenMode.ForRead);
                    if (!btr.IsLayout && !btr.IsAnonymous && !btr.IsFromExternalReference)
                        blockIds.Add(btrId);
                }

                if (blockIds.Count > 0)
                {
                    IdMapping idMap = new IdMapping();
                    sideDb.WblockCloneObjects(
                        blockIds, activeDb.BlockTableId, idMap,
                        DuplicateRecordCloning.Ignore, false);
                }
                tr.Commit();
            }
        }
    }
}
```

### Constructor Parameters

```csharp
// new Database(bool buildDefaultDrawing, bool noDocument)
new Database(false, true)  // empty shell for ReadDwgFile
new Database(true, true)   // new drawing from scratch (Layer 0, model space, etc.)
```

## Database.Purge -- Removing Unused Records

`Purge` filters an `ObjectIdCollection` in-place, removing IDs that are still referenced. The remaining IDs are safe to erase.

```csharp
public static void PurgeUnusedLayers(Database db)
{
    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        LayerTable lt = (LayerTable)tr.GetObject(db.LayerTableId, OpenMode.ForRead);
        ObjectIdCollection layerIds = new ObjectIdCollection();
        foreach (ObjectId id in lt)
            layerIds.Add(id);

        db.Purge(layerIds);  // filters in-place

        foreach (ObjectId id in layerIds)
        {
            SymbolTableRecord record = (SymbolTableRecord)tr.GetObject(id, OpenMode.ForWrite);
            record.Erase();
        }
        tr.Commit();
    }
}
```

For a full purge, loop over all symbol tables (`BlockTableId`, `LayerTableId`, `LinetypeTableId`, `TextStyleTableId`, `DimStyleTableId`, `RegAppTableId`) and repeat until nothing more can be purged -- removing one record may make others purgeable.

## Database.Audit -- Checking and Fixing Errors

```csharp
// fix: true = attempt repair, false = report only
// logToFile: true = create .adt audit log
db.Audit(true, false);
```

For side databases, always save to a new file after auditing to preserve the original.

## HostApplicationServices.WorkingDatabase

The `WorkingDatabase` property determines which database receives new objects when code does not explicitly specify a target. Critical when working with side databases -- symbol name resolution (e.g., layer "0") uses `WorkingDatabase`, not the transaction's database.

```csharp
Database previousDb = HostApplicationServices.WorkingDatabase;
try
{
    HostApplicationServices.WorkingDatabase = sideDb;

    using (Transaction tr = sideDb.TransactionManager.StartTransaction())
    {
        // Operations now resolve against sideDb
        tr.Commit();
    }
}
finally
{
    HostApplicationServices.WorkingDatabase = previousDb;
}
```

## Gotchas

- `WblockCloneObjects` requires the source transaction to be open during the call. If the transaction commits or aborts before cloning, the ObjectIds become invalid.
- `DeepCloneObjects` cannot cross database boundaries -- use `WblockCloneObjects` for inter-database copies.
- The `deferTranslation` parameter (last bool on clone methods) should almost always be `false`. Setting it to `true` defers ObjectId resolution and requires manual `TranslateIdsToOwnerSpace()`.
- `Wblock()` with no arguments creates a clean copy, stripping unused objects. Equivalent to WBLOCK `*` in the UI.
- `new Database(false, true)` creates an empty shell -- do NOT start transactions before calling `ReadDwgFile`.
- `new Database(true, true)` creates a valid default drawing. Use this when building a new .dwg from scratch.
- `Purge()` modifies the input collection in-place. Run in a loop because removing one record may make others purgeable.
- `Audit(true, false)` can modify the database silently. Save to a new file to preserve the original.
- Failing to restore `WorkingDatabase` after switching will cause the active document to malfunction. Always use try/finally.
- `ReadDwgFile` with `FileOpenMode.OpenForReadAndAllShare` is the safest mode for batch processing.
- `IdMapping` iteration includes both primary and dependency entries. Filter on `IdPair.IsPrimary` to process only requested objects.
- `WblockCloneObjects` automatically clones dependent objects (layers, linetypes, text styles). You do not need to clone symbol table records separately when copying entities.
- `DuplicateRecordCloning.Replace` overwrites the destination record entirely, which can change the appearance of existing entities that reference it.

## Related Skills

- `acad-xrefs` -- xref binding uses clone operations internally; `BindXrefs` is a specialized form of `WblockCloneObjects`
- `acad-blocks` -- block import across drawings uses `Insert` or `WblockCloneObjects` with block table as destination
- `acad-xdata-dictionaries` -- xdata and extension dictionary entries travel with cloned objects; dictionary cloning requires explicit handling
- `acad-layers` -- layer records are symbol table entries that follow `DuplicateRecordCloning` rules during cross-database cloning
