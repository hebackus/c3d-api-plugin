<!-- Developer's Guide > API Developer's Guide > Creating Custom Subassemblies Using .NET > Structure of Subassembly Programs > The Corridor State Object -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-CC3A54A2-7749-4BAA-B7F7-2172C5D3EE41.htm -->

# The Corridor State Object

A reference to an object of type CorridorState is passed to each of the SATemplate methods you override. The CorridorState object is the primary interface between the custom subassembly and the collection of points, links, and shapes of the current assembly which the subassembly is to connect to. It provides references to the current alignment, profile, station, offset, elevation, and style, which may affect the appearance of the subassembly. It also includes several parameter buckets used for collecting parameters of types boolean, long, double, string, alignment, profile, surface, and point. Each parameter is defined by a literal name and a value.

The CorridorState methods provide useful calculation functions for corridor design. These include the following:

IntersectAlignment | Finds the intersection of a cross-sectional line with an offset alignment.  
---|---  
IntersectLink | Finds the intersection of a cross-sectional line with a link on the assembly.  
IntersectSurface | Finds the intersection of a cross-sectional line with a surface.  
IsAboveSurface | Determines if a subassembly point is above or below a surface.  
SampleSection | Constructs a set of cross section links from a surface.  
SoeToXyz XyzToSoe | Converts between station, offset, elevation coordinates and X,Y,Z coordinates.
