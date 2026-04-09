<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Customize User Interface (CUI) Managed API (.NET) > Customization Sections (.NET) > Toolbars (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-B4F5F3D2-655C-4AAD-A8FD-89A898F5A457.htm -->

# Toolbars (.NET)

Toolbars are a collection of buttons, flyout toolbars and controls. 

Toolbar buttons use the image icons defined by their macros. Toolbar controls are defined in the ControlType enum. Use this enum to add new controls to toolbars. Adding new toolbars to workspaces requires adding a new WorkspaceToolbar, which is discussed under the “Workspaces (.NET)” topic. 

## Create a Toolbar

New toolbars are created by specifying the menu group in the constructor. In most cases you would add the toolbar to the menu group of a customization section. 

The following code sample creates a new toolbar called "New Toolbar", and sets the orientation and visibility properties. 

### C#
    
    
    Toolbar newTb = new Toolbar("New Toolbar", cs.MenuGroup);
    newTb.ElementID = "EID_NewToolbar";
    newTb.ToolbarOrient = ToolbarOrient.Floating;
    newTb.ToolbarVisible = ToolbarVisible.Show;

### VB.NET
    
    
    Dim newTb As Toolbar = New Toolbar("New Toolbar", cs.MenuGroup)
    newTb.ElementID = "EID_NewToolbar"
    newTb.ToolbarOrient = ToolbarOrient.Floating
    newTb.ToolbarVisible = ToolbarVisible.Show

## Modify an Existing Toolbar

The Toolbars collection of the customization section’s menu group can be used to access a toolbar by index, name, or alias. A toolbar can be returned by its name with the FindToolbarUsingName() method or alias with the FindToolbarUsingAlias() method. 

### C# 
    
    
    // Get toolbar by index
    Toolbar someToolbar = cs.MenuGroup.Toolbars[1];
    
    // Get toolbar by name
    Toolbar someToolbar = cs.MenuGroup.Toolbars.FindToolbarWithName("DRAW");
    
    // Get toolbar by alias
    Toolbar someToolbar = cs.MenuGroup.Toolbars.FindToolbarUsingAlias("TB_DRAW");

### VB.NET
    
    
    ' Get toolbar by index
    Dim someToolbar As Toolbar = cs.MenuGroup.Toolbars(1)
    
    ' Get toolbar by name
    Dim someToolbar As Toolbar = cs.MenuGroup.Toolbars.FindToolbarWithName("DRAW")
    
    ' Get toolbar by alias
    Dim someToolbar As Toolbar = cs.MenuGroup.Toolbars.FindToolbarUsingAlias("TB_DRAW")

Now, using the reference to the Draw toolbar, you can add, remove, or modify the toolbar and its elements. Add new toolbar elements by specifying the parent toolbar in the element’s constructor, as shown below: 

### C#
    
    
    ToolbarButton newButton = new ToolbarButton(drawToolbar, -1);
    newButton.MacroID = "ID_Pline";
    Toolbarcontrol newControl = new ToolbarControl(ControlType.NamedViewControl, drawToolbar, -1);
    ToolbarFlyout newFlyout = new ToolbarFlyout(drawToolbar, -1);
    newFlyout.ToolbarReference = "DIMENSION";

### VB.NET
    
    
    Dim newButton As ToolbarButton = New ToolbarButton(drawToolbar, -1)
    newButton.MacroID = "ID_Pline"
    Dim newControl As Toolbarcontrol = New ToolbarControl(ControlType.NamedViewControl, drawToolbar, -1)
    Dim newFlyout As ToolbarFlyout = New ToolbarFlyout(drawToolbar, -1)
    newFlyout.ToolbarReference = "DIMENSION"

Toolbar flyouts are special elements that do not have a MacroID. Instead, they require a reference to a toolbar. This reference determines the items to be displayed in the flyout. You can create new toolbars for the referenced toolbar.
