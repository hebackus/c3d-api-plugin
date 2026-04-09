<!-- Developer's Guide > API Developer's Guide > Surfaces > Surface Analysis > Creating an Elevation Analysis -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-12C5A116-1571-4F19-9BAF-811863C9D26C.htm -->

# Creating an Elevation Analysis

An elevation analysis creates a 2-dimensional projection of a surface and then adds bands of color indicating ranges of altitude. Calling Surface.Analysis.GetElevationData() returns an array of SurfaceAnalysisElevationData objects, one for each elevation region created by the analysis, or an empty array if no analysis exists. Each elevation region represents a portion of the surface’s total elevation. The collection lets you modify the color, minimum elevation, and maximum elevation of each region. 

Note that each time a surface’s elevation analysis is generated in the GUI, Autodesk Civil 3D discards all existing elevation regions for the surface and creates a new collection of regions. Changes to the previous collection of SurfaceAnalysisElevationData objects are discarded. 

The .NET API does not have an equivalent to the COM API SurfaceAnalysisElevation.CalculateElevationRegions() method, but you can implement one that does the same thing. This example shows one implementation, and the implemented method being used by a command: 
    
    
    /// <summary>
    /// Calculates elevation regions for a given surface, and returns an array that can be passed 
    /// to Surface.Analysis.SetElevationData()
    /// </summary>
    /// <param name="surface">A Civil 3D Surface object</param>
    /// <param name="steps">The number of elevation steps to calculate</param>
    /// <param name="startColor">The index of the start color.  Each subsequent color index is incremeted by 2.</param>
    /// <returns>An array of SurfaceAnalysisElevationData objects.</returns>
    private SurfaceAnalysisElevationData[] CalculateElevationRegions(Autodesk.Civil.Land.DatabaseServices.Surface surface, int steps, short startColor)
    {
        // calculate increments based on # of steps:
        double minEle = surface.GetGeneralProperties().MinimumElevation;
        double maxEle = surface.GetGeneralProperties().MaximumElevation;
        double incr = (maxEle - minEle) / steps;
    
        SurfaceAnalysisElevationData[] newData = new SurfaceAnalysisElevationData[steps];
        for (int i = 0; i < steps; i++)
        {
            Color newColor = Color.FromColorIndex(ColorMethod.ByLayer, (short)(100 + (i * 2)));
            newData[i] = new SurfaceAnalysisElevationData(minEle + (incr * i), minEle + (incr * (i + 1)), newColor);
        }
    
        return newData;
    }
    
    /// <summary>
    /// Illustrates performing an elevation analysis
    /// </summary>
    [CommandMethod("SurfaceAnalysis")]
    public void SurfaceAnalysis()
    {
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            // Select first TIN Surface              
            ObjectId surfaceId = doc.GetSurfaceIds()[0];
            TinSurface oSurface = surfaceId.GetObject(OpenMode.ForWrite) as TinSurface;
    
            // get existing analysis, if any:
            SurfaceAnalysisElevationData[] analysisData = oSurface.Analysis.GetElevationData();
            editor.WriteMessage("Existing Analysis length: {0}\n", analysisData.Length);
                    
            SurfaceAnalysisElevationData[] newData = CalculateElevationRegions(oSurface, 10, 100);
                    
            oSurface.Analysis.SetElevationData(newData);
    
            // commit the transaction
            ts.Commit();
        }
    }

Many elevation analysis features can be modified through the surface style. For example, you can use a number of pre-set color schemes (as defined in the ColorSchemeType enumeration).
