<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Basics of the AutoCAD .NET API (.NET) > Access the Object Hierarchy (.NET) > Access the Application Object (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-89D14077-DCEF-42D3-94F4-434D5AF23D41.htm -->

# Access the Application Object (.NET)

The Application object is at the root of the object hierarchy and it provides access to the main window of AutoCAD. For example, the following line of code updates the application: 

## C#
    
    
    Autodesk.AutoCAD.ApplicationServices.Application.UpdateScreen();

## VB.NET
    
    
    Autodesk.AutoCAD.ApplicationServices.Application.UpdateScreen()

## VBA/ActiveX Code Reference
    
    
    ThisDrawing.Application.Update
