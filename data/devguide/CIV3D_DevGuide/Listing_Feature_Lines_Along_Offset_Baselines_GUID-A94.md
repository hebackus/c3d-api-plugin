<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Corridors in COM > Feature Lines > Listing Feature Lines Along Offset Baselines -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-A947A53D-3513-4C53-B4AE-F220C5B9F38A.htm -->

# Listing Feature Lines Along Offset Baselines

As there can be many offset baselines in a single main baseline, the list of all feature lines along all offset baselines contains an extra layer. The AeccBaseline.OffsetBaselineFeatureLinesCol property contains a collection of AeccBaselineFeatureLines objects. These AeccBaselineFeatureLines objects not only contain the feature lines just as for the main baseline, but also contain properties identifying which offset baseline each group of feature lines belong to.

This sample shows how to modify the previous sample for feature lines along offset baselines: 
    
    
    Dim oBFeatureLinesCol As AeccBaselineFeatureLinesCol
    Set oBFeatureLinesCol = oBaseline.OffsetBaselineFeatureLinesCol
     
    Dim oBaselineFeatureLines As AeccBaselineFeatureLines
    ' Loop through the groups of collections, one group for each
    ' offset baseline.
    For Each oBaselineFeatureLines In oBFeatureLinesCol
     
       Dim oFeatureLinesCol As AeccFeatureLinesCol
       Set oFeatureLinesCol = oBaselineFeatureLines.FeatureLinesCol
       Debug.Print "# line collections:" & oFeatureLinesCol.Count
     
       ' [...]
       ' This section is the same as the previous topic.
     
    Next ' Groups of collections of feature lines
    

Each offset baseline and hardcoded offset baseline also has direct access to the feature lines related to itself. The AeccBaselineFeatureLines collection is accessed through the RelatedOffsetBaselineFeatureLines property in both types of offset baselines.
