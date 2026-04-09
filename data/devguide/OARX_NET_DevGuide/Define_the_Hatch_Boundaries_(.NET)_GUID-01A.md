<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Create Objects (.NET) > Create Hatches (.NET) > Define the Hatch Boundaries (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-01A47A4F-9FC5-4DB6-8C3E-B72D75688965.htm -->

# Define the Hatch Boundaries (.NET)

Once the Hatch object is created, the hatch boundaries can be added. Boundaries can be any combination of lines, arcs, circles, 2D polylines, ellipses, splines, and regions. 

The first boundary added must be the outer boundary, which defines the outermost limits to be filled by the hatch. To add the outer boundary, use the AppendLoop method with the HatchLoopTypes.Outermost constant for the type of loop to append. 

Once the outer boundary is defined, you can continue adding additional boundaries. Add inner boundaries using the AppendLoop method with the HatchLoopTypes.Default constant. 

Inner boundaries define islands within the hatch. How these islands are handled by the Hatch object depends on the setting of the HatchStyle property. The HatchStyle property can be set to one of the following conditions: 

Hatch style definitions   
---  
HatchStyle  |  Condition  |  Description   
|  Normal  (HatchStyle.Normal)  |  Specifies standard style, or normal. This option hatches inward from the outermost area boundary. If AutoCAD encounters an internal boundary, it turns off hatching until it encounters another boundary. This is the default setting for the HatchStyle property.   
|  Outer  (HatchStyle.Outer)  |  Fills the outermost areas only. This style also hatches inward from the area boundary, but it turns off hatching if it encounters an internal boundary and does not turn it back on again.   
|  Ignore  (HatchStyle.Ignore)  |  Ignores internal structure. This option hatches through all internal objects.   
  
When you have finished defining the hatch it must be evaluated before it can be displayed. Use the EvaluateHatch method to do this. 

## Create a Hatch object

The following example creates an associated hatch in Model space. Once the hatch has been created, you can change the size of the circle that the hatch is associated with. The hatch will change to match the size of the circle. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("AddHatch")]
    public static void AddHatch()
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
    
            // Create a circle object for the closed boundary to hatch
            using (Circle acCirc = new Circle())
            {
                acCirc.Center = new Point3d(3, 3, 0);
                acCirc.Radius = 1;
    
                // Add the new circle object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acCirc);
                acTrans.AddNewlyCreatedDBObject(acCirc, true);
    
                // Adds the circle to an object id array
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
     
    <CommandMethod("AddHatch")> _
    Public Sub AddHatch()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, OpenMode.ForRead)
    
            '' Open the Block table record Model space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                            OpenMode.ForWrite)
    
            '' Create a circle object for the closed boundary to hatch
            Using acCirc As Circle = New Circle()
                acCirc.Center = New Point3d(3, 3, 0)
                acCirc.Radius = 1
    
                '' Add the new circle object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acCirc)
                acTrans.AddNewlyCreatedDBObject(acCirc, True)
    
                '' Adds the circle to an object id array
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
                    acHatch.EvaluateHatch(True)
                End Using
            End Using
    
            '' Save the new object to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub AddHatch()
        Dim hatchObj As AcadHatch
        Dim patternName As String
        Dim PatternType As Long
        Dim bAssociativity As Boolean
     
        ' Define the hatch
        patternName = "ANSI31"
        PatternType = 0
        bAssociativity = True
     
        ' Create the associative Hatch object
        Set hatchObj = ThisDrawing.ModelSpace.AddHatch _
                           (PatternType, patternName, bAssociativity)
     
        ' Create the outer boundary for the hatch. (a circle)
        Dim outerLoop(0 To 0) As AcadEntity
        Dim center(0 To 2) As Double
        Dim radius As Double
        center(0) = 3: center(1) = 3: center(2) = 0
        radius = 1
        Set outerLoop(0) = ThisDrawing.ModelSpace. _
                               AddCircle(center, radius)
     
        ' Append the outerboundary to the hatch
        ' object, and display the hatch
        hatchObj.AppendOuterLoop (outerLoop)
        hatchObj.Evaluate
        ThisDrawing.Regen True
    End Sub
