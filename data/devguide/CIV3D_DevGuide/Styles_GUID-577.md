<!-- Developer's Guide > API Developer's Guide > Getting Started > Migrating COM code to .NET > Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-5779FEA7-B7D1-4389-8DEA-2C792524E0FF.htm -->

# Styles

In the COM API, styles are held by the root document object. In the .NET API, they are located under CivilDocument.Styles, which is an object of type StylesRoot and contains style objects inherited from StyleBase. Getting and setting style attributes for StyleBase objects requires using a GetDisplayStyle*() method rather than a property. Here’s an example from COM VBA:
    
    
    oAlignmentStyle.ArrowDisplayStyle2d.Visible = False
    oAlignmentStyle.ArrowDisplayStyle3d.Visible = False
    ' Display curves using violet.
    oAlignmentStyle.CurveDisplayStyle2d.color = 200 ' violet
    oAlignmentStyle.CurveDisplayStyle3d.color = 200 ' violet
    oAlignmentStyle.CurveDisplayStyle2d.Visible = True
    oAlignmentStyle.CurveDisplayStyle3d.Visible = True
    

This is the equivalent code in VB.NET:
    
    
    oAlignmentStyle.GetDisplayStyleModel(AlignmentDisplayStyleType.Arrow).Visible = False
    oAlignmentStyle.GetDisplayStylePlan(AlignmentDisplayStyleType.Arrow).Visible = False
    ' Display curves using violet.
    oAlignmentStyle.GetDisplayStyleModel(AlignmentDisplayStyleType.Curve).Color = Autodesk.AutoCAD.Colors.Color.FromRgb(191, 0, 255) ' violet
    oAlignmentStyle.GetDisplayStylePlan(AlignmentDisplayStyleType.Curve).Color = Autodesk.AutoCAD.Colors.Color.FromRgb(191, 0, 255) ' violet
    oAlignmentStyle.GetDisplayStyleModel(AlignmentDisplayStyleType.Curve).Visible = True
    oAlignmentStyle.GetDisplayStylePlan(AlignmentDisplayStyleType.Curve).Visible = True
