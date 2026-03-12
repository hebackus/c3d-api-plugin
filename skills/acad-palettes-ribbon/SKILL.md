---
name: acad-palettes-ribbon
description: PaletteSet dockable tool palettes, Ribbon API (tabs, panels, buttons, combos), application menu, IExtensionApplication lifecycle for UI registration
---

# AutoCAD Palettes and Ribbon

Use this skill when creating dockable tool palettes via PaletteSet, building ribbon tabs and panels, adding ribbon buttons and controls, or registering UI in the IExtensionApplication lifecycle.

## PaletteSet

PaletteSet is a dockable, floatable container that holds one or more tabbed palettes. Each palette is a WinForms UserControl (or WPF content via ElementHost).

### Creating a PaletteSet

```csharp
using Autodesk.AutoCAD.Windows;

// GUID must be unique per PaletteSet — used for persistence
private static PaletteSet _paletteSet;

[CommandMethod("SHOWMYPALETTE")]
public void ShowMyPalette()
{
    if (_paletteSet == null)
    {
        _paletteSet = new PaletteSet(
            "My Tool Palette",                              // display name
            new Guid("A1B2C3D4-E5F6-7890-ABCD-EF1234567890")); // unique GUID

        _paletteSet.Style = PaletteSetStyles.ShowPropertiesMenu
                          | PaletteSetStyles.ShowAutoHideButton
                          | PaletteSetStyles.ShowCloseButton;

        _paletteSet.DockEnabled = DockSides.Left | DockSides.Right;
        _paletteSet.MinimumSize = new System.Drawing.Size(250, 200);
        _paletteSet.Size = new System.Drawing.Size(350, 600);
        _paletteSet.Opacity = 100;
        _paletteSet.KeepFocus = true;

        // Add a WinForms UserControl as a palette tab
        MyUserControl control = new MyUserControl();
        _paletteSet.Add("Properties", control);

        // Add a second tab
        MySecondControl control2 = new MySecondControl();
        _paletteSet.Add("Settings", control2);
    }

    _paletteSet.Visible = true;
}
```

### PaletteSet Properties

- `Name` (string, get/set) -- display name in the title bar
- `Style` (PaletteSetStyles, get/set) -- combination of style flags
- `DockEnabled` (DockSides, get/set) -- allowed dock sides
- `Dock` (DockSides, get/set) -- current dock position
- `Visible` (bool, get/set) -- show or hide the palette set
- `Opacity` (int, get/set) -- transparency 0-100
- `Size` (System.Drawing.Size, get/set) -- current size
- `MinimumSize` (System.Drawing.Size, get/set) -- minimum allowed size
- `KeepFocus` (bool, get/set) -- retain focus when clicking inside
- `RolledUp` (bool, get/set) -- whether auto-hidden (rolled up)
- `TitleBarLocation` (PaletteSetTitleBarLocation, get/set) -- title bar position
- `Activate(int index)` -- activate a specific palette tab by index

### PaletteSetStyles Flags

- `ShowPropertiesMenu` -- right-click context menu with palette list
- `ShowAutoHideButton` -- auto-hide pin button
- `ShowCloseButton` -- close button in title bar
- `ShowTabForSingle` -- show tab strip even with one palette
- `Snappable` -- snap to edges when floating
- `UsePaletteNameAsTitleForSingle` -- use palette name as title when single tab
- `NameEditable` -- allow renaming via title bar

### Adding WPF Content via ElementHost

```csharp
using System.Windows.Forms.Integration;

// Create a WinForms UserControl that hosts WPF content
UserControl host = new UserControl();
ElementHost elementHost = new ElementHost();
elementHost.Dock = DockStyle.Fill;
elementHost.Child = new MyWpfUserControl();  // WPF UserControl
host.Controls.Add(elementHost);

_paletteSet.Add("WPF Tab", host);
```

### PaletteSet Events

```csharp
_paletteSet.StateChanged += OnPaletteStateChanged;
_paletteSet.SizeChanged += OnPaletteSizeChanged;
_paletteSet.DockStateChanged += OnDockStateChanged;
_paletteSet.PaletteActivated += OnPaletteActivated;
_paletteSet.PaletteAdded += OnPaletteAdded;
_paletteSet.VisibleChanged += OnVisibleChanged;
_paletteSet.Load += OnPaletteLoad;
```

#### StateChanged

Fires when the palette is shown, hidden, rolled up, or unrolled.

```csharp
private void OnPaletteStateChanged(object sender, PaletteSetStateEventArgs e)
{
    // e.NewState is the new PaletteSetState
    if (e.NewState == PaletteSetState.Show)
    {
        // Palette became visible — refresh data
        RefreshContent();
    }
    else if (e.NewState == PaletteSetState.Hide)
    {
        // Palette was hidden
    }
}
```

#### DockStateChanged

Fires when the palette docks or undocks.

```csharp
private void OnDockStateChanged(object sender, EventArgs e)
{
    PaletteSet ps = (PaletteSet)sender;
    DockSides currentDock = ps.Dock;
    // Adjust layout based on dock state if needed
}
```

### Dock States

- `DockSides.None` -- floating
- `DockSides.Left` -- docked to the left
- `DockSides.Right` -- docked to the right
- `DockSides.Top` -- docked to the top (rarely used)
- `DockSides.Bottom` -- docked to the bottom (rarely used)

### PaletteSet Persistence

PaletteSet automatically saves and restores its dock state, position, and size between sessions when a GUID is provided. The state is stored in the Windows registry under the AutoCAD profile.

```csharp
// The GUID in the constructor enables automatic persistence
_paletteSet = new PaletteSet("My Palette",
    new Guid("A1B2C3D4-E5F6-7890-ABCD-EF1234567890"));

// Custom state persistence (manual)
_paletteSet.Load += (s, e) =>
{
    // Restore custom settings from registry or file
    string savedFilter = LoadSetting("PaletteFilter");
    if (savedFilter != null)
        ApplyFilter(savedFilter);
};

// Save custom state when palette closes
_paletteSet.StateChanged += (s, e) =>
{
    if (e.NewState == PaletteSetState.Hide)
        SaveSetting("PaletteFilter", GetCurrentFilter());
};
```

## Ribbon API

The Ribbon API lives in `Autodesk.Windows` (referenced via `AdWindows.dll`). It provides RibbonControl, RibbonTab, RibbonPanel, and various button/control types.

### Creating a Ribbon Tab

```csharp
using Autodesk.Windows;

public void CreateRibbonTab()
{
    RibbonControl ribbon = ComponentManager.Ribbon;
    if (ribbon == null) return;

    // Create a new tab
    RibbonTab tab = new RibbonTab();
    tab.Title = "My Tools";
    tab.Id = "MY_TOOLS_TAB";
    tab.Name = "My Tools Tab";

    // Create a panel
    RibbonPanelSource panelSource = new RibbonPanelSource();
    panelSource.Title = "Drawing Tools";
    panelSource.Id = "MY_DRAWING_PANEL";

    RibbonPanel panel = new RibbonPanel();
    panel.Source = panelSource;

    tab.Panels.Add(panel);
    ribbon.Tabs.Add(tab);

    // Make the tab active
    tab.IsActive = true;
}
```

### RibbonButton

```csharp
RibbonButton button = new RibbonButton();
button.Text = "Create Block";
button.ShowText = true;
button.ShowImage = true;
button.Size = RibbonItemSize.Large;
button.Orientation = System.Windows.Controls.Orientation.Vertical;
button.LargeImage = LoadImage("Images/create_block_32.png");
button.Image = LoadImage("Images/create_block_16.png");
button.CommandParameter = "CREATEBLOCK ";  // trailing space executes immediately
button.CommandHandler = new RibbonCommandHandler();

panelSource.Items.Add(button);
```

### RibbonCommandHandler

```csharp
public class RibbonCommandHandler : System.Windows.Input.ICommand
{
    public event EventHandler CanExecuteChanged;

    public bool CanExecute(object parameter)
    {
        return true;
    }

    public void Execute(object parameter)
    {
        RibbonButton button = parameter as RibbonButton;
        if (button == null) return;

        Document doc = Application.DocumentManager.MdiActiveDocument;
        if (doc == null) return;

        string cmdName = (string)button.CommandParameter;
        doc.SendStringToExecute(cmdName, true, false, true);
    }
}
```

### Loading Ribbon Images

```csharp
using System.Windows.Media.Imaging;

private static BitmapImage LoadImage(string relativePath)
{
    string dllPath = System.Reflection.Assembly.GetExecutingAssembly().Location;
    string dir = System.IO.Path.GetDirectoryName(dllPath);
    string fullPath = System.IO.Path.Combine(dir, relativePath);

    BitmapImage image = new BitmapImage();
    image.BeginInit();
    image.UriSource = new Uri(fullPath, UriKind.Absolute);
    image.EndInit();
    return image;
}

// From embedded resource
private static BitmapImage LoadEmbeddedImage(string resourceName)
{
    var assembly = System.Reflection.Assembly.GetExecutingAssembly();
    using (var stream = assembly.GetManifestResourceStream(resourceName))
    {
        BitmapImage image = new BitmapImage();
        image.BeginInit();
        image.StreamSource = stream;
        image.CacheOption = BitmapCacheOption.OnLoad;
        image.EndInit();
        image.Freeze();
        return image;
    }
}
```

### RibbonSplitButton

A button with a dropdown menu of sub-items.

```csharp
RibbonSplitButton splitButton = new RibbonSplitButton();
splitButton.Text = "Label";
splitButton.ShowText = true;
splitButton.Size = RibbonItemSize.Large;
splitButton.IsSplit = true;  // top half executes default, bottom shows dropdown
splitButton.LargeImage = LoadImage("Images/label_32.png");

RibbonButton subItem1 = new RibbonButton();
subItem1.Text = "Label Pipes";
subItem1.CommandParameter = "LABELPIPES ";
subItem1.CommandHandler = new RibbonCommandHandler();

RibbonButton subItem2 = new RibbonButton();
subItem2.Text = "Label Structures";
subItem2.CommandParameter = "LABELSTRUCTURES ";
subItem2.CommandHandler = new RibbonCommandHandler();

splitButton.Items.Add(subItem1);
splitButton.Items.Add(subItem2);

panelSource.Items.Add(splitButton);
```

### RibbonToggleButton

A button that stays pressed to indicate an on/off state.

```csharp
RibbonToggleButton toggleButton = new RibbonToggleButton();
toggleButton.Text = "Auto Label";
toggleButton.ShowText = true;
toggleButton.Size = RibbonItemSize.Standard;
toggleButton.Image = LoadImage("Images/auto_label_16.png");
toggleButton.CheckStateChanged += (s, e) =>
{
    bool isChecked = toggleButton.IsChecked;
    // Enable or disable auto-labeling
    SetAutoLabel(isChecked);
};

panelSource.Items.Add(toggleButton);
```

### RibbonCombo

A dropdown combo box in the ribbon.

```csharp
RibbonCombo combo = new RibbonCombo();
combo.Id = "LAYER_COMBO";
combo.Size = RibbonItemSize.Large;
combo.Width = 180;
combo.ShowImage = false;

combo.Items.Add(new RibbonButton { Text = "Option A", Id = "OPT_A" });
combo.Items.Add(new RibbonButton { Text = "Option B", Id = "OPT_B" });
combo.Items.Add(new RibbonButton { Text = "Option C", Id = "OPT_C" });

combo.CurrentChanged += (s, e) =>
{
    RibbonButton selected = combo.Current as RibbonButton;
    if (selected != null)
    {
        string selectedId = selected.Id;
        // Handle selection change
    }
};

panelSource.Items.Add(combo);
```

### RibbonRowPanel

Arrange multiple small items in horizontal rows within a panel.

```csharp
RibbonRowPanel rowPanel = new RibbonRowPanel();

// First row
RibbonButton btn1 = new RibbonButton();
btn1.Text = "Zoom Extents";
btn1.ShowText = true;
btn1.Size = RibbonItemSize.Standard;
btn1.CommandParameter = "ZOOM E ";
btn1.CommandHandler = new RibbonCommandHandler();
rowPanel.Items.Add(btn1);

// Row break — start a new row
rowPanel.Items.Add(new RibbonRowBreak());

// Second row
RibbonButton btn2 = new RibbonButton();
btn2.Text = "Regen";
btn2.ShowText = true;
btn2.Size = RibbonItemSize.Standard;
btn2.CommandParameter = "REGEN ";
btn2.CommandHandler = new RibbonCommandHandler();
rowPanel.Items.Add(btn2);

panelSource.Items.Add(rowPanel);
```

### Ribbon Item Properties Summary

- `Text` (string) -- display text
- `ShowText` (bool) -- show text label
- `ShowImage` (bool) -- show icon
- `Image` (ImageSource) -- 16x16 small icon
- `LargeImage` (ImageSource) -- 32x32 large icon
- `Size` (RibbonItemSize) -- `Standard` (small) or `Large`
- `Orientation` (Orientation) -- `Vertical` or `Horizontal` text/icon layout
- `Id` (string) -- unique identifier
- `ToolTip` (object) -- tooltip (string or RibbonToolTip)
- `KeyTip` (string) -- keyboard accelerator
- `IsEnabled` (bool) -- enabled state
- `IsVisible` (bool) -- visibility
- `CommandParameter` (object) -- command string for handler
- `CommandHandler` (ICommand) -- executes on click

## Application Menu

The application menu (File menu) can be customized by accessing `ComponentManager.Ribbon.ApplicationMenu`.

```csharp
RibbonControl ribbon = ComponentManager.Ribbon;

// Add item to application menu
ApplicationMenu appMenu = ribbon.ApplicationMenu;

RibbonButton appMenuItem = new RibbonButton();
appMenuItem.Text = "My Custom Export";
appMenuItem.Id = "MY_EXPORT";
appMenuItem.CommandParameter = "MYCUSTOMEXPORT ";
appMenuItem.CommandHandler = new RibbonCommandHandler();

appMenu.MenuContent.Items.Add(appMenuItem);
```

## IExtensionApplication Lifecycle for UI Registration

Register ribbon and palette UI in the `IExtensionApplication.Initialize` method. The ribbon may not be available immediately at startup, so defer creation if necessary.

```csharp
public class MyPlugin : IExtensionApplication
{
    private static PaletteSet _paletteSet;

    public void Initialize()
    {
        // Ribbon may not exist yet at Initialize time — defer
        if (ComponentManager.Ribbon != null)
        {
            CreateRibbon();
        }
        else
        {
            ComponentManager.ItemInitialized += OnComponentInitialized;
        }
    }

    private void OnComponentInitialized(object sender, RibbonItemEventArgs e)
    {
        if (ComponentManager.Ribbon != null)
        {
            ComponentManager.ItemInitialized -= OnComponentInitialized;
            CreateRibbon();
        }
    }

    private void CreateRibbon()
    {
        RibbonControl ribbon = ComponentManager.Ribbon;

        RibbonTab tab = new RibbonTab();
        tab.Title = "My Plugin";
        tab.Id = "MYPLUGIN_TAB";

        RibbonPanelSource panelSource = new RibbonPanelSource();
        panelSource.Title = "Tools";
        RibbonPanel panel = new RibbonPanel();
        panel.Source = panelSource;

        RibbonButton paletteBtn = new RibbonButton();
        paletteBtn.Text = "Show Palette";
        paletteBtn.Size = RibbonItemSize.Large;
        paletteBtn.ShowText = true;
        paletteBtn.LargeImage = LoadImage("Images/palette_32.png");
        paletteBtn.CommandParameter = "SHOWMYPALETTE ";
        paletteBtn.CommandHandler = new RibbonCommandHandler();

        panelSource.Items.Add(paletteBtn);
        tab.Panels.Add(panel);
        ribbon.Tabs.Add(tab);
    }

    public void Terminate()
    {
        // Clean up palette
        if (_paletteSet != null)
        {
            _paletteSet.Visible = false;
            _paletteSet = null;
        }

        // Remove ribbon tab
        RibbonControl ribbon = ComponentManager.Ribbon;
        if (ribbon != null)
        {
            RibbonTab tab = ribbon.FindTab("MYPLUGIN_TAB");
            if (tab != null)
                ribbon.Tabs.Remove(tab);
        }
    }
}
```

## Gotchas

- **PaletteSet GUID must be unique** -- reusing a GUID from another PaletteSet causes state corruption and crashes on restore.
- **`ComponentManager.Ribbon` may be null during `Initialize`** -- the ribbon loads asynchronously. Always check for null and defer via `ComponentManager.ItemInitialized`.
- **`CommandParameter` needs a trailing space** -- without it, the command string is placed on the command line but not executed. The space acts as Enter.
- **`KeepFocus = true` on PaletteSet** -- required for interactive controls (text boxes, combo boxes) inside palettes. Without it, focus returns to the drawing editor immediately.
- **Ribbon images must be frozen** -- WPF BitmapImage objects used as `Image` or `LargeImage` should be `Freeze()`-d for cross-thread access. Non-frozen images throw on the ribbon's render thread.
- **PaletteSet content cannot access `MdiActiveDocument` directly during construction** -- the document context is not established until the palette is shown. Defer document access to event handlers or `Load`.
- **`SendStringToExecute` is asynchronous** -- it queues the command; it does not run immediately. Do not assume the command has completed after the call returns.
- **Ribbon tabs persist across NETLOAD/NETUNLOAD** -- if the plugin is reloaded, duplicate tabs appear. Check for existing tabs by Id before adding.
- **PaletteSet minimum size interacts with dock** -- when docked, the palette cannot be smaller than `MinimumSize`. If `MinimumSize` is too large, the palette cannot dock into narrow side panels.
- **`RibbonSplitButton.IsSplit = true`** -- when true, the top portion executes the first item's command and the bottom arrow opens the dropdown. When false, the entire button opens the dropdown.
- **ElementHost in PaletteSet** -- wrap WPF content in a WinForms UserControl first, then add the UserControl to PaletteSet. Adding an ElementHost directly can cause layout issues.
- **Ribbon state after drawing switch** -- ribbon tab selection resets when switching documents. Re-activating a custom tab requires handling `DocumentBecameCurrent`.
- **PaletteSet `Visible = true` outside a command context** -- may require `Application.DocumentManager.MdiActiveDocument.LockDocument()` if the palette modifies the database on show.
- **RibbonToggleButton `IsChecked`** -- read this property inside the `CheckStateChanged` handler; the value reflects the new state after the click.

## Related Skills

- `acad-palettes` -- deep PaletteSet API reference, Tool Palette API, Properties Palette, lifecycle and zero-document state
- `acad-events-overrules` -- IExtensionApplication lifecycle for registering palettes and ribbon at startup
- `acad-editor-input` -- command execution via `SendStringToExecute` triggered by ribbon buttons
- `acad-blocks` -- tool palette block content and block insertion commands from ribbon
