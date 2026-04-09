<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Control the Drawing Windows (.NET) > Use Tiled Viewports (.NET) > Identify and Manipulate the Active Viewport (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-2CEED409-0E15-4F48-9AA1-D12D246E27DB.htm -->

# Identify and Manipulate the Active Viewport (.NET)

The active viewport is represented in the Viewports table by a record named "*Active", which is not a unique name as all tiled viewports currently displayed on the Model tab are named "*Active". Each tiled viewport that is displayed is assigned a number. The number of the active viewport can be obtained by: 

  * Retrieving the value of the CVPORT system variable 
  * Using the ActiveViewportId property of the Editor object to get the object id for the active viewport and then open the Viewport object to access its Number property 

Once you have the active viewport, you control its display properties, enable drafting aids for the viewport such as grid and snap, as well as the size of the viewport itself. Tiled viewports are defined by two corner points: lower-left and upper-right. The LowerLeftCorner and UpperRightCorner properties represent the graphic placement of the viewport on the display. 

A single tiled viewport configuration has a lower-left corner of (0,0) and an upper-right corner of (1,1). The lower-left corner of the drawing window is always represented by the point of (0,0), and the upper-right corner is presented by (1,1) no matter the number of tiled viewports on the Model tab. When more than one tiled viewport is displayed, the lower-left and upper-right corners will vary but one viewport will have a lower-left corner of (0,0) and another will have an upper-right corner of (1,1) 

These properties are defined as follows (using a four-way split as an example): 

In this example: 

  * Viewport 1-LowerLeftCorner = (0, .5), UpperRightCorner = (.5, 1) 
  * Viewport 2-LowerLeftCorner = (.5, .5), UpperRightCorner = (1, 1) 
  * Viewport 3-LowerLeftCorner = (0, 0), UpperRightCorner = (.5, .5) 
  * Viewport 4-LowerLeftCorner = (.5, 0), UpperRightCorner = (1, .5) 

## Create a new tiled viewport configuration with two horizontal windows

The following example creates a two horizontal viewports as a named viewport configuration and redefines the active display. 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("CreateModelViewport")]
    public static void CreateModelViewport()
    {
        // Get the current database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Viewport table for read
            ViewportTable acVportTbl;
            acVportTbl = acTrans.GetObject(acCurDb.ViewportTableId,
                                            OpenMode.ForRead) as ViewportTable;
    
            // Check to see if the named view 'TEST_VIEWPORT' exists
            if (acVportTbl.Has("TEST_VIEWPORT") == false)
            {
                // Open the View table for write
                acTrans.GetObject(acCurDb.ViewportTableId, OpenMode.ForWrite);
    
                // Add the new viewport to the Viewport table and the transaction
                using (ViewportTableRecord acVportTblRecLwr = new ViewportTableRecord())
                {
                    acVportTbl.Add(acVportTblRecLwr);
                    acTrans.AddNewlyCreatedDBObject(acVportTblRecLwr, true);
    
                    // Name the new viewport 'TEST_VIEWPORT' and assign it to be
                    // the lower half of the drawing window
                    acVportTblRecLwr.Name = "TEST_VIEWPORT";
                    acVportTblRecLwr.LowerLeftCorner = new Point2d(0, 0);
                    acVportTblRecLwr.UpperRightCorner = new Point2d(1, 0.5);
    
                    // Add the new viewport to the Viewport table and the transaction
                    using (ViewportTableRecord acVportTblRecUpr = new ViewportTableRecord())
                    {
                        acVportTbl.Add(acVportTblRecUpr);
                        acTrans.AddNewlyCreatedDBObject(acVportTblRecUpr, true);
    
                        // Name the new viewport 'TEST_VIEWPORT' and assign it to be
                        // the upper half of the drawing window
                        acVportTblRecUpr.Name = "TEST_VIEWPORT";
                        acVportTblRecUpr.LowerLeftCorner = new Point2d(0, 0.5);
                        acVportTblRecUpr.UpperRightCorner = new Point2d(1, 1);
    
                        // To assign the new viewports as the active viewports, the 
                        // viewports named '*Active' need to be removed and recreated
                        // based on 'TEST_VIEWPORT'.
    
                        // Step through each object in the symbol table
                        foreach (ObjectId acObjId in acVportTbl)
                        {
                            // Open the object for read
                            ViewportTableRecord acVportTblRec;
                            acVportTblRec = acTrans.GetObject(acObjId,
                                                                OpenMode.ForRead) as ViewportTableRecord;
    
                            // See if it is one of the active viewports, and if so erase it
                            if (acVportTblRec.Name == "*Active")
                            {
                                acTrans.GetObject(acObjId, OpenMode.ForWrite);
                                acVportTblRec.Erase();
                            }
                        }
    
                        // Clone the new viewports as the active viewports
                        foreach (ObjectId acObjId in acVportTbl)
                        {
                            // Open the object for read
                            ViewportTableRecord acVportTblRec;
                            acVportTblRec = acTrans.GetObject(acObjId,
                                                                OpenMode.ForRead) as ViewportTableRecord;
    
                            // See if it is one of the active viewports, and if so erase it
                            if (acVportTblRec.Name == "TEST_VIEWPORT")
                            {
                                ViewportTableRecord acVportTblRecClone;
                                acVportTblRecClone = acVportTblRec.Clone() as ViewportTableRecord;
    
                                // Add the new viewport to the Viewport table and the transaction
                                acVportTbl.Add(acVportTblRecClone);
                                acVportTblRecClone.Name = "*Active";
                                acTrans.AddNewlyCreatedDBObject(acVportTblRecClone, true);
                            }
                        }
    
                        // Update the display with the new tiled viewports arrangement
                        acDoc.Editor.UpdateTiledViewportsFromDatabase();
                    }
                }
    
                // Commit the changes
                acTrans.Commit();
            }
    
            // Dispose of the transaction
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("CreateModelViewport")> _
    Public Sub CreateModelViewport()
        '' Get the current database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
    
            '' Open the Viewport table for read
            Dim acVportTbl As ViewportTable
            acVportTbl = acTrans.GetObject(acCurDb.ViewportTableId, OpenMode.ForRead)
    
            '' Check to see if the named view 'TEST_VIEWPORT' exists
            If (acVportTbl.Has("TEST_VIEWPORT") = False) Then
                '' Open the View table for write
                acTrans.GetObject(acCurDb.ViewportTableId, OpenMode.ForWrite)
    
                '' Add the new viewport to the Viewport table and the transaction
                Using acVportTblRecLwr As ViewportTableRecord = New ViewportTableRecord()
                    acVportTbl.Add(acVportTblRecLwr)
                    acTrans.AddNewlyCreatedDBObject(acVportTblRecLwr, True)
    
                    '' Name the new viewport 'TEST_VIEWPORT' and assign it to be
                    '' the lower half of the drawing window
                    acVportTblRecLwr.Name = "TEST_VIEWPORT"
                    acVportTblRecLwr.LowerLeftCorner = New Point2d(0, 0)
                    acVportTblRecLwr.UpperRightCorner = New Point2d(1, 0.5)
    
                    '' Add the new viewport to the Viewport table and the transaction
                    Using acVportTblRecUpr As ViewportTableRecord = New ViewportTableRecord()
                        acVportTbl.Add(acVportTblRecUpr)
                        acTrans.AddNewlyCreatedDBObject(acVportTblRecUpr, True)
    
                        '' Name the new viewport 'TEST_VIEWPORT' and assign it to be
                        '' the upper half of the drawing window
                        acVportTblRecUpr.Name = "TEST_VIEWPORT"
                        acVportTblRecUpr.LowerLeftCorner = New Point2d(0, 0.5)
                        acVportTblRecUpr.UpperRightCorner = New Point2d(1, 1)
    
                        '' To assign the new viewports as the active viewports, the 
                        '' viewports named '*Active' need to be removed and recreated
                        '' based on 'TEST_VIEWPORT'.
    
                        '' Step through each object in the symbol table
                        For Each acObjId As ObjectId In acVportTbl
                            '' Open the object for read
                            Dim acVportTblRec As ViewportTableRecord
                            acVportTblRec = acTrans.GetObject(acObjId, _
                                                              OpenMode.ForRead)
    
                            '' See if it is one of the active viewports, and if so erase it
                            If (acVportTblRec.Name = "*Active") Then
                                acTrans.GetObject(acObjId, OpenMode.ForWrite)
                                acVportTblRec.Erase()
                            End If
                        Next
    
                        '' Clone the new viewports as the active viewports
                        For Each acObjId As ObjectId In acVportTbl
                            '' Open the object for read
                            Dim acVportTblRec As ViewportTableRecord
                            acVportTblRec = acTrans.GetObject(acObjId, _
                                                              OpenMode.ForRead)
    
                            '' See if it is one of the active viewports, and if so erase it
                            If (acVportTblRec.Name = "TEST_VIEWPORT") Then
                                Dim acVportTblRecClone As ViewportTableRecord
                                acVportTblRecClone = acVportTblRec.Clone()
    
                                '' Add the new viewport to the Viewport table and the transaction
                                acVportTbl.Add(acVportTblRecClone)
                                acVportTblRecClone.Name = "*Active"
                                acTrans.AddNewlyCreatedDBObject(acVportTblRecClone, True)
                            End If
                        Next
    
                        '' Update the display with the new tiled viewports arrangement
                        acDoc.Editor.UpdateTiledViewportsFromDatabase()
                    End Using
                End Using
    
                '' Commit the changes
                acTrans.Commit()
            End If
    
            '' Dispose of the transaction
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CreateModelViewport()
        ' Create a new viewport
        Dim vportObj As AcadViewport
        Set vportObj = ThisDrawing.Viewports.Add("TEST_VIEWPORT")
     
        ' Split vportObj into 2 horizontal windows
        vportObj.Split acViewport2Horizontal
     
        ' Now set vportObj to be the active viewport
        ThisDrawing.ActiveViewport = vportObj
    End Sub
