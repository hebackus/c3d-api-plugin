<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Corridors in COM > Feature Lines > Listing Feature Lines Along a Baseline -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-53436D33-3C3A-4E30-9CD7-0F24EA43B0FF.htm -->

# Listing Feature Lines Along a Baseline

The set of all feature lines along a main baseline are held in the AeccBaseline.MainBaselineFeatureLines property, an object of type AeccBaselineFeatureLines. This object contains information about all the feature lines, such as a list of all codes used. Its AeccBaselineFeatureLines.FeatureLinesCol property is a collection of collections of feature lines. Each feature line (an object of type AeccFeatureLine) contains the code string used to create the feature line and a collection of all feature line points.

This sample lists all the feature line collections and feature lines along the main baseline. It also lists the code and every point location for each feature line.
    
    
    Dim oBaselineFeatureLines As AeccBaselineFeatureLines
    Set oBaselineFeatureLines = oBaseline.MainBaselineFeatureLines
     
    Dim oFeatureLinesCol As AeccFeatureLinesCol
    Set oFeatureLinesCol = oBaselineFeatureLines.FeatureLinesCol
    Debug.Print "# line collections:" & oFeatureLinesCol.Count
     
    Dim oFeatureLines As AeccFeatureLines
    For Each oFeatureLines In oFeatureLinesCol
       Debug.Print "Feature Line collection"
       Debug.Print "# lines in collection: " & oFeatureLines.Count
       Dim oFeatureLine As AeccFeatureLine
       For Each oFeatureLine In oFeatureLines
          Debug.Print
          Debug.Print "Feature Line code: " & oFeatureLine.CodeName
     
          ' Print out all point locations of the
          ' feature line.
          Dim oFeatureLinePoint As AeccFeatureLinePoint
          For Each oFeatureLinePoint In oFeatureLine.FeatureLinePoints
             Dim X As Double
             Dim Y As Double
             Dim Z As Double
             X = oFeatureLinePoint.XYZ(0)
             Y = oFeatureLinePoint.XYZ(1)
             Z = oFeatureLinePoint.XYZ(2)
             Debug.Print "Point: " & X & ", " & Y & ", " & Z
          Next ' Points in a feature line
       Next ' Feature lines
    Next ' Collections of feature lines
