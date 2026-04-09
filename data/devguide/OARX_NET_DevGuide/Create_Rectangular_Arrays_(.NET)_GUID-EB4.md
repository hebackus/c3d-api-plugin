<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Array Objects (.NET) > Create Rectangular Arrays (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-EB4639C2-4BCB-46DA-A00D-07FB443BBF0A.htm -->

# Create Rectangular Arrays (.NET)

This example creates a circle and then performs a rectangular array of the circle, creating five rows and five columns of circles. 

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
     
    [CommandMethod("RectangularArrayObject")]
    public static void RectangularArrayObject()
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
    
            // Create a circle that is at 2,2 with a radius of 0.5
            using (Circle acCirc = new Circle())
            {
                acCirc.Center = new Point3d(2, 2, 0);
                acCirc.Radius = 0.5;
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acCirc);
                acTrans.AddNewlyCreatedDBObject(acCirc, true);
    
                // Create a rectangular array with 5 rows and 5 columns
                int nRows = 5;
                int nColumns = 5;
    
                // Set the row and column offsets along with the base array angle
                double dRowOffset = 1;
                double dColumnOffset = 1;
                double dArrayAng = 0;
    
                // Get the angle from X for the current UCS 
                Matrix3d curUCSMatrix = acDoc.Editor.CurrentUserCoordinateSystem;
                CoordinateSystem3d curUCS = curUCSMatrix.CoordinateSystem3d;
                Vector2d acVec2dAng = new Vector2d(curUCS.Xaxis.X,
                                                   curUCS.Xaxis.Y);
    
                // If the UCS is rotated, adjust the array angle accordingly
                dArrayAng = dArrayAng + acVec2dAng.Angle;
    
                // Use the upper-left corner of the objects extents for the array base point
                Extents3d acExts = acCirc.Bounds.GetValueOrDefault();
                Point2d acPt2dArrayBase = new Point2d(acExts.MinPoint.X,
                                                      acExts.MaxPoint.Y);
    
                // Track the objects created for each column
                DBObjectCollection acDBObjCollCols = new DBObjectCollection();
                acDBObjCollCols.Add(acCirc);
    
                // Create the number of objects for the first column
                int nColumnsCount = 1;
                while (nColumns > nColumnsCount)
                {
                    Entity acEntClone = acCirc.Clone() as Entity;
                    acDBObjCollCols.Add(acEntClone);
    
                    // Caclucate the new point for the copied object (move)
                    Point2d acPt2dTo = PolarPoints(acPt2dArrayBase,
                                                   dArrayAng,
                                                   dColumnOffset * nColumnsCount);
    
                    Vector2d acVec2d = acPt2dArrayBase.GetVectorTo(acPt2dTo);
                    Vector3d acVec3d = new Vector3d(acVec2d.X, acVec2d.Y, 0);
                    acEntClone.TransformBy(Matrix3d.Displacement(acVec3d));
    
                    acBlkTblRec.AppendEntity(acEntClone);
                    acTrans.AddNewlyCreatedDBObject(acEntClone, true);
    
                    nColumnsCount = nColumnsCount + 1;
                }
    
                // Set a value in radians for 90 degrees
                double dAng = Math.PI / 2;
    
                // Track the objects created for each row and column
                DBObjectCollection acDBObjCollLvls = new DBObjectCollection();
    
                foreach (DBObject acObj in acDBObjCollCols)
                {
                    acDBObjCollLvls.Add(acObj);
                }
    
                // Create the number of objects for each row
                foreach (Entity acEnt in acDBObjCollCols)
                {
                    int nRowsCount = 1;
    
                    while (nRows > nRowsCount)
                    {
                        Entity acEntClone = acEnt.Clone() as Entity;
                        acDBObjCollLvls.Add(acEntClone);
    
                        // Caclucate the new point for the copied object (move)
                        Point2d acPt2dTo = PolarPoints(acPt2dArrayBase,
                                                       dArrayAng + dAng,
                                                       dRowOffset * nRowsCount);
    
                        Vector2d acVec2d = acPt2dArrayBase.GetVectorTo(acPt2dTo);
                        Vector3d acVec3d = new Vector3d(acVec2d.X, acVec2d.Y, 0);
                        acEntClone.TransformBy(Matrix3d.Displacement(acVec3d));
    
                        acBlkTblRec.AppendEntity(acEntClone);
                        acTrans.AddNewlyCreatedDBObject(acEntClone, true);
    
                        nRowsCount = nRowsCount + 1;
                    }
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
     
    <CommandMethod("RectangularArrayObject")> _
    Public Sub RectangularArrayObject()
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
    
            '' Create a circle that is at 2,2 with a radius of 0.5
            Using acCirc As Circle = New Circle()
                acCirc.Center = New Point3d(2, 2, 0)
                acCirc.Radius = 0.5
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acCirc)
                acTrans.AddNewlyCreatedDBObject(acCirc, True)
    
                '' Create a rectangular array with 5 rows and 5 columns
                Dim nRows As Integer = 5
                Dim nColumns As Integer = 5
    
                '' Set the row and column offsets along with the base array angle
                Dim dRowOffset As Double = 1
                Dim dColumnOffset As Double = 1
                Dim dArrayAng As Double = 0
    
                '' Get the angle from X for the current UCS 
                Dim curUCSMatrix As Matrix3d = acDoc.Editor.CurrentUserCoordinateSystem
                Dim curUCS As CoordinateSystem3d = curUCSMatrix.CoordinateSystem3d
                Dim acVec2dAng As Vector2d = New Vector2d(curUCS.Xaxis.X, _
                                                          curUCS.Xaxis.Y)
    
                '' If the UCS is rotated, adjust the array angle accordingly
                dArrayAng = dArrayAng + acVec2dAng.Angle
    
                '' Use the upper-left corner of the objects extents for the array base point
                Dim acExts As Extents3d = acCirc.Bounds.GetValueOrDefault()
                Dim acPt2dArrayBase As Point2d = New Point2d(acExts.MinPoint.X, _
                                                             acExts.MaxPoint.Y)
    
                '' Track the objects created for each column
                Dim acDBObjCollCols As DBObjectCollection = New DBObjectCollection()
                acDBObjCollCols.Add(acCirc)
    
                '' Create the number of objects for the first column
                Dim nColumnsCount As Integer = 1
                While (nColumns > nColumnsCount)
                    Dim acEntClone As Entity = acCirc.Clone()
                    acDBObjCollCols.Add(acEntClone)
    
                    '' Caclucate the new point for the copied object (move)
                    Dim acPt2dTo As Point2d = PolarPoints(acPt2dArrayBase, _
                                                          dArrayAng, _
                                                          dColumnOffset * nColumnsCount)
    
                    Dim acVec2d As Vector2d = acPt2dArrayBase.GetVectorTo(acPt2dTo)
                    Dim acVec3d As Vector3d = New Vector3d(acVec2d.X, acVec2d.Y, 0)
                    acEntClone.TransformBy(Matrix3d.Displacement(acVec3d))
    
                    acBlkTblRec.AppendEntity(acEntClone)
                    acTrans.AddNewlyCreatedDBObject(acEntClone, True)
    
                    nColumnsCount = nColumnsCount + 1
                End While
    
                '' Set a value in radians for 90 degrees
                Dim dAng As Double = Math.PI / 2
    
                '' Track the objects created for each row and column
                Dim acDBObjCollLvls As DBObjectCollection = New DBObjectCollection()
    
                For Each acObj As DBObject In acDBObjCollCols
                    acDBObjCollLvls.Add(acObj)
                Next
    
                '' Create the number of objects for each row
                For Each acEnt As Entity In acDBObjCollCols
                    Dim nRowsCount As Integer = 1
    
                    While (nRows > nRowsCount)
                        Dim acEntClone As Entity = acEnt.Clone()
                        acDBObjCollLvls.Add(acEntClone)
    
                        '' Caclucate the new point for the copied object (move)
                        Dim acPt2dTo As Point2d = PolarPoints(acPt2dArrayBase, _
                                                              dArrayAng + dAng, _
                                                              dRowOffset * nRowsCount)
    
                        Dim acVec2d As Vector2d = acPt2dArrayBase.GetVectorTo(acPt2dTo)
                        Dim acVec3d As Vector3d = New Vector3d(acVec2d.X, acVec2d.Y, 0)
                        acEntClone.TransformBy(Matrix3d.Displacement(acVec3d))
    
                        acBlkTblRec.AppendEntity(acEntClone)
                        acTrans.AddNewlyCreatedDBObject(acEntClone, True)
    
                        nRowsCount = nRowsCount + 1
                    End While
                Next
            End Using
    
            '' Save the new objects to the database
            acTrans.Commit()
        End Using
    End Sub

## VBA/ActiveX Code Reference
    
    
    Sub RectangularArrayObject()
        ' Create the circle
        Dim circleObj As AcadCircle
        Dim center(0 To 2) As Double
        Dim radius As Double
        center(0) = 2#: center(1) = 2#: center(2) = 0#
        radius = 0.5
        Set circleObj = ThisDrawing.ModelSpace. _
                                      AddCircle(center, radius)
        ZoomAll
     
        ' Define the rectangular array
        Dim numberOfRows As Long
        Dim numberOfColumns As Long
        Dim numberOfLevels As Long
        Dim distanceBwtnRows As Double
        Dim distanceBwtnColumns As Double
        Dim distanceBwtnLevels As Double
        numberOfRows = 5
        numberOfColumns = 5
        numberOfLevels = 0
        distanceBwtnRows = 1
        distanceBwtnColumns = 1
        distanceBwtnLevels = 0
     
        ' Create the array of objects
        Dim retObj As Variant
        retObj = circleObj.ArrayRectangular _
                      (numberOfRows, numberOfColumns, numberOfLevels, _
                       distanceBwtnRows, distanceBwtnColumns, distanceBwtnLevels)
     
        ZoomAll
    End Sub
