<!-- Developer's Guide > API Developer's Guide > Surfaces > Surface Analysis > Accessing a Watershed Analysis -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-A3E34034-4CFE-4AFF-9B0E-379BDC9AD420.htm -->

# Accessing a Watershed Analysis

A watershed analysis predicts how water will flow over and off a surface. The analysis data is managed by an object of type SurfaceAnalysisWatershedDataCollection returned by the Surface.Analysis.GetWatershedData() method. 

The .NET API does not implement an equivalent to the COM API AeccSurfaceAnalysisWatershed.CalculateWatersheds() method, but you can use the SurfaceAnalysis.GetWatershedData() method to access watershed data from an existing analysis, and change properties (such as AreaColor) of watershed regions. 

Each item in the SurfaceAnalysisWatershedDataCollection represents a watershed region. Depending on the nature of the drain target, each watershed region is a different type specified by the WatershedType enumeration. (For more information about watershed region types, see “Types of Watersheds” in the Autodesk Civil 3D User’s Guide). Other properties, such as the region color, hatch pattern, description, and visibility, are all accessible. 

This example illustrates reading the properties of an existing watershed analysis: 
    
    
    [CommandMethod("SurfaceWatershedAnalysis")]
    public void SurfaceWatershedAnalysis()
    {
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            // Select first TIN Surface              
            ObjectId surfaceId = doc.GetSurfaceIds()[0];
            CivSurface oSurface = surfaceId.GetObject(OpenMode.ForRead) as CivSurface;
    
            SurfaceAnalysisWatershedDataCollection analysisData = oSurface.Analysis.GetWatershedData();
            editor.WriteMessage("Number of watershed regions: {0}\n", analysisData.Count);
            foreach (SurfaceAnalysisWatershedData watershedData in analysisData)
            {
                editor.WriteMessage("Data item AreaId: {0} \n" 
                    + "Description: {1}\n" 
                    + "Type: {2}\n"
                    + "Drains into areas: {3}\n"
                    + "Visible? {4}\n", 
                    watershedData.AreaID, watershedData.Description, watershedData.Type, 
                    String.Join(", ", watershedData.DrainsInto), watershedData.Visible);
            }
                    
            // commit the transaction
            ts.Commit();
        }           
    }
