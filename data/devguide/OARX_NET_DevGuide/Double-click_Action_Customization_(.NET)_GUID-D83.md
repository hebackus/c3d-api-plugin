<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Customize User Interface (CUI) Managed API (.NET) > Customization Sections (.NET) > Double-click Action Customization (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-D8326E2F-CEBE-4362-ABFC-5C19777109D2.htm -->

# Double-click Action Customization (.NET)

Double-click actions can be used to start an editing command when an object in the drawing area is double-clicked. 

Double clicking on most objects in the drawing window displays the Properties palette. This behavior can be changed with the DoubleClickAction and DoubleClickCmd classes. Use these classes to add editing behavior for a custom object. 

The customization of the double-click behavior is done by first attaching a MacroId to a DoubleClickCmd object. This defines the action that will be performed. Next, attach a DoubleClickAction object to a drawing object using the DxfName() property. Finally attach the action to the command. 

### C#
    
    
    DoubleClickAction dblClickAction = new DoubleClickAction(cs.MenuGroup, "My Double click", -1);
    dblClickAction.DxfName = "Polyline";
    
    DoubleClickCmd dblClickCmd = new DoubleClickCmd(dblClickAction);
    dblClickCmd.MacroID = "MM_1567";
    dblClickAction.DoubleClickCmd = dblClickCmd;

### VB.NET
    
    
    Dim dblClickAction as DoubleClickAction = New DoubleClickAction(cs.MenuGroup, "My Double click", -1)
    dblClickAction.DxfName = "Polyline"
    
    Dim dblClickCmd As DoubleClickCmd = New DoubleClickCmd(dblClickAction)
    dblClickCmd.MacroID = "MM_1567"
    dblClickAction.DoubleClickCmd = dblClickCmd

dblClickAction in the previous code samples is now set to execute the polyline edit macro (MM_1567) when a Polyline graphical object is double-clicked. If a double-click action for an object is overridden, the new action takes precedence, and the old action becomes inactive.
