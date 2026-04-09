<!-- Developer's Guide > API Developer's Guide > Alignments > Alignment Style > Alignment Label Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-FADF2DCC-965B-47ED-9FF2-907EF8EA059B.htm -->

# Alignment Label Styles

The style of text labels and graphical markers displayed along an alignment are set by specifying a LabelSet (by name or ObjectID) when the alignment is first created with one of the Alignment::Create() methods, or by assigning the label set object to the CivilDocument.Styles.LabelSetStyles.AlignmentLabelSetStyles  property. The AlignmentLabelSetStyles collection consists of separate sets of styles to be placed at major stations, minor stations, and where the alignment geometry, design speed, or station equations change.

Alignment labels are described in the AlignmentLabelSetStyle collection, which is a collection of AlignmentLabelSetItem objects. Labels at major stations are described by AlignmentLabelSetItem objects with a LabelStyleType property of LabelStyleType.AlignmentMajorStation. Minor station labels are described by AlignmentLabelSetItem objects with a LabelStyleType property of LabelStyleType.AlignmentMinorStation. Each AlignmentLabelSetItem object has a related LabelStyle object (which you can get or set with the LabelStyleId and LabelStyleName properties) and a number of properties describing the limits of the labels and the interval between labels along the alignment. When a new AlignmentLabelSetItem is created for a minor station label (using BaseLabelSetStyle.Add()), it must reference a parent major station label AlignmentLabelSetItem object.

Labels may be placed at the endpoints of each alignment entity. Such labels are controlled through the AlignmentLabelSetItem.GetLabeledAlignmentGeometryPoints() and AlignmentLabelSetItem.GetLabeledAlignmentGeometryPoints() methods. These methods also access labels at each change in alignment design speeds and station equations. The get method returns a Dictionary hash object: Dictionary<AlignmentPointType, bool>, specifiying the location of the geometry point, and the bool indicates whether the point is labeled.

Label text for all label styles at alignment stations is controlled by a LabelStyle object’s Text component, which is set by the LabelStyle.SetComponent() method. The following list of property fields indicates valid values for the Text component:

Valid property fields for LabelStyleComponentType.Text Contents  
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
  
Label styles are described in detail in the chapter 2 section [Label Styles](<GUID-641D7838-292D-43FD-AA50-140B7D9B774F.htm>).
