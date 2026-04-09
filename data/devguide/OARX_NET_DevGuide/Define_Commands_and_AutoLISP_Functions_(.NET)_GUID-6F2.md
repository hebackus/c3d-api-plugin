<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Basics of the AutoCAD .NET API (.NET) > Define Commands and AutoLISP Functions (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-6F28B00B-36BE-4D32-998E-39B62A69E52F.htm -->

# Define Commands and AutoLISP Functions (.NET)

Commands and AutoLISP® functions can be defined with the AutoCAD .NET API through the use of two attributes: CommandMethod and LispFunction. You place one of the two attributes before the method that should be called when the command or AutoLISP function is executed in AutoCAD. 

Methods used for commands should not be defined with arguments. However, a method used to define an AutoLISP function should be defined with a single argument of the ResultBuffer object type.
