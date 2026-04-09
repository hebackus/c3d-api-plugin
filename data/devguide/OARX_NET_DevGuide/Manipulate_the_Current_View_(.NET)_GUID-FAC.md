<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Control the Drawing Windows (.NET) > Zoom and Pan the Current View (.NET) > Manipulate the Current View (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-FAC1A5EB-2D9E-497B-8FD9-E11D2FF87B93.htm -->

# Manipulate the Current View (.NET)

You access the current view of a viewport in Model or Paper space by using the GetCurrentView method of the Editor object. The GetCurrentView method returns a ViewTableRecord object. You use the ViewTableRecord object to manipulate the magnification, position, and orientation of the view in the active viewport. Once the ViewTableRecord object has been changed, you update the current view of the active viewport with the SetCurrentView method. 

Some of the common properties that you will use to manipulate the current view are: 

  * **CenterPoint** \- Center point of a view in DCS coordinates. 
  * **Height** \- Height of a view in DCS coordinates. Increase the height to zoom out; decrease the height to zoom in. 
  * **Target** \- Target of a view in WCS coordinates. 
  * **ViewDirection** \- Vector from the target to the camera of a view in WCS coordinates. 
  * **ViewTwist** \- Twist angle in radians of a view. 
  * **Width** \- Width of a view in DCS coordinates. Increase the width to zoom out; decrease the width to zoom in. 

## VBA Code Cross Reference

The AutoCAD .NET API does not offer methods to directly manipulate the current view of a drawing like those found in the ActiveX Automation library. For example, if you want to zoom to the extents of the objects in a drawing or the limits of a drawing, you must manipulate the Width, Height and CenterPoint properties of the current view. To get the extents of limits of a drawing, you use the Extmin, Extmax, Limmin, and Limmax properties of the Database object. 

## Function used to manipulate the current view

This example code is a common procedure that is used by later examples. The Zoom procedure accepts four parameters to accomplish zooming to a boundary, panning or centering the view of a drawing, and scaling the view of a drawing by a given factor. The Zoom procedure expects all coordinate values to be provided in WCS coordinates. 

The parameters of the Zoom procedure are: 

  * **Minimum point** \- 3D point used to define the lower-left corner of the area to display. 
  * **Maximum point** \- 3D point used to define the upper-right corner of the area to display. 
  * **Center point** \- 3D point used to define the center of a view. 
  * **Scale factor** \- Real number used to specify the scale to increase or decrease the size of a view. 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.Geometry;
     
    static void Zoom(Point3d pMin, Point3d pMax, Point3d pCenter, double dFactor)
    {
        // Get the current document and database
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        int nCurVport = System.Convert.ToInt32(Application.GetSystemVariable("CVPORT"));
    
        // Get the extents of the current space when no points 
        // or only a center point is provided
        // Check to see if Model space is current
        if (acCurDb.TileMode == true)
        {
            if (pMin.Equals(new Point3d()) == true && 
                pMax.Equals(new Point3d()) == true)
            {
                pMin = acCurDb.Extmin;
                pMax = acCurDb.Extmax;
            }
        }
        else
        {
            // Check to see if Paper space is current
            if (nCurVport == 1)
            {
                // Get the extents of Paper space
                if (pMin.Equals(new Point3d()) == true && 
                    pMax.Equals(new Point3d()) == true)
                {
                    pMin = acCurDb.Pextmin;
                    pMax = acCurDb.Pextmax;
                }
            }
            else
            {
                // Get the extents of Model space
                if (pMin.Equals(new Point3d()) == true && 
                    pMax.Equals(new Point3d()) == true)
                {
                    pMin = acCurDb.Extmin;
                    pMax = acCurDb.Extmax;
                }
            }
        }
    
        // Start a transaction
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Get the current view
            using (ViewTableRecord acView = acDoc.Editor.GetCurrentView())
            {
                Extents3d eExtents;
    
                // Translate WCS coordinates to DCS
                Matrix3d matWCS2DCS;
                matWCS2DCS = Matrix3d.PlaneToWorld(acView.ViewDirection);
                matWCS2DCS = Matrix3d.Displacement(acView.Target - Point3d.Origin) * matWCS2DCS;
                matWCS2DCS = Matrix3d.Rotation(-acView.ViewTwist, 
                                                acView.ViewDirection, 
                                                acView.Target) * matWCS2DCS;
    
                // If a center point is specified, define the min and max 
                // point of the extents
                // for Center and Scale modes
                if (pCenter.DistanceTo(Point3d.Origin) != 0)
                {
                    pMin = new Point3d(pCenter.X - (acView.Width / 2),
                                        pCenter.Y - (acView.Height / 2), 0);
    
                    pMax = new Point3d((acView.Width / 2) + pCenter.X,
                                        (acView.Height / 2) + pCenter.Y, 0);
                }
    
                // Create an extents object using a line
                using (Line acLine = new Line(pMin, pMax))
                {
                    eExtents = new Extents3d(acLine.Bounds.Value.MinPoint,
                                                acLine.Bounds.Value.MaxPoint);
                }
    
                // Calculate the ratio between the width and height of the current view
                double dViewRatio;
                dViewRatio = (acView.Width / acView.Height);
    
                // Tranform the extents of the view
                matWCS2DCS = matWCS2DCS.Inverse();
                eExtents.TransformBy(matWCS2DCS);
    
                double dWidth;
                double dHeight;
                Point2d pNewCentPt;
    
                // Check to see if a center point was provided (Center and Scale modes)
                if (pCenter.DistanceTo(Point3d.Origin) != 0)
                {
                    dWidth = acView.Width;
                    dHeight = acView.Height;
    
                    if (dFactor == 0)
                    {
                        pCenter = pCenter.TransformBy(matWCS2DCS);
                    }
    
                    pNewCentPt = new Point2d(pCenter.X, pCenter.Y);
                }
                else // Working in Window, Extents and Limits mode
                {
                    // Calculate the new width and height of the current view
                    dWidth = eExtents.MaxPoint.X - eExtents.MinPoint.X;
                    dHeight = eExtents.MaxPoint.Y - eExtents.MinPoint.Y;
    
                    // Get the center of the view
                    pNewCentPt = new Point2d(((eExtents.MaxPoint.X + eExtents.MinPoint.X) * 0.5),
                                                ((eExtents.MaxPoint.Y + eExtents.MinPoint.Y) * 0.5));
                }
    
                // Check to see if the new width fits in current window
                if (dWidth > (dHeight * dViewRatio)) dHeight = dWidth / dViewRatio;
    
                // Resize and scale the view
                if (dFactor != 0)
                {
                    acView.Height = dHeight * dFactor;
                    acView.Width = dWidth * dFactor;
                }
    
                // Set the center of the view
                acView.CenterPoint = pNewCentPt;
    
                // Set the current view
                acDoc.Editor.SetCurrentView(acView);
            }
    
            // Commit the changes
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.Geometry
     
    Public Sub Zoom(ByVal pMin As Point3d, ByVal pMax As Point3d, _
                    ByVal pCenter As Point3d, ByVal dFactor As Double)
        '' Get the current document and database
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        Dim nCurVport As Integer = System.Convert.ToInt32(Application.GetSystemVariable("CVPORT"))
    
        '' Get the extents of the current space when no points 
        '' or only a center point is provided
        '' Check to see if Model space is current
        If acCurDb.TileMode = True Then
            If pMin.Equals(New Point3d()) = True And _
                pMax.Equals(New Point3d()) = True Then
    
                pMin = acCurDb.Extmin
                pMax = acCurDb.Extmax
            End If
        Else
            '' Check to see if Paper space is current
            If nCurVport = 1 Then
                If pMin.Equals(New Point3d()) = True And _
                    pMax.Equals(New Point3d()) = True Then
    
                    pMin = acCurDb.Pextmin
                    pMax = acCurDb.Pextmax
                End If
            Else
                '' Get the extents of Model space
                If pMin.Equals(New Point3d()) = True And _
                    pMax.Equals(New Point3d()) = True Then
    
                    pMin = acCurDb.Extmin
                    pMax = acCurDb.Extmax
                End If
            End If
        End If
    
        '' Start a transaction
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            '' Get the current view
            Using acView As ViewTableRecord = acDoc.Editor.GetCurrentView()
                Dim eExtents As Extents3d
    
                '' Translate WCS coordinates to DCS
                Dim matWCS2DCS As Matrix3d
                matWCS2DCS = Matrix3d.PlaneToWorld(acView.ViewDirection)
                matWCS2DCS = Matrix3d.Displacement(acView.Target - Point3d.Origin) * matWCS2DCS
                matWCS2DCS = Matrix3d.Rotation(-acView.ViewTwist, _
                                               acView.ViewDirection, _
                                               acView.Target) * matWCS2DCS
    
                '' If a center point is specified, define the min and max 
                '' point of the extents
                '' for Center and Scale modes
                If pCenter.DistanceTo(Point3d.Origin) <> 0 Then
                    pMin = New Point3d(pCenter.X - (acView.Width / 2), _
                                       pCenter.Y - (acView.Height / 2), 0)
    
                    pMax = New Point3d((acView.Width / 2) + pCenter.X, _
                                       (acView.Height / 2) + pCenter.Y, 0)
                End If
    
                '' Create an extents object using a line
                Using acLine As Line = New Line(pMin, pMax)
                    eExtents = New Extents3d(acLine.Bounds.Value.MinPoint, _
                                             acLine.Bounds.Value.MaxPoint)
                End Using
    
                '' Calculate the ratio between the width and height of the current view
                Dim dViewRatio As Double
                dViewRatio = (acView.Width / acView.Height)
    
                '' Tranform the extents of the view
                matWCS2DCS = matWCS2DCS.Inverse()
                eExtents.TransformBy(matWCS2DCS)
    
                Dim dWidth As Double
                Dim dHeight As Double
                Dim pNewCentPt As Point2d
    
                '' Check to see if a center point was provided (Center and Scale modes)
                If pCenter.DistanceTo(Point3d.Origin) <> 0 Then
                    dWidth = acView.Width
                    dHeight = acView.Height
    
                    If dFactor = 0 Then
                        pCenter = pCenter.TransformBy(matWCS2DCS)
                    End If
    
                    pNewCentPt = New Point2d(pCenter.X, pCenter.Y)
                Else '' Working in Window, Extents and Limits mode
                     '' Calculate the new width and height of the current view
                    dWidth = eExtents.MaxPoint.X - eExtents.MinPoint.X
                    dHeight = eExtents.MaxPoint.Y - eExtents.MinPoint.Y
    
                    '' Get the center of the view
                    pNewCentPt = New Point2d(((eExtents.MaxPoint.X + eExtents.MinPoint.X) * 0.5), _
                                             ((eExtents.MaxPoint.Y + eExtents.MinPoint.Y) * 0.5))
                End If
    
                '' Check to see if the new width fits in current window
                If dWidth > (dHeight * dViewRatio) Then dHeight = dWidth / dViewRatio
    
                '' Resize and scale the view
                If dFactor <> 0 Then
                    acView.Height = dHeight * dFactor
                    acView.Width = dWidth * dFactor
                End If
    
                '' Set the center of the view
                acView.CenterPoint = pNewCentPt
    
                '' Set the current view
                acDoc.Editor.SetCurrentView(acView)
            End Using
    
            '' Commit the changes
            acTrans.Commit()
        End Using
    End Sub
