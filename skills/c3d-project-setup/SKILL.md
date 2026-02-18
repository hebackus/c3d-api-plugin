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

The `acad_path.props` file defines three path variables for the three subdirectory locations where Civil 3D DLLs reside:

| Variable | Resolved Path | DLLs |
|----------|--------------|------|
| `$(ArxMgdPath)` | `C:\Program Files\Autodesk\AutoCAD 2026` | `acdbmgd.dll`, `acmgd.dll`, `accoremgd.dll` |
| `$(OMFMgdPath)` | `C:\Program Files\Autodesk\AutoCAD 2026\ACA` | `AecBaseMgd.dll` |
| `$(AeccMgdPath)` | `C:\Program Files\Autodesk\AutoCAD 2026\C3D` | `AeccDbMgd.dll` |

| DLL | Variable | Purpose |
|-----|----------|---------|
| `acdbmgd.dll` | `$(ArxMgdPath)` | AutoCAD database managed wrapper |
| `acmgd.dll` | `$(ArxMgdPath)` | AutoCAD application managed wrapper |
| `accoremgd.dll` | `$(ArxMgdPath)` | AutoCAD core managed wrapper |
| `AecBaseMgd.dll` | `$(OMFMgdPath)` | AEC base classes |
| `AeccDbMgd.dll` | `$(AeccMgdPath)` | Civil 3D database classes |
| `AeccPressurePipesMgd.dll` | `$(AeccMgdPath)` | Civil 3D pressure pipe network classes |

**CRITICAL:** Set `Copy Local` (Private) to **False** for all Autodesk DLLs. These are resolved at runtime by the Civil 3D host process. Setting them to True causes version conflicts and bloated output.

In .csproj (full reference block pattern):
```xml
<Reference Include="acdbmgd">
  <SpecificVersion>False</SpecificVersion>
  <HintPath>$(ArxMgdPath)\acdbmgd.dll</HintPath>
  <Private>False</Private>
</Reference>
<Reference Include="acmgd">
  <SpecificVersion>False</SpecificVersion>
  <HintPath>$(ArxMgdPath)\acmgd.dll</HintPath>
  <Private>False</Private>
</Reference>
<Reference Include="accoremgd">
  <SpecificVersion>False</SpecificVersion>
  <HintPath>$(ArxMgdPath)\accoremgd.dll</HintPath>
  <Private>False</Private>
</Reference>
<Reference Include="AecBaseMgd">
  <SpecificVersion>False</SpecificVersion>
  <HintPath>$(OMFMgdPath)\AecBaseMgd.dll</HintPath>
  <Private>False</Private>
</Reference>
<Reference Include="AeccDbMgd">
  <SpecificVersion>False</SpecificVersion>
  <HintPath>$(AeccMgdPath)\AeccDbMgd.dll</HintPath>
  <Private>False</Private>
</Reference>
<Reference Include="AeccPressurePipesMgd">
  <HintPath>$(AeccMgdPath)\AeccPressurePipesMgd.dll</HintPath>
  <Private>False</Private>
</Reference>
```

## Project File Pattern (from this codebase)

The `acad_path.props` file defines the Civil 3D installation paths:
```xml
<Civil3DPath>C:\Program Files\Autodesk\AutoCAD 2026</Civil3DPath>
<ArxMgdPath>$(Civil3DPath)</ArxMgdPath>
<OMFMgdPath>$(Civil3DPath)\ACA</OMFMgdPath>
<AeccMgdPath>$(Civil3DPath)\C3D</AeccMgdPath>
```

Import it in your .csproj (path is relative to your project; projects in `CSharp/<PluginName>/` use two levels up):
```xml
<Import Project="..\..\acad_path.props" />
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

In project Properties > Debug (or `launchSettings.json`):
1. **Start external program:** `C:\Program Files\Autodesk\AutoCAD 2026\acad.exe`
2. **Command line arguments:** `/ld "C:\Program Files\Autodesk\AutoCAD 2026\AecBase.dbx" /p "<<C3D_Imperial>>" /nologo`
3. **Working directory:** `C:\Program Files\Autodesk\AutoCAD 2026\UserDataCache`

Note: Both `acad.exe` and `AecBase.dbx` live under the same AutoCAD install path (`C:\Program Files\Autodesk\AutoCAD 2026`).

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
