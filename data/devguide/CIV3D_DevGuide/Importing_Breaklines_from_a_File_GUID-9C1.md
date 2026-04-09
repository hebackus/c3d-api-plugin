<!-- Developer's Guide > API Developer's Guide > Surfaces > Working with TIN Surfaces > Importing Breaklines from a File -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-9C1B2EB0-3D46-427C-A8AF-5CE9FB36F3B8.htm -->

# Importing Breaklines from a File

You can import breaklines from a file in .FLT format, using SurfaceDefinitionBreaklines.ImportBreaklineFromFile(). When you import the file, all breaklines in the FLT file are copied into the surface as Add Breakline operations, and the link to the file is not maintained. The option available on the GUI to maintain a link to the file is not available via the API. 

This sample shows how to import breaklines from a file named eg1.flt, and to get the first newly created breakline: 
    
    
    [CommandMethod("ImportBreaklines")]
    public void ImportBreaklines()
    {
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            // Prompt the user to select a TIN surface and a polyline, and create a breakline from the polyline
    
            ObjectId surfaceId = promptForEntity("Select a TIN surface to add a breakline to", typeof(TinSurface));
            TinSurface oSurface = surfaceId.GetObject(OpenMode.ForWrite) as TinSurface;
            string breaklines = "eg1.flt";
            oSurface.BreaklinesDefinition.ImportBreaklinesFromFile(breaklines);
    
            // commit the transaction
            ts.Commit();
        }
    }
