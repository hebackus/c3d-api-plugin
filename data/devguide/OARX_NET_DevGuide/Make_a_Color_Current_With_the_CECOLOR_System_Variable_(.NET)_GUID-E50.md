<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Colors (.NET) > Make a Color Current With the CECOLOR System Variable (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-E50CC1AF-9448-4F30-9A2A-9142AB57163D.htm -->

# Make a Color Current With the CECOLOR System Variable (.NET)

This example sets the color Red current with the CECOLOR system variable. 

## C#
    
    
    Application.SetSystemVariable("CECOLOR", "1");

## VB.NET
    
    
    Application.SetSystemVariable("CECOLOR", "1")

## VBA/ActiveX Code Reference
    
    
    ThisDrawing.SetVariable "CECOLOR", "1"
