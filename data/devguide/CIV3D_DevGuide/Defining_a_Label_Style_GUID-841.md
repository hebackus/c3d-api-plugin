<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Root Objects and Common Concepts in COM > Label Styles > Defining a Label Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-84127585-A2F8-41F0-B76A-AD2E6A8E4EDF.htm -->

# Defining a Label Style

A label style consists of collections of different features of a label. The properties containing these collections are: AeccLabelStyle.BlockComponents for symbols, AeccLabelStyle.DirectionArrowComponents for direction arrows, AeccLabelStyle.LineComponents for lines, AeccLabelStyle.TextComponents for text, and AeccLabelStyle.TickComponents for both major and minor tick marks. Not all of these may have meaning depending on the label style type. For example, adding a tick mark component to a label style meant for a point has no visible effect. Label styles also depend on graphical objects that may or may not be part of the current document. For example, if the style references a block that is not part of the current document, then the specified block or tick components are not shown.

To add a feature to a label style, add a new component to the corresponding collection. Then set the properties of that component to the appropriate values. Always make sure to set the Visible property to True.
    
    
    ' Add a line to the collection of lines in our label style.
    Dim oLabelStyleLineComponent As AeccLabelStyleLineComponent
    Set oLabelStyleLineComponent = oLabelStyle.LineComponents _
      .Add("New Line")
     
    ' Now the line can be changed to suit our purpose.
    oLabelStyleLineComponent.Visibility = True
    oLabelStyleLineComponent.color = 40 ' orange-yellow
    oLabelStyleLineComponent.Angle = 2.094 ' radians, = 120 deg
    ' Negative lengths are allowed. They mean the line
    ' is drawn in the opposite direction of the angle
    ' specified.
    oLabelStyleLineComponent.Length = -0.015
    oLabelStyleLineComponent.StartPointXOffset = 0.005
    oLabelStyleLineComponent.StartPointYOffset = -0.005
    

When first created, the label style object is set according to the ambient settings. Because of this, a new label style object may already contain features. If you are creating a new label style object, be sure to check for such existing features or your style might contain unintended elements.
    
    
    ' Check to see if text components already exist in the
    ' collection. If any do, just modify the first text
    ' feature instead of making a new one.
    Dim oLabelStyleTextComponent As AeccLabelStyleTextComponent
    If (oLabelStyle.TextComponents.Count > 0) Then
        Set oLabelStyleTextComponent = oLabelStyle _
          .TextComponents.Item(0)
    Else
        Set oLabelStyleTextComponent = oLabelStyle _
          .TextComponents.Add("New Text")
    End If
    

The ambient settings also define which units are used. If you are creating an application designed to work with different drawings, you should take ambient settings into account or labels may demonstrate unexpected behavior in each document.
