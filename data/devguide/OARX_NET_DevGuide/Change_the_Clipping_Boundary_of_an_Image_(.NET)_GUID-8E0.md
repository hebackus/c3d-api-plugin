<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Advanced Drawing and Organizational Techniques (.NET) > Work with Raster Images (.NET) > Change the Clipping Boundary of an Image (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-8E0F973E-6416-4580-A2B0-6D91B9968BB7.htm -->

# Change the Clipping Boundary of an Image (.NET)

You can define a region of an image for display and plotting by clipping the image. The clipping boundary must be a 2D polygon or rectangle with vertices constrained to lie within the boundaries of the image. Multiple instances of the same image can have different boundaries. 

Use the IsClipped property when you want to show or hide the image boundary, and the ClipBoundaryType property to determine if the clipping boundary is defined as rectangular or polygonal. 

Use the following methods to get or set the clipping boundary for an image: 

GetClipBoundary
    Returns a collection of clip boundary vertices in image pixel coordinates. Invert the PixelToModelTransform matrix to convert these to model coordinates.
SetClipBoundary
    Specifies a polygonal clip boundary.
SetClipBoundaryToWholeImage
    Sets the clip boundary to coincide with the image borders. Any existing clip boundary is deleted.

## Clip a raster image

This example adds a raster image in model space, and then clips the image based on a clip boundary. This example uses the _WorldMap.tif file_ found in the VBA sample directory. If you do not have this image, or if it is located in a different directory, revise the code to use a valid path and file name. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    
    [CommandMethod("ClippingRasterBoundary")]
    public void ClippingRasterBoundary()
    {
        // Get the current database and start a transaction
        Database acCurDb;
        acCurDb = Application.DocumentManager.MdiActiveDocument.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Define the name and image to use
            string strImgName = "WorldMap";
            string strFileName = "C:\\AutoCAD\\Sample\\VBA\\WorldMap.TIF";
    
            RasterImageDef acRasterDef;
            bool bRasterDefCreated = false;
            ObjectId acImgDefId;
    
            // Get the image dictionary
            ObjectId acImgDctID = RasterImageDef.GetImageDictionary(acCurDb);
    
            // Check to see if the dictionary does not exist, it not then create it
            if (acImgDctID.IsNull)
            {
                acImgDctID = RasterImageDef.CreateImageDictionary(acCurDb);
            }
    
            // Open the image dictionary
            DBDictionary acImgDict = acTrans.GetObject(acImgDctID, OpenMode.ForRead) as DBDictionary;
    
            // Check to see if the image definition already exists
            if (acImgDict.Contains(strImgName))
            {
                acImgDefId = acImgDict.GetAt(strImgName);
    
                acRasterDef = acTrans.GetObject(acImgDefId, OpenMode.ForWrite) as RasterImageDef;
            }
            else
            {
                // Create a raster image definition
                RasterImageDef acRasterDefNew = new RasterImageDef();
    
                // Set the source for the image file
                acRasterDefNew.SourceFileName = strFileName;
    
                // Load the image into memory
                acRasterDefNew.Load();
    
                // Add the image definition to the dictionary
                acTrans.GetObject(acImgDctID, OpenMode.ForWrite);
                acImgDefId = acImgDict.SetAt(strImgName, acRasterDefNew);
    
                acTrans.AddNewlyCreatedDBObject(acRasterDefNew, true);
    
                acRasterDef = acRasterDefNew;
    
                bRasterDefCreated = true;
            }
    
            // Open the Block table for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Model space for write
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                            OpenMode.ForWrite) as BlockTableRecord;
    
            // Create the new image and assign it the image definition
            using (RasterImage acRaster = new RasterImage())
            {
                acRaster.ImageDefId = acImgDefId;
    
                // Use ImageWidth and ImageHeight to get the size of the image in pixels (1024 x 768).
                // Use ResolutionMMPerPixel to determine the number of millimeters in a pixel so you 
                // can convert the size of the drawing into other units or millimeters based on the 
                // drawing units used in the current drawing.
    
                // Define the width and height of the image
                Vector3d width;
                Vector3d height;
    
                // Check to see if the measurement is set to English (Imperial) or Metric units
                if (acCurDb.Measurement == MeasurementValue.English)
                {
                    width = new Vector3d((acRasterDef.ResolutionMMPerPixel.X * acRaster.ImageWidth) / 25.4, 0, 0);
                    height = new Vector3d(0, (acRasterDef.ResolutionMMPerPixel.Y * acRaster.ImageHeight) / 25.4, 0);
                }
                else
                {
                    width = new Vector3d(acRasterDef.ResolutionMMPerPixel.X * acRaster.ImageWidth, 0, 0);
                    height = new Vector3d(0, acRasterDef.ResolutionMMPerPixel.Y * acRaster.ImageHeight, 0);
                }
    
                // Define the position for the image 
                Point3d insPt = new Point3d(5.0, 5.0, 0.0);
    
                // Define and assign a coordinate system for the image's orientation
                CoordinateSystem3d coordinateSystem = new CoordinateSystem3d(insPt, width * 2, height * 2);
                acRaster.Orientation = coordinateSystem;
    
                // Set the rotation angle for the image
                acRaster.Rotation = 0;
    
                // Define the clipping boundary in drawing units
                Point2dCollection acPt2dColl = new Point2dCollection();
                Matrix3d acMat3d = acRaster.PixelToModelTransform.Inverse();
                acPt2dColl.Add(new Point3d(5.5, 15, 0).TransformBy(acMat3d).Convert2d(new Plane()));
                acPt2dColl.Add(new Point3d(12.5, 15, 0).TransformBy(acMat3d).Convert2d(new Plane()));
                acPt2dColl.Add(new Point3d(12.5, 10.5, 0).TransformBy(acMat3d).Convert2d(new Plane()));
                acPt2dColl.Add(new Point3d(5.5, 10.5, 0).TransformBy(acMat3d).Convert2d(new Plane()));
                acPt2dColl.Add(new Point3d(5.5, 15, 0).TransformBy(acMat3d).Convert2d(new Plane()));
    
                // Clip the image
                acRaster.SetClipBoundary(ClipBoundaryType.Rectangle, acPt2dColl);
    
                // Enable the display of the clip
                acRaster.IsClipped = true;
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acRaster);
                acTrans.AddNewlyCreatedDBObject(acRaster, true);
    
                // Connect the raster definition and image together so the definition
                // does not appear as "unreferenced" in the External References palette.
                RasterImage.EnableReactors(true);
                acRaster.AssociateRasterDef(acRasterDef);
    
                if (bRasterDefCreated)
                {
                    acRasterDef.Dispose();
                }
            }
    
            // Save the new object to the database
            acTrans.Commit();
    
            // Dispose of the transaction
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    
    <CommandMethod("ClippingRasterBoundary")> _
    Public Sub ClippingRasterBoundary()
        ' Get the current database and start a transaction
        Dim acCurDb As Autodesk.AutoCAD.DatabaseServices.Database
        acCurDb = Application.DocumentManager.MdiActiveDocument.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            ' Define the name and image to use
            Dim strImgName As String = "WorldMap"
            Dim strFileName As String = "C:\AutoCAD\Sample\VBA\WorldMap.TIF"
    
            Dim acRasterDef As RasterImageDef
            Dim bRasterDefCreated As Boolean = False
            Dim acImgDefId As ObjectId
    
            ' Get the image dictionary
            Dim acImgDctID As ObjectId = RasterImageDef.GetImageDictionary(acCurDb)
    
            ' Check to see if the dictionary does not exist, it not then create it
            If acImgDctID.IsNull Then
                acImgDctID = RasterImageDef.CreateImageDictionary(acCurDb)
            End If
    
            ' Open the image dictionary
            Dim acImgDict As DBDictionary = acTrans.GetObject(acImgDctID, OpenMode.ForRead)
    
            ' Check to see if the image definition already exists
            If acImgDict.Contains(strImgName) Then
                acImgDefId = acImgDict.GetAt(strImgName)
    
                acRasterDef = acTrans.GetObject(acImgDefId, OpenMode.ForWrite)
            Else
                ' Create a raster image definition
                Dim acRasterDefNew As New RasterImageDef
    
                ' Set the source for the image file
                acRasterDefNew.SourceFileName = strFileName
    
                ' Load the image into memory
                acRasterDefNew.Load()
    
                ' Add the image definition to the dictionary
                acTrans.GetObject(acImgDctID, OpenMode.ForWrite)
                acImgDefId = acImgDict.SetAt(strImgName, acRasterDefNew)
    
                acTrans.AddNewlyCreatedDBObject(acRasterDefNew, True)
    
                acRasterDef = acRasterDefNew
    
                bRasterDefCreated = True
            End If
    
            ' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead)
    
            ' Open the Block table record Model space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForWrite)
    
            ' Create the new image and assign it the image definition
            Using acRaster As New RasterImage
                acRaster.ImageDefId = acImgDefId
    
                ' Use ImageWidth and ImageHeight to get the size of the image in pixels (1024 x 768).
                ' Use ResolutionMMPerPixel to determine the number of millimeters in a pixel so you 
                ' can convert the size of the drawing into other units or millimeters based on the 
                ' drawing units used in the current drawing.
    
                ' Define the width and height of the image
                Dim width As Vector3d
                Dim height As Vector3d
    
                ' Check to see if the measurement is set to English (Imperial) or Metric units
                If acCurDb.Measurement = MeasurementValue.English Then
                    width = New Vector3d((acRasterDef.ResolutionMMPerPixel.X * acRaster.ImageWidth) / 25.4, 0, 0)
                    height = New Vector3d(0, (acRasterDef.ResolutionMMPerPixel.Y * acRaster.ImageHeight) / 25.4, 0)
                Else
                    width = New Vector3d(acRasterDef.ResolutionMMPerPixel.X * acRaster.ImageWidth, 0, 0)
                    height = New Vector3d(0, acRasterDef.ResolutionMMPerPixel.Y * acRaster.ImageHeight, 0)
                End If
    
                ' Define the position for the image 
                Dim insPt As New Point3d(5.0, 5.0, 0.0)
    
                ' Define and assign a coordinate system for the image's orientation
                Dim coordinateSystem As New CoordinateSystem3d(insPt, width * 2, height * 2)
                acRaster.Orientation = coordinateSystem
    
                ' Set the rotation angle for the image
                acRaster.Rotation = 0
    
                ' Define the clipping boundary in drawing units
                Dim acPt2dColl As New Point2dCollection
                Dim acMat3d As Matrix3d = acRaster.PixelToModelTransform.Inverse()
                acPt2dColl.Add(New Point3d(5.5, 15, 0).TransformBy(acMat3d).Convert2d(New Plane()))
                acPt2dColl.Add(New Point3d(12.5, 15, 0).TransformBy(acMat3d).Convert2d(New Plane()))
                acPt2dColl.Add(New Point3d(12.5, 10.5, 0).TransformBy(acMat3d).Convert2d(New Plane()))
                acPt2dColl.Add(New Point3d(5.5, 10.5, 0).TransformBy(acMat3d).Convert2d(New Plane()))
                acPt2dColl.Add(New Point3d(5.5, 15, 0).TransformBy(acMat3d).Convert2d(New Plane()))
    
                ' Clip the image
                acRaster.SetClipBoundary(ClipBoundaryType.Rectangle, acPt2dColl)
    
                ' Enable the display of the clip
                acRaster.IsClipped = True
    
                ' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acRaster)
                acTrans.AddNewlyCreatedDBObject(acRaster, True)
    
                ' Connect the raster definition and image together so the definition
                ' does not appear as "unreferenced" in the External References palette.
                RasterImage.EnableReactors(True)
                acRaster.AssociateRasterDef(acRasterDef)
    
                If bRasterDefCreated Then
                    acRasterDef.Dispose()
                End If
            End Using
    
            ' Save the new object to the database
            acTrans.Commit()
    
            ' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub ClippingRasterBoundary()
        Dim insertionPoint(0 To 2) As Double
        Dim scalefactor As Double
        Dim rotationAngle As Double
        Dim imageName As String
        Dim rasterObj As AcadRasterImage
    
        imageName = "C:/AutoCAD/sample/VBA/WorldMap.TIF"
        insertionPoint(0) = 5
        insertionPoint(1) = 5
        insertionPoint(2) = 0
        scalefactor = 2
        rotationAngle = 0
    
        ' Creates a raster image in model space
        Set rasterObj = ThisDrawing.ModelSpace.AddRaster(imageName, insertionPoint, _
                                                         scalefactor, rotationAngle)
    
        ' Establish the clip boundary with an array of points
        Dim clipPoints(0 To 9) As Double
        clipPoints(0) = 5.5: clipPoints(1) = 15
        clipPoints(2) =12.5: clipPoints(3) = 15
        clipPoints(4) = 12.5: clipPoints(5) = 10.5
        clipPoints(6) = 5.5: clipPoints(7) = 10.5
        clipPoints(8) = 5.5: clipPoints(9) = 15
    
        ' Clip the image
        rasterObj.ClipBoundary clipPoints
    
        ' Enable the display of the clip
        rasterObj.ClippingEnabled = True
        ThisDrawing.Regen acActiveViewport
    End Sub
