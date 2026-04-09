<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Pipe Networks in COM > Pipes > Creating Pipe Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-756DBB67-0893-4432-8D84-5A2C88BB39BB.htm -->

# Creating Pipe Styles

A pipe style controls the visual appearance of pipes in a document. All pipe style objects in a document are stored in the AeccPipeDocument.PipeStyles collection. Pipe styles have four display methods and three hatch methods for controlling general appearance attributes and three properties for controlling display attributes that are specific to pipes. The methods DisplayStyleModel|Profile|Section|Plan, and HatchStylePlan|Profile|Section all take a parameter describing the feature being modified, and return a reference to the AeccDisplayStyle or AeccHatchDisplayStyle object controlling common display attributes, such as line styles and color. The properties PlanOption and ProfileOption set the size of the inner wall, outer wall, and end lines according to either the physical properties of the pipe, a custom sizes using drawing units, or a certain percentage of its previous drawing size. The HatchOption property sets the area of the pipe covered by any hatching used. A pipe object is given a style by assigning the AeccPipe.Style property to a AeccPipeStyle object.

This sample creates a new pipe style object, sets some of its properties, and assigns it to a pipe object:
    
    
    ' Create a new pipe style object.
    Dim oPipeStyle As AeccPipeStyle
    Set oPipeStyle = oPipeDocument.PipeStyles.Add("Pipe Style 01")
    With oPipeStyle.PlanOption
        ' Set the display size of the pipes in plan view, using
        ' absolute drawing units for the inside, outside, and
        ' ends of each pipe.
        .InnerDiameter = 2.1
        .OuterDiameter = 2.4
        .EndLineSize = 2.1
     
        ' Indicate that we will use our own measurements for
        ' the inside and outside of the pipe, and not base
        ' the drawing on the actual physical measurements of
        ' the pipe.
        .WallSizeType = aeccUserDefinedWallSize
     
        ' Indicate what kind of custom sizing to use.
        .WallSizeOptions = aeccPipeUseAbsoluteUnits
    End With
     
    ' Modify the colors of pipes using this style when shown in
    ' plan view.
    oPipeStyle.DisplayStylePlan(aeccDispCompPipeOutsideWalls) _
      .Color = 40 ' orange
    oPipeStyle.DisplayStylePlan(aeccDispCompPlanInsideWalls) _
      .Color = 255 ' white
    oPipeStyle.DisplayStylePlan(aeccDispCompPipeEndLine) _
      .color = 255 ' white
     
    ' Set a pipe to use this style.
    Set oPipe.Style = oPipeStyle
