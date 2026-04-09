<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Linetypes (.NET) > Make a Linetype Active (.NET) > Assign a Linetype to an Object (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-5CD59567-BE5C-4E7E-8ADB-E6802FFDBEFE.htm -->

# Assign a Linetype to an Object (.NET)

The following example creates a circle and assigns the “Center” linetype to it. 

## C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("SetObjectLinetype")]
    public static void SetObjectLinetype()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Linetype table for read
            LinetypeTable acLineTypTbl;
            acLineTypTbl = acTrans.GetObject(acCurDb.LinetypeTableId,
                                             OpenMode.ForRead) as LinetypeTable;
    
            string sLineTypName = "Center";
    
            if (acLineTypTbl.Has(sLineTypName) == false)
            {
                acCurDb.LoadLineTypeFile(sLineTypName, "acad.lin");
            }
    
            // Open the Block table for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                         OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Model space for write
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                            OpenMode.ForWrite) as BlockTableRecord;
    
            // Create a circle object
            using (Circle acCirc = new Circle())
            {
                acCirc.Center = new Point3d(2, 2, 0);
                acCirc.Radius = 1;
                acCirc.Linetype = sLineTypName;
    
                acBlkTblRec.AppendEntity(acCirc);
                acTrans.AddNewlyCreatedDBObject(acCirc, true);
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
     
    <CommandMethod("SetObjectLinetype")> _
    Public Sub SetObjectLinetype()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Linetype table for read
            Dim acLineTypTbl As LinetypeTable
            acLineTypTbl = acTrans.GetObject(acCurDb.LinetypeTableId, _
                                             OpenMode.ForRead)
    
            Dim sLineTypName As String = "Center"
    
            If acLineTypTbl.Has(sLineTypName) = False Then
                acCurDb.LoadLineTypeFile(sLineTypName, "acad.lin")
            End If
    
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                         OpenMode.ForRead)
    
            '' Open the Block table record Model space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForWrite)
    
            '' Create a circle object
            Using acCirc As Circle = New Circle()
                acCirc.Center = New Point3d(2, 2, 0)
                acCirc.Radius = 1
                acCirc.Linetype = sLineTypName
    
                acBlkTblRec.AppendEntity(acCirc)
                acTrans.AddNewlyCreatedDBObject(acCirc, True)
            End Using
    
            '' Save the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

## VBA/ActiveX Code Reference
    
    
    Sub SetObjectLinetype()
        ' Load the Center linetype
        Dim linetypeName As String
        linetypeName = "Center"
     
        On Error Resume Next
        ThisDrawing.Linetypes.Load linetypeName, "acad.lin"
     
        ' Define the center point of the circle
        Dim centerPt(0 To 2) As Double
        centerPt(0) = 0: centerPt(1) = 3: centerPt(2) = 0
     
        ' Create a new circle and assign it the ACI value of 4
        Dim circleObj As AcadCircle
        Set circleObj = ThisDrawing.ModelSpace.AddCircle(centerPt, 1)
        circleObj.Linetype = linetypeName
     
        circleObj.Update
    End Sub
