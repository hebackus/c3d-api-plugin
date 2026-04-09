<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Open and Close Objects (.NET) > Use Transactions With the Transaction Manager (.NET) > Nest Transactions (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-8D8B9EE8-9D85-4C29-93A0-0BDC90F66EA7.htm -->

# Nest Transactions (.NET)

Transactions can be nested one inside another. You might have an outer transaction to undo all the changes made by your routine and inner transactions to undo just portions of the changes made. When you work with nested transactions, you start with a top transaction which is also the outer most transaction. 

As you start new transactions, they are added into the previous transaction. Nested transactions must be committed or aborted in the opposite order in which they are created. So if you have three transactions, you must close the third or innermost one before the second and finally the first. If you abort the first transaction, the changes made by all three transactions are undone. 

The following illustration shows how transactions appear when nested. 

## Use nested transactions to create and modify objects

The following example demonstrates using three transactions to create a Circle and Line object, and then change their colors. The color of the circle is changed in the second and third transaction, but since the third transaction is aborted only the changes made in the first and second transactions are saved to the database. Additionally, the number of active transactions is printed in the Command Line window as they are created and closed. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    using Autodesk.AutoCAD.EditorInput;
     
    [CommandMethod("NestedTransactions")]
    public static void NestedTransactions()
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Create a reference to the Transaction Manager
        Autodesk.AutoCAD.DatabaseServices.TransactionManager acTransMgr;
        acTransMgr = acCurDb.TransactionManager;
    
        // Create a new transaction
        using (Transaction acTrans1 = acTransMgr.StartTransaction())
        {
            // Print the current number of active transactions
            acDoc.Editor.WriteMessage("\nNumber of transactions active: " +
                                      acTransMgr.NumberOfActiveTransactions.ToString());
    
            // Open the Block table for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans1.GetObject(acCurDb.BlockTableId,
                                          OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Model space for write
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans1.GetObject(acBlkTbl[BlockTableRecord.ModelSpace],
                                             OpenMode.ForWrite) as BlockTableRecord;
    
            // Create a circle with a radius of 3 at 5,5
            using (Circle acCirc = new Circle())
            {
                acCirc.Center = new Point3d(5, 5, 0);
                acCirc.Radius = 3;
    
                // Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acCirc);
                acTrans1.AddNewlyCreatedDBObject(acCirc, true);
    
                // Create the second transaction
                using (Transaction acTrans2 = acTransMgr.StartTransaction())
                {
                    acDoc.Editor.WriteMessage("\nNumber of transactions active: " +
                                              acTransMgr.NumberOfActiveTransactions.ToString());
    
                    // Change the circle's color
                    acCirc.ColorIndex = 5;
    
                    // Get the object that was added to Transaction 1 and set it to the color 5
                    using (Line acLine = new Line(new Point3d(2, 5, 0), new Point3d(10, 7, 0)))
                    {
                        acLine.ColorIndex = 3;
    
                        // Add the new object to Model space and the transaction
                        acBlkTblRec.AppendEntity(acLine);
                        acTrans2.AddNewlyCreatedDBObject(acLine, true);
                    }
    
                    // Create the third transaction
                    using (Transaction acTrans3 = acTransMgr.StartTransaction())
                    {
                        acDoc.Editor.WriteMessage("\nNumber of transactions active: " +
                                                  acTransMgr.NumberOfActiveTransactions.ToString());
    
                        // Change the circle's color
                        acCirc.ColorIndex = 3;
    
                        // Update the display of the drawing
                        acDoc.Editor.WriteMessage("\n");
                        acDoc.Editor.Regen();
    
                        // Request to keep or discard the changes in the third transaction
                        PromptKeywordOptions pKeyOpts = new PromptKeywordOptions("");
                        pKeyOpts.Message = "\nKeep color change ";
                        pKeyOpts.Keywords.Add("Yes");
                        pKeyOpts.Keywords.Add("No");
                        pKeyOpts.Keywords.Default = "No";
                        pKeyOpts.AllowNone = true;
    
                        PromptResult pKeyRes = acDoc.Editor.GetKeywords(pKeyOpts);
    
                        if (pKeyRes.StringResult == "No")
                        {
                            // Discard the changes in transaction 3
                            acTrans3.Abort();
                        }
                        else
                        {
                            // Save the changes in transaction 3
                            acTrans3.Commit();
                        }
    
                        // Dispose the transaction
                    }
    
                    acDoc.Editor.WriteMessage("\nNumber of transactions active: " +
                                              acTransMgr.NumberOfActiveTransactions.ToString());
    
                    // Keep the changes to transaction 2
                    acTrans2.Commit();
                }
            }
    
            acDoc.Editor.WriteMessage("\nNumber of transactions active: " +
                                      acTransMgr.NumberOfActiveTransactions.ToString());
    
            // Keep the changes to transaction 1
            acTrans1.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    Imports Autodesk.AutoCAD.EditorInput
     
    <CommandMethod("NestedTransactions")> _
    Public Sub NestedTransactions()
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Create a reference to the Transaction Manager
        Dim acTransMgr As Autodesk.AutoCAD.DatabaseServices.TransactionManager
        acTransMgr = acCurDb.TransactionManager
    
        '' Create a new transaction
        Using acTrans1 As Transaction = acTransMgr.StartTransaction()
    
            '' Print the current number of active transactions
            acDoc.Editor.WriteMessage(vbLf & "Number of transactions active: " & _
                                      acTransMgr.NumberOfActiveTransactions.ToString())
    
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans1.GetObject(acCurDb.BlockTableId, OpenMode.ForRead)
    
            '' Open the Block table record Model space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans1.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                             OpenMode.ForWrite)
    
            '' Create a circle with a radius of 3 at 5,5
            Using acCirc As Circle = New Circle()
                acCirc.Center = New Point3d(5, 5, 0)
                acCirc.Radius = 3
    
                '' Add the new object to Model space and the transaction
                acBlkTblRec.AppendEntity(acCirc)
                acTrans1.AddNewlyCreatedDBObject(acCirc, True)
    
                '' Create the second transaction
                Using acTrans2 As Transaction = acTransMgr.StartTransaction()
    
                    acDoc.Editor.WriteMessage(vbLf & "Number of transactions active: " & _
                                              acTransMgr.NumberOfActiveTransactions.ToString())
    
                    '' Change the circle's color
                    acCirc.ColorIndex = 5
    
                    '' Get the object that was added to Transaction 1 and set it to the color 5
                    Using acLine As Line = New Line(New Point3d(2, 5, 0), New Point3d(10, 7, 0))
                        acLine.ColorIndex = 3
    
                        '' Add the new object to Model space and the transaction
                        acBlkTblRec.AppendEntity(acLine)
                        acTrans2.AddNewlyCreatedDBObject(acLine, True)
                    End Using
    
                    '' Create the third transaction
                    Using acTrans3 As Transaction = acTransMgr.StartTransaction()
    
                        acDoc.Editor.WriteMessage(vbLf & "Number of transactions active: " & _
                                                  acTransMgr.NumberOfActiveTransactions.ToString())
    
                        '' Change the circle's color
                        acCirc.ColorIndex = 3
    
                        '' Update the display of the drawing
                        acDoc.Editor.WriteMessage(vbLf)
                        acDoc.Editor.Regen()
    
                        '' Request to keep or discard the changes in the third transaction
                        Dim pKeyOpts As PromptKeywordOptions = New PromptKeywordOptions("")
                        pKeyOpts.Message = vbLf & "Keep color change "
                        pKeyOpts.Keywords.Add("Yes")
                        pKeyOpts.Keywords.Add("No")
                        pKeyOpts.Keywords.Default = "No"
                        pKeyOpts.AllowNone = True
    
                        Dim pKeyRes As PromptResult = acDoc.Editor.GetKeywords(pKeyOpts)
    
                        If pKeyRes.StringResult = "No" Then
                            '' Discard the changes in transaction 3
                            acTrans3.Abort()
                        Else
                            '' Save the changes in transaction 3
                            acTrans3.Commit()
                        End If
    
                        '' Dispose the transaction
                    End Using
    
                    acDoc.Editor.WriteMessage(vbLf & "Number of transactions active: " & _
                                              acTransMgr.NumberOfActiveTransactions.ToString())
    
                    '' Keep the changes to transaction 2
                    acTrans2.Commit()
                End Using
            End Using
    
            acDoc.Editor.WriteMessage(vbLf & "Number of transactions active: " & _
                                      acTransMgr.NumberOfActiveTransactions.ToString())
    
            '' Keep the changes to transaction 1
            acTrans1.Commit()
        End Using
    End Sub
