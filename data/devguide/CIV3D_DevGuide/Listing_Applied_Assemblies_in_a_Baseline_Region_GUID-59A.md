<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Corridors in COM > Assemblies and Subassemblies > Listing Applied Assemblies in a Baseline Region -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-59A59BAA-1091-4A15-89CC-7990F4011075.htm -->

# Listing Applied Assemblies in a Baseline Region

The collection of all applied assemblies used in a baseline region are contained in the AeccBaselineRegion.AppliedAssemblies property.

The following sample displays information about the construction of an assembly for every assembly in a baseline region:
    
    
    Dim oAppliedAssembly As AeccAppliedAssembly
    For Each oAppliedAssembly In oBaselineRegion.AppliedAssemblies
        Debug.Print "Applied Assembly"
        Dim lCount As Long
        lCount = oAppliedAssembly.GetShapes().Count
        Debug.Print "  Num Shapes: " & lCount
        Debug.Print
        lCount = oAppliedAssembly.GetLinks().Count
        Debug.Print "  Num Links: " & lCount
        lCount = oAppliedAssembly.GetPoints().Count
        Debug.Print "  Num Points: " & lCount
    Next
    

An AeccAppliedAssembly object does not contain its baseline station position. Instead, each calculated point contains a method for determining its position with a baseline station, offset, and elevation called AeccCalculatedPoint.GetStationOffsetElevationToBaseline. Each calculated shape contains a collection of all links that form the shape, and each calculated link contains a collection of all points that define the link. Finally, each shape, link, and point contain an array of all corridor codes that apply to that element.

This sample retrieves all calculated point in an applied assembly and prints their locations:
    
    
    Dim oPoint As AeccCalculatedPoint
    For Each oPoint In oAppliedAssembly.GetPoints()
       Dim vPos As Variant
       vPos = oPoint.GetStationOffsetElevationToBaseline()
       Debug.Print "Position:  Station = " & vPos(0) & _
         " Offset = " & vPos(1) & " Elevation = " & vPos(2)
    Next
