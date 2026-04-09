<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Performing Surface Analysis > Creating an Elevation Analysis -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-CB3E1FCB-4796-4796-A624-B2DEB5DCEFDD.htm -->

# Creating an Elevation Analysis

An elevation analysis creates a 2-dimensional projection of a surface and then add bands of color indicating ranges of altitude. The analysis is managed by an object of type AeccSurfaceAnalysisElevation, located in the AeccSurface.SurfaceAnalysis.ElevationAnalysis property. This object contains a method for creating elevation regions and a read-only collection containing these regions. The method, CalculateElevationRegions, creates a series of contiguous regions each representing a portion of the surface’s total elevation. Each time it is called it discards all existing elevation regions for the surface and creates a new collection of regions. The collection, ElevationRegions, lets you modify the color, minimum elevation, and maximum elevation of each region. Always check the number of regions through the AeccSurfaceAnalysisElevation.ElevationRegions.Count property as CalculateElevationRegions may create fewer regions than specified by the first parameter.

CalculateElevationRegions creates regions according to the statistical method specified in the AeccSurfaceStyle.ElevationStyle.GroupValuesBy property. The elevation style object also contains other means of modifying how elevation analyses are made, such as using one of the preset color schemes.

This sample creates an elevation analysis for a surface using shades of green:
    
    
    Dim oSurfaceAnalysisElevation As AeccSurfaceAnalysisElevation
    Set oSurfaceAnalysisElevation = oSurface.SurfaceAnalysis _
      .ElevationAnalysis
    Dim oElevationRegions As AeccElevationRegions
    Set oElevationRegions = oSurfaceAnalysisElevation _
      .CalculateElevationRegions(6, False)
    ' See exactly how many regions were created.
    Debug.Print oSurfaceAnalysisElevation.ElevationRegions.Count
     
    oElevationRegions.Item(0).Color = 80 ' bright green
    oElevationRegions.Item(1).Color = 82
    oElevationRegions.Item(2).Color = 84
    oElevationRegions.Item(3).Color = 86
    oElevationRegions.Item(4).Color = 88 ' dark green
     
    ' Adjust the range of one of the regions.
    oElevationRegions.Item(2).MaximumElevation = _
      oElevationRegions.Item(2).MaximumElevation - 5
    

Many elevation analysis features can be modified through the surface style - see the [Surface Style](<GUID-41D881E2-68C2-407B-A88E-6FE35E84FF29.htm>) section. For example, you can choose from among a number of pre-set color schemes.
