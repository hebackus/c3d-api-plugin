<!-- Developer's Guide > API Developer's Guide > Corridors > Corridor Slope Patterns > Adding and Modifying Slope Patterns -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-6DC91DA0-6D99-4EC1-99C5-10361E581FFE.htm -->

# Adding and Modifying Slope Patterns

A slope pattern is a pattern that is applied to the area between two Corridor feature lines (typically, between a grading footprint and daylight line) to indicate the direction of slope. A Corridor's collection of SlopePattern objects is held in its SlopePatterns collection. This collection also exposes an Add() method that allows you to add a new SlopePattern defined by two CorridorFeatureLine objects and the ObjectId for a SlopePatternStyle. Once the SlopePattern has been added, its start and end stations can be set. 

In this example, all existing slope patterns are listed, and then a new SlopePattern is added to the corridor, and its stations are set. 
    
    
    // add slope pattern
    CorridorFeatureLine featureLine1 = null;
    CorridorFeatureLine featureLine2 = null;
    string fl1name = "ETW";
    string f2name = "Ditch_Out";
    
    Baseline baseline = corridor.Baselines[0];
    foreach (FeatureLineCollection fl in baseline.MainBaselineFeatureLines.FeatureLineCollectionMap)
    {
        foreach (CorridorFeatureLine cfl in fl)
        {
            if (cfl.CodeName == fl1name)
            {
                featureLine1 = cfl;
                break;
            }
            if (cfl.CodeName == f2name)
            {
                featureLine2 = cfl;
                break;
            }
        }
    }
    
    // get a style for the slope pattern:
    ObjectId slopePatterStyleId = _civilDoc.Styles.SlopePatternStyles["Standard"];
    
    CorridorSlopePattern pattern = corridor.SlopePatterns.Add(featureLine1, featureLine2, slopePatterStyleId);
    // set the stations:
    _editor.WriteMessage("First station: {0} \nEnd station: {1}\n", baseline.StartStation, baseline.EndStation);
    pattern.StartStation = baseline.StartStation;
    pattern.EndStation = baseline.EndStation;
