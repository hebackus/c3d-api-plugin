<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Alignments in COM > Alignment Style > Alignment Label Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-F44D4A68-2942-4C36-87BC-B75DEE10F814.htm -->

# Alignment Label Styles

The style of text labels and graphical markers displayed along an alignment are set by passing an AeccAlignmentLabelSet object when the alignment is first created with the AeccAlignments.Add and AeccAlignments.AddFromPolyline methods or by assigning the label set object to the AeccAlignment.LabelStyle property. The AeccAlignmentLabelSet object consists of separate sets of styles to be placed at major stations, minor stations, and where the alignment geometry, design speed, or station equations change.

Labels at major stations are described in the AeccAlignmentLabelSet.MajorStationLabelSet property, which is a collection of AeccLabelMajorStationSetItem objects. Each AeccLabelMajorStationSetItem object consists of a single AeccLabelStyle object and a number of properties describing the limits of the labels and the interval between labels along the alignment.

Labels at minor stations are described in the AeccAlignmentLabelSet.MinorStationLabelSet property, which is a collection of AeccLabelMinorStationSetItem objects. Each AeccLabelMinorStationSetItem object consists of a single AeccLabelStyle object and a number of properties describing the limits of the labels and the interval between labels along the alignment. When a new AeccLabelMinorStationSetItem is created it must reference a parent AeccLabelMajorStationSetItem object.

Labels may be placed at the endpoints of each alignment entity. Such labels are controlled through the AeccAlignmentLabelSet.GeometryPointLabelSet property, an AeccLabelSet. The label set is a collection of AeccLabelStyle objects. Labels at each change in alignment design speeds and station equations (the AeccAlignmentLabelSet.GeometryPointLabelSet and AeccAlignmentLabelSet.GeometryPointLabelSet properties respectively) are also AeccLabelSet objects. 

All label styles at alignment stations can draw from the following list of property fields:

Valid property fields for AeccLabelStyleTextComponent.Contents  
---  
<[Station Value(Uft|FS|P0|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[Raw Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[Northing(Uft|P4|RN|AP|Sn|OF)]>  
<[Easting(Uft|P4|RN|AP|Sn|OF)]>  
<[Design Speed(P3|RN|AP|Sn|OF)]>  
<[Instantaneous Direction(Udeg|FDMSdSp|MB|P4|RN|DSn|CU|AP|OF)]>  
<[Perpendicular Direction(Udeg|FDMSdSp|MB|P4|RN|DSn|CU|AP|OF)]>  
<[Alignment Name(CP)]>  
<[Alignment Description(CP)]>  
<[Alignment Length(Uft|P3|RN|AP|Sn|OF)]>  
<[Alignment Start Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[Alignment End Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
  
Label styles for minor stations, geometry points, design speeds, and station equations can also use the following property fields:

<[Offset From Major Station(Uft|P3|RN|AP|Sn|OF)]> | Minor stations  
---|---  
<[Geometry Point Text(CP)]> | Geometry points  
<[Geometry Point Entity Before Data(CP)]> | Geometry points  
<[Geometry Point Entity After Data(CP)]> | Geometry points  
<[Design Speed Before(P3|RN|AP|Sn|OF)]> | Design speeds  
<[Station Ahead(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]> | Station equations  
<[Station Back(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]> | Station equations  
<[Increase/Decrease(CP)]> | Station equations  
  
Label styles are described in detail in the chapter 1 section [Label Styles](<GUID-CB057BA7-7EAE-4915-9B90-8451776C1407.htm>).
