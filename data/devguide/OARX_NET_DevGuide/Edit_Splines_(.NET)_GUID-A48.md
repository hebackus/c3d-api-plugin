<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Edit Splines (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-A48AD068-9868-4F7A-8A51-F72A358EBB09.htm -->

# Edit Splines (.NET)

You can edit the properties of an open or closed spline, and even convert it to a polyline. Use the following properties to open or close a spline, change its control points, or reverse the direction of a spline: 

Degree
    

Returns the polynomial representation of the spline. 

EndFitTangent
    

Returns the end tangent of the spline as a directional vector. 

FitTolerance
    

Refits the spline to the existing points with new tolerance values. 

NumControlPoints
    

Returns the number of control points for the spline. 

NumFitPoints
    

Returns the number of fit points for the spline. 

StartFitTangent
    

Returns the start tangent for the spline. 

In addition, you can use the following methods to edit splines: 

InsertFitPointAt
    

Adds a single fit point to the spline at a given index. 

ElevateDegree
    

Increases the degree of the spline to the given degree. 

GetControlPointAt
    

Gets the control point of the spline at a given index. (Gets one control point only.) The NumControlPoints property contains the number of control points of the spline. 

GetFitPointAt
    

Gets the fit point of the spline at a given index. (Gets one fit point only. To query all the fit points of the spline, use the FitData property and then query the FitData object returned with its GetFitPoints member function.) The NumFitPoints property contains the number of fit points of the spline. 

RemoveFitPointAt
    

Deletes the fit point of a spline at a given index. 

ReverseCurve
    

Reverses the direction of a spline. 

SetControlPointAt
    

Sets the control point of the spline at a given index. 

SetFitPointAt
    

Sets the fit point of the spline at a given index. (Sets one fit point only. To change all the fit points of the spline, use the FitPoints property.) 

SetWeightAt
    

Sets the weight of the control point at a given index. 

Use the following read-only properties to query splines: 

Area
    

Gets the enclosed area of a spline. 

Closed
    

Indicates whether the spline is open or closed. 

Degree
    

Gets the degree of the spline's polynomial representation. 

IsPeriodic
    

Specifies if the given spline is periodic. 

IsPlanar
    

Specifies if the given spline is planar. 

IsRational
    

Specifies if the given spline is rational. 

NumControlPoints
    

Gets the number of control points of the spline. 

NumfFitPoints
    

Gets the number of fit points of the spline. 

## Change a control point on a spline

This example creates a spline and then changes the first control point for the spline. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("EditSpline")]
    public static void EditSpline()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Block table for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                         OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Model space for write
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                            OpenMode.ForWrite) as BlockTableRecord;
                    
            // Create a Point3d Collection
            Point3dCollection acPt3dColl = new Point3dCollection();
            acPt3dColl.Add(new Point3d(1, 1, 0));
            acPt3dColl.Add(new Point3d(5, 5, 0));
            acPt3dColl.Add(new Point3d(10, 0, 0));
    
            // Set the start and end tangency
            Vector3d acStartTan = new Vector3d(0.5, 0.5, 0);
            Vector3d acEndTan = new Vector3d(0.5, 0.5, 0);
    
            // Create a spline
            using (Spline acSpline = new Spline(acPt3dColl,
                                                acStartTan,
                                                acEndTan, 4, 0))
            {
    
                // Set a control point
                acSpline.SetControlPointAt(0, new Point3d(0, 3, 0));
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acSpline);
                acTrans.AddNewlyCreatedDBObject(acSpline, true);
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
     
    <CommandMethod("EditSpline")> _
    Public Sub EditSpline()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                         OpenMode.ForRead)
    
            '' Open the Block table record Model space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForWrite)
    
            '' Create a Point3d Collection
            Dim acPt3dColl As Point3dCollection = New Point3dCollection()
            acPt3dColl.Add(New Point3d(1, 1, 0))
            acPt3dColl.Add(New Point3d(5, 5, 0))
            acPt3dColl.Add(New Point3d(10, 0, 0))
    
            '' Set the start and end tangency
            Dim acStartTan As Vector3d = New Vector3d(0.5, 0.5, 0)
            Dim acEndTan As Vector3d = New Vector3d(0.5, 0.5, 0)
    
            '' Create a spline
            Using acSpline As Spline = New Spline(acPt3dColl, _
                                                  acStartTan, _
                                                  acEndTan, 4, 0)
    
                '' Set a control point
                acSpline.SetControlPointAt(0, New Point3d(0, 3, 0))
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acSpline)
                acTrans.AddNewlyCreatedDBObject(acSpline, True)
            End Using
    
            '' Save the new objects to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub EditSpline()
        ' Create the spline
        Dim splineObj As AcadSpline
        Dim startTan(0 To 2) As Double
        Dim endTan(0 To 2) As Double
        Dim fitPoints(0 To 8) As Double
     
        startTan(0) = 0.5: startTan(1) = 0.5: startTan(2) = 0
        endTan(0) = 0.5: endTan(1) = 0.5: endTan(2) = 0
        fitPoints(0) = 1: fitPoints(1) = 1: fitPoints(2) = 0
        fitPoints(3) = 5: fitPoints(4) = 5: fitPoints(5) = 0
        fitPoints(6) = 10: fitPoints(7) = 0: fitPoints(8) = 0
        Set splineObj = ThisDrawing.ModelSpace. _
                                      AddSpline(fitPoints, startTan, endTan)
        splineObj.Update
     
        ' Change the coordinate of the first fit point
        Dim controlPoint(0 To 2) As Double
        controlPoint(0) = 0
        controlPoint(1) = 3
        controlPoint(2) = 0
        splineObj.SetControlPoint 0, controlPoint
        splineObj.Update
    End Sub
