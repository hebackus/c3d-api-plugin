<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Pipe Networks in COM > Base Objects > Accessing Pipe Network-Specific Base Objects -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-7B57B1D5-BD2A-4A32-A6A2-BC4271990385.htm -->

# Accessing Pipe Network-Specific Base Objects

Applications that access pipe networks require special versions of the base objects representing the application and document. The AeccPipeApplication object is identical to the AeccApplication it is inherited from except that its AeccPipeApplication.ActiveDocument property returns an object of type AeccPipeDocument instead of AeccDocument. The AeccPipeDocument object contains collections of pipe network-related items, such as pipe networks, pipe styles, and interference checks. It also contains all of the methods and properties of AeccDocument.

When using pipe network root objects, be sure to reference the “Autodesk Civil Engineering Pipe 6.0 Object Library” (AeccXPipe.tlb) and “Autodesk Civil Engineering UI Pipe 6.0 Object Library” (AeccXUIPipe.tlb) libraries.

This sample demonstrates how to retrieve the pipe network root objects:
    
    
    Dim oApp As AcadApplication
    Set oApp = ThisDrawing.Application
    Dim sAppName As String
    sAppName = "AeccXUiPipe.AeccPipeApplication"
    Dim oPipeApplication As AeccPipeApplication
    Set oPipeApplication = oApp.GetInterfaceObject(sAppName)
     
    ' Get a reference to the currently active document.
    Dim oPipeDocument As AeccPipeDocument
    Set oPipeDocument = oPipeApplication.ActiveDocument
