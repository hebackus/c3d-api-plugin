<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > About .NET and the AutoCAD .NET API (.NET) > Overview of the AutoCAD .NET API (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-390A47DB-77AF-433A-994C-2AFBBE9996AE.htm -->

# Overview of the AutoCAD .NET API (.NET)

The AutoCAD .NET API enables you to manipulate the application and drawing files programmatically with the assemblies or libraries that are exposed. With these objects exposed, they can be accessed by many different programming languages and environments. 

There are several advantages to implementing a .NET API for AutoCAD: 

  * Programmatic access to drawings is opened up to more programming environments. Before the .NET API, developers were limited to ActiveX® Automation and languages that supported COM, AutoLISP®, and C++ with ObjectARX. 
  * Integrating with other Windows® based applications, such as Microsoft Excel and Word, is made dramatically easier by using an application’s native .NET API or exposed ActiveX/COM library. 
  * .NET is designed for both 32-bit and 64-bit operating systems. 

Note: Starting with AutoCAD 2020, 32-bit support is no longer available. 

  * Allows access to advanced programming interfaces with a lower learning curve than those for more traditional programming languages such as C++. 

Objects are the main building blocks of the AutoCAD .NET API. Each exposed object represents a precise part of the program or a drawing, and they are grouped into different assemblies and namespaces. There are many different types of objects in the AutoCAD .NET API. For example: 

  * Graphical objects such as lines, arcs, text, and dimensions 
  * Style settings such as text and dimension styles 
  * Organizational structures such as layers, groups, and blocks 
  * The drawing displays such as view and viewport 
  * The drawing and application 

## Unmanaged to Managed Class Mappings

Most ObjectARX classes map to one managed wrapper class. Although there are exceptions, the first four letters of an ObjectARX class name frequently provide a clue to the corresponding managed namespace. The following table shows the most likely mapping of ObjectARX class prefixes to .NET namespaces. 

ObjectARX class prefixes and .NET namespaces  |   
---|---  
Unmanaged Prefix  |  Managed Namespace   
AcAp  |  Autodesk.AutoCAD.ApplicationServices   
AcBr  |  Autodesk.AutoCAD.BoundaryRepresentation   
AcCm  |  Autodesk.AutoCAD.Colors   
AcDb  |  Autodesk.AutoCAD.DatabaseServices   
AcGe  |  Autodesk.AutoCAD.Geometry   
AcGi  |  Autodesk.AutoCAD.GraphicsInterface   
AcLy  |  Autodesk.AutoCAD.LayerManager   
AcPl  |  Autodesk.AutoCAD.PlottingServices   
AcRx  |  Autodesk.AutoCAD.Runtime   
AcUt  |  Autodesk.AutoCAD.DatabaseServices  Autodesk.AutoCAD.ApplicationServices   
  
See “Mapping ObjectARX Classes to Managed Types” in the _AutoCAD Managed Class Reference_ for a complete listing of direct class equivalences.
