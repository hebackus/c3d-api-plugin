<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Edit Hatches (.NET) > Edit Hatch Patterns (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-68CAD757-1857-4250-B92B-430318E5C110.htm -->

# Edit Hatch Patterns (.NET)

You can change the angle or spacing of an existing hatch pattern or replace it with a solid-fill, gradient fill, or one of the predefined patterns that AutoCAD offers. The Pattern option in the Boundary Hatch dialog box or Pattern gallery on the ribbon displays a list of these patterns. To reduce file size, the hatch is defined in the drawing as a single graphic object. 

Use the following properties and methods to edit the hatch patterns: 

GradientAngle
    

Specifies the gradient angle of the hatch. 

GradientName
    

Returns the gradient name of the hatch. 

GradientShift
    

Specifies the gradient shift of the hatch. 

GradientType
    

Returns the gradient type of the hatch. 

PatternAngle
    

Specifies the angle (in radians) of the hatch pattern. 

PatternDouble
    

Specifies if the user-defined hatch is double-hatched. 

PatternName
    

Returns the hatch pattern name of the hatch. (Use the SetHatchPattern method to set the hatch pattern name and type of the hatch.) 

PatternScale
    

Specifies the hatch pattern scale. 

PatternSpace
    

Specifies the user-defined hatch pattern spacing. 

PatternType
    

Returns the hatch pattern type of the hatch. (Use the SetHatchPattern method to set the hatch pattern name and type of the hatch.) 

SetGradient
    

Sets the gradient type and name for the hatch. 

SetHatchPattern
    

Sets the pattern type and name for the hatch. 

## Change the pattern spacing of a hatch

This example creates a hatch. It then adds two to the current pattern spacing for the hatch. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("EditHatchPatternScale")]
    public static void EditHatchPatternScale()
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
    
            // Create a circle object for the boundary of the hatch
            using (Circle acCirc = new Circle())
            {
                acCirc.Center = new Point3d(5, 3, 0);
                acCirc.Radius = 3;
    
                acBlkTblRec.AppendEntity(acCirc);
                acTrans.AddNewlyCreatedDBObject(acCirc, true);
    
                // Adds the arc and line to an object id collection
                ObjectIdCollection acObjIdColl = new ObjectIdCollection();
                acObjIdColl.Add(acCirc.ObjectId);
    
                // Create the hatch object and append it to the block table record
                using (Hatch acHatch = new Hatch())
                {
                    acBlkTblRec.AppendEntity(acHatch);
                    acTrans.AddNewlyCreatedDBObject(acHatch, true);
    
                    // Set the properties of the hatch object
                    // Associative must be set after the hatch object is appended to the 
                    // block table record and before AppendLoop
                    acHatch.SetHatchPattern(HatchPatternType.PreDefined, "ANSI31");
                    acHatch.Associative = true;
                    acHatch.AppendLoop(HatchLoopTypes.Outermost, acObjIdColl);
    
                    // Evaluate the hatch
                    acHatch.EvaluateHatch(true);
    
                    // Increase the pattern scale by 2 and re-evaluate the hatch
                    acHatch.PatternScale = acHatch.PatternScale + 2;
                    acHatch.SetHatchPattern(acHatch.PatternType, acHatch.PatternName);
                    acHatch.EvaluateHatch(true);
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
     
    <CommandMethod("EditHatchPatternScale")> _
    Public Sub EditHatchPatternScale()
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
    
            '' Create a circle object for the boundary of the hatch
            Using acCirc As Circle = New Circle()
                acCirc.Center = New Point3d(5, 3, 0)
                acCirc.Radius = 3
    
                acBlkTblRec.AppendEntity(acCirc)
                acTrans.AddNewlyCreatedDBObject(acCirc, True)
    
                '' Adds the arc and line to an object id collection
                Dim acObjIdColl As ObjectIdCollection = New ObjectIdCollection()
                acObjIdColl.Add(acCirc.ObjectId)
    
                '' Create the hatch object and append it to the block table record
                Using acHatch As Hatch = New Hatch()
                    acBlkTblRec.AppendEntity(acHatch)
                    acTrans.AddNewlyCreatedDBObject(acHatch, True)
    
                    '' Set the properties of the hatch object
                    '' Associative must be set after the hatch object is appended to the 
                    '' block table record and before AppendLoop
                    acHatch.SetHatchPattern(HatchPatternType.PreDefined, "ANSI31")
                    acHatch.Associative = True
                    acHatch.AppendLoop(HatchLoopTypes.Outermost, acObjIdColl)
    
                    '' Evaluate the hatch
                    acHatch.EvaluateHatch(True)
    
                    '' Increase the pattern scale by 2 and re-evaluate the hatch
                    acHatch.PatternScale = acHatch.PatternScale + 2
                    acHatch.SetHatchPattern(acHatch.PatternType, acHatch.PatternName)
                    acHatch.EvaluateHatch(True)
                End Using
            End Using
    
            '' Save the new object to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub EditHatchPatternScale()
        Dim hatchObj As AcadHatch
        Dim patternName As String
        Dim PatternType As Long
        Dim bAssociativity As Boolean
     
        ' Define the hatch
        patternName = "ANSI31"
        PatternType = 0
        bAssociativity = True
     
        ' Create the associative Hatch object
        Set hatchObj = ThisDrawing.ModelSpace. _
                           AddHatch(PatternType, patternName, bAssociativity)
     
        ' Create the outer loop for the hatch.
        Dim outerLoop(0 To 0) As AcadEntity
        Dim center(0 To 2) As Double
        Dim radius As Double
        center(0) = 5
        center(1) = 3
        center(2) = 0
        radius = 3
        Set outerLoop(0) = ThisDrawing.ModelSpace. _
                               AddCircle(center, radius)
        hatchObj.AppendOuterLoop (outerLoop)
        hatchObj.Evaluate
     
        ' Change the scale of the hatch pattern by
        ' adding 2 to the current scale
        hatchObj.patternScale = hatchObj.patternScale + 2
        hatchObj.Evaluate
        ThisDrawing.Regen True
    End Sub
