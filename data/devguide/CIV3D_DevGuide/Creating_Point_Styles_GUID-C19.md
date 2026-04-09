<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Points in COM > Style > Creating Point Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-C19CE03C-C57F-493C-9AE2-BE2B03977418.htm -->

# Creating Point Styles

A point style is a group of settings that define how a point is drawn. These settings include marker style, marker color and line type, and label color and line type. Point objects can use any of the point styles that are currently stored in the document. Styles are assigned to a point through the point’s AeccPoint.Style property. Existing point styles are stored in the document’s AeccDocument.PointStyles property.

You can also create custom styles and add them to the document’s collection of point styles. First, add a new style to the document’s list of styles using the AeccDocument.PointStyles.Add method. This method returns a new style object that is set with all the properties of the default style. You can then make the changes to the style object you require.

This sample creates a new points style, adjusts the style settings, and the assigns the style to point “Point1”:
    
    
    ' Create the style objects to use.
    Dim oPointStyles As AeccPointStyles
    Dim oPointStyle As AeccPointStyle
     
    Set oPointStyles = oDocument.PointStyles
     
    ' Add the style to the document's collection of point styles.
    Set oPointStyle = oPointStyles.Add("Sample Point Style")
     
    ' This style substitutes the normal point marker
    ' with a dot with a circle around it.
    oPointStyle.MarkerType = aeccUseCustomMarker
    oPointStyle.CustomMarkerStyle = aeccCustomMarkerDot
    oPointStyle.CustomMarkerSuperimposeStyle = _
      aeccCustomMarkerSuperimposeCircle
     
    ' Now set the point to use this style.
    oPoint1.Style = oPointStyle
