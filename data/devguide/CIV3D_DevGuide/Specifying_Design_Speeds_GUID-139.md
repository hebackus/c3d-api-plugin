<!-- Developer's Guide > API Developer's Guide > Alignments > Stations > Specifying Design Speeds -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-139B5F29-C442-465D-BC4E-C31A58086939.htm -->

# Specifying Design Speeds

You can assign design speeds along the length of an alignment to aid in the future design of a roadway based on the alignment. The collection of speeds along an alignment are contained in the Alignment::DesignSpeeds property. Each item in the collection is an object of type DesignSpeed, which contains a raw station value, a speed to be used from that station on until the next specified design speed or the end of the alignment, the design speed number, and an optional string comment.
    
    
    // Starting at station 0 + 00.00
    DesignSpeed myDesignSpeed = myAlignment.DesignSpeeds.Add(0, 45);
    myDesignSpeed.Comment = "Straigtaway";
    // Starting at station 4 + 30.00
    myDesignSpeed = myAlignment.DesignSpeeds.Add(430, 30);
    myDesignSpeed.Comment = "Start of curve";
    // Starting at station 14 + 27.131 to the end
    myDesignSpeed = myAlignment.DesignSpeeds.Add(1427.131, 35);
    myDesignSpeed.Comment = "End of curve";
    // make alignment design speed-based:
    myAlignment.UseDesignSpeed = true;
