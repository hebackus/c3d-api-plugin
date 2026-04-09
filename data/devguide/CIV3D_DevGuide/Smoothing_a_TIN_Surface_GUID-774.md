<!-- Developer's Guide > API Developer's Guide > Surfaces > Working with TIN Surfaces > Smoothing a TIN Surface -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-774B7CB3-DE97-4EFF-82F0-8D42F6339188.htm -->

# Smoothing a TIN Surface

Surface smoothing adds points at system-determined elevations using Natural Neighbor Interpolation (NNI) or Kriging methods, which results in smoothed contours with no overlapping. See the Autodesk Civil 3D User’s Guide for more information about the two supported smoothing methods. 

TinSurface objects expose these two smoothing operations with the SmoothSurfaceByNNI() and SmoothSurfaceByKriging() methods. 

Setting up a smoothing operation takes a couple of steps: 

  1. Create a SurfacePointOutputOptions object. 
  2. Set the OutputLocations property (enumerated by SurfacePointOutputLocationsType) to specify the output locations. The other options you need to set on SurfacePointOutputOptions depend on what is specified for this setting: 
     1. EdgeMidPoints – specifies the Edges property, an array of TinSurfaceEdge objects representing edges on the surface. 
     2. RandomPoints – specifies the number of points (RandomPointsNumber) and output regions (OutputRegions, a Point3dCollection ) 
     3. Centroids – specifies the OutputRegions property. 
     4. GridBased – sets the OutputRegions property, grid spacing (GridSpacingX and GridSpacingY), and grid orientation (GridOrientation). 
  3. If you are using the Kriging method, you need to also create a KrigingMethodOptions object to set the options for this method: 
     1. SemivariogramModel property – set to one of the models enumerated by KrigingSemivariogramType. 
     2. SampleVertices property – set to the collection of vertices to which to smooth (for example, you can use the TinSurface.GetVerticesInsidePolylines() to get this collection). 
     3. Optionally set NuggetEffect, VariogramParamA and VariogramParamC depending on the model selected. 
  4. Pass the options to SmoothSurfaceByNNI() or SmoothSurfaceByKriging(). These methods return a SurfaceOperationSmooth object that includes the number of output points in the operation. 

This example illustrates setting up and using the SmoothSurfaceByNNI() method, using the Centroids output location: 
    
    
    [CommandMethod("SmoothTinSurface")]
    public void SmoothTinSurface()
    {
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            try
            {
                // Select a TIN Surface:     
                ObjectId surfaceId = promptForEntity("Select a TIN surface to smooth\n", typeof(TinSurface));
                TinSurface oSurface = surfaceId.GetObject(OpenMode.ForWrite) as TinSurface;
    
                // Select a polyline to define the output region:
                ObjectId polylineId = promptForEntity("Select a polyline to define the output region\n", typeof(Polyline));
                Point3dCollection points = new Point3dCollection();
                Polyline polyline = polylineId.GetObject(OpenMode.ForRead) as Polyline;
    
                // Convert the polyline into a collection of points:
                int count = polyline.NumberOfVertices;
                for (int i = 0; i < count; i++)
                {
                    points.Add(polyline.GetPoint3dAt(i));
                }
    
                // Set the options:
                SurfacePointOutputOptions output = new SurfacePointOutputOptions();
                output.OutputLocations = SurfacePointOutputLocationsType.Centroids;
                output.OutputRegions = new Point3dCollection[] { points };
    
                SurfaceOperationSmooth op = oSurface.SmoothSurfaceByNNI(output);
    
                editor.WriteMessage("Output Points: {0}\n", op.OutPutPoints.Count);
    
                // Commit the transaction
                ts.Commit();
            }
            catch (System.Exception e) { editor.WriteMessage(e.Message); }
        }
    }
