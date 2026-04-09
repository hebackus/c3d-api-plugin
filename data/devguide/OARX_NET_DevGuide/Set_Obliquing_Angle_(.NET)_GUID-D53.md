<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Add Text to Drawings (.NET) > Use Single-Line Text (.NET) > Format Single-Line Text (.NET) > Set Obliquing Angle (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-D53956B2-6014-468E-A420-455D8EC75BFF.htm -->

# Set Obliquing Angle (.NET)

The obliquing angle determines the forward or backward slant of the text. The angle represents the offset from its vertical axis (90 degrees). To set the obliquing angle, use the ObliquingAngle property to change a text style or the Oblique property of a text object. The obliquing angle must be provided in radians. A positive angle denotes a lean to the right, a negative value will have 2*PI added to it to convert it to its positive equivalent. 

## Create oblique text

This example creates a single-line text object then slants it 45 degrees. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("ObliqueText")]
    public static void ObliqueText()
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
    
            // Create a single-line text object
            using (DBText acText = new DBText())
            {
                acText.Position = new Point3d(3, 3, 0);
                acText.Height = 0.5;
                acText.TextString = "Hello, World.";
    
                // Change the oblique angle of the text object to 45 degrees(0.707 in radians)
                acText.Oblique = 0.707;
    
                acBlkTblRec.AppendEntity(acText);
                acTrans.AddNewlyCreatedDBObject(acText, true);
            }
    
            // Save the changes and dispose of the transaction
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("ObliqueText")> _
    Public Sub ObliqueText()
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
    
            '' Create a single-line text object
            Using acText As DBText = New DBText()
                acText.Position = New Point3d(3, 3, 0)
                acText.Height = 0.5
                acText.TextString = "Hello, World."
    
                '' Change the oblique angle of the text object to 45 degrees(0.707 in radians)
                acText.Oblique = 0.707
    
                acBlkTblRec.AppendEntity(acText)
                acTrans.AddNewlyCreatedDBObject(acText, True)
            End Using
    
            '' Save the changes and dispose of the transaction
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub ObliqueText()
        Dim textObj As AcadText
        Dim textString As String
        Dim insertionPoint(0 To 2) As Double
        Dim height As Double
     
        ' Define the text object
        textString = "Hello, World."
        insertionPoint(0) = 3
        insertionPoint(1) = 3
        insertionPoint(2) = 0
        height = 0.5
     
        ' Create the text object in model space
        Set textObj = ThisDrawing.ModelSpace. _
                          AddText(textString, insertionPoint, height)
     
        ' Change the value of the ObliqueAngle
        ' to 45 degrees (.707 radians)
        textObj.ObliqueAngle = 0.707
        textObj.Update
    End Sub
