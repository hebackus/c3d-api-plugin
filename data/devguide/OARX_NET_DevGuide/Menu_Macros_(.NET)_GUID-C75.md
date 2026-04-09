<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Customize User Interface (CUI) Managed API (.NET) > Customization Sections (.NET) > Menu Macros (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-C75BC92C-0784-44B7-9D5C-62D5A74B2333.htm -->

# Menu Macros (.NET)

Menu macros define the command sequences to be passed to the AutoCAD Command prompt when a user interface element is clicked. 

The CUIx file defines menu macros that are attached to elements. An interface element must have a MacroID to identify the action to be performed when the element is clicked; each macro has a unique identity string to represent that command. The MenuMacro class defines a macro string, which can be a simple command, a command sequence with options and values, or a complex DIESEL expression. 

For information on creating macros and using DIESEL, see “About Command Customization” and “About DIESEL Expressions in Macros” in the AutoCAD help system. 

## PopMenus with DIESEL Expressions

The DIESEL expressions passed to the PopMenu.DisplayName() and PopMenuItem.DisplayName() properties are evaluated by the AutoCAD application environment during runtime. In this case, the properties return the name of the menu item as it would appear in the pulldown menu. When called from a stand-alone application, these methods just return the DIESEL expression.
