<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Data Bands in COM > Defining a Data Band Style > Data Band Concepts -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-A750A904-7408-48FF-8CF7-1E54D76C4846.htm -->

# Data Band Concepts

Data bands are a way to display more information with profile views and section views, including differences between sections, profile geometry, and superelevation along an alignment. Data bands consist of one or more strips at the top or bottom of each graph with tick marks, graphics, and labels describing particular features of the subject of the graph. 

The bottom of a profile view with four data bands 

A band is described by an object derived from the AeccBandStyle type: AeccBandSegmentDataStyle, AeccBandProfileDataStyle, AeccBandHorizontalGeometryStyle, AeccBandVerticalGeometryStyle, or AeccBandSuperElevationStyle. All such styles in the document are stored in collections depending on the band type:

Band Style Type | Collection of Band Style Objects  
---|---  
AeccBandSegmentDataStyle | AeccDocument.SectionViewBandStyles. SectionDataBandStyles  
AeccBandProfileDataStyle | AeccDocument.ProfileViewBandStyles. ProfileDataBandStyles  
AeccBandHorizontalGeometryStyle | AeccDocument.ProfileViewBandStyles. HorizontalGeometryBandStyles  
AeccBandVerticalGeometryStyle | AeccDocument.ProfileViewBandStyles. VerticalGeometryBandStyles  
AeccBandSuperElevationStyle | AeccDocument.ProfileViewBandStyles. SuperElevationBandStyles  
  
Each collection has an Add method for creating new band styles.

The location of information displayed in the band depends on which band style objects are visible. Each data location (for example, at profile stations or at horizontal geometry points) consists of multiple style elements (text labels, tick marks, lines, or blocks). Different band styles have different locations where information can be displayed, and will display information with different graphical effects.

Each information location is managed by a set of three style objects that control:

  * The visual style of the text label (properties ending with “LabelDisplayStylePlan“, objects of type AeccDisplayStyle).
  * The contents and nature of the text , tick marks, lines, and blocks (properties ending with “LabelStyle“, objects of type AeccBandLabelStyle).
  * The visual style of the tick mark (properties ending with “TickDisplayStylePlan“, objects of type AeccDisplayStyle).

The display styles have priority over the label style when setting the color or linetype. 

Note:

If either the display style or the label style element is not set to be visible, then the data element is not visible.

A title can be displayed on the left side of each band. The style of the text and box around the text are controlled by the AeccBandStyle.TitleBoxTextDisplayStylePlan and AeccBandStyle.TitleBoxDisplayStylePlan properties, both object of type AeccDisplayStyle. The text of the title and its location are controlled through the AeccBandStyle.TitleStyle property, an object of type AeccBandTitleStyle. The AeccBandTitleStyle.Text property contains the actual string to be displayed, which may include property fields from the following list: 

Valid property fields for AeccBandTitleStyle.Text  
---  
<[Parent Alignment(CP)]>  
<[Section1 Name(CP)]>  
<[Section1 Type(CP)]>  
<[Section1 Left Length(Uft|P3|RN|AP|Sn|OF)]>  
<[Section1 Right Length(Uft|P3|RN|AP|Sn|OF)]>  
<[Section2 Name(CP)]>  
<[Section2 Type(CP)]>  
<[Section2 Left Length(Uft|P3|RN|AP|Sn|OF)]>  
<[Section2 Right Length(Uft|P3|RN|AP|Sn|OF)]>  
<[Sample Line Name(CP)]>  
<[Sample Line Group(CP)]>  
<[Sample Line Number(Sn)]>  
<[Profile1 Name(CP)]>  
<[Profile2 Name(CP)]>  
  
The following code sets the title for a section view data band showing two sections:
    
    
    oBandSectionDataStyle.TitleStyle.Text = _
      "<[Section1 Name(CP)]> and <[Section1 Name(CP)]>"
