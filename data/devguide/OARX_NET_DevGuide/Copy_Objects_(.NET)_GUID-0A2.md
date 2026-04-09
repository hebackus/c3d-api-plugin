<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Copy Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-0A20B625-3972-4428-AAF2-545E3D32EE30.htm -->

# Copy Objects (.NET)

You can create a copy of most non-graphical and graphical objects within the same database. An object can be copied in the same database with the Clone method or properties from one object can be copied to another object using the CopyFrom method. Once an object is copied, you can modify the returned object before adding it to the database. The Clone and TransformBy methods can be used together to replicate many modifying commands, such as COPY, MIRROR, ARRAY, and OFFSET. The CopyFrom method can be used to replicate the MATCHPROP command with objects in the same database. 

To copy non-graphical or graphical objects between two drawings, use the WblockCloneObjects method. This method enables you to replicate the COPYBASE, COPYCLIP, and PASTECLIP commands. 

Note: Do not use the CopyFrom method to copy objects between two databases.
