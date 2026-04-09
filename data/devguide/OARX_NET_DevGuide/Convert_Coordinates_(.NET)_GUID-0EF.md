<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Work in Three-Dimensional Space (.NET) > Convert Coordinates (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-0EFA65CC-C1AB-4B99-8159-C31602C1A5E8.htm -->

# Convert Coordinates (.NET)

The TransformBy method can translate a point or a displacement from one coordinate system to another. You use the AlignCoordinateSystem method to specify which coordinate system you are translating from and which coordinate system you are going to. The AlignCoordinateSystem method requires the following: 

  * Origin point of the coordinate system you are translating from 
  * Three 3D vectors that represent the X, Y and X axes of the coordinate system you are translating from 
  * Origin point of the coordinate system you are translating to 
  * Three 3D vectors that represent the X, Y and X axes of the coordinate system you are translating to 

WCS 
    

World coordinate system: The reference coordinate system. All other coordinate systems are defined relative to the WCS, which never changes. Values measured relative to the WCS are stable across changes to other coordinate systems. All points passed in and out of the methods and properties in the .NET API are expressed in the WCS unless otherwise specified. 

UCS 
    

User coordinate system (UCS): The working coordinate system. The user specifies a UCS to make drawing tasks easier. All points passed to AutoCAD commands, including those returned from AutoLISP routines and external functions, are points in the current UCS (unless the user precedes them with an * at the Command prompt). If you want your application to send coordinates in the WCS, OCS, or DCS to AutoCAD commands, you must first convert them to the UCS by calling the translating them and then transforming the Point3d or Point 2d object with the TransformBy method that represents the coordinate value. 

OCS
    

Object coordinate system (also known as Entity coordinate system or ECS): Point values specified by certain methods and properties for the Polyline2d and Polyline objects are expressed in this coordinate system, relative to the object. These points are usually converted into the WCS, current UCS, or current DCS, according to the intended use of the object. Conversely, points in WCS, UCS, or DCS must be translated into an OCS before they are written to the database by means of the same properties. 

When converting coordinates to or from the OCS you must consider the normal of the OCS. 

DCS 
    

Display coordinate system: The coordinate system where objects are transformed before they are displayed. The origin of the DCS is the point stored in the AutoCAD system variable TARGET, and its _Z_ axis is the viewing direction. In other words, a viewport is always a plan view of its DCS. These coordinates can be used to determine where something will be displayed to the user. 

PSDCS 
    

Paper space DCS: This coordinate system can be transformed only to or from the DCS of a Model space viewport. This is essentially a 2D transformation, where the _X_ and _Y_ coordinates are always scaled. Therefore, it can be used to find the scale factor between the two coordinate systems. The PSDCS can be transformed only into a Model space viewport. 

## Translate OCS coordinates to WCS coordinates

This example creates a polyline in Model space. The first vertex for the polyline is then displayed in both the OCS and WCS coordinates. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("TranslateCoordinates")]
    public static void TranslateCoordinates()
    {
        // Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Block table record for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                         OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Model space for write
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                            OpenMode.ForWrite) as BlockTableRecord;
    
            // Create a 2D polyline with two segments (3 points)
            using (Polyline2d acPoly2d = new Polyline2d())
            {
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPoly2d);
                acTrans.AddNewlyCreatedDBObject(acPoly2d, true);
    
                // Before adding vertexes, the polyline must be in the drawing
                Point3dCollection acPts2dPoly = new Point3dCollection();
                acPts2dPoly.Add(new Point3d(1, 1, 0));
                acPts2dPoly.Add(new Point3d(1, 2, 0));
                acPts2dPoly.Add(new Point3d(2, 2, 0));
                acPts2dPoly.Add(new Point3d(3, 2, 0));
                acPts2dPoly.Add(new Point3d(4, 4, 0));
    
                foreach (Point3d acPt3d in acPts2dPoly)
                {
                    Vertex2d acVer2d = new Vertex2d(acPt3d, 0, 0, 0, 0);
                    acPoly2d.AppendVertex(acVer2d);
                    acTrans.AddNewlyCreatedDBObject(acVer2d, true);
                }
    
                // Set the normal of the 2D polyline
                acPoly2d.Normal = new Vector3d(0, 1, 2);
    
                // Get the first coordinate of the 2D polyline
                Point3dCollection acPts3d = new Point3dCollection();
                Vertex2d acFirstVer = null;
    
                foreach (ObjectId acObjIdVert in acPoly2d)
                {
                    acFirstVer = acTrans.GetObject(acObjIdVert,
                                                   OpenMode.ForRead) as Vertex2d;
    
                    acPts3d.Add(acFirstVer.Position);
    
                    break;
                }
    
                // Get the first point of the polyline and 
                // use the eleveation for the Z value
                Point3d pFirstVer = new Point3d(acFirstVer.Position.X,
                                                acFirstVer.Position.Y,
                                                acPoly2d.Elevation);
    
                // Translate the OCS to WCS
                Matrix3d mWPlane = Matrix3d.WorldToPlane(acPoly2d.Normal);
                Point3d pWCSPt = pFirstVer.TransformBy(mWPlane);
    
                Application.ShowAlertDialog("The first vertex has the following " +
                                            "coordinates:" +
                                            "\nOCS: " + pFirstVer.ToString() +
                                            "\nWCS: " + pWCSPt.ToString());
            }
    
            // Save the new objects to the database
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("TranslateCoordinates")> _
    Public Sub TranslateCoordinates()
        '' Get the current document and database, and start a transaction
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                         OpenMode.ForRead)
    
            '' Open the Block table record Model space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForWrite)
    
            '' Create a 2D polyline with two segments (3 points)
            Dim acPoly2d As Polyline2d = New Polyline2d()
    
            '' Add the new object to the block table record and the transaction
            acBlkTblRec.AppendEntity(acPoly2d)
            acTrans.AddNewlyCreatedDBObject(acPoly2d, True)
    
            '' Before adding vertexes, the polyline must be in the drawing
            Dim acPts2dPoly As Point3dCollection = New Point3dCollection()
            acPts2dPoly.Add(New Point3d(1, 1, 0))
            acPts2dPoly.Add(New Point3d(1, 2, 0))
            acPts2dPoly.Add(New Point3d(2, 2, 0))
            acPts2dPoly.Add(New Point3d(3, 2, 0))
            acPts2dPoly.Add(New Point3d(4, 4, 0))
    
            For Each acPt3d As Point3d In acPts2dPoly
                Dim acVer2d As Vertex2d = New Vertex2d(acPt3d, 0, 0, 0, 0)
                acPoly2d.AppendVertex(acVer2d)
                acTrans.AddNewlyCreatedDBObject(acVer2d, True)
            Next
    
            '' Set the normal of the 2D polyline
            acPoly2d.Normal = New Vector3d(0, 1, 2)
    
            '' Get the first coordinate of the 2D polyline
            Dim acPts3d As Point3dCollection = New Point3dCollection()
            Dim acFirstVer As Vertex2d = Nothing
            For Each acObjIdVert As ObjectId In acPoly2d
                acFirstVer = acTrans.GetObject(acObjIdVert, _
                                               OpenMode.ForRead)
    
                acPts3d.Add(acFirstVer.Position)
    
                Exit For
            Next
    
            '' Get the first point of the polyline and 
            '' use the eleveation for the Z value
            Dim pFirstVer As Point3d = New Point3d(acFirstVer.Position.X, _
                                                   acFirstVer.Position.Y, _
                                                   acPoly2d.Elevation)
    
            '' Translate the OCS to WCS
            Dim mWPlane As Matrix3d = Matrix3d.WorldToPlane(acPoly2d.Normal)
            Dim pWCSPt As Point3d = pFirstVer.TransformBy(mWPlane)
    
            Application.ShowAlertDialog("The first vertex has the following " & _
                                        "coordinates:" & _
                                        vbLf & "OCS: " + pFirstVer.ToString() & _
                                        vbLf & "WCS: " + pWCSPt.ToString())
    
            '' Save the new objects to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub TranslateCoordinates()
        ' Create a polyline in model space.
        Dim plineObj As AcadPolyline
        Dim points(0 To 14) As Double
     
        ' Define the 2D polyline points
        points(0) = 1: points(1) = 1: points(2) = 0
        points(3) = 1: points(4) = 2: points(5) = 0
        points(6) = 2: points(7) = 2: points(8) = 0
        points(9) = 3: points(10) = 2: points(11) = 0
        points(12) = 4: points(13) = 4: points(14) = 0
     
        ' Create a light weight Polyline object in model space
        Set plineObj = ThisDrawing.ModelSpace.AddPolyline(points)
     
        ' Find the X and Y coordinates of the
        ' first vertex of the polyline
        Dim firstVertex As Variant
        firstVertex = plineObj.Coordinate(0)
     
        ' Find the Z coordinate for the polyline
        ' using the elevation property
        firstVertex(2) = plineObj.Elevation
     
        ' Change the normal for the pline so that the
        ' difference between the coordinate systems
        ' is obvious.
        Dim plineNormal(0 To 2) As Double
        plineNormal(0) = 0#
        plineNormal(1) = 1#
        plineNormal(2) = 2#
        plineObj.Normal = plineNormal
     
        ' Translate the OCS coordinate into WCS
        Dim coordinateWCS As Variant
        coordinateWCS = ThisDrawing.Utility.TranslateCoordinates _
                            (firstVertex, acOCS, acWorld, False, plineNormal)
     
        ' Display the coordinates of the point
        MsgBox "The first vertex has the following coordinates:" _
               & vbCrLf & "OCS: (" & firstVertex(0) & "," & _
               firstVertex(1) & "," & firstVertex(2) & ")" & vbCrLf & _
               "WCS: (" & coordinateWCS(0) & "," & _
               coordinateWCS(1) & "," & coordinateWCS(2) & ")"
    End Sub
