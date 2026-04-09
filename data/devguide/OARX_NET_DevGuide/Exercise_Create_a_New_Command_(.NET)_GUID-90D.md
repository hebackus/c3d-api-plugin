<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Getting Started with Microsoft Visual Studio (.NET) > Exercises: Create Your First Project (.NET) > Exercise: Create a New Command (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-90D867AA-6513-4F0C-A498-7453FEA4FEC3.htm -->

# Exercise: Create a New Command (.NET)

Now that you have created a project and added the necessary library references, it is time to create a command. The command will create a new multiline text (MText) object in Model space. These and other concepts are discussed in-depth in later chapters. 

## To define a new command that creates a new MText object

  1. In the Solution Explorer, double-click _Class1.vb_ or _Class1.cs_ based on the type of project you created. 

A code window is opened for the Class1 module and it should look like the following: 

### C#
         
         using System;
         using System.Collections.Generic;
         using System.Linq;
         using System.Text;
          
         namespace MyFirstProject1
         {
           public class Class1
           {
           }
         }

### VB.NET
         
         Public Class Class1
          
         End Class

  2. Change the code in the code window to match the following: 

### C#
         
         using System;
         using System.Collections.Generic;
         using System.Linq;
         using System.Text;
          
         using Autodesk.AutoCAD.Runtime;
         using Autodesk.AutoCAD.ApplicationServices;
         using Autodesk.AutoCAD.DatabaseServices;
          
         [assembly: CommandClass(typeof(MyFirstProject1.Class1))]
          
         namespace MyFirstProject1
         {
           public class Class1
           {
               [CommandMethod("AdskGreeting")]
               public void AdskGreeting()
               {
                   // Get the current document and database, and start a transaction
                   Document acDoc = Application.DocumentManager.MdiActiveDocument;
                   Database acCurDb = acDoc.Database;
          
                   // Starts a new transaction with the Transaction Manager
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
          
                       /* Creates a new MText object and assigns it a location,
                       text value and text style */
                       using (MText objText = new MText())
                       {
                           // Specify the insertion point of the MText object
                           objText.Location = new Autodesk.AutoCAD.Geometry.Point3d(2, 2, 0);
          
                           // Set the text string for the MText object
                           objText.Contents = "Greetings, Welcome to AutoCAD .NET";
          
                           // Set the text style for the MText object
                           objText.TextStyleId = acCurDb.Textstyle;
          
                           // Appends the new MText object to model space
                           acBlkTblRec.AppendEntity(objText);
          
                           // Appends to new MText object to the active transaction
                           acTrans.AddNewlyCreatedDBObject(objText, true);
                       }
         
                       // Saves the changes to the database and closes the transaction
                       acTrans.Commit();
                   }
               }
           }
         }

### VB.NET
         
         Imports Autodesk.AutoCAD.Runtime
         Imports Autodesk.AutoCAD.ApplicationServices
         Imports Autodesk.AutoCAD.DatabaseServices
              
         Public Class Class1
           <CommandMethod("AdskGreeting")> _
           Public Sub AdskGreeting()
               '' Get the current document and database, and start a transaction
               Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
               Dim acCurDb As Database = acDoc.Database
          
               Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
                   '' Open the Block table record for read
                   Dim acBlkTbl As BlockTable
                   acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                                OpenMode.ForRead)
          
                   '' Open the Block table record Model space for write
                   Dim acBlkTblRec As BlockTableRecord
                   acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.ModelSpace), _
                                                   OpenMode.ForWrite)
          
                   '' Creates a new MText object and assigns it a location,
                   '' text value and text style
                   Using objText As MText = New MText
          
                       '' Specify the insertion point of the MText object
                       objText.Location = New Autodesk.AutoCAD.Geometry.Point3d(2, 2, 0)
          
                       '' Set the text string for the MText object
                       objText.Contents = "Greetings, Welcome to AutoCAD .NET"
          
                       '' Set the text style for the MText object
                       objText.TextStyleId = acCurDb.Textstyle
          
                       '' Appends the new MText object to model space
                       acBlkTblRec.AppendEntity(objText)
          
                       '' Appends to new MText object to the active transaction
                       acTrans.AddNewlyCreatedDBObject(objText, True)
                   End Using
         
                   '' Saves the changes to the database and closes the transaction
                   acTrans.Commit()
               End Using
           End Sub
         End Class
