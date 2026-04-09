<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Create Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-DE29EA57-7E55-4AC0-B3B3-68749CA0DC0C.htm -->

# Create Objects (.NET)

AutoCAD often offers several different ways to create the same graphical object. While the AutoCAD .NET API does not offer the same combinations of creating objects, it does offer a basic object constructor for each object type but also offers overrides for many of the object constructors as well. 

For example, in AutoCAD there are four different ways you can create a circle: (1) by specifying the center and radius, (2) by two points defining the diameter, (3) by three points defining the circumference, or (4) by two tangents and a radius. However, in AutoCAD .NET API there is two creation methods provided to create a circle. One method accepts no parameters, while the second requires a center point, the normal direction for the circle, and a radius. 

Note: Objects are created using the New keyword and then appended to the parent object using Add or AppendEntity based on if you are working with a container (symbol table or dictionary) or a BlockTableRecord object. 

## Set the default property values for an object

When a new graphical object is created, the following entity property values are assigned the current entity values defined in the database of the current document: 

  * Color 
  * Layer 
  * Linetype 
  * Linetype scale 
  * Lineweight 
  * Plot style name 
  * Visibility 
  * Transparency 

Note: If the properties of an object need to be set to the default values of the current database, call the SetDatabaseDefaults method of the object to be changed.
