---
name: c3d-project-setup
description: Set up a .NET project for AutoCAD Civil 3D 2026 plugin development - references, namespaces, project config, and debugging
---

# Civil 3D .NET Project Setup

Use this skill when creating a new Civil 3D plugin project or troubleshooting build/reference issues.

## Project Type

- **Class Library** targeting **.NET 8.0** (or .NET Framework 4.8 for older C3D versions)
- **Platform:** x64 only
- **Output:** DLL loaded via `NETLOAD` command in Civil 3D

## Required DLL References

Browse to the Civil 3D install directory and add these base libraries:

| DLL | Purpose |
|-----|---------|
| `acdbmgd.dll` | AutoCAD database managed wrapper |
| `acmgd.dll` | AutoCAD application managed wrapper |
| `accoremgd.dll` | AutoCAD core managed wrapper |
| `AecBaseMgd.dll` | AEC base classes |
| `AeccDbMgd.dll` | Civil 3D database classes |

**CRITICAL:** Set `Copy Local` (Private) to **False** for all Autodesk DLLs. These are resolved at runtime by the Civil 3D host process. Setting them to True causes version conflicts and bloated output.

In .csproj:
```xml
<Reference Include="acdbmgd">
  <HintPath>$(Civil3DPath)\acdbmgd.dll</HintPath>
  <Private>False</Private>
</Reference>
```

## Project File Pattern (from this codebase)

The `acad_path.props` file defines the Civil 3D installation path:
```xml
<Civil3DPath>C:\Program Files\Autodesk\AutoCAD 2026</Civil3DPath>
```

Import it in your .csproj:
```xml
<Import Project="..\acad_path.props" />
```

## Required Namespaces

```csharp
// AutoCAD base
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.EditorInput;

// Civil 3D
using Autodesk.Civil.ApplicationServices;
using Autodesk.Civil.DatabaseServices;
using Autodesk.Civil.Settings;
```

## Entry Point Pattern

Implement `IExtensionApplication` for initialization:

```csharp
using Autodesk.AutoCAD.Runtime;

namespace MyPlugin
{
    public class MyPlugin : IExtensionApplication
    {
        public void Initialize()
        {
            // Called when assembly is loaded via NETLOAD
        }

        public void Terminate()
        {
            // Called when Civil 3D shuts down
        }

        [CommandMethod("MYCOMMAND")]
        public void MyCommand()
        {
            CivilDocument doc = CivilApplication.ActiveDocument;
            Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
            // ...
        }
    }
}
```

## Debugging Setup

In project Properties > Debug:
1. **Start external program:** `C:\Program Files\Autodesk\AutoCAD 2026\acad.exe`
2. **Command line arguments:** `/ld "C:\Program Files\Autodesk\AutoCAD 2026\AecBase.dbx" /p "<<C3D_Imperial>>"`
3. **Working directory:** `C:\Program Files\Autodesk\AutoCAD 2026\UserDataCache\`

## COM Interop (When .NET API is Incomplete)

Most Civil 3D features are exposed in the .NET API, including sites, parcels, sections, section views, data bands, and labels. COM interop may still be needed for certain advanced or niche features not covered by the managed wrappers. Use COM interop:

```csharp
// Add COM interop DLL references:
// Autodesk.AEC.Interop.Base
// Autodesk.AEC.Interop.UiBase
// Autodesk.AECC.Interop.<domain>   (Land, Roadway, Pipe, Survey)
// Autodesk.AECC.Interop.UiLand
```

## Gotchas

- Express editions of Visual Studio cannot debug with external programs
- There is no NETUNLOAD command - .NET assemblies stay loaded until Civil 3D shuts down
- The `CommandMethod` attribute defines the AutoCAD command name (case-insensitive)
- Always use `[CommandMethod("COMMANDNAME")]` on **public void** methods

## Related Skills

- `c3d-root-objects` - CivilApplication, transactions, settings
- `c3d-label-styles` - Label style creation and components
