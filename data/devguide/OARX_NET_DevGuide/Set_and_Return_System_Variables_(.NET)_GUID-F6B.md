<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Set and Return System Variables (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-F6B3122D-A6F4-4112-A838-4662E0E1B30B.htm -->

# Set and Return System Variables (.NET)

The Application object provides the SetSystemVariable and GetSystemVariable methods for setting and retrieving AutoCAD system variables. For example, to assign an integer to the MAXSORT system variable, use the following code: 

## C#
    
    
    // Get the current value from a system variable
    int nMaxSort = System.Convert.ToInt32(Application.GetSystemVariable("MAXSORT"));
     
    // Set system variable to new value
    Application.SetSystemVariable("MAXSORT", 100);

## VB.NET
    
    
    '' Get the current value from a system variable
    Dim nMaxSort as Integer = Application.GetSystemVariable("MAXSORT")
     
    '' Set system variable to new value
    Application.SetSystemVariable("MAXSORT", 100)

## VBA/ActiveX Code Reference
    
    
    '' Get the current value from a system variable
    Dim nMaxSort as Integer
    nMaxSort = ThisDrawing.GetVariable("MAXSORT")
     
    '' Set system variable to new value
    ThisDrawing.SetVariable "MAXSORT", 100
