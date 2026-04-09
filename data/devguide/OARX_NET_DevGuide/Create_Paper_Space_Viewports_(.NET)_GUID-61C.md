<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Viewports (.NET) > Create Paper Space Viewports (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-61C22902-F63B-4204-86EC-FA37312D1B6E.htm -->

# Create Paper Space Viewports (.NET)

Paper space viewports are created by creating instances of Viewport objects and adding them to the block reference used by a layout other than Model. The constructor for the Viewport object does not accept any parameters to create a new viewport object. Once an instance of a Viewport object is created, you can define its placement with the CenterPoint, Width and Height properties. 

After creating the Viewport object, you can set properties of the view itself, such as viewing direction (ViewDirection property), lens length for perspective views (LensLength property), and grid display (GridOn property). You can also control properties of the viewport itself, such as layer (Layer property), linetype (Linetype property), and linetype scaling (LinetypeScale property). 

## Create and enable a floating viewport

This example sets paper space active, creates a floating viewport, defines the view for the viewport, and enables the viewport. 

### C#
    
    
    using System.Runtime.InteropServices;
     
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [DllImport("acad.exe", CallingConvention = CallingConvention.Cdecl,
     EntryPoint = "?acedSetCurrentVPort@@YA?AW4ErrorStatus@Acad@@PBVAcDbViewport@@@Z")]
    extern static private int acedSetCurrentVPort(IntPtr AcDbVport);
     
    [CommandMethod("CreateFloatingViewport")]
    public static void CreateFloatingViewport()
    {
        // Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Block table for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                         OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Paper space for write
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.PaperSpace],
                                            OpenMode.ForWrite) as BlockTableRecord;
    
            // Switch to the previous Paper space layout
            Application.SetSystemVariable("TILEMODE", 0);
            acDoc.Editor.SwitchToPaperSpace();
    
            // Create a Viewport
            using (Viewport acVport = new Viewport())
            {
                acVport.CenterPoint = new Point3d(3.25, 3, 0);
                acVport.Width = 6;
                acVport.Height = 5;
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acVport);
                acTrans.AddNewlyCreatedDBObject(acVport, true);
    
                // Change the view direction
                acVport.ViewDirection = new Vector3d(1, 1, 1);
    
                // Enable the viewport
                acVport.On = true;
    
                // Activate model space in the viewport
                acDoc.Editor.SwitchToModelSpace();
    
                // Set the new viewport current via an imported ObjectARX function
                acedSetCurrentVPort(acVport.UnmanagedObject);
            }
    
            // Save the new objects to the database
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports System.Runtime.InteropServices
     
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <DllImport("acad.exe", CallingConvention:=CallingConvention.Cdecl, _
     EntryPoint:="?acedSetCurrentVPort@@YA?AW4ErrorStatus@Acad@@PBVAcDbViewport@@@Z")> _
    Public Shared Function acedSetCurrentVPort(ByVal AcDbVport As IntPtr) As IntPtr
    End Function
     
    <CommandMethod("CreateFloatingViewport")> _
    Public Sub CreateFloatingViewport()
        '' Get the current document and database, and start a transaction
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                         OpenMode.ForRead)
    
            '' Open the Block table record Paper space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.PaperSpace), _
                                            OpenMode.ForWrite)
    
            '' Switch to the previous Paper space layout
            Application.SetSystemVariable("TILEMODE", 0)
            acDoc.Editor.SwitchToPaperSpace()
    
            '' Create a Viewport
            Using acVport As Viewport = New Viewport()
                acVport.CenterPoint = New Point3d(3.25, 3, 0)
                acVport.Width = 6
                acVport.Height = 5
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acVport)
                acTrans.AddNewlyCreatedDBObject(acVport, True)
    
                '' Change the view direction
                acVport.ViewDirection = New Vector3d(1, 1, 1)
    
                '' Enable the viewport
                acVport.On = True
    
                '' Activate model space in the viewport
                acDoc.Editor.SwitchToModelSpace()
    
                '' Set the new viewport current via an imported ObjectARX function
                acedSetCurrentVPort(acVport.UnmanagedObject)
            End Using
    
            '' Save the new objects to the database
            acTrans.Commit()
        End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub CreateFloatingViewport()
        ' Set the active space to paper space
        ThisDrawing.ActiveSpace = acPaperSpace
     
        ' Create the paperspace viewport
        Dim newVport As AcadPViewport
        Dim center(0 To 2) As Double
        center(0) = 3.25
        center(1) = 3
        center(2) = 0
        Set newVport = ThisDrawing.PaperSpace. _
                                        AddPViewport(center, 6, 5)
     
        ' Change the view direction for the viewport
        Dim viewDir(0 To 2) As Double
        viewDir(0) = 1
        viewDir(1) = 1
        viewDir(2) = 1
        newVport.direction = viewDir
     
        ' Enable the viewport
        newVport.Display True
     
        ' Switch to model space
        ThisDrawing.MSpace = True
     
        ' Set newVport current
        ' (not always necessary but a good idea)
        ThisDrawing.ActivePViewport = newVport
    End Sub

Note: To set or modify aspects of the view (view direction, lens length, and so forth), the Viewport object's On property must be set to FALSE, and before you can set a viewport current the On property must be set to TRUE. 

## Create four floating viewports

This example takes the example from "Create and enable a floating viewport" and continues it by creating four floating viewports and setting the view of each to top, front, right, and isometric views, respectively. Each viewport is set to a scale of 1:2. To ensure there is something to see in these viewports, you may want to create a 3D solid sphere in Model space before trying this example. 

### C#
    
    
    using System.Runtime.InteropServices;
     
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [DllImport("acad.exe", CallingConvention = CallingConvention.Cdecl,
     EntryPoint = "?acedSetCurrentVPort@@YA?AW4ErrorStatus@Acad@@PBVAcDbViewport@@@Z")]
    extern static private int acedSetCurrentVPort(IntPtr AcDbVport);
     
    [CommandMethod("FourFloatingViewports")]
    public static void FourFloatingViewports()
    {
      // Get the current document and database, and start a transaction
      Document acDoc = Application.DocumentManager.MdiActiveDocument;
      Database acCurDb = acDoc.Database;
     
      using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
      {
          // Open the Block table for read
          BlockTable acBlkTbl;
          acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                       OpenMode.ForRead) as BlockTable;
     
          // Open the Block table record Paper space for write
          BlockTableRecord acBlkTblRec;
          acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.PaperSpace],
                                          OpenMode.ForWrite) as BlockTableRecord;
     
          // Switch to the previous Paper space layout
          Application.SetSystemVariable("TILEMODE", 0);
          acDoc.Editor.SwitchToPaperSpace();
     
          Point3dCollection acPt3dCol = new Point3dCollection();
          acPt3dCol.Add(new Point3d(2.5, 5.5, 0));
          acPt3dCol.Add(new Point3d(2.5, 2.5, 0));
          acPt3dCol.Add(new Point3d(5.5, 5.5, 0));
          acPt3dCol.Add(new Point3d(5.5, 2.5, 0));
     
          Vector3dCollection acVec3dCol = new Vector3dCollection();
          acVec3dCol.Add(new Vector3d(0, 0, 1));
          acVec3dCol.Add(new Vector3d(0, 1, 0));
          acVec3dCol.Add(new Vector3d(1, 0, 0));
          acVec3dCol.Add(new Vector3d(1, 1, 1));
     
          double dWidth = 2.5;
          double dHeight = 2.5;
     
          Viewport acVportLast = null;
          int nCnt = 0;
     
          foreach (Point3d acPt3d in acPt3dCol)
          {
              using (Viewport acVport = new Viewport())
              {
                  acVport.CenterPoint = acPt3d;
                  acVport.Width = dWidth;
                  acVport.Height = dHeight;
    
                  // Add the new object to the block table record and the transaction
                  acBlkTblRec.AppendEntity(acVport);
                  acTrans.AddNewlyCreatedDBObject(acVport, true);
    
                  // Change the view direction
                  acVport.ViewDirection = acVec3dCol[nCnt];
    
                  // Enable the viewport
                  acVport.On = true;
    
                  // Record the last viewport created
                  acVportLast = acVport;
    
                  // Increment the counter by 1
                  nCnt = nCnt + 1;
              }
          }
     
          if (acVportLast != null)
          {
              // Activate model space in the viewport
              acDoc.Editor.SwitchToModelSpace();
     
              // Set the new viewport current via an imported ObjectARX function
              acedSetCurrentVPort(acVportLast.UnmanagedObject);
          }
     
          // Save the new objects to the database
          acTrans.Commit();
      }
    }

### VB.NET
    
    
    Imports System.Runtime.InteropServices
     
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <DllImport("acad.exe", CallingConvention:=CallingConvention.Cdecl, _
     EntryPoint:="?acedSetCurrentVPort@@YA?AW4ErrorStatus@Acad@@PBVAcDbViewport@@@Z")> _
    Public Shared Function acedSetCurrentVPort(ByVal AcDbVport As IntPtr) As IntPtr
    End Function
     
    <CommandMethod("FourFloatingViewports")> _
    Public Sub FourFloatingViewports()
      '' Get the current document and database, and start a transaction
      Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
      Dim acCurDb As Database = acDoc.Database
     
      Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
          '' Open the Block table for read
          Dim acBlkTbl As BlockTable
          acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                       OpenMode.ForRead)
     
          '' Open the Block table record Paper space for write
          Dim acBlkTblRec As BlockTableRecord
          acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.PaperSpace), _
                                          OpenMode.ForWrite)
     
          '' Switch to the previous Paper space layout
          Application.SetSystemVariable("TILEMODE", 0)
          acDoc.Editor.SwitchToPaperSpace()
     
          Dim acPt3dCol As Point3dCollection = New Point3dCollection()
          acPt3dCol.Add(New Point3d(2.5, 5.5, 0))
          acPt3dCol.Add(New Point3d(2.5, 2.5, 0))
          acPt3dCol.Add(New Point3d(5.5, 5.5, 0))
          acPt3dCol.Add(New Point3d(5.5, 2.5, 0))
     
          Dim acVec3dCol As Vector3dCollection = New Vector3dCollection()
          acVec3dCol.Add(New Vector3d(0, 0, 1))
          acVec3dCol.Add(New Vector3d(0, 1, 0))
          acVec3dCol.Add(New Vector3d(1, 0, 0))
          acVec3dCol.Add(New Vector3d(1, 1, 1))
     
          Dim dWidth As Double = 2.5
          Dim dHeight As Double = 2.5
     
          Dim acVportLast As Viewport = Nothing
          Dim nCnt As Integer = 0
     
          For Each acPt3d As Point3d In acPt3dCol
              Using acVport As Viewport = New Viewport()
                  acVport.CenterPoint = acPt3d
                  acVport.Width = dWidth
                  acVport.Height = dHeight
    
                  '' Add the new object to the block table record and the transaction
                  acBlkTblRec.AppendEntity(acVport)
                  acTrans.AddNewlyCreatedDBObject(acVport, True)
    
                  '' Change the view direction
                  acVport.ViewDirection = acVec3dCol(nCnt)
    
                  '' Enable the viewport
                  acVport.On = True
    
                  '' Record the last viewport created
                  acVportLast = acVport
    
                  '' Increment the counter by 1
                  nCnt = nCnt + 1
              End Using
          Next
     
          If acVportLast <> Nothing Then
              '' Activate model space in the viewport
              acDoc.Editor.SwitchToModelSpace()
     
              '' Set the new viewport current via an imported ObjectARX function
              acedSetCurrentVPort(acVportLast.UnmanagedObject)
          End If
     
          '' Save the new objects to the database
          acTrans.Commit()
      End Using
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub FourFloatingViewports()
        Dim topVport, frontVport As AcadPViewport
        Dim rightVport, isoVport As AcadPViewport
        Dim pt(0 To 2) As Double
        Dim viewDir(0 To 2) As Double
        ThisDrawing.ActiveSpace = acPaperSpace
        ThisDrawing.MSpace = True
     
        ' Take the existing PViewport and make it the topVport
        pt(0) = 2.5: pt(1) = 5.5: pt(2) = 0
        Set topVport = ThisDrawing.ActivePViewport
        ' No need to set Direction for top view
        topVport.center = pt
        topVport.width = 2.5
        topVport.height = 2.5
        topVport.Display True
        topVport.StandardScale = acVp1_2
     
        ' Create and setup frontVport
        pt(0) = 2.5: pt(1) = 2.5: pt(2) = 0
        Set frontVport = ThisDrawing.PaperSpace. _
                                          AddPViewport(pt, 2.5, 2.5)
        viewDir(0) = 0: viewDir(1) = 1: viewDir(2) = 0
        frontVport.direction = viewDir
        frontVport.Display acOn
        frontVport.StandardScale = acVp1_2
     
        ' Create and setup rightVport
        pt(0) = 5.5: pt(1) = 5.5: pt(2) = 0
        Set rightVport = ThisDrawing.PaperSpace. _
                                          AddPViewport(pt, 2.5, 2.5)
        viewDir(0) = 1: viewDir(1) = 0: viewDir(2) = 0
        rightVport.direction = viewDir
        rightVport.Display acOn
        rightVport.StandardScale = acVp1_2
     
        ' Create and set up isoVport
        pt(0) = 5.5: pt(1) = 2.5: pt(2) = 0
        Set isoVport = ThisDrawing.PaperSpace. _
                                        AddPViewport(pt, 2.5, 2.5)
        viewDir(0) = 1: viewDir(1) = 1: viewDir(2) = 1
        isoVport.direction = viewDir
        isoVport.Display acOn
        isoVport.StandardScale = acVp1_2
     
        ThisDrawing.MSpace = True
        ThisDrawing.ActivePViewport = isoVport
     
        ' Finish: Perform a regen in all viewports
        ThisDrawing.Regen True
    End Sub

## Create a nonrectangular viewport

This example creates a rectangular viewport and then uses a circle as the clipping boundary. 

### C#
    
    
    using System.Runtime.InteropServices;
     
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
     
    [DllImport("acad.exe", CallingConvention = CallingConvention.Cdecl,
     EntryPoint = "?acedSetCurrentVPort@@YA?AW4ErrorStatus@Acad@@PBVAcDbViewport@@@Z")]
    extern static private int acedSetCurrentVPort(IntPtr AcDbVport);
     
    [CommandMethod("CreateNonRectangularFloatingViewport")]
    public static void CreateNonRectangularFloatingViewport()
    {
        // Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Block table for read
            BlockTable acBlkTbl;
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId,
                                         OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Paper space for write
            BlockTableRecord acBlkTblRec;
            acBlkTblRec = acTrans.GetObject(acBlkTbl[BlockTableRecord.PaperSpace],
                                            OpenMode.ForWrite) as BlockTableRecord;
    
            // Switch to the previous Paper space layout
            Application.SetSystemVariable("TILEMODE", 0);
            acDoc.Editor.SwitchToPaperSpace();
    
            // Create a Viewport
            using (Viewport acVport = new Viewport())
            {
                acVport.CenterPoint = new Point3d(9, 6.5, 0);
                acVport.Width = 2.5;
                acVport.Height = 2.5;
    
                // Set the scale to 1" = 8'
                acVport.CustomScale = 96;
    
                // Create a circle
                using (Circle acCirc = new Circle())
                {
                    acCirc.Center = acVport.CenterPoint;
                    acCirc.Radius = 1.25;
    
                    // Add the new object to the block table record and the transaction
                    acBlkTblRec.AppendEntity(acCirc);
                    acTrans.AddNewlyCreatedDBObject(acCirc, true);
    
                    // Clip the viewport using the circle  
                    acVport.NonRectClipEntityId = acCirc.ObjectId;
                    acVport.NonRectClipOn = true;
                }
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acVport);
                acTrans.AddNewlyCreatedDBObject(acVport, true);
    
                // Change the view direction
                acVport.ViewDirection = new Vector3d(0, 0, 1);
    
                // Enable the viewport
                acVport.On = true;
    
                // Activate model space in the viewport
                acDoc.Editor.SwitchToModelSpace();
    
                // Set the new viewport current via an imported ObjectARX function
                acedSetCurrentVPort(acVport.UnmanagedObject);
            }
    
            // Save the new objects to the database
            acTrans.Commit();
        }
    }

### VB.NET
    
    
    Imports System.Runtime.InteropServices
     
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
     
    <DllImport("acad.exe", CallingConvention:=CallingConvention.Cdecl, _
     EntryPoint:="?acedSetCurrentVPort@@YA?AW4ErrorStatus@Acad@@PBVAcDbViewport@@@Z")> _
    Public Shared Function acedSetCurrentVPort(ByVal AcDbVport As IntPtr) As IntPtr
    End Function
     
    <CommandMethod("CreateNonRectangularFloatingViewport")> _
    Public Sub CreateNonRectangularFloatingViewport()
        '' Get the current document and database, and start a transaction
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            '' Open the Block table for read
            Dim acBlkTbl As BlockTable
            acBlkTbl = acTrans.GetObject(acCurDb.BlockTableId, _
                                         OpenMode.ForRead)
    
            '' Open the Block table record Paper space for write
            Dim acBlkTblRec As BlockTableRecord
            acBlkTblRec = acTrans.GetObject(acBlkTbl(BlockTableRecord.PaperSpace), _
                                            OpenMode.ForWrite)
    
            '' Switch to the previous Paper space layout
            Application.SetSystemVariable("TILEMODE", 0)
            acDoc.Editor.SwitchToPaperSpace()
    
            '' Create a rectangular viewport to change to a non-rectangular viewport
            Using acVport As Viewport = New Viewport()
                acVport.CenterPoint = New Point3d(9, 6.5, 0)
                acVport.Width = 2.5
                acVport.Height = 2.5
    
                '' Set the scale to 1" = 8'
                acVport.CustomScale = 96
    
                '' Create a circle
                Using acCirc As Circle = New Circle()
                    acCirc.Center = acVport.CenterPoint
                    acCirc.Radius = 1.25
    
                    '' Add the new object to the block table record and the transaction
                    acBlkTblRec.AppendEntity(acCirc)
                    acTrans.AddNewlyCreatedDBObject(acCirc, True)
    
                    '' Clip the viewport using the circle  
                    acVport.NonRectClipEntityId = acCirc.ObjectId
                    acVport.NonRectClipOn = True
                End Using
    
                '' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acVport)
                acTrans.AddNewlyCreatedDBObject(acVport, True)
    
                '' Change the view direction
                acVport.ViewDirection = New Vector3d(0, 0, 1)
    
                '' Enable the viewport
                acVport.On = True
    
                '' Activate model space
                acDoc.Editor.SwitchToModelSpace()
    
                '' Set the new viewport current via an imported ObjectARX function
                acedSetCurrentVPort(acVport.UnmanagedObject)
            End Using
    
            '' Save the new objects to the database
            acTrans.Commit()
        End Using
    End Sub
