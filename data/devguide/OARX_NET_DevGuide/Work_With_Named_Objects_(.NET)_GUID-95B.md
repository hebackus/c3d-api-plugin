<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Work With Named Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-95B5DDB0-E2D1-4E60-A7E2-AE26959C3D83.htm -->

# Work With Named Objects (.NET)

In addition to the graphical objects used by AutoCAD, there are several types of nongraphical objects stored in a drawing database. These objects have descriptive designations associated with them. For example, blocks, layers, groups, and dimension styles all have a name assigned to them and in most cases can be renamed. The names of symbol table records are displayed in the user interface of AutoCAD, while the object id of an object is used to reference the object in most cases throughout the AutoCAD .NET API. 

For example, the object id of a LayerTableRecord object is assigned to a graphical object’s Layer property and not the actual name that is assigned to the LayerTableRecord. However, the object id of a LayerTableRecord object can be obtained from the Layer table using the name of the layer you want to access.
