<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Work in Three-Dimensional Space (.NET) > Define a User Coordinate System (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-096085E3-5AD5-4454-BF10-C9177FDB5979.htm -->

# Define a User Coordinate System (.NET)

You define a user coordinate system ( UCS ) object to change the location of the (0, 0, 0) origin point and the orientation of the _XY_ plane and _Z_ axis. You can locate and orient a UCS anywhere in 3D space, and you can define, save, and recall as many user coordinate systems as you require. Coordinate input and display are relative to the current UCS. 

To indicate the origin and orientation of the UCS, you can display the UCS icon at the UCS origin point using the IconAtOrigin property of a Viewport object or the UCSICON system variable. If the UCS icon is turned on (IconVisible property) and is not displayed at the origin, it is displayed at the WCS coordinate defined by the UCSORG system variable. 

You can create a new user coordinate system using the Add method of the UCSTable object. This method requires four values as input: the coordinate of the origin, a coordinate on the _X_ and _Y_ axes, and the name of the UCS. 

All coordinates in the AutoCAD ® ActiveX Automation are entered in the world coordinate system. Use the GetUCSMatrix method to return the transformation matrix of a given UCS. Use this transformation matrix to find the equivalent WCS coordinates. 

To make a UCS active, use the ActiveUCS property on the Document object. If changes are made to the active UCS, the new UCS object must be reset as the active UCS for the changes to appear. To reset the active UCS, simply call the ActiveUCS property again with the updated UCS object. 

## Create a new UCS, make it active, and translate the coordinates of a point into the UCS coordinates

The following subroutine creates a new UCS and sets it as the active UCS for the drawing. It then asks the user to pick a point in the drawing, and returns both WCS and UCS coordinates for the point. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.EditorInput;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("NewUCS")]
    public static void NewUCS()
    {
        // Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the UCS table for read
            UcsTable acUCSTbl;
            acUCSTbl = acTrans.GetObject(acCurDb.UcsTableId,
                                            OpenMode.ForRead) as UcsTable;
    
            UcsTableRecord acUCSTblRec;
    
            // Check to see if the "New_UCS" UCS table record exists
            if (acUCSTbl.Has("New_UCS") == false)
            {
                acUCSTblRec = new UcsTableRecord();
                acUCSTblRec.Name = "New_UCS";
    
                // Open the UCSTable for write
                acTrans.GetObject(acCurDb.UcsTableId, OpenMode.ForWrite);
    
                // Add the new UCS table record
                acUCSTbl.Add(acUCSTblRec);
                acTrans.AddNewlyCreatedDBObject(acUCSTblRec, true);
            }
            else
            {
                acUCSTblRec = acTrans.GetObject(acUCSTbl["New_UCS"],
                                                OpenMode.ForWrite) as UcsTableRecord;
            }
    
            acUCSTblRec.Origin = new Point3d(4, 5, 3);
            acUCSTblRec.XAxis = new Vector3d(1, 0, 0);
            acUCSTblRec.YAxis = new Vector3d(0, 1, 0);
    
            // Open the active viewport
            ViewportTableRecord acVportTblRec;
            acVportTblRec = acTrans.GetObject(acDoc.Editor.ActiveViewportId,
                                                OpenMode.ForWrite) as ViewportTableRecord;
    
            // Display the UCS Icon at the origin of the current viewport
            acVportTblRec.IconAtOrigin = true;
            acVportTblRec.IconEnabled = true;
    
            // Set the UCS current
            acVportTblRec.SetUcs(acUCSTblRec.ObjectId);
            acDoc.Editor.UpdateTiledViewportsFromDatabase();
    
            // Display the name of the current UCS
            UcsTableRecord acUCSTblRecActive;
            acUCSTblRecActive = acTrans.GetObject(acVportTblRec.UcsName,
                                                    OpenMode.ForRead) as UcsTableRecord;
    
            Application.ShowAlertDialog("The current UCS is: " +
                                        acUCSTblRecActive.Name);
    
            PromptPointResult pPtRes;
            PromptPointOptions pPtOpts = new PromptPointOptions("");
    
            // Prompt for a point
            pPtOpts.Message = "\nEnter a point: ";
            pPtRes = acDoc.Editor.GetPoint(pPtOpts);
    
            Point3d pPt3dWCS;
            Point3d pPt3dUCS;
    
            // If a point was entered, then translate it to the current UCS
            if (pPtRes.Status == PromptStatus.OK)
            {
                pPt3dWCS = pPtRes.Value;
                pPt3dUCS = pPtRes.Value;
    
                // Translate the point from the current UCS to the WCS
                Matrix3d newMatrix = new Matrix3d();
                newMatrix = Matrix3d.AlignCoordinateSystem(Point3d.Origin,
                                                            Vector3d.XAxis,
                                                            Vector3d.YAxis,
                                                            Vector3d.ZAxis,
                                                            acVportTblRec.Ucs.Origin,
                                                            acVportTblRec.Ucs.Xaxis,
                                                            acVportTblRec.Ucs.Yaxis,
                                                            acVportTblRec.Ucs.Zaxis);
    
                pPt3dWCS = pPt3dWCS.TransformBy(newMatrix);
    
                Application.ShowAlertDialog("The WCS coordinates are: \n" +
                                            pPt3dWCS.ToString() + "\n" +
                                            "The UCS coordinates are: \n" +
                                            pPt3dUCS.ToString());
            }
    
            // Save the new objects to the database
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.EditorInput
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("NewUCS")> _
    Public Sub NewUCS()
        '' Get the current document and database, and start a transaction
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            '' Open the UCS table for read
            Dim acUCSTbl As UcsTable
            acUCSTbl = acTrans.GetObject(acCurDb.UcsTableId, _
                                         OpenMode.ForRead)
    
            Dim acUCSTblRec As UcsTableRecord
    
            '' Check to see if the "New_UCS" UCS table record exists
            If acUCSTbl.Has("New_UCS") = False Then
                acUCSTblRec = New UcsTableRecord()
                acUCSTblRec.Name = "New_UCS"
    
                '' Open the UCSTable for write
                acTrans.GetObject(acCurDb.UcsTableId, OpenMode.ForWrite)
    
                '' Add the new UCS table record
                acUCSTbl.Add(acUCSTblRec)
                acTrans.AddNewlyCreatedDBObject(acUCSTblRec, True)
            Else
                acUCSTblRec = acTrans.GetObject(acUCSTbl("New_UCS"), _
                                                OpenMode.ForWrite)
            End If
    
            acUCSTblRec.Origin = New Point3d(4, 5, 3)
            acUCSTblRec.XAxis = New Vector3d(1, 0, 0)
            acUCSTblRec.YAxis = New Vector3d(0, 1, 0)
    
            '' Open the active viewport
            Dim acVportTblRec As ViewportTableRecord
            acVportTblRec = acTrans.GetObject(acDoc.Editor.ActiveViewportId, _
                                              OpenMode.ForWrite)
    
            '' Display the UCS Icon at the origin of the current viewport
            acVportTblRec.IconAtOrigin = True
            acVportTblRec.IconEnabled = True
    
            '' Set the UCS current
            acVportTblRec.SetUcs(acUCSTblRec.ObjectId)
            acDoc.Editor.UpdateTiledViewportsFromDatabase()
    
            '' Display the name of the current UCS
            Dim acUCSTblRecActive As UcsTableRecord
            acUCSTblRecActive = acTrans.GetObject(acVportTblRec.UcsName, _
                                                  OpenMode.ForRead)
    
            Application.ShowAlertDialog("The current UCS is: " & _
                                        acUCSTblRecActive.Name)
    
            Dim pPtRes As PromptPointResult
            Dim pPtOpts As PromptPointOptions = New PromptPointOptions("")
    
            '' Prompt for a point
            pPtOpts.Message = vbLf & "Enter a point: "
            pPtRes = acDoc.Editor.GetPoint(pPtOpts)
    
            Dim pPt3dWCS As Point3d
            Dim pPt3dUCS As Point3d
    
            '' If a point was entered, then translate it to the current UCS
            If pPtRes.Status = PromptStatus.OK Then
                pPt3dWCS = pPtRes.Value
                pPt3dUCS = pPtRes.Value
    
                '' Translate the point from the current UCS to the WCS
                Dim newMatrix As Matrix3d = New Matrix3d()
                newMatrix = Matrix3d.AlignCoordinateSystem(Point3d.Origin, _
                                                           Vector3d.XAxis, _
                                                           Vector3d.YAxis, _
                                                           Vector3d.ZAxis, _
                                                           acVportTblRec.Ucs.Origin, _
                                                           acVportTblRec.Ucs.Xaxis, _
                                                           acVportTblRec.Ucs.Yaxis, _
                                                           acVportTblRec.Ucs.Zaxis)
    
                pPt3dWCS = pPt3dWCS.TransformBy(newMatrix)
    
                Application.ShowAlertDialog("The WCS coordinates are: " & vbLf & _
                                            pPt3dWCS.ToString() & vbLf & _
                                            "The UCS coordinates are: " & vbLf & _
                                            pPt3dUCS.ToString())
            End If
    
            '' Save the new objects to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub NewUCS()
        ' Define the variables we will need
        Dim ucsObj As AcadUCS
        Dim origin(0 To 2) As Double
        Dim xAxisPnt(0 To 2) As Double
        Dim yAxisPnt(0 To 2) As Double
     
        ' Define the UCS points
        origin(0) = 4: origin(1) = 5: origin(2) = 3
        xAxisPnt(0) = 5: xAxisPnt(1) = 5: xAxisPnt(2) = 3
        yAxisPnt(0) = 4: yAxisPnt(1) = 6: yAxisPnt(2) = 3
     
        ' Add the UCS to the
        ' UserCoordinatesSystems collection
        Set ucsObj = ThisDrawing.UserCoordinateSystems. _
                         Add(origin, xAxisPnt, yAxisPnt, "New_UCS")
     
        ' Display the UCS icon
        ThisDrawing.ActiveViewport.UCSIconAtOrigin = True
        ThisDrawing.ActiveViewport.UCSIconOn = True
     
        ' Make the new UCS the active UCS
        ThisDrawing.ActiveUCS = ucsObj
        MsgBox "The current UCS is : " & ThisDrawing.ActiveUCS.Name _
               & vbCrLf & " Pick a point in the drawing."
     
        ' Find the WCS and UCS coordinate of a point
        Dim WCSPnt As Variant
        Dim UCSPnt As Variant
     
        WCSPnt = ThisDrawing.Utility.GetPoint(, "Enter a point: ")
        UCSPnt = ThisDrawing.Utility.TranslateCoordinates _
                     (WCSPnt, acWorld, acUCS, False)
     
        MsgBox "The WCS coordinates are: " & WCSPnt(0) & ", " _
               & WCSPnt(1) & ", " & WCSPnt(2) & vbCrLf & _
               "The UCS coordinates are: " & UCSPnt(0) & ", " _
               & UCSPnt(1) & ", " & UCSPnt(2)
    End Sub
