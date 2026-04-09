<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-F5601807-2FA9-486F-A212-E693D452D81F.htm -->

# Create and Edit AutoCAD Entities (.NET)

You can create a range of objects, from simple lines and circles to spline curves, ellipses, and associative hatch areas. In general, you add objects to a BlockTableRecord object using the AppendEntity function. Once an object is created, you can change its properties such as layer, color, and linetype. 

The drawing database is similar to other database programs, you can think of a Line object in Model space as table record and Model space as its database table. When working with a database, you must open and close records before working with them. The objects stored in the Database object are no different, you use the GetObject function to retrieve an object from the database and define how you want to work with the object.
