<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Work in Three-Dimensional Space (.NET) > Specify 3D Coordinates (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-D6867645-8152-434A-A18C-4FC7920C3513.htm -->

# Specify 3D Coordinates (.NET)

Entering 3D world coordinate system (WCS) coordinates is similar to entering 2D WCS coordinates. In addition to specifying _X_ and _Y_ values, you specify a _Z_ value. 2D coordinates are represented by a Point2d object, while you use a Point3d object to represent 3D coordinates. Most properties and methods in the AutoCAD .NET API utilize 3D coordinates. 

## Define and query the coordinates for 2D and 3D polylines

This example creates two polylines, each with three coordinates. The first polyline is a 2D polyline, the second polyline is 3D. Notice that the length of the array containing the vertices is expanded to include the _Z_ coordinates in the creation of the 3D polyline. The example concludes by querying the coordinates of the polylines and displaying the coordinates in a message box. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("Polyline_2D_3D")]
    public static void Polyline_2D_3D()
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
    
            // Create a polyline with two segments (3 points)
            using (Polyline acPoly = new Polyline())
            {
                acPoly.AddVertexAt(0, new Point2d(1, 1), 0, 0, 0);
                acPoly.AddVertexAt(1, new Point2d(1, 2), 0, 0, 0);
                acPoly.AddVertexAt(2, new Point2d(2, 2), 0, 0, 0);
                acPoly.ColorIndex = 1;
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPoly);
                acTrans.AddNewlyCreatedDBObject(acPoly, true);
    
    
                // Create a 3D polyline with two segments (3 points)
                using (Polyline3d acPoly3d = new Polyline3d())
                {
                    acPoly3d.ColorIndex = 5;
    
                    // Add the new object to the block table record and the transaction
                    acBlkTblRec.AppendEntity(acPoly3d);
                    acTrans.AddNewlyCreatedDBObject(acPoly3d, true);
    
                    // Before adding vertexes, the polyline must be in the drawing
                    Point3dCollection acPts3dPoly = new Point3dCollection();
                    acPts3dPoly.Add(new Point3d(1, 1, 0));
                    acPts3dPoly.Add(new Point3d(2, 1, 0));
                    acPts3dPoly.Add(new Point3d(2, 2, 0));
    
                    foreach (Point3d acPt3d in acPts3dPoly)
                    {
                        using (PolylineVertex3d acPolVer3d = new PolylineVertex3d(acPt3d))
                        {
                            acPoly3d.AppendVertex(acPolVer3d);
                            acTrans.AddNewlyCreatedDBObject(acPolVer3d, true);
                        }
                    }
    
                    // Get the coordinates of the lightweight polyline
                    Point2dCollection acPts2d = new Point2dCollection();
                    for (int nCnt = 0; nCnt < acPoly.NumberOfVertices; nCnt++)
                    {
                        acPts2d.Add(acPoly.GetPoint2dAt(nCnt));
                    }
    
                    // Get the coordinates of the 3D polyline
                    Point3dCollection acPts3d = new Point3dCollection();
                    foreach (ObjectId acObjIdVert in acPoly3d)
                    {
                        PolylineVertex3d acPolVer3d;
                        acPolVer3d = acTrans.GetObject(acObjIdVert,
                                                        OpenMode.ForRead) as PolylineVertex3d;
    
                        acPts3d.Add(acPolVer3d.Position);
                    }
    
                    // Display the Coordinates
                    Application.ShowAlertDialog("2D polyline (red): \n" +
                                                acPts2d[0].ToString() + "\n" +
                                                acPts2d[1].ToString() + "\n" +
                                                acPts2d[2].ToString());
    
                    Application.ShowAlertDialog("3D polyline (blue): \n" +
                                                acPts3d[0].ToString() + "\n" +
                                                acPts3d[1].ToString() + "\n" +
                                                acPts3d[2].ToString());
                }
            }
    
            // Save the new object to the database
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("Polyline_2D_3D")> _
    Public Sub Polyline_2D_3D()
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
    
            '' Create a polyline with two segments (3 points)
            Using acPoly As Polyline = New Polyline()
                acPoly.AddVertexAt(0, New Point2d(1, 1), 0, 0, 0)
                acPoly.AddVertexAt(1, New Point2d(1, 2), 0, 0, 0)
                acPoly.AddVertexAt(2, New Point2d(2, 2), 0, 0, 0)
                acPoly.ColorIndex = 1
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acPoly)
                acTrans.AddNewlyCreatedDBObject(acPoly, True)
    
                '' Create a 3D polyline with two segments (3 points)
                Using acPoly3d As Polyline3d = New Polyline3d()
                    acPoly3d.ColorIndex = 5
    
                    '' Add the new object to the block table record and the transaction
                    acBlkTblRec.AppendEntity(acPoly3d)
                    acTrans.AddNewlyCreatedDBObject(acPoly3d, True)
    
                    '' Before adding vertexes, the polyline must be in the drawing
                    Dim acPts3dPoly As Point3dCollection = New Point3dCollection()
                    acPts3dPoly.Add(New Point3d(1, 1, 0))
                    acPts3dPoly.Add(New Point3d(2, 1, 0))
                    acPts3dPoly.Add(New Point3d(2, 2, 0))
    
                    For Each acPt3d As Point3d In acPts3dPoly
                        Using acPolVer3d As PolylineVertex3d = New PolylineVertex3d(acPt3d)
                            acPoly3d.AppendVertex(acPolVer3d)
                            acTrans.AddNewlyCreatedDBObject(acPolVer3d, True)
                        End Using
                    Next
    
                    '' Get the coordinates of the lightweight polyline
                    Dim acPts2d As Point2dCollection = New Point2dCollection()
                    For nCnt As Integer = 0 To acPoly.NumberOfVertices - 1
                        acPts2d.Add(acPoly.GetPoint2dAt(nCnt))
                    Next
    
                    '' Get the coordinates of the 3D polyline
                    Dim acPts3d As Point3dCollection = New Point3dCollection()
                    For Each acObjIdVert As ObjectId In acPoly3d
                        Dim acPolVer3d As PolylineVertex3d
                        acPolVer3d = acTrans.GetObject(acObjIdVert, _
                                                       OpenMode.ForRead)
    
                        acPts3d.Add(acPolVer3d.Position)
                    Next
    
                    '' Display the Coordinates
                    Application.ShowAlertDialog("2D polyline (red): " & vbLf & _
                                                acPts2d(0).ToString() & vbLf & _
                                                acPts2d(1).ToString() & vbLf & _
                                                acPts2d(2).ToString())
    
                    Application.ShowAlertDialog("3D polyline (blue): " & vbLf & _
                                                acPts3d(0).ToString() & vbLf & _
                                                acPts3d(1).ToString() & vbLf & _
                                                acPts3d(2).ToString())
                End Using
            End Using
    
            '' Save the new objects to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub Polyline_2D_3D()
        Dim pline2DObj As AcadLWPolyline
        Dim pline3DObj As AcadPolyline
     
        Dim points2D(0 To 5) As Double
        Dim points3D(0 To 8) As Double
     
        ' Define three 2D polyline points
        points2D(0) = 1: points2D(1) = 1
        points2D(2) = 1: points2D(3) = 2
        points2D(4) = 2: points2D(5) = 2
     
        ' Define three 3D polyline points
        points3D(0) = 1: points3D(1) = 1: points3D(2) = 0
        points3D(3) = 2: points3D(4) = 1: points3D(5) = 0
        points3D(6) = 2: points3D(7) = 2: points3D(8) = 0
     
        ' Create the 2D light weight Polyline
        Set pline2DObj = ThisDrawing.ModelSpace. _
                                          AddLightWeightPolyline(points2D)
        pline2DObj.Color = acRed
        pline2DObj.Update
     
        ' Create the 3D polyline
        Set pline3DObj = ThisDrawing.ModelSpace. _
                                          AddPolyline(points3D)
        pline3DObj.Color = acBlue
        pline3DObj.Update
     
        ' Query the coordinates of the polylines
        Dim get2Dpts As Variant
        Dim get3Dpts As Variant
     
        get2Dpts = pline2DObj.Coordinates
        get3Dpts = pline3DObj.Coordinates
     
        ' Display the coordinates
     
        MsgBox ("2D polyline (red): " & vbCrLf & "(" & _
                get2Dpts(0) & ", " & get2Dpts(1) & ")" & vbCrLf & "(" & _
                get2Dpts(2) & ", " & get2Dpts(3) & ")"& vbCrLf & "(" & _
                get2Dpts(4) & ", " & get2Dpts(5) & ")")
     
        MsgBox ("3D polyline (blue): " & vbCrLf & "(" & _
                get3Dpts(0) & ", " & get3Dpts(1) & ", " & _
                get3Dpts(2) & ")" & vbCrLf & "(" & _
                get3Dpts(3) & ", " & get3Dpts(4) & ", " & _
                get3Dpts(5) & ")" & vbCrLf & "(" & _
                get3Dpts(6) & ", " & get3Dpts(7) & ", " & _
                get3Dpts(8) & ")")
    End Sub
