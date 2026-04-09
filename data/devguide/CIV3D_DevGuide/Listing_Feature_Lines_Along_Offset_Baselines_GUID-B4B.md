<!-- Developer's Guide > API Developer's Guide > Corridors > Feature Lines > Listing Feature Lines Along Offset Baselines -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-B4BE3092-875A-4D33-800E-228588F45F48.htm -->

# Listing Feature Lines Along Offset Baselines

As there can be many offset baselines in a single main baseline, the list of all feature lines along all offset baselines contains an extra layer. The Baseline.OffsetBaselineFeatureLinesCol property contains a collection of BaselineFeatureLines objects. These BaselineFeatureLines objects not only contain the feature lines just as for the main baseline, but also contain properties identifying which offset baseline each group of feature lines belong to.

This sample shows how to modify the previous sample for feature lines along offset baselines: 
    
    
    // Get all the offset feature lines:
    foreach (BaselineFeatureLines oBaselineFeaturelines in oBaseline.OffsetBaselineFeatureLinesCol)
    {                            
        foreach (FeatureLineCollection oFeatureLineCollection in oBaselineFeaturelines.FeatureLineCollectionMap)
        {
            ed.WriteMessage("Feature Line Collection\n# Lines in collection: {0}\n",
            oFeatureLineCollection.Count);
            foreach (FeatureLine oFeatureLine in oFeatureLineCollection)
            {
                ed.WriteMessage("Feature line code: {0}\n", oFeatureLine.CodeName);
                // print out all point locations on the feature line
                foreach (FeatureLinePoint oFeatureLinePoint in oFeatureLine.FeatureLinePoints)
                {
                    ed.WriteMessage("Point: {0},{1},{2}\n",
                        oFeatureLinePoint.XYZ.X,
                        oFeatureLinePoint.XYZ.Y,
                        oFeatureLinePoint.XYZ.Z);
                }
     
            }
     
        }
    }
    

Each offset baseline and hardcoded offset baseline also has direct access to the feature lines related to itself. The BaselineFeatureLines collection is accessed through the RelatedOffsetBaselineFeatureLines property in both types of offset baselines.
