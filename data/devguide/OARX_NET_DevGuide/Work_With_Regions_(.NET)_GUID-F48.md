<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Create Objects (.NET) > Work With Regions (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-F4895976-6867-4AFC-A96F-BF522ACE5AC7.htm -->

# Work With Regions (.NET)

Regions are two-dimensional enclosed areas you create from closed shapes called loops. A loop is a closed boundary that is made up of straight and curved objects which do not intersect themselves. Loops can be combinations of lines, lightweight polylines, 2D and 3D polylines, circles, arcs, ellipses, elliptical arcs, splines, 3D faces, traces, and solids. 

The objects that make up the loops must either be closed or form closed areas by sharing endpoints with other objects. They must also be coplanar (on the same plane). The loops that make up a region must be defined as an array of objects.
