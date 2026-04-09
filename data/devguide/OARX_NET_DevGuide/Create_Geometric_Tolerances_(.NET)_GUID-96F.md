<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Dimensions and Tolerances (.NET) > Use Geometric Tolerances (.NET) > Create Geometric Tolerances (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-96F75668-7AC0-444A-92A8-297A9494743C.htm -->

# Create Geometric Tolerances (.NET)

You create a geometric tolerance by creating an instance of a FeatureControlFrame object. When you create an instance of a FeatureControlFrame object, its constructor can accept an optional set of parameters. The following parameters can be supplied when you create a new FeatureControlFrame object: 

  * Text string comprising the tolerance symbol (Text property) 
  * Insertion point (Location property) 
  * Normal vector (Normal property) 
  * Direction vector (Direction property) 

## Create a geometric tolerance

This example creates a simple geometric tolerance in Model space. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("CreateGeometricTolerance")]
    public static void CreateGeometricTolerance()
    {
        // Get the current database
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
    
            // Create the Geometric Tolerance (Feature Control Frame)
            using (FeatureControlFrame acFcf = new FeatureControlFrame())
            {
                acFcf.Text = "{\\Fgdt;j}%%v{\\Fgdt;n}0.001%%v%%v%%v%%v";
                acFcf.Location = new Point3d(5, 5, 0);
    
                // Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acFcf);
                acTrans.AddNewlyCreatedDBObject(acFcf, true);
            }
    
            // Commit the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("CreateGeometricTolerance")> _
    Public Sub CreateGeometricTolerance()
        '' Get the current database
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
    
            '' Create the Geometric Tolerance (Feature Control Frame)
            Using acFcf As FeatureControlFrame = New FeatureControlFrame()
                acFcf.Text = "{\Fgdt;j}%%v{\Fgdt;n}0.001%%v%%v%%v%%v"
                acFcf.Location = New Point3d(5, 5, 0)
    
                '' Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acFcf)
                acTrans.AddNewlyCreatedDBObject(acFcf, True)
            End Using
    
            '' Commit the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CreateGeometricTolerance()
        Dim toleranceObj As AcadTolerance
        Dim textString As String
        Dim insertionPoint(0 To 2) As Double
        Dim direction(0 To 2) As Double
     
        ' Define the tolerance object
        textString = "{\Fgdt;j}%%v{\Fgdt;n}0.001%%v%%v%%v%%v"
        insertionPoint(0) = 5
        insertionPoint(1) = 5
        insertionPoint(2) = 0
        direction(0) = 1
        direction(1) = 0
        direction(2) = 0
     
        ' Create the tolerance object in model space
        Set toleranceObj = ThisDrawing.ModelSpace. _
                               AddTolerance(textString, insertionPoint, direction)
     
        ZoomAll
    End Sub
