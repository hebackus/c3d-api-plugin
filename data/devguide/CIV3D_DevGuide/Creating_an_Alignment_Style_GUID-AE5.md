<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Alignments in COM > Alignment Style > Creating an Alignment Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-AE512C92-10A3-4770-82F1-736CF4F975CF.htm -->

# Creating an Alignment Style

A style governs many aspects of how alignments are drawn, including direction arrows and curves, spirals, and lines within an alignment. All alignment styles are contained in the AeccDocument.AlignmentStyles collection. Alignment styles must be added to this collection before being used by an alignment object. A style is normally assigned to an alignment when it is first created, but it can also be assigned to an existing alignment through the AeccAlignment.Style property. 
    
    
    Dim oAlignmentStyle As AeccAlignmentStyle
    Set oAlignmentStyle = oAeccDocument.AlignmentStyles _
      .Add("Sample alignment style")
     
    ' Do not show direction arrows.
    oAlignmentStyle.ArrowDisplayStylePlan.Visible = False 
    oAlignmentStyle.ArrowDisplayStyleModel.Visible = False
    ' Show curves in violet.
    oAlignmentStyle.CurveDisplayStylePlan.color = 200 ' violet
    oAlignmentStyle.CurveDisplayStyleModel.color = 200 ' violet
    ' Show straight sections in blue.
    oAlignmentStyle.LineDisplayStylePlan.color = 160 ' blue
    oAlignmentStyle.LineDisplayStyleModel.color = 160 ' blue
     
    ' Assign the style to an existing alignment.
    oAlignment.Style = oAlignmentStyle.Name
