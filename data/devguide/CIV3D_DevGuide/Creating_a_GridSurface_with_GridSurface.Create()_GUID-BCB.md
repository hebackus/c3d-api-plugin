<!-- Developer's Guide > API Developer's Guide > Surfaces > Creating Surfaces > Creating a GridSurface with GridSurface.Create() -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-BCB34370-91AD-44B9-9389-8BF4C84DC12B.htm -->

# Creating a GridSurface with GridSurface.Create()

You can create an empty GridSurface using the GridSurface.Create() method. There are two overloads of this method: one applies the default SurfaceStyle, while the other allows you to specify which SurfaceStyle to use. Both take the name of the new GridSurface, x and y spacing, and orientation. The units for x and y spacing and orientation are specified in the surface creation ambient settings (SettingsCmdCreateSurface Distance and Area properties). 

GridSurface objects are defined on a regularly-spaced grid, and each location on the grid (represented by the GridLocation structure) has a row index and column index. The grid address (0,0) is at the bottom left corner of the grid. 

The following example creates a new, empty GridSurface with 25’ x 25’ spacing, and then iterates through a 10 x 10 grid and adds a random elevation at each sample location: 
    
    
    [CommandMethod("CreateGridSurface")]
    public void CreateGridSurface()
    {
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            string surfaceName = "ExGridSurface";
            // Select a surface style to use 
            ObjectId surfaceStyleId = doc.Styles.SurfaceStyles["Slope Banding (2D)"];
    
            // Create the surface with grid spacing of 25' x 25', orientation 0 degrees:
            ObjectId surfaceId = GridSurface.Create(surfaceName, 25, 25, 0.0, surfaceStyleId);
            GridSurface surface = surfaceId.GetObject(OpenMode.ForWrite) as GridSurface;
    
            // Add some random elevations
            Random m_Generator = new Random();
            for (int i = 0; i < 10; i++)
            {
                for (int j = 0; j < 10; j++)
                {                        
                    double z = m_Generator.NextDouble() * 10;
                    GridLocation loc = new GridLocation(i, j);
                    surface.AddPoint(loc, z);
                }
            }
    
            // commit the create action
            ts.Commit();
        }
    }
