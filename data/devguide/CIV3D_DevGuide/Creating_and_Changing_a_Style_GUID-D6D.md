<!-- Developer's Guide > API Developer's Guide > Surfaces > Surface Styles > Creating and Changing a Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-D6D36308-BF32-46F2-81BC-6CC973513621.htm -->

# Creating and Changing a Style

Surface styles are stored in the CivilDocument.Styles.SurfaceStyles collection. To create a new style, call the SurfaceStyleCollection.Add() method with the name of your new style. The new style is created according to the document’s ambient settings. 

In addition to the properties inherited from StyleBase, a surface style consists of different objects governing the appearance of boundaries, contours, direction analysis, elevation analysis, grids, points, slope arrows, triangles, and watershed analysis. Usually a single style only displays some of these objects. When initially created, a style is set according to the document’s ambient settings and may show some unwanted style elements. Always set the visibility properties of all style elements to ensure the style behaves as you expect.
