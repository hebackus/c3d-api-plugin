<!-- Developer's Guide > API Developer's Guide > Corridors > Baselines > Listing Offset Baselines -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-7F156736-BAA5-4513-AB3A-7735DEE8E817.htm -->

# Listing Offset Baselines

Within a baseline region, it is possible to have secondary baselines that are offset from the main baseline. The collection of these offset baselines are contained in the BaselineRegion.OffsetBaselines property. The collection contains two kinds of baselines derived from the BaseBaseline class. One is the hardcoded offset baseline (an instances of the HardcodedOffsetBaseline class) which is a constant distance from the main baseline for the entire length of the offset baseline. The other is the offset baseline (an instance of the OffsetBaseline class), which is a variable distance from the main baseline.

Note:

The Autodesk Civil 3D .NET API does not include methods for creating new offset baselines or hardcoded offset baselines.

This code examines each offset baseline within a baseline region:
    
    
    foreach (BaseBaseline ob in oBaselineRegion.OffsetBaselines)
    {
        ed.WriteMessage("Offset baseline: \n");
        switch (ob.BaselineType)
        {
            case CorridorBaselineType.OffsetBaseline:
                OffsetBaseline offb = (OffsetBaseline)ob;
                ed.WriteMessage("Offset baseline, station {0} to {1}\n",
                    offb.StartStationOnMainBaseline, offb.EndStationOnMainBaseline);
                ed.WriteMessage(" is offset by: {0} horizontal and {1} vertical at start\n",
                    offb.GetOffsetElevationFromMainBaselineStation(offb.StartStationOnMainBaseline).X,
                    offb.GetOffsetElevationFromMainBaselineStation(offb.StartStationOnMainBaseline).Y);
                ed.WriteMessage(" is offset by: {0} horizontal and {1} vertical at end\n",
                    offb.GetOffsetElevationFromMainBaselineStation(offb.EndStationOnMainBaseline).X,
                    offb.GetOffsetElevationFromMainBaselineStation(offb.EndStationOnMainBaseline).Y);
     
                break;
     
            case CorridorBaselineType.HardcodedOffsetBaseline:
                HardcodedOffsetBaseline hob = (HardcodedOffsetBaseline)ob;
                ed.WriteMessage("Hardcoded offset baseline {0} \n",
                    hob.Name);
                ed.WriteMessage(" is offset by: {0} horizontal and {1} vertical\n",
                    hob.OffsetElevationFromMainBaseline.X,
                    hob.OffsetElevationFromMainBaseline.Y);
                break;
     
     
     
            default:
                break;
        }
    }
