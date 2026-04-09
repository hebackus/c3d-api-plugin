<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Dimensions and Tolerances (.NET) > Dimensioning Concepts (.NET) > Define the Dimension System Variables (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-AD41C7BB-4DBC-427C-95AD-5C44DD0F3C6C.htm -->

# Define the Dimension System Variables (.NET)

The dimension system variables control the appearance of dimensions. The dimension system variables include DIMAUNIT, DIMUPT, DIMTOFL, DIMFIT, DIMTIH, DIMTOH, DIMJUST, and DIMTAD. You can set these variables by using the SetSystemVariable method which can be accessed from the Application object. For example, the following line of code sets the DIMAUNIT system variable (the units format for angular dimensions) to radians (3): 

## C#
    
    
    Application.SetSystemVariable("DIMAUNIT", 3);

## VB.NET
    
    
    Application.SetSystemVariable("DIMAUNIT", 3)

## VBA/ActiveX Code Reference
    
    
    ThisDrawing.SetVariable "DIMAUNIT", 3
