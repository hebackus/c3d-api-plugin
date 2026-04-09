<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Advanced Drawing and Organizational Techniques (.NET) > Use External References (.NET) > Clip Blocks and Xrefs (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-72029044-0840-4187-9A58-F2A4518E3A23.htm -->

# Clip Blocks and Xrefs (.NET)

You can define a region of an external reference for display and plotting by clipping the external reference. The clipping boundary must be a 2D polygon or rectangle with vertices constrained to lie within the boundaries of the external reference. Multiple instances of the same external reference can have different boundaries. 

The SpatialFilter and SpatialFilterDefinition objects are used to define the properties of the clipping boundary for an external reference. Use the Enabled property of the SpatialFilterDefinition object show or hide the clipping boundary. 

## Clip an xref definition

This example attaches an external reference and then clips the external reference so only part of it is displayed. This example uses the _Exterior Elevations.dwg_ file found in the _Sample_ directory. If you do not have this image, or if it is located in a different directory, insert a valid path and file name. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    
    [CommandMethod("ClippingExternalReference")]
    public void ClippingExternalReference()
    {
        // Get the current database and start a transaction
        Database acCurDb;
        acCurDb = Application.DocumentManager.MdiActiveDocument.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Create a reference to a DWG file
            string PathName = "C:\\AutoCAD\\Sample\\Sheet Sets\\Architectural\\Res\\Exterior Elevations.dwg";
            ObjectId acXrefId = acCurDb.AttachXref(PathName, "Exterior Elevations");
    
            // If a valid reference is created then continue
            if (!acXrefId.IsNull)
            {
                // Attach the DWG reference to the current space
                Point3d insPt = new Point3d(1, 1, 0);
                using (BlockReference acBlkRef = new BlockReference(insPt, acXrefId))
                {
                    BlockTableRecord acBlkTblRec;
                    acBlkTblRec = acTrans.GetObject(acCurDb.CurrentSpaceId, OpenMode.ForWrite) as BlockTableRecord;
    
                    acBlkTblRec.AppendEntity(acBlkRef);
                    acTrans.AddNewlyCreatedDBObject(acBlkRef, true);
    
                    Application.ShowAlertDialog("The external reference is attached.");
    
                    Matrix3d mat = acBlkRef.BlockTransform;
                    mat.Inverse();
    
                    Point2dCollection ptCol = new Point2dCollection();
    
                    // Define the first corner of the clipping boundary
                    Point3d pt3d = new Point3d(-330, 400, 0);
                    pt3d.TransformBy(mat);
                    ptCol.Add(new Point2d(pt3d.X, pt3d.Y));
    
                    // Define the second corner of the clipping boundary
                    pt3d = new Point3d(1320, 1120, 0);
                    pt3d.TransformBy(mat);
                    ptCol.Add(new Point2d(pt3d.X, pt3d.Y));
    
                    // Define the normal and elevation for the clipping boundary 
                    Vector3d normal;
                    double elev = 0;
    
                    if (acCurDb.TileMode == true)
                    {
                        normal = acCurDb.Ucsxdir.CrossProduct(acCurDb.Ucsydir);
                        elev = acCurDb.Elevation;
                    }
                    else
                    {
                        normal = acCurDb.Pucsxdir.CrossProduct(acCurDb.Pucsydir);
                        elev = acCurDb.Pelevation;
                    }
    
                    // Set the clipping boundary and enable it
                    using (Autodesk.AutoCAD.DatabaseServices.Filters.SpatialFilter filter = 
                        new Autodesk.AutoCAD.DatabaseServices.Filters.SpatialFilter())
                    {
                        Autodesk.AutoCAD.DatabaseServices.Filters.SpatialFilterDefinition filterDef = 
                            new Autodesk.AutoCAD.DatabaseServices.Filters.SpatialFilterDefinition(ptCol, normal, elev, 0, 0, true);
                        filter.Definition = filterDef;
    
                        // Define the name of the extension dictionary and entry name
                        string dictName = "ACAD_FILTER";
                        string spName = "SPATIAL";
    
                        // Check to see if the Extension Dictionary exists, if not create it
                        if (acBlkRef.ExtensionDictionary.IsNull)
                        {
                            acBlkRef.CreateExtensionDictionary();
                        }
    
                        // Open the Extension Dictionary for write
                        DBDictionary extDict = acTrans.GetObject(acBlkRef.ExtensionDictionary, OpenMode.ForWrite) as DBDictionary;
    
                        // Check to see if the dictionary for clipped boundaries exists, 
                        // and add the spatial filter to the dictionary
                        if (extDict.Contains(dictName))
                        {
                            DBDictionary filterDict = acTrans.GetObject(extDict.GetAt(dictName), OpenMode.ForWrite) as DBDictionary;
    
                            if (filterDict.Contains(spName))
                            {
                                filterDict.Remove(spName);
                            }
    
                            filterDict.SetAt(spName, filter);
                        }
                        else
                        {
                            using (DBDictionary filterDict = new DBDictionary())
                            {
                                extDict.SetAt(dictName, filterDict);
    
                                acTrans.AddNewlyCreatedDBObject(filterDict, true);
                                filterDict.SetAt(spName, filter);
                            }
                        }
    
                        // Append the spatial filter to the drawing
                        acTrans.AddNewlyCreatedDBObject(filter, true);
                    }
                }
    
                Application.ShowAlertDialog("The external reference is clipped.");
            }
    
            // Save the new objects to the database
            acTrans.Commit();
    
            // Dispose of the transaction
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    
    <CommandMethod("ClippingExternalReference")> _
    Public Sub ClippingExternalReference()
        ' Get the current database and start a transaction
        Dim acCurDb As Autodesk.AutoCAD.DatabaseServices.Database
        acCurDb = Application.DocumentManager.MdiActiveDocument.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            ' Create a reference to a DWG file
            Dim PathName As String = "C:\AutoCAD\Sample\Sheet Sets\Architectural\Res\Exterior Elevations.dwg"
            Dim acXrefId As ObjectId = acCurDb.AttachXref(PathName, "Exterior Elevations")
    
            ' If a valid reference is created then continue
            If Not acXrefId.IsNull Then
                ' Attach the DWG reference to the current space
                Dim insPt As New Point3d(1, 1, 0)
                Using acBlkRef As New BlockReference(insPt, acXrefId)
    
                    Dim acBlkTblRec As BlockTableRecord
                    acBlkTblRec = acTrans.GetObject(acCurDb.CurrentSpaceId, OpenMode.ForWrite)
    
                    acBlkTblRec.AppendEntity(acBlkRef)
                    acTrans.AddNewlyCreatedDBObject(acBlkRef, True)
    
                    MsgBox("The external reference is attached.")
    
                    Dim mat As Matrix3d = acBlkRef.BlockTransform
                    mat.Inverse()
    
                    Dim ptCol As New Point2dCollection
    
                    ' Define the first corner of the clipping boundary
                    Dim pt3d As New Point3d(-330, 400, 0)
                    pt3d.TransformBy(mat)
                    ptCol.Add(New Point2d(pt3d.X, pt3d.Y))
    
                    ' Define the second corner of the clipping boundary
                    pt3d = New Point3d(1320, 1120, 0)
                    pt3d.TransformBy(mat)
                    ptCol.Add(New Point2d(pt3d.X, pt3d.Y))
    
                    ' Define the normal and elevation for the clipping boundary 
                    Dim normal As Vector3d
                    Dim elev As Double = 0
    
                    If acCurDb.TileMode = True Then
                        normal = acCurDb.Ucsxdir.CrossProduct(acCurDb.Ucsydir)
                        elev = acCurDb.Elevation
                    Else
                        normal = acCurDb.Pucsxdir.CrossProduct(acCurDb.Pucsydir)
                        elev = acCurDb.Pelevation
                    End If
    
                    ' Set the clipping boundary and enable it
                    Using filter As New Filters.SpatialFilter
                        Dim filterDef As New Filters.SpatialFilterDefinition(ptCol, normal, elev, 0, 0, True)
                        filter.Definition = filterDef
    
                        ' Define the name of the extension dictionary and entry name
                        Dim dictName As String = "ACAD_FILTER"
                        Dim spName As String = "SPATIAL"
    
                        ' Check to see if the Extension Dictionary exists, if not create it
                        If acBlkRef.ExtensionDictionary.IsNull Then
                            acBlkRef.CreateExtensionDictionary()
                        End If
    
                        ' Open the Extension Dictionary for write
                        Dim extDict As DBDictionary = acTrans.GetObject(acBlkRef.ExtensionDictionary, OpenMode.ForWrite)
    
                        ' Check to see if the dictionary for clipped boundaries exists, 
                        ' and add the spatial filter to the dictionary
                        If extDict.Contains(dictName) Then
                            Dim filterDict As DBDictionary = acTrans.GetObject(extDict.GetAt(dictName), OpenMode.ForWrite)
    
                            If (filterDict.Contains(spName)) Then filterDict.Remove(spName)
    
                            filterDict.SetAt(spName, filter)
                        Else
                            Using filterDict As New DBDictionary
                                extDict.SetAt(dictName, filterDict)
    
                                acTrans.AddNewlyCreatedDBObject(filterDict, True)
                                filterDict.SetAt(spName, filter)
                            End Using
                        End If
    
                        ' Append the spatial filter to the drawing
                        acTrans.AddNewlyCreatedDBObject(filter, True)
                    End Using
                End Using
    
                MsgBox("The external reference is clipped.")
            End If
    
            ' Save the new objects to the database
            acTrans.Commit()
    
            ' Dispose of the transaction
        End Using
    End Sub
