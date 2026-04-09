<!-- Developer's Guide > API Developer's Guide > Surfaces > Surface Properties -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-53259B3C-D0AB-4BDA-AF3E-F54FEAB9A409.htm -->

# Surface Properties

The Surface object exposes general surface properties, which you can access using the various GetGeneralProperties() methods. Calculating and returning properties is a resource-intensive process, so you are encouraged to call this method once and re-use the returned object, instead of calling the method for each property. TIN and Grid surfaces have type-specific properties (returned by GetTinProperties() and GetGridProperties() respectively). Both Tin and Grid surfaces also implement a GetTerrainProperties() method. 

This example gets general properties for the first surface in the database, and then depending on the surface type, it gets the Tin or Grid surface properties: 
    
    
    [CommandMethod("SurfaceProperties")]
    public void SurfaceProperties()
    {
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            try
            {
                // Get the first surface in a document    
                // "doc" is the CivilApplication.ActiveDocument
                ObjectId surfaceId = doc.GetSurfaceIds()[0];
                CivSurface oSurface = surfaceId.GetObject(OpenMode.ForRead) as CivSurface;
    
                // print out general properties:
                GeneralSurfaceProperties genProps = oSurface.GetGeneralProperties();
                String propsMsg = "\nGeneral Properties for " + oSurface.Name;
                propsMsg += "\n-------------------";
                propsMsg += "\nMin X: " + genProps.MinimumCoordinateX;
                propsMsg += "\nMin Y: " + genProps.MinimumCoordinateY;
                propsMsg += "\nMin Z: " + genProps.MinimumElevation;
                propsMsg += "\nMax X: " + genProps.MaximumCoordinateX;
                propsMsg += "\nMax Y: " + genProps.MaximumCoordinateY;
                propsMsg += "\nMax Z: " + genProps.MaximumElevation;
                propsMsg += "\nMean Elevation: " + genProps.MeanElevation;
                propsMsg += "\nNumber of Points: " + genProps.NumberOfPoints;
                propsMsg += "\n--";
    
                editor.WriteMessage(propsMsg);
    
                // Depending on the surface type, let's look at grid or TIN properties:
    
                if (oSurface is TinSurface)
                {
                    TinSurfaceProperties tinProps = ((TinSurface)oSurface).GetTinProperties();
                    propsMsg = "\nTIN Surface Properties for " + oSurface.Name;
                    propsMsg += "\n-------------------";
                    propsMsg += "\nMin Triangle Area: " + tinProps.MinimumTriangleArea;
                    propsMsg += "\nMin Triangle Length: " + tinProps.MinimumTriangleLength;
                    propsMsg += "\nMax Triangle Area: " + tinProps.MaximumTriangleArea;
                    propsMsg += "\nMax Triangle Length: " + tinProps.MaximumTriangleLength;
                    propsMsg += "\nNumber of Triangles: " + tinProps.NumberOfTriangles;
                    propsMsg += "\n--";
    
                    editor.WriteMessage(propsMsg);
                }
                else if (oSurface is GridSurface)
                {
                    #region GetGridProperties
                    GridSurfaceProperties gridProps = ((GridSurface)oSurface).GetGridProperties();
                    propsMsg = "\\Grid Surface Properties for " + oSurface.Name;
                    propsMsg += "\n-------------------";
                    propsMsg += "\n X Spacing: " + gridProps.SpacingX;
                    propsMsg += "\n Y Spacing: " + gridProps.SpacingY;
                    propsMsg += "\n Orientation: " + gridProps.Orientation;
                    propsMsg += "\n--";
    
                    editor.WriteMessage(propsMsg);
                    #endregion
                }
    
            }
            catch (System.Exception e) { editor.WriteMessage(e.Message); }
        }
    }
