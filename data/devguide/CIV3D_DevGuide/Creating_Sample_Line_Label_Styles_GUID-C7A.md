<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Sections in COM > Sample Lines > Creating Sample Line Label Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-C7A2534B-0BE3-4032-BC39-989358A50C6C.htm -->

# Creating Sample Line Label Styles

The style of sample line text labels, lines, and marks are controlled by an AeccLabelStyle object. The style can be set through the AeccSampleLine.LabelStyle property or by passing an AeccLabelStyle object when using the AeccSampleLineGroups.Add method. All labels styles for sample lines are stored in the AeccDocument.SampleLineLabelStyles collection. See the Root Objects chapter for more detailed information about the AeccLabelStyle class. 

Text labels for sample lines can use any of the following property fields:

Valid property fields for AeccLabelStyleTextComponent.Contents  
---  
<[Sample Line Name(CP)]>  
<[Sample Line Number(Sn)]>  
<[Left Swath Width(Uft|P3|RN|AP|Sn|OF)]>  
<[Right Swath Width(Uft|P3|RN|AP|Sn|OF)]>  
<[Distance from Previous Sample Line(Uft|P3|RN|AP|Sn|OF)]>  
<[Sample Line Parent Alignment Name(CP)]>  
<[Sample Line Group(CP)]>  
<[Sample Line Station Value(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[Sample Line Raw Station(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
  
Label styles are described in detail in the Chapter 1 section [Label Styles](<GUID-CB057BA7-7EAE-4915-9B90-8451776C1407.htm>).
