<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Corridors in COM > Root Objects > Accessing Corridor-Specific Base Objects -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-B69F8349-ED6C-471E-B472-DF8AA02B639E.htm -->

# Accessing Corridor-Specific Base Objects

Applications that access corridors require special versions of the base objects representing the application and document. The AeccRoadwayApplication object is identical to the AeccApplication it is inherited from except that its AeccRoadwayApplication.ActiveDocument property returns an object of type AeccRoadwayDocument instead of AeccDocument. The AeccRoadwayDocument object contains collections of road related items, such as corridors, subassemblies, and style objects in addition to all of the methods and properties of AeccDocument.

When using corridor root objects, be sure to reference the “Autodesk Civil Engineering Corridor 6.0 Object Library” (AeccXRoadway.tlb) and “Autodesk Civil Engineering UI Corridor 6.0 Object Library” (AeccXUIRoadway.tlb) libraries.

This sample demonstrates how to retrieve the corridor root objects:
    
    
    Dim oApp As AcadApplication
    Set oApp = ThisDrawing.Application
    Dim sAppName As String
    sAppName = "AeccXUiRoadway.AeccRoadwayApplication"
    Dim oRoadwayApplication As AeccRoadwayApplication
    Set oRoadwayApplication = oApp.GetInterfaceObject(sAppName)
     
    ' Get a reference to the currently active document.
    Dim oRoadwayDocument As AeccRoadwayDocument
    Set oRoadwayDocument = oRoadwayApplication.ActiveDocument
