<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Surface Style > Changing a Surface Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-0FDE932E-1CD3-42C0-9619-5098BE9EBD85.htm -->

# Changing a Surface Style

A surface style consists of different objects governing the appearance of boundaries, contours, direction analysis, elevation analysis, grids, points, slope arrows, triangles, and watershed analysis. Usually a single style only displays some of these objects. When initially created, a style is set according to the document’s ambient settings and may show some unwanted style elements. Always set the visibility properties of all style elements to ensure the style behaves as you expect. 
    
    
    ' Change the style so that it displays surface triangles,
    ' major contour lines, and any boundaries along the outside
    ' edge, but nothing else.
    oSurfaceStyle.TriangleStyle.DisplayStylePlan.Visible = True
    oSurfaceStyle.BoundaryStyle.DisplayExteriorBoundaries = True
    oSurfaceStyle.BoundaryStyle.DisplayStylePlan.Visible = True
    oSurfaceStyle.ContourStyle.MajorContourDisplayStylePlan _
      .Visible = True
     
    oSurfaceStyle.PointStyle.DisplayStylePlan.Visible = False
    oSurfaceStyle.BoundaryStyle.DisplayInteriorBoundaries = False
    oSurfaceStyle.ContourStyle.MinorContourDisplayStylePlan _
      .Visible = False
    oSurfaceStyle.ContourStyle.UserContourDisplayStylePlan _
      .Visible = False
    oSurfaceStyle.GridStyle.DisplayStylePlan.Visible = False
    oSurfaceStyle.DirectionStyle.DisplayStylePlan.Visible = False
    oSurfaceStyle.ElevationStyle.DisplayStylePlan.Visible = False
    oSurfaceStyle.SlopeStyle.DisplayStylePlan.Visible = False
    oSurfaceStyle.SlopeArrowStyle.DisplayStylePlan.Visible = False
    oSurfaceStyle.WatershedStyle.DisplayStylePlan.Visible = False
     
    ' This must be repeated for all Model display styles as well.
