<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Basics of the AutoCAD .NET API (.NET) > Understand the AutoCAD Object Hierarchy (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-7E64FDE7-C818-4566-ADF8-C40D50D91E32.htm -->

# Understand the AutoCAD Object Hierarchy (.NET)

An object is the main building block of the AutoCAD .NET API. Each exposed object represents a precise part of AutoCAD. There are many different types of objects in the AutoCAD .NET API. Some of the objects represented in the AutoCAD .NET API are: 

  * Graphical objects such as lines, arcs, text, and dimensions 
  * Style settings such as layers, linetypes, and dimension styles 
  * Organizational structures such as layers, groups, and blocks 
  * The drawing display such as view and viewport 
  * Even the drawing and the AutoCAD application 

The objects are structured in a hierarchical fashion, with the AutoCAD Application object at the root. This hierarchical structure is often referred to as the Object Model. The following illustration shows the basic relationships between the Application object and an entity that is in a BlockTableRecord, such as Model space. There are many more objects in the AutoCAD .NET API that are not represented here.
