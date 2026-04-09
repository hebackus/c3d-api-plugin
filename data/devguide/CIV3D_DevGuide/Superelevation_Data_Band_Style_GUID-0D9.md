<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Data Bands in COM > Defining a Data Band Style > Superelevation Data Band Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-0D900959-1535-418A-B1F5-BF9FEB446F4F.htm -->

# Superelevation Data Band Style

An AeccBandProfileDataStyle data band displays information related to the alignment superelevation. It can display slopes of superelevation elements as lines, the distance above or below the centerline representing the amount of slope. The superelevation elements that can be represented this way are:

  * Left inside pavement
  * Left inside shoulder
  * Left outside pavement
  * Left outside shoulder
  * Right inside pavement
  * Right inside shoulder
  * Right outside pavement
  * Right outside shoulder

You can also display a reference line through the center of the data band to help users interpret the element lines.

The data band can also display tick marks and text labels at points of change in the superelevation of the alignment. The following can be marked on the data band:

  * Full superelevation
  * Level crown
  * Normal crown
  * Reverse crown
  * Shoulder break over
  * Transition segment

The label styles for text labels can use any of the following property fields: 

Valid property fields for use with AeccBandLabelStyle text components  
---  
<[Station Value(Uft|FS|P2|RN|AP|Sn|TP|B2|EN|W0|OF)]>  
<[Superelevation critical point text(CP)]>  
<[Cross slope - Left outside pavement(FP|P2|RN|AP|Sn|OF)]>  
<[Cross slope - Left inside pavement(FP|P2|RN|AP|Sn|OF)]>  
<[Cross slope - Right outside pavement(FP|P2|RN|AP|Sn|OF)]>  
<[Cross slope - Right inside pavement(FP|P2|RN|AP|Sn|OF)]>  
<[Cross slope - Left outside shoulder(FP|P2|RN|AP|Sn|OF)]>  
<[Cross slope - Left inside shoulder(FP|P2|RN|AP|Sn|OF)]>  
<[Cross slope - Right outside shoulder(FP|P2|RN|AP|Sn|OF)]>  
<[Cross slope - Right inside shoulder(FP|P2|RN|AP|Sn|OF)]>  
  
This sample demonstrates the creation of a data band style displaying the slopes of the outside shoulders - the right shoulder in yellow and the left in blue. A gray reference line is also added.
    
    
    Dim oBandSuperElevationStyle As AeccBandSuperElevationStyle
    Set oBandSuperElevationStyle = oDocument.ProfileViewBandStyles _
      .SuperElevationBandStyles.Add("Superelevation Band")
     
     
    With oBandSuperElevationStyle
       ' Add graphical display of the slope of the left and right
       ' outside shoulders.  If the line is above the centerline, 
       ' then the slope is positive.
       .LeftOutsideShoulderLineDisplayStylePlan.Visible = True
       .LeftOutsideShoulderLineDisplayStylePlan.color = 151
       ' Color 151 = pale blue
       .RightOutsideShoulderLineDisplayStylePlan.Visible = True
       .RightOutsideShoulderLineDisplayStylePlan.color = 51
       ' Color 51 = pale yellow
     
       ' Add a reference line through the center of the data band.
       .ReferenceLineDisplayStylePlan.Visible = True
       .ReferenceLineDisplayStylePlan.color = 252 ' gray
     
       ' Modify how the title is displayed.
       .TitleBoxDisplayStylePlan.color = 10 ' red
       .TitleBoxDisplayStylePlan.Linetype = "DOT"
       .TitleBoxDisplayStylePlan.Visible = True
       .TitleBoxTextDisplayStylePlan.color = 80 ' green
       .TitleBoxTextDisplayStylePlan.Visible = True
       .TitleStyle.Text = "Profile Geometry"
       .TitleStyle.TextHeight = 0.0125
       .TitleStyle.TextBoxWidth = 0.21
     
       ' Hide the rest of the information locations and
       ' graphical displays.
       .FullSuperLabelDisplayStylePlan.Visible = False
       .FullSuperTickDisplayStylePlan.Visible = False
       .LeftInsidePavementLineDisplayStylePlan.Visible = False
       .LeftInsideShoulderLineDisplayStylePlan.Visible = False
       .LeftOutsidePavementLineDisplayStylePlan.Visible = False
       .LevelCrownLabelDisplayStylePlan.Visible = False
       .LevelCrownTickDisplayStylePlan.Visible = False
       .NormalCrownLabelDisplayStylePlan.Visible = False
       .NormalCrownTickDisplayStylePlan.Visible = False
       .ReverseCrownLabelDisplayStylePlan.Visible = False
       .ReverseCrownTickDisplayStylePlan.Visible = False
       .RightInsidePavementLineDisplayStylePlan.Visible = False
       .RightInsideShoulderLineDisplayStylePlan.Visible = False
       .RightOutsidePavementLineDisplayStylePlan.Visible = False
       .ShoulderBreakOverLabelDisplayStylePlan.Visible = False
       .ShoulderBreakOverTickDisplayStylePlan.Visible = False
       .TransitionSegmentLabelDisplayStylePlan.Visible = False
    End With
    

This style produces a data band that looks like this:
