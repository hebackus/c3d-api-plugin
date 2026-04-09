<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Basics of the AutoCAD .NET API (.NET) > Understand the AutoCAD Object Hierarchy (.NET) >  Graphical and Non-graphical Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-1ECA7D76-EF28-43E3-A22B-CC2906270A73.htm -->

#  Graphical and Non-graphical Objects (.NET)

Graphical objects, also known as entities, are the visible objects (lines, circles, raster images, and so forth) that make up a drawing. Adding graphical objects to a drawing is done by referencing the correct block table record, and then using the AppendEntity method with the new object to append it to the drawing. 

To modify or query objects, obtain a reference to the object from the appropriate block table record, and then use the methods or properties of the object itself. Each graphical object has methods that perform most of the same functionality as the AutoCAD editing commands such as Copy, Erase, Move, Mirror, and so forth. 

These objects also have methods to retrieve the extended data (xdata), highlight and unhighlight, and set the properties from another entity. Most graphical objects have some properties in common with each other such as LayerId, LinetypeId, Color, and Handle. Each graphical object also has specific properties, such as Center, StartPoint, Radius, and FitTolerance. 

Non-graphical objects are the invisible (informational) objects that are part of a drawing, such as Layers, Linetypes, Dimension styles, Table styles, and so forth. To create a new symbol table records, use the Add method on the owner table or use the SetAt method to add a dictionary to the named object dictionary. To modify or query these objects, use the methods or properties of the object itself. Each non-graphical object has methods and properties specific to its purpose; all have methods to retrieve extended data (xdata), and erase themselves.
