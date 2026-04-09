<!-- Developer's Guide > API Developer's Guide > Corridors > Feature Lines > Listing Feature Lines Along a Baseline -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-8F71F9D1-4035-4FCE-B24D-3F21970B42FA.htm -->

# Listing Feature Lines Along a Baseline

The set of all feature lines along a main baseline are held in the Baseline.MainBaselineFeatureLines property, an object of type BaselineFeatureLines. This object contains information about all the feature lines, such as a list of all codes used. The BaselineFeatureLines.FeatureLinesCol property is a collection of feature line collections. Each feature line (an object of type FeatureLine) contains the code string used to create the feature line and a collection of all feature line points.

This sample lists all the feature line collections and feature lines along the main baseline. It also lists the code and every point location for each feature line.
    
    
    // Get all the feature lines:
    foreach (FeatureLineCollection oFeatureLineCollection in oBaseline.MainBaselineFeatureLines.FeatureLineCollectionMap)
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
                    oFeatureLinePoint.XYZ.Z );
            }
        }
    }
