<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Pipe Networks in COM > Interference Checks > Interference Check Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-EC18C08D-8BFB-4B6A-9154-73CD4E866CFA.htm -->

# Interference Check Styles

Either a symbol or a model of the actual intersection region can be drawn at each interference location. The display of these intersections is controlled by an AeccInterferenceStyle object. The collection of all interference style objects in the document are stored in the AeccPipeDocument.InterferenceStyles collection. Set the style of an interference object by assigning an AeccInterferenceStyle object to the AeccInterference.Style property:
    
    
    Set oInterference.Style = oInterferenceStyle
    

There are three different styles of interference displays you can chose from. First, you can display a 3D model of the intersection region. This is done by setting the ModelOptions style property to aeccTrueSolidInterference. The ModelSolidDisplayStyle2D property, an object of type AeccDisplayStyle, controls the visible appearance of the model such as color and line types. Make sure the ModelSolidDisplayStyle2D.Visible property is set to True.

Another possibility is to draw a 3D sphere at the location of intersection. This is done by setting the ModelOptions style property to aeccSphereInterference. If the InterferenceSizeType property is set to aeccSolidExtents, then the sphere is automatically sized to just circumscribe the region of intersection (that is, it is the smallest sphere that still fits the model of the intersection region). You can set the size of the sphere by setting the InterferenceSizeType property to aeccUserDefined, setting the ModelSizeOptions property to use either absolute units or drawing units, and setting the corresponding AbsoluteModelSize or DrawingScaleModelSize property to the desired value. Again, the ModelSolidDisplayStyle2D property controls the visual features such as color and line type. Make sure the ModelSolidDisplayStyle2D.Visible property is set to True.

The third option is to place a symbol at the location of intersection. Set the PlanSymbolDisplayStyle2D.Visible style property to True to make symbols visible. The style property MarkerStyle, an object of type AeccMarkerStyle, controls all aspects of how the symbol is drawn.

This sample creates a new interference style object that displays an X symbol with a superimposed circle at points of intersection:
    
    
    ' Create a new interference style object.
    Dim oInterferenceStyle As AeccInterferenceStyle
    Set oInterferenceStyle = oPipeDocument.InterferenceStyles _
      .Add("Interference style 01")
     
    ' Draw a symbol of a violet X with circle with a specified
    ' drawing size at the points of intersection.
    oInterferenceStyle.PlanSymbolDisplayStyle2D.Visible = True
    With oInterferenceStyle.MarkerStyle
        .MarkerType = aeccUseCustomMarker
        .CustomMarkerStyle = aeccCustomMarkerX
        .CustomMarkerSuperimposeStyle = _
          aeccCustomMarkerSuperimposeCircle
        .MarkerDisplayStylePlan.color = 200 ' violet
        .MarkerDisplayStylePlan.Visible = True
        .MarkerSizeType = aeccAbsoluteUnits
        .MarkerSize = 5.5
    End With
    ' Hide any model display at intersection points.
    oInterferenceStyle.ModelSolidDisplayStyle2D.Visible = False
