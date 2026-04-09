<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Alignments in COM > Stations > Superelevation -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-89ACE346-7D8F-4F13-B3AC-A4241D46B5C0.htm -->

# Superelevation

Another setting that can be applied to certain stations of an alignment is the superelevation, used to adjust the angle of roadway section components for corridors based on the alignment. The inside and outside shoulders and road surfaces can be adjusted for both the left and right sides of the road. The collection of all superelevation information for an alignment is stored in the AeccAlignment.SuperelevationData property. Note that, unlike most Autodesk Civil 3D API collections, the Add method does not return a new default entity but instead passes a reference to the new object through the second parameter. An individual superelevation data element (type AeccSuperelevationDataElement) can be accessed through the AeccAlignment.SuperelevationAtStation method. 

This code creates a new superelevation data element at station 11+00.00 and sets the properties of that element:
    
    
    Dim oSuperElevationData As AeccSuperElevationData
    Dim oSuperElevationElem As AeccSuperElevationDataElem
     
    ' Create an element at station 11+00.0.  A new default
    ' superelevation data element is assigned to our
    ' oSuperElevationElem variable.
    Set oSuperElevationData = oAlignment.SuperelevationData
    oSuperElevationData.Add 1100, oSuperElevationElem
     
    oSuperElevationElem.SegmentCrossSlope _
       (aeccSuperLeftOutShoulderCrossSlope) = 0.05
    oSuperElevationElem.SegmentCrossSlope _
       (aeccSuperLeftOutLaneCrossSlope) = 0.02
    oSuperElevationElem.SegmentCrossSlope _
       (aeccSuperLeftInLaneCrossSlope) = 0.01
    oSuperElevationElem.SegmentCrossSlope _
       (aeccSuperLeftInShoulderCrossSlope) = 0.03
    oSuperElevationElem.SegmentCrossSlope _
       (aeccSuperRightInShoulderCrossSlope) = 0.03
    oSuperElevationElem.SegmentCrossSlope _
       (aeccSuperRightInLaneCrossSlope) = 0.01
    oSuperElevationElem.SegmentCrossSlope _
       (aeccSuperRightOutLaneCrossSlope) = 0.02
    oSuperElevationElem.SegmentCrossSlope _
       (aeccSuperRightOutShoulderCrossSlope) = 0.05
    oSuperElevationElem.TransPointType = aeccSuperManual
    oSuperElevationElem.TransPointDesc = "Manual adjustment"
    oSuperElevationElem.RawStation = 1100
    

Each superelevation data element represents a point in the transition of the roadway cross section. A single transition from normal to full superelevation and back is a _zone_. A collection of data elements representing a single zone can be retrieved by calling the AeccAlignment.SuperelevationZoneAtStation method.

This sample retrieves the data elements that are part of the superelevation zone starting at station 0+00.00, and prints all their descriptions:
    
    
    Set oSuperElevationData = _ 
       oAlignment.SuperelevationZoneAtStation(0)
     
    For Each oSuperElevationElem In oSuperElevationData
        Debug.Print oSuperElevationElem.TransPointDesc
    Next
