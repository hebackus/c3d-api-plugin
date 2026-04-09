<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Advanced Drawing and Organizational Techniques (.NET) > Work with Raster Images (.NET) > Attach and Scale a Raster Image (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-00A0BCD9-4519-4746-BC73-88544D75D789.htm -->

# Attach and Scale a Raster Image (.NET)

Images can be attached and placed in a drawing file, but they are not actually part of the file. The image is linked to the drawing file through a path name or a data management document ID. Linked image paths can be changed or removed at any time. To attach an image, you first create a RasterImageDef object which contains the definition information about the image file stored on disk being referenced and then you create a RasterImage object. 

Once you have created a RasterImageDef object, you assign it to a RasterImage object. The RasterImage object represents the object you interact with in the drawing window and allows you to control the insertion point, scale, orientation, and appearance of the image among other properties. A single RasterImageDef object can be used to attach an image multiple times. Each attachment has its own clip boundary and its own settings for brightness, contrast, fade, and transparency. 

You can set the scale factor for a raster image with the Scale property after you create a RasterImage object so that the image's geometry scale matches the scale of the geometry created in the AutoCAD drawing. When you attach an image, the image is inserted at a scale factor of 1 image unit of measurement to 1 AutoCAD unit of measurement. To set the image scale factor, you need to know the scale of the geometry on the image, and you need to know what unit of measurement (inches, feet, and so forth) you want to use to define 1 AutoCAD unit. The image file must contain resolution information defining the DPI, or dots per inch, and number of pixels in the image. 

If an image has resolution information, AutoCAD combines it with the scale factor and the AutoCAD unit of measurement you supply to scale the image in your drawing. For example, if your raster image is a scanned blueprint on which the scale is 1 inch equals 50 feet, or 1:600, and your AutoCAD drawing is set up so that 1 unit represents 1 inch, then to set the scale factor of the image to 600. AutoCAD scales the image so the geometry in the image is brought into alignment with the vector geometry in the drawing. 

Note: If no resolution information is defined with the attached image file, AutoCAD calculates the image's original width as one unit. After insertion, the image width in AutoCAD units is equal to the scale factor. 

## Attach a raster image

This example adds a raster image in model space. This example uses the _WorldMap.tif_ file found in the VBA sample directory. If you do not have this image, or if it is located in a different directory, revise the code to use a valid path and file name. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    
    [CommandMethod("AttachRasterImage")]
    public void AttachRasterImage()
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
    
    <CommandMethod("AttachRasterImage")> _
    Public Sub AttachRasterImage()
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
    
    
    Sub AttachRasterImage()
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
    
        On Error GoTo ERRORHANDLER
        ' Attach the raster image in model space
        Set rasterObj = ThisDrawing.ModelSpace.AddRaster(imageName, insertionPoint, _
                                                         scalefactor, rotationAngle)
        ZoomAll
     Exit Sub
    
    ERRORHANDLER:
        MsgBox Err.Description
    End Sub
