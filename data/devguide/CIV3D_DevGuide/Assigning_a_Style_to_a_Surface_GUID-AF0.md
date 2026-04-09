<!-- Developer's Guide > API Developer's Guide > Surfaces > Surface Styles > Assigning a Style to a Surface -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-AF0CDCBE-B8F6-4594-AE61-2C513D746C8F.htm -->

# Assigning a Style to a Surface

To assign a style to a surface, set the Surface object’s StyleId property to the ObjectId of a valid SurfaceStyle object. 

This example illustrates creating a new style, changing its settings, and then assigning it to the first surface in the document. Only the plan display settings are changed for brevity, though you would normally also change the model display settings as well. 
    
    
    [CommandMethod("SurfaceStyle")]
    public void SurfaceStyle()
    {
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            // create a new style called 'example style':
            ObjectId styleId = doc.Styles.SurfaceStyles.Add("example style");
    
            // modify the style:
            SurfaceStyle surfaceStyle = styleId.GetObject(OpenMode.ForWrite) as SurfaceStyle;
    
            // display surface triangles
            surfaceStyle.GetDisplayStylePlan(SurfaceDisplayStyleType.Triangles).Visible = true;
            surfaceStyle.GetDisplayStyleModel(SurfaceDisplayStyleType.Triangles).Visible = true;
    
            // display boundaries, exterior only:
            surfaceStyle.GetDisplayStylePlan(SurfaceDisplayStyleType.Boundary).Visible = true;
            surfaceStyle.BoundaryStyle.DisplayExteriorBoundaries = true;
            surfaceStyle.BoundaryStyle.DisplayInteriorBoundaries = false;
    
            // display major contours:
            surfaceStyle.GetDisplayStylePlan(SurfaceDisplayStyleType.MajorContour).Visible = true;
    
            // turn off display of other items:
            surfaceStyle.GetDisplayStylePlan(SurfaceDisplayStyleType.MinorContour).Visible = false;
            surfaceStyle.GetDisplayStylePlan(SurfaceDisplayStyleType.UserContours).Visible = false;
            surfaceStyle.GetDisplayStylePlan(SurfaceDisplayStyleType.Directions).Visible = false;
            surfaceStyle.GetDisplayStylePlan(SurfaceDisplayStyleType.Elevations).Visible = false;                
            surfaceStyle.GetDisplayStylePlan(SurfaceDisplayStyleType.Slopes).Visible = false;                
            surfaceStyle.GetDisplayStylePlan(SurfaceDisplayStyleType.SlopeArrows).Visible = false;                
            surfaceStyle.GetDisplayStylePlan(SurfaceDisplayStyleType.Watersheds).Visible = false;
                    
            // do the same for all model display settings as well
    
    
            // assign the style to the first surface in the document:
            CivSurface surf = doc.GetSurfaceIds()[0].GetObject(OpenMode.ForWrite) as CivSurface;
            surf.StyleId = styleId;
    
            // commit the transaction
            ts.Commit();
        }
    }
