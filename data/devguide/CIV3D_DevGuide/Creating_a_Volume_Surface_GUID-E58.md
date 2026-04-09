<!-- Developer's Guide > API Developer's Guide > Surfaces > Creating Surfaces > Creating a Volume Surface -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-E5899496-9E00-4CA8-A321-76268124CD62.htm -->

# Creating a Volume Surface

A volume surface represents the difference or composite between two TIN or grid surface areas in a document. You can create a volume surface using the Create() method for either the TinVolumeSurface or GridVolumeSurface class. 

In this example, the user is prompted to select the base and comparison surfaces, and then a new TinVolumeSurface is created from them. The implementation of promptForTinSurface() is left out for clarity. 
    
    
    CommandMethod("CreateTinVolumeSurface")]
    public void CreateTinVolumeSurface()
    {
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            string surfaceName = "ExampleVolumeSurface";
            // Prompt user to select surfaces to use
            // promptForTinSurface uses Editor.GetEntity() to select a TIN surface
            ObjectId baseId = promptForTinSurface("Select the base surface");
            ObjectId comparisonId = promptForTinSurface("Select the comparison surface");
    
            try
            {
                // Create the surface
                ObjectId surfaceId = TinVolumeSurface.Create(surfaceName, baseId, comparisonId);
                TinVolumeSurface surface = surfaceId.GetObject(OpenMode.ForWrite) as TinVolumeSurface;
            }
    
            catch (System.Exception e)
            {
                editor.WriteMessage("Surface create failed: {0}", e.Message);
            }
    
            // commit the create action
            ts.Commit();
        }
    }
