<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Draw With Precision (.NET) > Calculate Points and Values (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-9825A799-D48C-4E72-A7EB-6200AE5F452E.htm -->

# Calculate Points and Values (.NET)

By using the methods provided by the Editor object and the Geometry and Runtime namespaces, you can quickly solve a mathematical problem or locate points in your drawing. Some of the available methods are: 

  * Get the distance between two 2D or 3D points using the GetDistanceTo and DistanceTo methods 
  * Get the angle from the X-axis using two 2D points using the GetVectorTo method with the Angle property of the returned value 
  * Convert an angle as a string to a real (double) value with the StringToAngle method 
  * Convert an angle from a real (double) value to a string with the AngleToString method 
  * Convert a distance from a string to a real (double) value with the StringToDistance method 
  * Find the distance between two points entered by the user with the GetDistance method 

Note: The AutoCAD .NET API does not contain methods to calculate a point based on a distance and angle (polar point) and for translating coordinates between different coordinate systems. If you need these utilities, you will want to utilize the PolarPoint and TranslateCoordinates methods from the ActiveX Automation library. 

## Get angle from X-axis

This example calculates a vector between two points and determines the angle from the X-axis. 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.Geometry;
     
    [CommandMethod("AngleFromXAxis")]
    public static void AngleFromXAxis()
    {
      Point2d pt1 = new Point2d(2, 5);
      Point2d pt2 = new Point2d(5, 2);
     
      Application.ShowAlertDialog("Angle from XAxis: " +
                                  pt1.GetVectorTo(pt2).Angle.ToString());
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.Geometry
     
    <CommandMethod("AngleFromXAxis")> _
    Public Sub AngleFromXAxis()
      Dim pt1 As Point2d = New Point2d(2, 5)
      Dim pt2 As Point2d = New Point2d(5, 2)
     
      Application.ShowAlertDialog("Angle from XAxis: " & _
                                  pt1.GetVectorTo(pt2).Angle.ToString())
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub AngleFromXAxis()
        ' This example finds the angle, in radians, between the X axis
        ' and a line defined by two points.
     
        Dim pt1(0 To 2) As Double
        Dim pt2(0 To 2) As Double
        Dim retAngle As Double
     
        pt1(0) = 2: pt1(1) = 5: pt1(2) = 0
        pt2(0) = 5: pt2(1) = 2: pt2(2) = 0
     
        ' Return the angle
        retAngle = ThisDrawing.Utility.AngleFromXAxis(pt1, pt2)
     
        ' Display the angle found
        MsgBox "The angle in radians between the X axis is " & retAngle
    End Sub

## Calculate Polar Point

This example calculates a point based on a base point, an angle and distance. 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.Geometry;
     
    static Point2d PolarPoints(Point2d pPt, double dAng, double dDist)
    {
      return new Point2d(pPt.X + dDist * Math.Cos(dAng),
                         pPt.Y + dDist * Math.Sin(dAng));
    }
     
    static Point3d PolarPoints(Point3d pPt, double dAng, double dDist)
    {
      return new Point3d(pPt.X + dDist * Math.Cos(dAng),
                         pPt.Y + dDist * Math.Sin(dAng),
                         pPt.Z);
    }
     
    [CommandMethod("PolarPoints")]
    public static void PolarPoints()
    {
      Point2d pt1 = PolarPoints(new Point2d(5, 2), 0.785398, 12);
     
      Application.ShowAlertDialog("\nPolarPoint: " +
                                  "\nX = " + pt1.X +
                                  "\nY = " + pt1.Y);
     
      Point3d pt2 = PolarPoints(new Point3d(5, 2, 0), 0.785398, 12);
     
      Application.ShowAlertDialog("\nPolarPoint: " +
                                  "\nX = " + pt2.X +
                                  "\nY = " + pt2.Y +
                                  "\nZ = " + pt2.Z);
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.Geometry
     
    Public Shared Function PolarPoints(ByVal pPt As Point2d, _
                                       ByVal dAng As Double, _
                                       ByVal dDist As Double)
     
      Return New Point2d(pPt.X + dDist * Math.Cos(dAng), _
                         pPt.Y + dDist * Math.Sin(dAng))
    End Function
     
    Public Shared Function PolarPoints(ByVal pPt As Point3d, _
                                       ByVal dAng As Double, _
                                       ByVal dDist As Double)
     
      Return New Point3d(pPt.X + dDist * Math.Cos(dAng), _
                         pPt.Y + dDist * Math.Sin(dAng), _
                         pPt.Z)
    End Function
     
    <CommandMethod("PolarPoints")> _
    Public Sub PolarPoints()
      Dim pt1 As Point2d
      pt1 = PolarPoints(New Point2d(5, 2), 0.785398, 12)
     
      Application.ShowAlertDialog(vbLf & "PolarPoint: " & _
                                  vbLf & "X = " & pt1.X & _
                                  vbLf & "Y = " & pt1.Y)
     
      Dim pt2 As Point3d
      pt2 = PolarPoints(New Point3d(5, 2, 0), 0.785398, 12)
     
      Application.ShowAlertDialog(vbLf & "PolarPoint: " & _
                                  vbLf & "X = " & pt2.X & _
                                  vbLf & "Y = " & pt2.Y & _
                                  vbLf & "Z = " & pt2.Z)
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub PolarPoints()
        ' This example finds the coordinate of a point that is a given
        ' distance and angle from a base point.
     
        Dim polarPnt As Variant
        Dim basePnt(0 To 2) As Double
        Dim angle As Double
        Dim distance As Double
     
        basePnt(0) = 2#: basePnt(1) = 2#: basePnt(2) = 0#
        angle = 0.785398
        distance = 6
        polarPnt = ThisDrawing.Utility.PolarPoint(basePnt, angle, distance)
     
        MsgBox vbLf + "PolarPoint: " + _
               vbLf + "X = " + CStr(polarPnt(0)) + _
               vbLf + "Y = " + CStr(polarPnt(1)) + _
               vbLf + "Z = " + CStr(polarPnt(2))
    End Sub

## Find the distance between two points with the GetDistance method

This example uses the GetDistance method to obtain two points and displays the calculated distance. 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.EditorInput;
    using Autodesk.AutoCAD.Runtime;
     
    [CommandMethod("GetDistanceBetweenTwoPoints")]
    public static void GetDistanceBetweenTwoPoints()
    {
      Document acDoc = Application.DocumentManager.MdiActiveDocument;
     
      PromptDoubleResult pDblRes;
      pDblRes = acDoc.Editor.GetDistance("\nPick two points: ");
     
      Application.ShowAlertDialog("\nDistance between points: " +
                                  pDblRes.Value.ToString());
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.EditorInput
    Imports Autodesk.AutoCAD.Runtime
     
    <CommandMethod("GetDistanceBetweenTwoPoints")> _
    Public Sub GetDistanceBetweenTwoPoints()
      Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
     
      Dim pDblRes As PromptDoubleResult
      pDblRes = acDoc.Editor.GetDistance(vbLf & "Pick two points: ")
     
      Application.ShowAlertDialog(vbLf & "Distance between points: " & _
                                  pDblRes.Value.ToString())
    End Sub

### VBA/ActiveX Code Reference
    
    
    Sub GetDistanceBetweenTwoPoints()
        Dim returnDist As Double
     
        ' Return the value entered by user. A prompt is provided.
        returnDist = ThisDrawing.Utility.GetDistance(, "Pick two points.")
     
        MsgBox "The distance between the two points is: " & returnDist
    End Sub
