<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Customize User Interface (CUI) Managed API (.NET) > Customization Sections (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-269300ED-3423-4FF2-9642-ECCB2C627752.htm -->

# Customization Sections (.NET)

The user interface and workspace data of a CUIx file can be accessed using the CUI managed API. 

There are two specific objects in the CUI managed API that are used to access the customization sections of a CUIx file: MenuGroup and Workspaces. The MenuGroup object contains the menu and interface data used to manipulate the AutoCAD drawing environment, while the Workspaces object is used to control the display of elements in the user interface. Workspace information can be stored in any CUIx file, but is only accessible from a CUIx file that is loaded as a main or enterprise customization file. 

## MenuGroup Collection Object

The individual elements—for example toolbars, pop menus, and shortcuts—can be accessed through collections under the MenuGroup collection object. Collections have no public constructor and are initialized when the CUIx file is parsed in the customization section constructor. 

The following objects are part of the MenuGroup collection object: 

  * AcceleratorCollection \- Shortcut key combinations that can be pressed to start an action 
  * PanelSet \- Tabs used to display and organize panels on the ribbon 
  * DigitizerButtonGroupCollection \- Legacy customizable button definitions used for a digitizer/tablet 
  * DoubleClickCollection \- Actions performed when an object is double-clicked in the drawing area 
  * ImageMenuCollection \- Legacy image title menus that can be displayed 
  * LspFileCollection \- AutoLISP (LSP) files loaded when the CUIx file is loaded into the AutoCAD drawing environment 
  * MouseButtonGroupCollection \- Customizable buttons on a mouse 
  * PopMenuCollection \- Pop (pull-down and shortcut) menus that can be displayed on the menu bar or when the user right-clicks in the drawing area 
  * QuickAccessToolbarCollection \- Toolbars that can be displayed above or below the ribbon 
  * ObjectTypeCollection \- Settings that control which object types and properties are displayed on the Quick Properties palette or rollover tooltips 
  * RibbonRoot \- Top level of the ribbon 
  * ScreenMenuCollection \- Legacy screen menus that can be displayed in the Screen Menu interface 
  * TabletMenuCollection \- Legacy tablet menus that can be used to configure a digitizer/tablet 
  * TemporaryOverrideCollection \- Key combinations that can be pressed and held to temporally override one or more drafting or application settings 
  * ToolbarCollection \- Classic toolbars that can be displayed and docked along the edges of the AutoCAD application window 
  * ToolPanelCollection \- Panels used to organize and display tools on a ribbon tab 

## Workspaces Object

Customization sections contain a collection of workspaces, which can be accessed by index entry or by specifying the workspace name using the IndexOfWorkspaceName() method. A workspace consists of a Quick Access toolbar, classic toolbars, pop menus, dockable windows, and ribbon tabs and panels which are organized using the following objects and collections: 

  * WorkspaceQuickAccessToolbar
  * WorkspaceToolbarCollection
  * WorkspacePopMenuCollection
  * WorkspaceDockableWindowCollection
  * WSRibbonRoot

You can reference a element in a workspace by using one of the following methods: 

  * FindDockableWindow() \- Returns a dockable window (WorkspaceDockableWindow) object based on the provided name 
  * FindWorkspacePopMenu() \- Returns a pop menu (WorkspacePopMenu) object based on the provided element and menu group names 
  * FindWorkspaceToolbar() \- Returns a classic toolbar (WorkspaceToolbar) object based on the provided toolbar and menu group names 
  * FindPanelSource() \- Returns a ribbon panel source (RibbonPanelSource) object based on the provided customization section 
  * FindTabReference() \- Returns a ribbon tab reference (WSRibbonTabSourceReference) object based on the provided menu group name and ID 
  * FindTabReference() \- Returns a ribbon tab source (RibbonTabSource) object based on the provided customization section 

### Adding Elements to a Workspace

Toolbars, pop menus, and ribbon tabs created in the main CUIx file, need to be added to a workspace before they will display in the AutoCAD user interface. New elements added to a toolbar, pop menu, or ribbon panel already displayed in a workspace will be shown automatically when that workspace is reloaded. 

The following code demonstrates how to add a toolbar to a workspace: 

#### C#
    
    
    Toolbar someToolbar = CustomizationSection.MenuGroup.Toolbars[4];
    WorkspaceToolbar wkToolbar = new WorkspaceToolbar(parentWorksapce, someToolbar);

#### VB.NET
    
    
    Dim someToolbar As Toolbar = CustomizationSection.MenuGroup.Toolbars(4)
    Dim wkToolbar As WorkspaceToolbar = New WorkspaceToolbar(parentWorksapce, someToolbar)

Set the Display property of the toolbar to True (or 1) to show it in the workspace. 

### Dockable Windows in a Workspace 

The collection of dockable windows is accessed from CustomizationSection.Workspaces.DockableWindows. Use the DockFloat and Orientation properties to dock or float a window. 

Changes to a workspace will only come into effect after the workspace is reloaded in the application. Restarting the application does not reload the workspace. This must be done using the WSCURRENT system variable or by re-selecting the workspace from the Workspace Switching icon on the status bar.
