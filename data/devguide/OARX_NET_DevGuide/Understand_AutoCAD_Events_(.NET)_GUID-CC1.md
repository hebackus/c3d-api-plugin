<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Use Events (.NET) > Understand AutoCAD Events (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-CC1C9D4A-9517-40BF-8D3D-CBC15C9646B9.htm -->

# Understand AutoCAD Events (.NET)

There are many different types of events in AutoCAD. The following is some of the common types of events: 

  * **Application** \- Events respond to the AutoCAD closing, changes to system variables, begin double clicking, and entering and leaving modal states. 
  * **Database** \- Events respond to the saving drawings, addition, deletion, or modification of objects, insertion of block references, attachment and changes to external drawings (xrefs). There are also document level events for system variable changes. 
  * **Document** \- Events respond to the closing drawings, issuing of AutoCAD commands, issuing AutoLISP command or statements, and changes to system variables. 
  * **DocumentCollection** \- Events respond to the creation and destruction of a document, document is activated or deactivated, and lock mode changes to a document. 
  * **Editor** \- Events respond to the changes during requests for user input. 
  * **Graphics** \- Events respond to the creation and destruction of views, and view configuration changes. 
  * **Plotting** \- Events respond to plotting a layout. 
  * **Publishing** \- Events respond to publishing a layout. 
  * **Runtime** \- Events respond to loading and unloading modules, and variables changed or are changing. 
  * **Windows** \- Events respond to changes to the status bar, tray items, palettes and InfoCenter. 

Subroutines that respond to events are called _event handlers_ and are executed automatically each and every time their designated event is triggered. Information contained in the arguments returned by an event, such as a system variable name in the SystemVariableChanging event, are passed from the event handler to the SystemVariableChangingEventArgs object.
