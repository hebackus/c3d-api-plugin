<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Basics of the AutoCAD .NET API (.NET) > Understand the AutoCAD Object Hierarchy (.NET) > The Collection Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-B55EF18D-1619-4475-8C0B-5215C2AD2B52.htm -->

# The Collection Objects (.NET)

AutoCAD groups most graphical and non-graphical objects into collections or container objects. Although collections contain different types of data, they can be processed using similar techniques. Each collection has a method for adding an object to or obtaining an item from a collection. Most collections use the Add or SetAt methods to add an object to a collection. 

Most collections offer similar methods and properties to make them easy to use and learn. The Count property returns a zero-based count of the objects in a collection, while the Item function returns an object from a collection. Examples of collection members in the AutoCAD .NET API are: 

  * Layer table record in the Layers symbol table 
  * Layout in the ACAD_LAYOUT dictionary 
  * Document in the DocumentCollection 
  * Attributes in a block reference
