<!-- Developer's Guide > API Developer's Guide > Surfaces -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-84BF7EAC-6DF4-447E-A0DB-82C03EA2F584.htm -->

# Surfaces

This chapter covers Civil 3D Surface objects, and how to work with them using the Autodesk Civil 3D .NET API. 

There are four classes of surface in Civil 3D: 

  * TinSurface
  * GridSurface
  * TinVolumeSurface
  * GridVolumeSurface

The first two represent a single layer of terrain, while the second two represent a volume between two layers. All four derive from a generic Surface object, which exposes the common methods and properties shared by all surfaces.
