<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Colors (.NET) > Assign a Color Value to an Object (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-8ABF5190-C179-4D45-9473-3C78897D352E.htm -->

# Assign a Color Value to an Object (.NET)

The following example creates four circles and assigns a different color to each circle using four different methods. 

## C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    using Autodesk.AutoCAD.Colors;
     
    [CommandMethod("SetObjectColor")]
    public static void SetObjectColor()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Define an array of colors for the layers
            Color[] acColors = new Color[3];
            acColors[0] = Color.FromColorIndex(ColorMethod.ByAci, 1);
            acColors[1] = Color.FromRgb(23, 54, 232);
            acColors[2] = Color.FromNames("PANTONE Yellow 0131 C",
                                          "PANTONE(R) pastel coated");
    
            // Open the Block table for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                         OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Model space for write
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                            OpenMode.ForWrite) as BlockTableRecord;
    
            // Create a circle object and assign it the ACI value of 4
            Point3d acPt = new Point3d(0, 3, 0);
            using (Circle acCirc = new Circle())
            {
                acCirc.Center = acPt;
                acCirc.Radius = 1;
                acCirc.ColorIndex = 4;
    
                acBlkTblRec.AppendEntity(acCirc);
                acTrans.AddNewlyCreatedDBObject(acCirc, true);
    
                int nCnt = 0;
    
                while (nCnt < 3)
                {
                    // Create a copy of the circle
                    Circle acCircCopy;
                    acCircCopy = acCirc.Clone() as Circle;
    
                    // Shift the copy along the Y-axis
                    acPt = new Point3d(acPt.X, acPt.Y + 3, acPt.Z);
                    acCircCopy.Center = acPt;
    
                    // Assign the new color to the circle
                    acCircCopy.Color = acColors[nCnt];
    
                    acBlkTblRec.AppendEntity(acCircCopy);
                    acTrans.AddNewlyCreatedDBObject(acCircCopy, true);
    
                    nCnt = nCnt + 1;
                }
            }
    
            // Save the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

## VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    Imports Autodesk.AutoCAD.Colors
     
    <CommandMethod("SetObjectColor")> _
    Public Sub SetObjectColor()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Define an array of colors for the layers
            Dim acColors(2) As Color
            acColors(0) = Color.FromColorIndex(ColorMethod.ByAci, 1)
            acColors(1) = Color.FromRgb(23, 54, 232)
            acColors(2) = Color.FromNames("PANTONE Yellow 0131 C", _
                                          "PANTONE(R) pastel coated")
    
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                         OpenMode.ForRead)
    
            '' Open the Block table record Model space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForWrite)
    
            '' Create a circle object and assign it the ACI value of 4
            Dim acPt As Point3d = New Point3d(0, 3, 0)
            Using acCirc As Circle = New Circle()
                acCirc.Center = acPt
                acCirc.Radius = 1
                acCirc.ColorIndex = 4
    
                acBlkTblRec.AppendEntity(acCirc)
                acTrans.AddNewlyCreatedDBObject(acCirc, True)
    
                Dim nCnt As Integer = 0
    
                While (nCnt < 3)
                    '' Create a copy of the circle
                    Dim acCircCopy As Circle
                    acCircCopy = acCirc.Clone()
    
                    '' Shift the copy along the Y-axis
                    acPt = New Point3d(acPt.X, acPt.Y + 3, acPt.Z)
                    acCircCopy.Center = acPt
    
                    '' Assign the new color to the circle
                    acCircCopy.Color = acColors(nCnt)
    
                    acBlkTblRec.AppendEntity(acCircCopy)
                    acTrans.AddNewlyCreatedDBObject(acCircCopy, True)
    
                    nCnt = nCnt + 1
                End While
            End Using
    
            '' Save the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

## VBA/ActiveX Code Reference
    
    
    Sub SetObjectColor()
        ' Define an array of colors
        Dim colorObj(2) As New AcadAcCmColor
     
        colorObj(0).ColorMethod = acColorMethodByACI
        colorObj(0).ColorIndex = acRed
        Call colorObj(1).SetRGB(23, 54, 232)
        Call colorObj(2).SetColorBookColor("PANTONE(R) pastel coated", _
                                           "PANTONE Yellow 0131 C")
     
        ' Define the center point of the circle
        Dim centerPt(0 To 2) As Double
        centerPt(0) = 0: centerPt(1) = 3: centerPt(2) = 0
     
        ' Create a new circle and assign it the ACI value of 4
        Dim circleObj As AcadCircle
        Set circleObj = ThisDrawing.ModelSpace.AddCircle(centerPt, 1)
        circleObj.color = acCyan
     
        Dim nCnt As Integer
     
        ' Create 3 more circles
        While (nCnt < 3)
           ' Create a copy of the circle
           Dim circleObjCopy As AcadCircle
           Set circleObjCopy = circleObj.Copy
     
           ' Shift the copy along the Y-axis
           centerPt(1) = centerPt(1) + 3
           circleObjCopy.Center = centerPt
     
           ' Assign the new color to the circle
           circleObjCopy.TrueColor = colorObj(nCnt)
     
           nCnt = nCnt + 1
        Wend
    End Sub
