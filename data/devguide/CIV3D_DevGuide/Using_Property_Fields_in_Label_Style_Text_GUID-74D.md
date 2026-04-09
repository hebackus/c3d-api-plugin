<!-- Developer's Guide > API Developer's Guide > Root Objects and Common Concepts > Label Styles > Using Property Fields in Label Style Text -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-74D3A5B2-2063-4851-967E-5A67F0ADC832.htm -->

# Using Property Fields in Label Style Text

Text within a label is designated by the LabelStyleTextComponent.Contents property, a PropertyString value. Of course, text labels are most useful if they can provide some sort of information that is unique to each particular item being labeled. This is accomplished by specifying property fields within the string. These property fields are of the form “<[_Property name_(_modifier 1_ |[..] _modifier n_)]>”. Modifier values are optional and can be in any order. Any number of property fields can be combined with normal text in the Contents property. 

In this example, a string component of a label is modified to show design speeds and station values for a point along an alignment:
    
    
    var newTextComponent = ts.GetObject(textCompCol[0], OpenMode.ForWrite) as LabelStyleTextComponent;
    newTextComponent.Text.Contents.Value = "SPD=<[Design Speed(P0|RN|AP|Sn)]>";
    newTextComponent.Text.Contents.Value += "STA=<[Station Value(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>";
    

Valid property fields for each element are listed in the appropriate chapter.
