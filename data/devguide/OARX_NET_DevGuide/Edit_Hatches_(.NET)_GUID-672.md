<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Edit Hatches (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-6724C1A9-70C7-4C0A-9952-00E06249C6C0.htm -->

# Edit Hatches (.NET)

You can edit both hatch boundaries and hatch patterns. If you edit the boundary of an associative hatch, the pattern is updated as long as the editing results in a valid boundary. Associative hatches are updated even if they are on layers that are turned off. You can modify hatch patterns or choose a new pattern for an existing hatch, but associativity can only be set when a hatch is created. You can check to see if a Hatch object is associative by using the Associative property. 

You must re-evaluate a hatch using the EvaluateHatch method to see any edits to the hatch.
