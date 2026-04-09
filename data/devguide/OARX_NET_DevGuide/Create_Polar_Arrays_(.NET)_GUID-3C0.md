<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Array Objects (.NET) > Create Polar Arrays (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-3C0954E5-CBFE-4A37-A88F-E8941434D72D.htm -->

# Create Polar Arrays (.NET)

This example creates a circle, and then performs a polar array of the circle. This creates four circles filling 180 degrees around a base point of (4, 4, 0). 

## C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    static Point2d PolarPoints(Point2d pPt, double dAng, double dDist)
    {
      return new Point2d(pPt.X + dDist * Math.Cos(dAng),
                         pPt.Y + dDist * Math.Sin(dAng));
    }
     
    [CommandMethod("PolarArrayObject")]
    public static void PolarArrayObject()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
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
    
            // Create a circle that is at 2,2 with a radius of 1
            using (Circle acCirc = new Circle())
            {
                acCirc.Center = new Point3d(2, 2, 0);
                acCirc.Radius = 1;
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acCirc);
                acTrans.AddNewlyCreatedDBObject(acCirc, true);
    
                // Create a 4 object polar array that goes a 180
                int nCount = 1;
    
                // Set a value in radians for 60 degrees
                double dAng = 1.0472;
    
                // Use (4,4,0) as the base point for the array
                Point2d acPt2dArrayBase = new Point2d(4, 4);
    
                while (nCount < 4)
                {
                    Entity acEntClone = acCirc.Clone() as Entity;
    
                    Extents3d acExts;
                    Point2d acPtObjBase;
    
                    // Typically the upper-left corner of an object's extents is used
                    // for the point on the object to be arrayed unless it is
                    // an object like a circle.
                    Circle acCircArrObj = acEntClone as Circle;
    
                    if (acCircArrObj != null)
                    {
                        acPtObjBase = new Point2d(acCircArrObj.Center.X,
                                                  acCircArrObj.Center.Y);
                    }
                    else
                    {
                        acExts = acEntClone.Bounds.GetValueOrDefault();
                        acPtObjBase = new Point2d(acExts.MinPoint.X,
                                                  acExts.MaxPoint.Y);
                    }
    
                    double dDist = acPt2dArrayBase.GetDistanceTo(acPtObjBase);
                    double dAngFromX = acPt2dArrayBase.GetVectorTo(acPtObjBase).Angle;
    
                    Point2d acPt2dTo = PolarPoints(acPt2dArrayBase,
                                                   (nCount * dAng) + dAngFromX,
                                                   dDist);
    
                    Vector2d acVec2d = acPtObjBase.GetVectorTo(acPt2dTo);
                    Vector3d acVec3d = new Vector3d(acVec2d.X, acVec2d.Y, 0);
                    acEntClone.TransformBy(Matrix3d.Displacement(acVec3d));
    
                    /*
                    // The following code demonstrates how to rotate each object like
                    // the ARRAY command does.
                    acExts = acEntClone.Bounds.GetValueOrDefault();
                    acPtObjBase = new Point2d(acExts.MinPoint.X,
                                              acExts.MaxPoint.Y);
                    
                    // Rotate the cloned entity around its upper-left extents point
                    Matrix3d curUCSMatrix = acDoc.Editor.CurrentUserCoordinateSystem;
                    CoordinateSystem3d curUCS = curUCSMatrix.CoordinateSystem3d;
                    acEntClone.TransformBy(Matrix3d.Rotation(nCount * dAng,
                                                             curUCS.Zaxis,
                                                             new Point3d(acPtObjBase.X,
                                                                         acPtObjBase.Y, 0)));
                    */
    
                    acBlkTblRec.AppendEntity(acEntClone);
                    acTrans.AddNewlyCreatedDBObject(acEntClone, true);
    
                    nCount = nCount + 1;
                }
            }
    
            // Save the new objects to the database
            acTrans.Commit();
        }
    }

## VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    Public Shared Function PolarPoints(ByVal pPt As Point2d, _
                                       ByVal dAng As Double, _
                                       ByVal dDist As Double)
     
      Return New Point2d(pPt.X + dDist * Math.Cos(dAng), _
                         pPt.Y + dDist * Math.Sin(dAng))
    End Function
     
    <CommandMethod("PolarArrayObject")> _
    Public Sub PolarArrayObject()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Block table record for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                         OpenMode.ForRead)
    
            '' Open the Block table record Model space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForWrite)
    
            '' Create a circle that is at 2,2 with a radius of 1
            Using acCirc As Circle = New Circle()
                acCirc.Center = New Point3d(2, 2, 0)
                acCirc.Radius = 1
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acCirc)
                acTrans.AddNewlyCreatedDBObject(acCirc, True)
    
                '' Create a 4 object polar array that goes a 180
                Dim nCount As Integer = 1
    
                '' Set a value in radians for 60 degrees
                Dim dAng As Double = 1.0472
    
                '' Use (4,4,0) as the base point for the array
                Dim acPt2dArrayBase As Point2d = New Point2d(4, 4)
    
                While (nCount < 4)
                    Dim acEntClone As Entity = acCirc.Clone()
    
                    Dim acExts As Extents3d
                    Dim acPtObjBase As Point2d
    
                    '' Typically the upper-left corner of an object's extents is used
                    '' for the point on the object to be arrayed unless it is
                    '' an object like a circle.
                    Dim acCircArrObj As Circle = acEntClone
    
                    If IsDBNull(acCircArrObj) = False Then
                         acPtObjBase = New Point2d(acCircArrObj.Center.X, _
                                                   acCircArrObj.Center.Y)
                    Else
                         acExts = acEntClone.Bounds.GetValueOrDefault()
                         acPtObjBase = New Point2d(acExts.MinPoint.X, _
                                                   acExts.MaxPoint.Y)
                    End If
    
                    Dim dDist As Double = acPt2dArrayBase.GetDistanceTo(acPtObjBase)
                    Dim dAngFromX As Double = acPt2dArrayBase.GetVectorTo(acPtObjBase).Angle
    
                    Dim acPt2dTo As Point2d = PolarPoints(acPt2dArrayBase, _
                                                          (nCount * dAng) + dAngFromX, _
                                                          dDist)
    
                    Dim acVec2d As Vector2d = acPtObjBase.GetVectorTo(acPt2dTo)
                    Dim acVec3d As Vector3d = New Vector3d(acVec2d.X, acVec2d.Y, 0)
                    acEntClone.TransformBy(Matrix3d.Displacement(acVec3d))
    
                    '' The following code demonstrates how to rotate each object like
                    '' the ARRAY command does.
                    'acExts = acEntClone.Bounds.GetValueOrDefault()
                    'acPtObjBase = New Point2d(acExts.MinPoint.X, _
                    '                          acExts.MaxPoint.Y)
                    '
                    '' Rotate the cloned entity and around its upper-left extents point
                    'Dim curUCSMatrix As Matrix3d = acDoc.Editor.CurrentUserCoordinateSystem
                    'Dim curUCS As CoordinateSystem3d = curUCSMatrix.CoordinateSystem3d
                    'acEntClone.TransformBy(Matrix3d.Rotation(nCount * dAng, _
                    '                                         curUCS.Zaxis, _
                    '                                         New Point3d(acPtObjBase.X, _
                    '                                                     acPtObjBase.Y, 0)))
    
                    acBlkTblRec.AppendEntity(acEntClone)
                    acTrans.AddNewlyCreatedDBObject(acEntClone, True)
    
                    nCount = nCount + 1
                End While
            End Using
    
            '' Save the new objects to the database
            acTrans.Commit()
        End Using
    End Sub

## VBA/ActiveX Code Reference
    
    
    Sub PolarArrayObject()
        ' Create the circle
        Dim circleObj As AcadCircle
        Dim center(0 To 2) As Double
        Dim radius As Double
        center(0) = 2#: center(1) = 2#: center(2) = 0#
        radius = 1
        Set circleObj = ThisDrawing.ModelSpace. _
                                      AddCircle(center, radius)
        ZoomAll
     
        ' Define the polar array
        Dim noOfObjects As Integer
        Dim angleToFill As Double
        Dim basePnt(0 To 2) As Double
        noOfObjects = 4
        angleToFill = 3.14          ' 180 degrees
        basePnt(0) = 4#: basePnt(1) = 4#: basePnt(2) = 0#
     
        ' The following example will create 4 copies
        ' of an object by rotating and copying it about
        ' the point (4,4,0).
        Dim retObj As Variant
        retObj = circleObj.ArrayPolar _
                             (noOfObjects, angleToFill, basePnt)
     
        ZoomAll
    End Sub
