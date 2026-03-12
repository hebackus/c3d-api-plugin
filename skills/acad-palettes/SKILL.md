---
name: acad-palettes
description: PaletteSet deep API reference (constructors, AddVisual WPF hosting, events, persistence, theming), Tool Palette API (catalogs, schemes, ToolPaletteManager), Properties Palette COM interfaces, lifecycle and zero-document state, decision matrix for choosing palette type
---

# AutoCAD Palette APIs

Use this skill when creating custom dockable palettes, choosing between PaletteSet/Tool Palettes/Properties Palette, or handling palette lifecycle with zero-document state.

## PaletteSet and Palette

`Autodesk.AutoCAD.Windows.PaletteSet` is the managed wrapper over `AduiPaletteSet`. It inherits from `Autodesk.AutoCAD.Windows.Window`, implements `ICollection`, and hosts one or more child `Palette` tabs.

`Autodesk.AutoCAD.Windows.Palette` is a sealed class wrapping `CAdUiPalette`. Access its parent via `Palette.PaletteSet`.

### Constructors

Official constructors:

- `PaletteSet(string name)` -- creates an unnamed palette set (no persistence)
- `PaletteSet(string name, Guid toolID)` -- GUID enables automatic state persistence across sessions

Community-reported constructor (not officially documented):

- `PaletteSet(string name, string cmd, Guid toolID)` -- `cmd` is the command name AutoCAD replays when restoring an open palette on startup. See Gotchas for safety requirements.

### Hosting Methods

- `Palette Add(string name, Control control)` -- host a WinForms `UserControl`
- `Palette Add(string name, Uri htmlPage)` -- host HTML-backed content
- `Palette AddVisual(string name, Visual control)` -- host a WPF visual directly (no ElementHost needed)
- `Palette AddVisual(string name, Visual control, bool bResizeContentToPaletteSize)` -- WPF visual with explicit resize control. When `true`, the WPF content resizes with the palette. When `false`, the content retains its natural size.

`AddVisual` is the preferred approach for WPF content in modern plugins. It avoids the WinForms UserControl + ElementHost wrapper that `Add(string, Control)` requires.

### High-Value Members

| Member | Type | Purpose |
| --- | --- | --- |
| `Name` | `string` | Window caption / palette-set name |
| `Visible` | `bool` | Show or hide the palette set |
| `KeepFocus` | `bool` | Whether the palette retains input focus when AutoCAD requests it back |
| `Dock` | `DockSides` (read-only) | Current docking side |
| `DockEnabled` | `DockSides` | Which docking sides the user may use |
| `Style` | `PaletteSetStyles` | Style flags (close button, auto-hide, etc.) |
| `Location` | `System.Drawing.Point` | Floating palette position |
| `Size` | `System.Drawing.Size` | Current palette size |
| `MinimumSize` | `System.Drawing.Size` | Minimum allowed size |
| `AutoRollUp` | `bool` | Enable/disable auto-roll-up behavior |
| `TitleBarLocation` | `PaletteSetTitleBarLocation` | Title-bar placement |
| `SetThemedIcon(Icon, ColorThemeEnum)` | method | Theme-aware icon assignment |

DPI-oriented members: `DeviceIndependentLocation`, `DeviceIndependentSize`, `DeviceIndependentMinimumSize`.

Caption-icon properties: `LightThemedIcon`, `DarkThemedIcon`, `LargeLightThemedIcon`, `LargeDarkThemedIcon`.

### Events and Persistence Hooks

- `Focused` -- palette received focus
- `PaletteActivated` -- a palette tab was activated
- `Load` -- palette-set data loaded from XML (persistence restore)
- `Save` -- palette-set data saved to XML (persistence store)
- `SizeChanged` -- palette resized
- `StateChanged` -- show/hide/roll-up state changed
- `PaletteSetHostMoved` -- host window moved

Key event-argument members:

- `PalettePersistEventArgs.ConfigurationSection` -- the XML configuration section during `Load`/`Save`
- `PaletteSetStateEventArgs.NewState` -- identifies which state changed during `StateChanged`

### Theming

Theme-based icon APIs supersede older icon methods. Use `SetThemedIcon(...)` or the themed icon properties (`LightThemedIcon`, `DarkThemedIcon`) for light/dark theme fidelity.

### Example: WinForms Palette Singleton

```csharp
using System;
using System.Drawing;
using System.Windows.Forms;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.Windows;

public sealed class SamplePaletteCommands
{
    private static readonly Guid PaletteId =
        new Guid("E4E1D31A-8B4A-4F47-B10A-3B9E3D5C9E90");

    private static PaletteSet _paletteSet;

    [CommandMethod("SHOW_SAMPLE_PALETTE")]
    public static void ShowSamplePalette()
    {
        if (_paletteSet == null)
        {
            _paletteSet = new PaletteSet("Sample Palette", PaletteId)
            {
                MinimumSize = new Size(320, 220),
                KeepFocus = false
            };

            _paletteSet.Add("General", new SamplePaletteControl());
        }

        _paletteSet.Visible = true;
    }
}

public sealed class SamplePaletteControl : UserControl
{
    public SamplePaletteControl()
    {
        Dock = DockStyle.Fill;
        Controls.Add(new Label
        {
            Dock = DockStyle.Fill,
            Text = "Palette content goes here.",
            TextAlign = ContentAlignment.MiddleCenter
        });
    }
}
```

### Example: WPF Palette via AddVisual

```csharp
using System;
using System.Drawing;
using System.Windows.Controls;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.Windows;

public sealed class WpfPaletteCommands
{
    private static readonly Guid PaletteId =
        new Guid("6AB6F5C2-DBCB-48AC-8A55-4620D2D8CBE7");

    private static PaletteSet _paletteSet;

    [CommandMethod("SHOW_WPF_PALETTE")]
    public static void ShowWpfPalette()
    {
        if (_paletteSet == null)
        {
            _paletteSet = new PaletteSet("WPF Palette", PaletteId)
            {
                MinimumSize = new Size(360, 240)
            };

            var view = new UserControl
            {
                Content = new TextBlock
                {
                    Text = "WPF content hosted by PaletteSet.AddVisual",
                    Margin = new System.Windows.Thickness(16)
                }
            };

            _paletteSet.AddVisual("Preview", view, true);
        }

        _paletteSet.Visible = true;
    }
}
```

## Lifecycle and Startup

### Application Initialization

Implement `IExtensionApplication` for initialization and termination. Use assembly-level `ExtensionApplication` and `CommandClass` attributes as load-time optimization hints.

### Command Context

- Without `CommandFlags.Session` -- command runs in document context (tied to current drawing)
- With `CommandFlags.Session` -- command runs in application context (survives MDI document switches)

Palette commands often need `CommandFlags.Session` because they must survive document switches, remain safe with no drawing active, and interact with UI state broader than a single drawing.

### Application and DocumentCollection Events

Events relevant to palette hosts:

- `Application` events -- `BeginQuit`, `QuitWillStart`, `Idle`, `EnterModal`, `LeaveModal`. Handlers stay active until AutoCAD shuts down or you unregister them.
- `DocumentCollection` events -- `DocumentActivated`, `DocumentCreated`, `DocumentDestroyed`, `DocumentToBeDestroyed`, `DocumentBecameCurrent`. Use these instead of trying to infer lifecycle from command strings like `OPEN`, `NEW`, `CLOSE`, `QUIT`.

### Zero-Document State

When no documents are open, AutoCAD exposes only a reduced application surface. Key facts:

- `DocumentDestroyed` is the recommended event for detecting entry into zero-document state
- At the time of the last document closing, `DocumentManager.Count` is still `1` during the `DocumentDestroyed` callback
- `MdiActiveDocument` may be `null` -- guard all document-dependent code paths

### Autoloader

`PackageContents.xml` flags `LoadOnCommandInvocation` and `LoadOnAutoCADStartup` control when your module loads. For command-driven palettes, prefer `LoadOnCommandInvocation` for startup-performance reasons.

### Recommended Pattern

1. Implement `IExtensionApplication`
2. Register application and document-collection events once in `Initialize()`
3. Unregister them in `Terminate()`
4. Keep the `PaletteSet` as a singleton
5. Create the palette lazily on the first command invocation
6. Use `CommandFlags.Session` when the command must be safe in application context
7. Guard every document-dependent code path for zero-document state

### Example: Lifecycle Wiring

```csharp
using System;
using System.Drawing;
using System.Windows.Forms;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.Windows;
using AcApp = Autodesk.AutoCAD.ApplicationServices.Core.Application;

[assembly: ExtensionApplication(typeof(PaletteLifecycleModule))]
[assembly: CommandClass(typeof(PaletteLifecycleModule))]

public sealed class PaletteLifecycleModule : IExtensionApplication
{
    private static readonly Guid PaletteId =
        new Guid("BB4DEB65-6F0A-4104-B8E9-A69A0B621B3E");

    private static PaletteSet _paletteSet;

    public void Initialize()
    {
        AcApp.QuitWillStart += OnQuitWillStart;
        AcApp.DocumentManager.DocumentActivated += OnDocumentActivated;
        AcApp.DocumentManager.DocumentDestroyed += OnDocumentDestroyed;
    }

    public void Terminate()
    {
        AcApp.QuitWillStart -= OnQuitWillStart;
        AcApp.DocumentManager.DocumentActivated -= OnDocumentActivated;
        AcApp.DocumentManager.DocumentDestroyed -= OnDocumentDestroyed;
    }

    [CommandMethod("SHOW_LIFECYCLE_PALETTE", CommandFlags.Session)]
    public static void ShowPalette()
    {
        EnsurePalette();
        _paletteSet.Visible = true;
    }

    private static void EnsurePalette()
    {
        if (_paletteSet != null) return;

        _paletteSet = new PaletteSet("Lifecycle Palette", PaletteId)
        {
            MinimumSize = new Size(300, 200)
        };

        _paletteSet.Add("Main", new UserControl { Dock = DockStyle.Fill });

        _paletteSet.Load += (sender, e) =>
        {
            // e.ConfigurationSection gives access to XML-backed persistence data
        };

        _paletteSet.StateChanged += (sender, e) =>
        {
            var activeDoc = AcApp.DocumentManager.MdiActiveDocument;
            if (activeDoc != null)
            {
                activeDoc.Editor.WriteMessage(
                    $"\nPalette state changed: {e.NewState}");
            }
        };
    }

    private static void OnDocumentActivated(object sender,
        DocumentCollectionEventArgs e)
    {
        // Refresh document-bound palette content here
    }

    private static void OnDocumentDestroyed(object sender,
        DocumentDestroyedEventArgs e)
    {
        bool enteringZeroDocState = AcApp.DocumentManager.Count == 1;
        if (enteringZeroDocState)
        {
            // Avoid document-dependent palette work until a new drawing exists
        }
    }

    private static void OnQuitWillStart(object sender, EventArgs e)
    {
        // Unhook external resources or stop background work
    }
}
```

## Tool Palette API

The Tool Palette API lives in the `Autodesk.AutoCAD.Windows.ToolPalette` namespace (`AcMgd.dll`, `AcTcMgd.dll`). It is the managed wrapper layer over `AcTc*` ObjectARX classes -- **not** the same as `PaletteSet`.

### Key Types

- `ToolPaletteManager` -- main entry point
- `Catalog`, `CatalogItem`, `CatalogItemCollection` -- catalog model
- `Palette` -- a tool palette within the Tool Palettes window (distinct from `Autodesk.AutoCAD.Windows.Palette`)
- `Tool`, `StockTool` -- individual tool definitions
- `Scheme`, `SchemeCollection` -- palette schemes

### ToolPaletteManager Members

- `ToolPaletteManager.Manager` -- static property returning the active manager
- `CatalogPath` -- absolute paths to workspace-catalog storage (semicolon-separated)
- `StockToolCatalogs` -- access to loaded stock-tool catalogs
- `Schemes` -- access to tool-palette schemes
- `LoadCatalogs(CatalogTypeFlags, LoadFlags)` -- loads workspace and stock-tool catalogs (discards currently loaded)
- `SaveCatalogs(CatalogTypeFlags, SaveFlags)` -- saves workspace and stock-tool catalogs
- `UnloadCatalogs(CatalogTypeFlags)` -- unloads workspace and stock-tool catalogs
- `GetShapePackage(string)` -- looks up a shape package in the shape catalog

### Runtime Model

Tool palettes are catalog-backed. Your application creates catalog, palette, and tool content once; AutoCAD saves it to ATC files with a path to your module. The Tool Palette framework loads your application when the Tool Palettes window initializes. This is fundamentally different from `PaletteSet`:

- `PaletteSet` -- direct custom UI host you fully control
- Tool Palette API -- persistent catalog-and-tool framework managed by AutoCAD

### When to Use

Use the Tool Palette API when extending the Tool Palettes window with catalog-backed tools, stock-tool behavior, or tool groups. Use `PaletteSet` for custom dockable UI with buttons, lists, grids, previews, and plugin-specific workflows.

For deeper Tool Palette behavior, Autodesk extension points become COM/ObjectARX oriented. The managed namespace exposes wrappers and interfaces (`IAcadTool`, `IAcadToolContextMenu`, `IAcadToolDragSource`, `IAcadToolDropTarget`), but the programming model is closer to framework customization than general-purpose dockable UI.

### Example: ToolPaletteManager Command

```csharp
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.Windows.ToolPalette;
using AcApp = Autodesk.AutoCAD.ApplicationServices.Core.Application;

public sealed class ToolPaletteCommands
{
    [CommandMethod("TOOLPALETTE_INFO", CommandFlags.Session)]
    public static void ToolPaletteInfo()
    {
        ToolPaletteManager manager = ToolPaletteManager.Manager;

        var editor = AcApp.DocumentManager.MdiActiveDocument?.Editor;
        if (editor == null) return;

        editor.WriteMessage($"\nCatalog path(s): {manager.CatalogPath}");

        manager.LoadCatalogs(
            CatalogTypeFlags.Catalog | CatalogTypeFlags.StockToolCatalog,
            LoadFlags.LoadLinks | LoadFlags.LoadImages);

        editor.WriteMessage("\nTool palette catalogs loaded.");
    }
}
```

## Properties Palette API

The Properties Palette (Property Inspector) is a COM-based module for inspecting and editing object properties. It is used by the Properties palette, Tool Palettes, Visualization Styles, and other UI hosts.

### Capabilities

- Display custom properties for custom objects
- Customize property categorization and editing
- Customize the Properties palette UI
- Display properties for a custom command
- Add custom tabs to the Properties palette

### Key Interfaces (ObjectARX/COM)

- `IOPMPropertyExtension` -- custom property exposure
- `IOPMPropertyDialog` -- custom property dialog
- `IPerPropertyBrowsing` -- per-property browsing customization
- `IAcPiCategorizeProperties` -- property categorization
- `IAcPiPropertyDisplay` -- property display customization

### When to Use

Use the Properties Palette API when your custom entities, custom objects, or commands need to participate in the built-in Properties palette. Use `PaletteSet` when you need a dockable window for your own commands and workflow.

## Decision Matrix

| Need | Best Fit | Why |
| --- | --- | --- |
| Dockable plugin UI with tabs, forms, WPF views, previews, command buttons | `PaletteSet` | Official managed host for custom palette windows |
| Host WinForms controls in a palette | `PaletteSet.Add(string, Control)` | Direct WinForms support |
| Host WPF content in a palette | `PaletteSet.AddVisual(...)` | Direct WPF visual hosting (no ElementHost) |
| Host HTML content in a palette | `PaletteSet.Add(string, Uri)` | Official HTML-backed overload |
| Tool catalogs, stock tools, tool groups | Tool Palette API | Framework behind the Tool Palettes feature and ATC-backed catalog model |
| Custom entity/command properties in Properties palette | Properties Palette / Property Inspector APIs | Designed specifically for property inspection and editing |
| Civil 3D-specific custom business UI | Usually `PaletteSet` | Civil 3D does not have a separate managed custom-palette framework; the host API is AutoCAD |

## Gotchas

- **Stable GUID controls state restoration** -- giving a `PaletteSet` a stable `Guid` is what lets AutoCAD restore persisted window state (docking, size, location) across sessions. Without a GUID (or with a changing one), the palette loses its position every restart. (Community-reported, strong field guidance.)

- **3-arg constructor startup safety** -- the community-reported `PaletteSet(string name, string cmd, Guid toolID)` replays `cmd` when restoring an open palette on startup. The command must be idempotent, safe in application context, and safe in zero-document or temporary-document startup conditions. (Community-reported.)

- **Restart-docked edge cases** -- palettes may show hidden tabs, missing controls, or misbehaving layout only when reopening docked from persisted state. Always test: show palette -> dock -> close AutoCAD -> reopen -> verify visibility, docking, focus, and control interactivity. (Community-reported.)

- **Zero-document guard** -- palette code that assumes `MdiActiveDocument` or a fully available command line must be guarded. During `DocumentDestroyed`, `DocumentManager.Count` is still `1` when the last document closes.

- **`KeepFocus` for interactive controls** -- set `KeepFocus = true` when the palette contains text boxes, combo boxes, or other interactive controls. Without it, focus returns to the drawing editor immediately after clicking inside the palette.

- **`MdiActiveDocument` null during construction** -- the document context is not established until the palette is shown. Defer document access to event handlers or `Load`, not the constructor.

- **`AddVisual` resize parameter** -- when `bResizeContentToPaletteSize` is `true`, the WPF content stretches with the palette. When `false`, the content keeps its natural size. Default behavior (no bool overload) resizes content to match the palette.

- **`Load`/`Save` events are XML-backed** -- these fire when AutoCAD persists or restores palette state. Use `PalettePersistEventArgs.ConfigurationSection` to read/write custom settings alongside the built-in state.

- **Themed icons supersede older icon methods** -- use `SetThemedIcon(...)` or the `LightThemedIcon`/`DarkThemedIcon` properties for proper light/dark theme support. Older icon properties do not participate in theme switching.

## Related Skills

- `acad-palettes-ribbon` -- practical ribbon API (tabs, panels, buttons, combos) and basic PaletteSet patterns with ElementHost WPF hosting
- `acad-events-overrules` -- application/document events for palette lifecycle management
- `acad-editor-input` -- command execution via `SendStringToExecute` triggered by palette controls
