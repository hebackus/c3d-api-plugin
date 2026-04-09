<!-- Developer's Guide > API Developer's Guide > Surfaces > Creating Surfaces > Creating a TIN Surface from a TIN file -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-4AB91109-E8AD-4D02-9CFB-145B73F21ECB.htm -->

# Creating a TIN Surface from a TIN file

You can create a new TIN surface from a binary .tin file using the TinSurface.CreateFromTin() method. This method takes two arguments, the database for the drawing to which the TIN surface will be added, and the path to a .tin file, as a string. 
    
    
    [CommandMethod("CreateFromTIN")]
    public void CreateFromTin()
    {
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            // Example TIN surface from Civil Tutorials:
            string tinFile = @"C:\Program Files\Autodesk\AutoCAD Civil 3D 2013\Help\Civil Tutorials\Corridor surface.tin";
            try
            {
                Database db = Application.DocumentManager.MdiActiveDocument.Database;
                ObjectId tinSurfaceId = TinSurface.CreateFromTin(db, tinFile);
                editor.WriteMessage("Import succeeded: {0} \n {1}", tinSurfaceId.ToString(), db.Filename);
            }
            catch (System.Exception e)
            {
                // handle bad file path 
                editor.WriteMessage("Import failed: {0}", e.Message);
            }
    
            // commit the transaction
            ts.Commit();
        }
    }
