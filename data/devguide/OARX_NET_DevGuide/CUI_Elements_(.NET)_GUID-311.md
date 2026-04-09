<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Customize User Interface (CUI) Managed API (.NET) > Customization Sections (.NET) > CUI Elements (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-311320E4-6829-4799-A5B0-9425C157A8FD.htm -->

# CUI Elements (.NET)

Many user interface elements share a number of properties in common with each other that describe . 

User interface elements such as ribbon buttons, pop-up menu items, toolbar buttons, toolbar controls, and shortcut keys have the following common properties: 

  * Name 
  * Parent 
  * ElementID 
  * MenuMacroReference 
  * MacroID 
  * Display Name 

Elements must define their parent in the constructor, which also adds the element into the parent object. 

In the following sample code, a new button is added to the last position of the Draw toolbar during initialization. An explicit call to the toolbar’s Add() method is not required. 

### C# 
    
    
    Toolbar drawToolbar = cs.MenuGroup.Toolbars.FindToolbarWithName("DRAW");
    ToolbarButton polyLineButton = new ToolbarButton(drawToolbar,-1);

### VB.NET
    
    
    Dim drawToolbar As Toolbar = cs.MenuGroup.Toolbars.FindToolbarWithName("DRAW")
    Dim polyLineButton As ToolbarButton = New ToolbarButton(drawToolbar,-1)

## Version Control

CUI elements derive from the VersionableElement base class, which adds a revision number to the element. Newly created or modified elements are tagged with the version number of the current _AcCui.dll_ file. 

The MenuMacro class, which represents an action or command, can contain multiple versions of a macro. When calling the macro property, the correct macro for the current version of the AutoCAD program is returned. Iterate through the MenuMacro.Macros collection for other versions of the macro.
