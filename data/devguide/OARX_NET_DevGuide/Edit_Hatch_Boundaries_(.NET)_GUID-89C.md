<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Edit Named and 2D Objects (.NET) > Edit Hatches (.NET) > Edit Hatch Boundaries (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-89CAED67-B3A0-4045-9D8B-9034D67E8D91.htm -->

# Edit Hatch Boundaries (.NET)

You can append, insert, or remove loops from the boundaries of a Hatch object. Associative hatches are updated to match any changes made to their boundaries. Non-associative hatches are not updated. 

To edit a hatch boundary, use one of the following methods: 

AppendLoop
    

Appends a loop to the hatch. You define the type of loop being appended with first parameter of the AppendLoop method and the constants defined by the HatchLoopTypes enum. 

GetLoopAt
    

Gets the loop at a given index of a hatch. 

InsertLoopAt
    

Inserts a loop at a given index of a hatch. 

RemoveLoopAt
    

Deletes a loop at a given index of a hatch. 

To query a hatch boundary, use one of the following methods: 

LoopTypeAt
    

Gets the type of loop at a given index of a hatch. 

NumberOfLoops
    

Gets the number of loops of a hatch. 

## Append an inner loop to a hatch

This example creates an associative hatch. It then creates a circle and appends the circle as an inner loop to the hatch. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("EditHatchAppendLoop")]
    public static void EditHatchAppendLoop()
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
    
            // Create an arc object for the closed boundary to hatch
            using (Arc acArc = new Arc(new Point3d(5, 3, 0), 3, 0, 3.141592))
            {
    
                acBlkTblRec.AppendEntity(acArc);
                acTrans.AddNewlyCreatedDBObject(acArc, true);
    
                // Create an line object for the closed boundary to hatch
                using (Line acLine = new Line(acArc.StartPoint, acArc.EndPoint))
                {
                    acBlkTblRec.AppendEntity(acLine);
                    acTrans.AddNewlyCreatedDBObject(acLine, true);
    
                    // Adds the arc and line to an object id collection
                    ObjectIdCollection acObjIdColl = new ObjectIdCollection();
                    acObjIdColl.Add(acArc.ObjectId);
                    acObjIdColl.Add(acLine.ObjectId);
    
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
    
                        // Create a circle object for the inner boundary of the hatch
                        using (Circle acCirc = new Circle())
                        {
                            acCirc.Center = new Point3d(5, 4.5, 0);
                            acCirc.Radius = 1;
    
                            acBlkTblRec.AppendEntity(acCirc);
                            acTrans.AddNewlyCreatedDBObject(acCirc, true);
    
                            // Adds the circle to an object id collection
                            acObjIdColl.Clear();
                            acObjIdColl.Add(acCirc.ObjectId);
    
                            // Append the circle as the inner loop of the hatch and evaluate it
                            acHatch.AppendLoop(HatchLoopTypes.Default, acObjIdColl);
                            acHatch.EvaluateHatch(true);
                        }
                    }
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
     
    <CommandMethod("EditHatchAppendLoop")> _
    Public Sub EditHatchAppendLoop()
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
    
            '' Create an arc object for the closed boundary to hatch
            Using acArc As Arc = New Arc(New Point3d(5, 3, 0), 3, 0, 3.141592)
    
                acBlkTblRec.AppendEntity(acArc)
                acTrans.AddNewlyCreatedDBObject(acArc, True)
    
                '' Create an line object for the closed boundary to hatch
                Using acLine As Line = New Line(acArc.StartPoint, acArc.EndPoint)
    
                    acBlkTblRec.AppendEntity(acLine)
                    acTrans.AddNewlyCreatedDBObject(acLine, True)
    
                    '' Adds the arc and line to an object id collection
                    Dim acObjIdColl As ObjectIdCollection = New ObjectIdCollection()
                    acObjIdColl.Add(acArc.ObjectId)
                    acObjIdColl.Add(acLine.ObjectId)
    
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
    
                        '' Create a circle object for the inner boundary of the hatch
                        Using acCirc As Circle = New Circle()
                            acCirc.Center = New Point3d(5, 4.5, 0)
                            acCirc.Radius = 1
    
                            acBlkTblRec.AppendEntity(acCirc)
                            acTrans.AddNewlyCreatedDBObject(acCirc, True)
    
                            '' Adds the circle to an object id collection
                            acObjIdColl.Clear()
                            acObjIdColl.Add(acCirc.ObjectId)
    
                            '' Append the circle as the inner loop of the hatch and evaluate it
                            acHatch.AppendLoop(HatchLoopTypes.Default, acObjIdColl)
                            acHatch.EvaluateHatch(True)
                        End Using
                    End Using
                End Using
            End Using
    
            '' Save the new object to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub EditHatchAppendLoop()
        Dim hatchObj As AcadHatch
        Dim patternName As String
        Dim PatternType As Long
        Dim bAssociativity As Boolean
     
        ' Define and create the hatch
        patternName = "ANSI31"
        PatternType = 0
        bAssociativity = True
        Set hatchObj = ThisDrawing.ModelSpace. _
                           AddHatch(PatternType, patternName, bAssociativity)
     
        ' Create the outer loop for the hatch.
        Dim outerLoop(0 To 1) As AcadEntity
        Dim center(0 To 2) As Double
        Dim radius As Double
        Dim startAngle As Double
        Dim endAngle As Double
        center(0) = 5: center(1) = 3: center(2) = 0
        radius = 3
        startAngle = 0
        endAngle = 3.141592
        Set outerLoop(0) = ThisDrawing.ModelSpace. _
                               AddArc(center, radius, startAngle, endAngle)
        Set outerLoop(1) = ThisDrawing.ModelSpace. _
                               AddLine(outerLoop(0).startPoint, outerLoop(0).endPoint)
     
        ' Append the outer loop to the hatch object
        hatchObj.AppendOuterLoop (outerLoop)
     
        ' Create a circle as the inner loop for the hatch.
        Dim innerLoop(0) As AcadEntity
        center(0) = 5: center(1) = 4.5: center(2) = 0
        radius = 1
        Set innerLoop(0) = ThisDrawing.ModelSpace. _
                               AddCircle(center, radius)
     
        ' Append the circle as an inner loop to the hatch
        hatchObj.AppendInnerLoop (innerLoop)
     
        ' Evaluate and display the hatch
        hatchObj.Evaluate
        ThisDrawing.Regen True
    End Sub
