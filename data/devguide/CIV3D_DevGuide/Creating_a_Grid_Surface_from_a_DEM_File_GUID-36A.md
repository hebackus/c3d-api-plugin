<!-- Developer's Guide > API Developer's Guide > Surfaces > Creating Surfaces > Creating a Grid Surface from a DEM File -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-36A8AABD-D122-4279-AF69-DD8F82807161.htm -->

# Creating a Grid Surface from a DEM File

You can create a GridSurface from a Digital Elevation Model (DEM) file using the GridSurface.CreateFromDEM() method. There are two overloads of this method: one that applies the default style, while the other allows you to specify the SurfaceStyle to use. Both take the filename and path of a DEM file, as a string. 
    
    
    [CommandMethod("CreateFromDEM")]
    public void CreateFromDEM()
    {
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            // Prompt user for a DEM file:
            // string demFile = @"C:\Program Files\Autodesk\AutoCAD Civil 3D 2013\Help\Civil Tutorials\Corridor surface.tin";
            PromptFileNameResult demResult = editor.GetFileNameForOpen("Enter the path and name of the DEM file to import:");
            editor.WriteMessage("Importing: {0}", demResult.StringResult);
    
            try
            {
                // surface style #3 is "slope banding" in the default template
                ObjectId surfaceStyleId = doc.Styles.SurfaceStyles[3];
                ObjectId gridSurfaceId = GridSurface.CreateFromDEM(demResult.StringResult, surfaceStyleId);
                editor.WriteMessage("Import succeeded: {0} \n", gridSurfaceId.ToString());
            }
            catch (System.Exception e)
            {
                // handle bad file data or other errors
                editor.WriteMessage("Import failed: {0}", e.Message);
            }
    
            // commit the transaction
            ts.Commit();
        }
    }
