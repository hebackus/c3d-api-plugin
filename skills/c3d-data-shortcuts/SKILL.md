---
name: c3d-data-shortcuts
description: Data shortcut references, DataShortcutManager, CreateReference, SynchronizeImport, cross-drawing object references, broken reference repair, working and project folders
---

# Civil 3D Data Shortcuts and Cross-Drawing References

Use this skill when working with data shortcuts, creating or managing cross-drawing references, synchronizing imported references, repairing broken references, or configuring data shortcut working and project folders.

## Overview

Data shortcuts allow Civil 3D objects in one drawing (the source) to be referenced read-only into other drawings (the host). The .NET API exposes this through the `DataShortcuts` static class and the `DataShortcutManager` class in `Autodesk.Civil.DataShortcuts`. The assembly is `AeccDataShortcutMgd.dll`.

```
Working Folder
  └── Project Folder (_Shortcuts/ subfolder)
        ├── Alignments.xml
        ├── Surfaces.xml
        ├── Pipe Networks.xml
        ├── Pressure Pipe Networks.xml
        ├── Corridors.xml
        └── View Frame Groups.xml
```

## Supported Reference Types (RefType Enum)

The `DataShortcuts.RefType` enumeration defines the publishable entity types:

```csharp
using Autodesk.Civil.DataShortcuts;

// Available RefType values:
// RefType.Surface
// RefType.Alignment          (parent alignments)
// RefType.AlignmentChildren  (child offset/widening alignments)
// RefType.Profile
// RefType.PipeNetwork
// RefType.PressureNetwork
// RefType.Corridor
// RefType.ViewFrameGroup
```

## Managing Working and Project Folders

### Get and Set Working Folder

```csharp
using Autodesk.Civil.DataShortcuts;

// Get current working folder path
string workingFolder = DataShortcuts.GetWorkingFolderPath();
ed.WriteMessage("Working folder: {0}\n", workingFolder);

// Set a new working folder path
DataShortcuts.SetWorkingFolderPath(@"C:\Civil3D Projects");
```

### Get and Set Project Folder

```csharp
// Get current project folder (relative to working folder)
string projectFolder = DataShortcuts.GetProjectFolderPath();
ed.WriteMessage("Project folder: {0}\n", projectFolder);

// Set project folder (relative path from working folder)
DataShortcuts.SetProjectFolderPath("MyProject");

// Get the data shortcut project ID for a given path
int projectId = DataShortcuts.GetDSProjectId(@"C:\Civil3D Projects\MyProject");

// Associate a data shortcut project with the current drawing
DataShortcuts.AssociateDSProject(projectId);
```

### Listing Published Items

```csharp
// Get all published items in the current project
DataShortcutManager dsMgr = DataShortcuts.CreateDataShortcutManager(ref projectId);

int count = dsMgr.GetPublishedItemsCount();
for (int i = 0; i < count; i++)
{
    DSEntityInfo info = dsMgr.GetPublishedItemAt(i);
    ed.WriteMessage("Name: {0}, Type: {1}, Source: {2}\n",
        info.Name, info.RefType, info.SourceDrawing);
}

// Clean up (DataShortcutManager implements IDisposable)
dsMgr.Dispose();
```

## Creating Data References (Importing Shortcuts)

### Using DataShortcuts.CreateReference

```csharp
using Autodesk.Civil.DataShortcuts;
using Autodesk.Civil.ApplicationServices;

// Create a reference to a published surface in the current drawing
DataShortcuts.CreateReference(
    doc.Database,           // target database (host drawing)
    "EG Surface",           // entity name in the source drawing
    RefType.Surface         // entity type
);
```

### Using DataShortcutManager.CreateReference

```csharp
int projectId = 0;
DataShortcutManager dsMgr = DataShortcuts.CreateDataShortcutManager(ref projectId);

// Find the published item index by name and type
int itemIndex = -1;
int count = dsMgr.GetPublishedItemsCount();
for (int i = 0; i < count; i++)
{
    DSEntityInfo info = dsMgr.GetPublishedItemAt(i);
    if (info.Name == "Main Road CL" && info.RefType == RefType.Alignment)
    {
        itemIndex = i;
        break;
    }
}

if (itemIndex >= 0)
{
    // Create the reference in the current drawing
    dsMgr.CreateReference(itemIndex, doc.Database);
    ed.WriteMessage("Reference created for alignment 'Main Road CL'.\n");
}

dsMgr.Dispose();
```

### Batch Import Multiple References

```csharp
int projectId = 0;
DataShortcutManager dsMgr = DataShortcuts.CreateDataShortcutManager(ref projectId);

RefType[] typesToImport = {
    RefType.Surface,
    RefType.Alignment,
    RefType.PipeNetwork
};

int imported = 0;
int count = dsMgr.GetPublishedItemsCount();
for (int i = 0; i < count; i++)
{
    DSEntityInfo info = dsMgr.GetPublishedItemAt(i);
    if (Array.IndexOf(typesToImport, info.RefType) >= 0)
    {
        try
        {
            dsMgr.CreateReference(i, doc.Database);
            imported++;
            ed.WriteMessage("Imported: {0} ({1})\n", info.Name, info.RefType);
        }
        catch (System.Exception ex)
        {
            ed.WriteMessage("Failed to import {0}: {1}\n", info.Name, ex.Message);
        }
    }
}
ed.WriteMessage("Total imported: {0}\n", imported);

dsMgr.Dispose();
```

## Identifying Reference Objects

### Checking If an Entity Is a Reference

```csharp
using (Transaction ts = db.TransactionManager.StartTransaction())
{
    Alignment align = ts.GetObject(alignId, OpenMode.ForRead) as Alignment;

    // Check if this entity is a data reference (read-only cross-drawing ref)
    if (align.IsReferenceObject)
    {
        ed.WriteMessage("'{0}' is a data reference.\n", align.Name);

        // Get reference information
        DataShortcutKey dsKey = align.GetReferenceInfo();
        ed.WriteMessage("  Source drawing: {0}\n", dsKey.SourceDrawing);
        ed.WriteMessage("  Source entity:  {0}\n", dsKey.SourceEntityName);
        ed.WriteMessage("  Ref type:       {0}\n", dsKey.RefType);
    }

    // Check for sub-objects (e.g., profiles that came along with an alignment ref)
    if (align.IsReferenceSubObject)
    {
        ed.WriteMessage("'{0}' is a reference sub-object.\n", align.Name);
    }

    ts.Commit();
}
```

### Iterating All Reference Entities in a Drawing

```csharp
CivilDocument doc = CivilApplication.ActiveDocument;

using (Transaction ts = db.TransactionManager.StartTransaction())
{
    // Check surfaces
    foreach (ObjectId surfId in doc.GetSurfaceIds())
    {
        var surf = ts.GetObject(surfId, OpenMode.ForRead) as Autodesk.Civil.DatabaseServices.Surface;
        if (surf.IsReferenceObject)
            ed.WriteMessage("DREF Surface: {0}\n", surf.Name);
    }

    // Check alignments
    foreach (ObjectId alignId in doc.GetAlignmentIds())
    {
        var align = ts.GetObject(alignId, OpenMode.ForRead) as Alignment;
        if (align.IsReferenceObject)
            ed.WriteMessage("DREF Alignment: {0}\n", align.Name);
    }

    // Check pipe networks
    foreach (ObjectId netId in doc.GetPipeNetworkIds())
    {
        var network = ts.GetObject(netId, OpenMode.ForRead) as Network;
        if (network.IsReferenceObject)
            ed.WriteMessage("DREF Network: {0}\n", network.Name);
    }

    ts.Commit();
}
```

## Synchronizing References (SynchronizeImport)

When the source drawing changes, data references in host drawings must be synchronized. References auto-synchronize on drawing open, but can also be forced programmatically.

### Synchronize All References

```csharp
using Autodesk.Civil.DataShortcuts;

// Synchronize all data references in the active drawing
DataShortcuts.SynchronizeImport(doc.Database);

ed.WriteMessage("All data references synchronized.\n");
```

### Synchronize a Specific Reference

```csharp
using (Transaction ts = db.TransactionManager.StartTransaction())
{
    Alignment align = ts.GetObject(alignId, OpenMode.ForRead) as Alignment;

    if (align.IsReferenceObject)
    {
        // Synchronize this specific reference entity
        DataShortcuts.SynchronizeImport(db, alignId);
        ed.WriteMessage("Synchronized reference: {0}\n", align.Name);
    }

    ts.Commit();
}
```

## Repairing Broken References

References break when the source drawing is moved, renamed, or deleted. The API provides repair methods.

### Detect Broken References

```csharp
int projectId = 0;
DataShortcutManager dsMgr = DataShortcuts.CreateDataShortcutManager(ref projectId);

int brokenCount = dsMgr.GetBrokenDRefCount(doc.Database);
ed.WriteMessage("Broken references: {0}\n", brokenCount);

for (int i = 0; i < brokenCount; i++)
{
    ObjectId brokenId = dsMgr.GetBrokenDRefEntityId(doc.Database, i);
    Entity ent = ts.GetObject(brokenId, OpenMode.ForRead) as Entity;
    ed.WriteMessage("  Broken: {0} (ObjectId: {1})\n", ent.Name, brokenId);
}

dsMgr.Dispose();
```

### Repair a Broken Data Reference in the Drawing

```csharp
// Repair a broken DREF by pointing it to a new source drawing path
DataShortcuts.RepairBrokenDRef(
    brokenEntityId,                          // ObjectId of the broken reference entity
    @"C:\Projects\Source\Design.dwg",        // new target drawing full path
    true                                     // auto-repair other broken refs to the same source
);
```

### Repair a Broken Data Shortcut in the Project

```csharp
int projectId = 0;
DataShortcutManager dsMgr = DataShortcuts.CreateDataShortcutManager(ref projectId);

// Repair broken shortcut by index (in the project XML, not the drawing)
bool repaired = DataShortcuts.RepairBrokenDataShortcut(
    shortcutIndex,                           // index of the broken shortcut
    @"C:\Projects\Source\Design.dwg",        // new target drawing full path
    true                                     // auto-repair others pointing to same source
);

if (repaired)
    ed.WriteMessage("Data shortcut repaired.\n");
else
    ed.WriteMessage("Repair failed.\n");

dsMgr.Dispose();
```

### Batch Repair All Broken References

```csharp
int projectId = 0;
DataShortcutManager dsMgr = DataShortcuts.CreateDataShortcutManager(ref projectId);
int brokenCount = dsMgr.GetBrokenDRefCount(doc.Database);

if (brokenCount > 0)
{
    // Repair first broken ref with autoRepairOther = true to fix all from same source
    ObjectId firstBrokenId = dsMgr.GetBrokenDRefEntityId(doc.Database, 0);
    DataShortcuts.RepairBrokenDRef(firstBrokenId, newSourceDrawingPath, true);
    ed.WriteMessage("Attempted repair of {0} broken reference(s).\n", brokenCount);
}
dsMgr.Dispose();
```

## DataShortcutKey Properties

When you call `entity.GetReferenceInfo()` on a reference entity, the returned `DataShortcutKey` contains:

- SourceDrawing (string, get) — full path to the source drawing file
- SourceEntityName (string, get) — name of the entity in the source drawing
- RefType (RefType, get) — type of referenced entity (Surface, Alignment, etc.)

## DataShortcuts Static Methods

- GetWorkingFolderPath() -> string — returns current working folder path
- SetWorkingFolderPath(string path) — sets the working folder path
- GetProjectFolderPath() -> string — returns current project folder (relative to working folder)
- SetProjectFolderPath(string path) — sets the project folder path
- GetDSProjectId(string projectPath) -> int — gets project ID from a full project path
- AssociateDSProject(int projectId) — associates a project with the current drawing
- CreateDataShortcutManager(ref int projectId) -> DataShortcutManager — creates a manager for the project
- CreateReference(Database db, string entityName, RefType type) — creates a DREF in the target database
- SynchronizeImport(Database db) — synchronizes all DREFs in the database
- SynchronizeImport(Database db, ObjectId entityId) — synchronizes a specific DREF
- RepairBrokenDRef(ObjectId brokenId, string targetDwgPath, bool autoRepairOther) — repairs a broken DREF entity
- RepairBrokenDataShortcut(int index, string targetDwgPath, bool autoRepairOther) -> bool — repairs a broken shortcut in the project

## DataShortcutManager Instance Methods

- GetPublishedItemsCount() -> int — number of published items in the project
- GetPublishedItemAt(int index) -> DSEntityInfo — info about a published item
- CreateReference(int itemIndex, Database db) — creates a DREF from a published item
- GetBrokenDRefCount(Database db) -> int — number of broken DREFs in a drawing
- GetBrokenDRefEntityId(Database db, int index) -> ObjectId — ObjectId of a broken DREF entity
- Dispose() — releases unmanaged resources (always call when done)

## Entity Reference Properties

- IsReferenceObject (bool, get) — true if the entity is a data reference from another drawing
- IsReferenceSubObject (bool, get) — true if the entity came as a child of a referenced parent
- GetReferenceInfo() -> DataShortcutKey — returns source drawing and entity info for a reference

## Gotchas

- Data reference entities are **read-only** in the host drawing; opening ForWrite on referenced properties throws an exception
- `DataShortcutManager` holds unmanaged resources; always call `Dispose()` or use a `using` block
- `SynchronizeImport` requires the source drawing to be accessible at the stored path; if moved, repair first
- `SetWorkingFolderPath` and `SetProjectFolderPath` do not validate the path; invalid paths cause failures on next shortcut operation
- `RepairBrokenDRef` with `autoRepairOther = true` only repairs entities referencing the **same source drawing**; entities from other sources need separate repair calls
- Reference sub-objects (e.g., profiles imported with an alignment) cannot be individually removed; removing the parent reference removes all children
- Creating a reference to an entity that already exists as a DREF in the drawing throws an exception; check `IsReferenceObject` first
- The `_Shortcuts` subfolder is created automatically by Civil 3D in the project folder; do not manually create or modify its XML files
- The `AECCFORCESYNCHRONIZEREFERENCES` built-in command can synchronize all references interactively, but the API method `SynchronizeImport` is the programmatic equivalent
- Pressure network references require Civil 3D 2020+ API; earlier versions only support gravity `PipeNetwork`

## Related Skills

- `c3d-root-objects` — CivilDocument, transactions, and collection access patterns used with reference entities
- `c3d-alignments` — Alignment creation and queries; alignment DREFs are the most common reference type
- `c3d-surfaces` — Surface objects that can be published and referenced across drawings
- `c3d-profiles` — Profiles that accompany alignment references as sub-objects
- `c3d-pipe-networks` — Gravity and pressure pipe networks publishable via data shortcuts
