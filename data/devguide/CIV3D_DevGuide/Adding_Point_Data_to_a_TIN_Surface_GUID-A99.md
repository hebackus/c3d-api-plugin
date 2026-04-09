<!-- Developer's Guide > API Developer's Guide > Surfaces > Working with TIN Surfaces > Adding Point Data to a TIN Surface -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-A9946E5B-D034-4223-B921-0BFDB6FAED1F.htm -->

# Adding Point Data to a TIN Surface

There are two techniques for adding points that are unique to TIN surfaces: 

  1. Using point files 
  2. Using point groups 

The TinSurface.PointFilesDefinition property contains the names of text files that contain point information. These text files must consist only of lines containing the point number, easting, northing, and elevation delineated by spaces. Except for comment lines beginning with “#”, any other information will result in an error. Unlike TIN or LandXML files, text files do not contain a list of faces - the points are automatically joined into a series of triangles based on the document settings. 

The method PointFilesDefinition.AddPointFile() takes the path to a point file, and the ObjectId of a PointFileFormat object. This object is obtained from the Database’s PointFileFormatCollection using the same string used to describe the format in the Civil 3D GUI: 

This is an example of adding a PENZD format point file to an existing surface. The file in this example is from the Civil 3D tutorials directory. 
    
    
    [CommandMethod("SurfacePointFile")]
    public void SurfacePointFile()
    {
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            // Select the first Surface in the document
            ObjectId surfaceId = doc.GetSurfaceIds()[0];
            TinSurface oSurface = surfaceId.GetObject(OpenMode.ForRead) as TinSurface;
    
            try
            {
                // add points from a point file to the surface
                // this is the location of an example PENZD file from the C3D tutorials, the actual path may 
                // differ based on the OS
                string penzdFile = @"C:\Program Files\Autodesk\AutoCAD Civil 3D 2013\Help\Civil Tutorials\EG-Surface-PENZD (space delimited).txt";
    
                // get the point file format object, required for import:
                PointFileFormatCollection ptFileFormats = PointFileFormatCollection.GetPointFileFormats(HostApplicationServices.WorkingDatabase);
                ObjectId ptFormatId = ptFileFormats["PENZD (space delimited)"];
    
                oSurface.PointFilesDefinition.AddPointFile(penzdFile, ptFormatId);
            }
    
            catch (System.Exception e)
            {
                editor.WriteMessage("Failed: {0}", e.Message);
            }
    
            // commit the transaction
            ts.Commit();
        }
    }
