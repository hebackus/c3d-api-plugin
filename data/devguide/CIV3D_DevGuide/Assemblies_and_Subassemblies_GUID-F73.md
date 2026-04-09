<!-- Developer's Guide > API Developer's Guide > Corridors > Assemblies and Subassemblies -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-F732A07B-467A-4812-BDB7-DD2961F8495A.htm -->

# Assemblies and Subassemblies

An assembly is a pattern for the cross section of a corridor at a particular station. An assembly consists of a connected set of subassemblies, each of which are linked to a centerpoint or to other subassemblies. A subassembly consists of a series of shapes, links, and points. When an assembly is used to define the cross-section of a corridor, a series of applied assemblies (an object of type AppliedAssembly) is added to the corridor. Each applied assembly consists of a collection of applied subassemblies, which in turn consist of shapes, links, and points that have been positioned relative to a specific station along the corridor baseline (CalculatedShape, CalculatedLink, and CalculatedPoint respectively). An applied assembly also has direct access to all the calculated shapes, links, and points of its constituent applied subassemblies. 

Subassemblies are individual components that make up a cross-section of a corridor model, such as curbs, travel lanes, side slopes, etc. A collection of subassemblies that make up a cross-section are grouped as an assembly. See the "Understanding Assemblies" topic in the Civil 3D User's Guide for more in depth information about how Assemblies are created and used in Civil 3D. 

In the .NET API, there are two types of Assembly objects - the Assembly object and the AppliedAssembly object. The Assembly object can be considered a template, and is held in the CivilDocument.AssemblyCollection. When an Assembly is applied to a corridor, multiple AppliedAssembly objects are created in the corridor's BaselineRegions.

Subassemblies that make up an Assembly are organized in groups, contained in the Assembly.Groups property. This collection contains AssemblyGroup objects. The AssemblyGroup.GetSubassemblyIds() method returns an ObjectIdCollection of all Subassemblies in the group.
