<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Linetypes (.NET) > Delete Linetypes (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-380C741C-147D-4289-8C3A-19BF7DDC1CFA.htm -->

# Delete Linetypes (.NET)

To delete a linetype, use the Erase method. You can delete a linetype at any time during a drawing session; however, linetypes that cannot be deleted include BYLAYER, BYBLOCK, CONTINUOUS, the current linetype, a linetype in use, and xref-dependent linetypes. Also, linetypes referenced by block definitions cannot be deleted, even if they are not used by any objects.
