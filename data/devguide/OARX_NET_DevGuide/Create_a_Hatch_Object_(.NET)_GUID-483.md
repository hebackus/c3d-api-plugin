<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Create Objects (.NET) > Create Hatches (.NET) > Create a Hatch Object (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-483D7C81-71E6-4775-914E-F4D6B99248ED.htm -->

# Create a Hatch Object (.NET)

When creating a Hatch object, you specify the hatch pattern type, the hatch pattern name, and the associativity. Once a Hatch object has been created, you will not be able to change the hatch associativity. 

To create a Hatch object, you create a new instance of the object and then use the AppendEntity method to add it to a BlockTableRecord object.
