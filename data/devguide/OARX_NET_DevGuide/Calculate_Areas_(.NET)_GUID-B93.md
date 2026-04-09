<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Draw With Precision (.NET) > Calculate Areas (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-B931C746-6FCF-4E89-9C71-62C2C0C86A9A.htm -->

# Calculate Areas (.NET)

You can find the area of an arc, circle, ellipse, lightweight polyline, polyline, region, hatch, planar-closed spline or any other entity that is derived from the base type of Curve by using the Area property. 

If you need to calculate the combined area of more than one object, you can keep a running total as you add or use the Boolean method on a series of regions to obtain a single region representing the desired area. From this single region you can use the Area property to obtain its area. The calculated area differs according to the type of object you query.
