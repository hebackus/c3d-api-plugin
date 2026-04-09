<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Linetypes (.NET) > Make a Linetype Active (.NET) > Make a Linetype Current With the CELTYPE System Variable (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-0BB17909-31D8-4CCF-8338-66ABDDBFE3DD.htm -->

# Make a Linetype Current With the CELTYPE System Variable (.NET)

This example sets a linetype current with the CELTYPE system variable. 

## C#
    
    
    Application.SetSystemVariable("CELTYPE", "Center");

## VB.NET
    
    
    Application.SetSystemVariable("CELTYPE", "Center")

## VBA/ActiveX Code Reference
    
    
    ThisDrawing.SetVariable "CELTYPE", "Center"
