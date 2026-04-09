<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Corridors in COM > Assemblies and Subassemblies -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-B1B9586F-3254-4927-BED8-3A1335119A6B.htm -->

# Assemblies and Subassemblies

An assembly is a pattern for the cross section of a corridor at a particular station. An assembly consists of a connected set of subassemblies, each of which are linked to a centerpoint or to other subassemblies. A subassembly consists of a series of shapes, links, and points. When an assembly is used to define the cross-section of a corridor, a series of applied assemblies (an object of type AeccAppliedAssembly) is added to the corridor. Each applied assembly consists of a collection of applied subassemblies, which in turn consist of shapes, links, and points that have been positioned relative to a specific station along the corridor baseline (AeccCalcualtedShapes, AeccCalculatedLinks, and AeccCalculatedPoints respectively). An applied assembly also has direct access to all the calculated shapes, links, and points of its constituent applied subassemblies. 

Note:

The Autodesk Civil 3D API does not include methods for creating or modifying assemblies.
