<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Alignments in COM > Stations > Specifying Design Speeds -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-C0AD79D2-73C2-406B-855E-E8067D5C1AC7.htm -->

# Specifying Design Speeds

You can assign design speeds along the length of an alignment to aid in the future design of a roadway based on the alignment. The collection of speeds along an alignment are contained in the AeccAlignment.DesignSpeeds property. Each item in the collection is an object of type AeccDesignSpeed, which contains a raw station value, a speed to be used from that station on until the next design speed specified or the end of the alignment, and an optional string comment.
    
    
    Dim oDesignSpeed As AeccDesignSpeed
    ' Starting at station 0 + 00.00
    Set oDesignSpeed = oAlignment.DesignSpeeds.Add(0#)
    oDesignSpeed.Value = 45
    oDesignSpeed.Comment = "Straightaway"
     
    ' Starting at station 4 + 30.00
    Set oDesignSpeed = oAlignment.DesignSpeeds.Add(430#)
    oDesignSpeed.Value = 30
    oDesignSpeed.Comment = "Start of curve"
     
    ' Starting at station 14 + 27.131 to the end.
    Set oDesignSpeed = oAlignment.DesignSpeeds.Add(1427.131)
    oDesignSpeed.Value = 35
    oDesignSpeed.Comment = "End of curve"
    ' Make Alignment speed-based
    oAlignment.DesignSpeedBased = True
