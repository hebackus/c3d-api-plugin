---
name: acad-sheet-sets
description: Use when reading or writing AutoCAD Sheet Set (.dst) files from a .NET plugin — accessing sheets, subsets, custom properties, lock management, and the AcSmSheetSetMgr COM API
---

# AutoCAD Sheet Set Manager (.NET)

**Sheet Set Manager has no managed .NET API — it is COM-only.**

Access it via `dynamic` COM using CLSIDs. Do NOT reference `AcSmComponents.Interop.dll` in .NET 8 plugins — it causes `ReflectionTypeLoadException` during `NETLOAD`. Use the dynamic pattern shown below.

## Key CLSIDs

```csharp
internal static class AcSmGuids
{
    // IAcSmSheetSetMgr — the root manager object
    public const string SheetSetMgr = "bcfa0ab8-cefc-43e9-841b-8141f44fe240";

    // IAcSmCustomPropertyValue — create new custom property values
    public const string CustomPropertyValue = "909a5a17-c368-40cb-8b92-d174395128df";
}
```

## Opening a Sheet Set Database

```csharp
using System;
using System.Runtime.InteropServices;

// Create the manager
var mgrType = Type.GetTypeFromCLSID(new Guid(AcSmGuids.SheetSetMgr), true);
dynamic mgr = Activator.CreateInstance(mgrType);

object db = null;
bool weOpened = false;
try
{
    // Reuse already-open database if available
    try { db = mgr.FindOpenDatabase(dstPath); } catch { }
    if (db == null)
    {
        db = mgr.OpenDatabase(dstPath, false); // false = read/write
        weOpened = true;
    }

    // ... use db ...
}
finally
{
    if (weOpened && db != null)
        mgr.Close(db);              // close only if we opened it

    if (db != null) Marshal.ReleaseComObject(db);
    Marshal.ReleaseComObject(mgr);
}
```

**CRITICAL:** Always call `Marshal.ReleaseComObject()` on every COM object when done. Failure to release causes the `.dst` file to stay locked after Civil 3D exits.

## Lock Management

The database must be locked before writing. Lock status codes:

```csharp
internal static class AcSmLockStatus
{
    public const int UnLocked        = 0;
    public const int Locked_Local    = 1;  // locked by current process
    public const int Locked_Remote   = 2;  // locked by another user
    public const int Locked_ReadOnly = 4;
    public const int Locked_AccessDenied = 8;
    public const int Locked_NotConnected = 16;
}
```

```csharp
dynamic db = database;

int status = (int)db.GetLockStatus();
if (status == AcSmLockStatus.UnLocked)
    db.LockDb(db);  // pass the db object as argument

// Unlock with commit=true to save, commit=false to discard
db.UnlockDb(db, commit: true);

// Query lock owner (returns empty strings if not locked)
string userName = "", machineName = "";
db.GetLockOwnerInfo(out userName, out machineName);
```

**Stale lock recovery** — if the same user/machine holds the lock (e.g., after a crash), force-release then re-acquire:

```csharp
if (userName.Equals(Environment.UserName, StringComparison.OrdinalIgnoreCase)
    && machineName.Equals(Environment.MachineName, StringComparison.OrdinalIgnoreCase))
{
    db.UnlockDb(db, false);
    db.LockDb(db);
}
```

## Reading Sheets and Subsets

The sheet set contains a tree of components — each is either a **sheet** or a **subset** (folder). Distinguish them by whether `GetSheetEnumerator()` succeeds.

```csharp
dynamic sheetSet = db.GetSheetSet();
try
{
    string name = (string)sheetSet.GetName();

    dynamic rootEnum = sheetSet.GetSheetEnumerator();
    try
    {
        rootEnum.Reset();
        dynamic comp;
        while ((comp = rootEnum.Next()) != null)
        {
            try
            {
                // Try as subset (has GetSheetEnumerator)
                try
                {
                    dynamic subsetEnum = comp.GetSheetEnumerator();
                    string subsetName = (string)comp.GetName();
                    // recurse into subsetEnum...
                    Marshal.ReleaseComObject(subsetEnum);
                    continue;
                }
                catch { /* not a subset */ }

                // It's a sheet
                string number = (string)(comp.GetNumber() ?? "");
                string title  = (string)(comp.GetTitle()  ?? "");
            }
            finally { Marshal.ReleaseComObject(comp); }
        }
    }
    finally { Marshal.ReleaseComObject(rootEnum); }
}
finally { Marshal.ReleaseComObject(sheetSet); }
```

## Reading Custom Properties

```csharp
// From a sheet component (already have dynamic comp)
dynamic bag = comp.GetCustomPropertyBag();  // may return null
if (bag == null) return;

try
{
    dynamic enumerator = bag.GetPropertyEnumerator();
    try
    {
        enumerator.Reset();
        while (true)
        {
            string propName = null;
            dynamic propValue = null;
            try { enumerator.Next(out propName, out propValue); }
            catch { break; }
            if (propName == null) break;

            try
            {
                int flags = (int)propValue.GetFlags();
                // Filter to custom sheet properties
                if ((flags & AcSmPropertyFlags.CUSTOM_SHEET_PROP) != 0 ||
                    (flags & AcSmPropertyFlags.IS_CHILD) != 0)
                {
                    string value = propValue.GetValue()?.ToString() ?? "";
                }
            }
            finally { if (propValue != null) Marshal.ReleaseComObject(propValue); }
        }
    }
    finally { Marshal.ReleaseComObject(enumerator); }
}
finally { Marshal.ReleaseComObject(bag); }
```

### Property Flags

```csharp
internal static class AcSmPropertyFlags
{
    public const int CUSTOM_SHEET_PROP = 1;  // user-defined per-sheet property
    public const int IS_CHILD          = 2;  // inherited from sheet set level
}
```

## Writing Custom Properties

Requires an active lock on the database.

```csharp
dynamic bag = sheet.GetCustomPropertyBag();
try
{
    dynamic propValue = null;
    try
    {
        // Try to get existing property
        try { propValue = bag.GetProperty(propertyName); }
        catch { /* doesn't exist yet */ }

        if (propValue == null)
        {
            // Create new property value object
            var pvType = Type.GetTypeFromCLSID(new Guid(AcSmGuids.CustomPropertyValue), true);
            propValue = Activator.CreateInstance(pvType);
            propValue.InitNew(bag);
            propValue.SetFlags(AcSmPropertyFlags.CUSTOM_SHEET_PROP);
        }

        propValue.SetValue(newValue);
        bag.SetProperty(propertyName, propValue);
    }
    finally { if (propValue != null) Marshal.ReleaseComObject(propValue); }
}
finally { Marshal.ReleaseComObject(bag); }
```

## Writing Sheet Number and Title

```csharp
// Requires lock on db
sheet.SetNumber("C1.01");
sheet.SetTitle("Site Plan");
```

## Commit or Discard Changes

```csharp
// Commit (save to .dst file)
db.UnlockDb(db, true);

// Discard (no changes written)
db.UnlockDb(db, false);
```

Always call `UnlockDb` in a `finally` block to avoid leaving the file locked.

## Project Setup

No extra DLL references needed beyond the standard three:

```xml
<Reference Include="acdbmgd">
  <HintPath>$(ArxMgdPath)\acdbmgd.dll</HintPath>
  <Private>False</Private>
</Reference>
<Reference Include="acmgd">
  <HintPath>$(ArxMgdPath)\acmgd.dll</HintPath>
  <Private>False</Private>
</Reference>
<Reference Include="accoremgd">
  <HintPath>$(ArxMgdPath)\accoremgd.dll</HintPath>
  <Private>False</Private>
</Reference>
```

Do **not** add `AcSmComponents.dll` or `AcSmComponents.Interop.dll` as references — they cause `ReflectionTypeLoadException` at `NETLOAD` time in .NET 8 plugins.

## Gotchas

- **Every COM object must be released.** Use `try/finally` with `Marshal.ReleaseComObject()`. Missing a release keeps the `.dst` locked until AutoCAD exits.
- **Enumerator.Next() signals end by throwing**, not by returning null — catch the exception to exit the loop (or check if the returned name is null).
- **Components have no type discriminator** — tell sheets from subsets by calling `GetSheetEnumerator()` and catching the exception if it fails.
- **`GetCustomPropertyBag()` can return null** — check before using. Sheets with no custom properties may return null.
- **Lock before write, unlock with commit.** If you open the database without acquiring a lock first, writes will silently fail.
- **`FindOpenDatabase` throws if the database is not open** — always wrap in try/catch and fall back to `OpenDatabase`.
- **Only close databases you opened.** If `FindOpenDatabase` returned an existing handle, do not call `mgr.Close(db)` — that would close a database another part of the application is using.
- **AcSmComponents.Interop.dll is .NET Framework only.** Do not reference it in .NET 8 plugins. Use `dynamic` COM via CLSID instead (the pattern shown above).

## Related Skills

- `/c3d-api:c3d-project-setup` - DLL references, acad_path.props, plugin setup
- `/c3d-api:autocad-class-reference` - AutoCAD .NET class overview
