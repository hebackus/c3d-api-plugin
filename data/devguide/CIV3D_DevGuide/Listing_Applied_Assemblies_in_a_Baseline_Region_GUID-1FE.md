<!-- Developer's Guide > API Developer's Guide > Corridors > Assemblies and Subassemblies > Listing Applied Assemblies in a Baseline Region -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-1FE5BC25-5F70-4A3A-8F30-9E8DA9D8DBE4.htm -->

# Listing Applied Assemblies in a Baseline Region

The collection of all applied assemblies used in a baseline region are contained in the BaselineRegion.AppliedAssemblies property.

The following sample displays information about the construction of an assembly for every assembly in a baseline region:
    
    
    // List the applied assemblies in the baseline region
    foreach (AppliedAssembly oAppliedAssembly in oBaselineRegion.AppliedAssemblies)
    {
        ed.WriteMessage("Applied Assembly, num shapes: {0}, num links: {1}, num points: {2}\n",
            oAppliedAssembly.Shapes.Count, oAppliedAssembly.Links.Count, oAppliedAssembly.Points.Count);
     
     
    }
    

An AppliedAssembly object does not contain its baseline station position. Instead, each calculated point contains a property for determining its position with a baseline station, offset, and elevation called CalculatedPoint.StationOffsetElevationToBaseline. Each calculated shape contains a collection of all links that form the shape, and each calculated link contains a collection of all points that define the link. Finally, each shape, link, and point contain an array of all corridor codes that apply to that element.

This sample retrieves all calculated points in an applied assembly and prints their locations:
    
    
    foreach (CalculatedPoint oPoint in oAppliedAssembly.Points)
    {
        ed.WriteMessage("Point position: Station: {0}, Offset: {1}, Elevation: {2}\n",
            oPoint.StationOffsetElevationToBaseline.X,
            oPoint.StationOffsetElevationToBaseline.Y,
            oPoint.StationOffsetElevationToBaseline.Z);
     
    }
