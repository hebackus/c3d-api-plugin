<!-- Developer's Guide > API Developer's Guide > Surfaces > Creating Surfaces > Creating a TIN Surface using TinSurface.Create() -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-1985347E-FC83-479B-B25C-4B381CB1548B.htm -->

# Creating a TIN Surface using TinSurface.Create()

You can create an empty TIN surface and add it to the document’s surface collection with the TinSurface.Create() method. This method has two overloads, one that specifies the SurfaceStyle to apply, while the other uses the default style. 

In this example, we create a new TIN surface with a specified style, and then add some random point data. 
    
    
    [CommandMethod("CreateTINSurface")]
    public void CreateTINSurface()
    {
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            string surfaceName = "ExampleTINSurface";
            // Select a style to use 
            ObjectId surfaceStyleId = doc.Styles.SurfaceStyles[3];
    
            // Create the surface
            ObjectId surfaceId = TinSurface.Create(surfaceName, surfaceStyleId);
    
            TinSurface surface = surfaceId.GetObject(OpenMode.ForWrite) as TinSurface;
    
            // Add some random points
            Point3dCollection points = new Point3dCollection();
            Random generator = new Random();
            for (int i = 0; i < 10; i++)
            {
                double x = generator.NextDouble() * 250;
                double y = generator.NextDouble() * 250;
                double z = generator.NextDouble() * 100;
                points.Add(new Point3d(x, y, z));
            }
    
            surface.AddVertices(points);
    
            // commit the create action
            ts.Commit();
        }
    }
