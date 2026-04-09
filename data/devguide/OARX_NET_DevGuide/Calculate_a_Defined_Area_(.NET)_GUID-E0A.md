<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Draw With Precision (.NET) > Calculate Areas (.NET) > Calculate a Defined Area (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-E0A39BC4-5C46-40D1-8507-A5F9E8D82E70.htm -->

# Calculate a Defined Area (.NET)

If the area you want to calculate is based on user specified points, you might consider creating an in memory object such as a lightweight polyline, and then query of the area of the object before discarding it. The following steps explain how you might accomplish this: 

  1. Use the GetPoint method in a loop to obtain the points from the user. 
  2. Create a lightweight polyline from the points provided by the user. Create a new Polyline object. Specify the number of vertices and the points they should be at. 
  3. Use the Area property to obtain the area of the newly created polyline. 
  4. Dispose of the polyline using its Dispose method. 

## Calculate the area defined by points entered from the user

This example prompts the user to enter five points. A polyline is then created out of the points entered. The polyline is closed, and the area of the polyline is displayed in a message box. Since the polyline is not added to a block, it needs to be disposed before the command ends. 

### C#
    
    
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    using Autodesk.AutoCAD.EditorInput;
    using Autodesk.AutoCAD.Runtime;
     
    [CommandMethod("CalculateDefinedArea")]
    public static void CalculateDefinedArea()
    {
        // Prompt the user for 5 points
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
     
        PromptPointResult pPtRes;
        Point2dCollection colPt = new Point2dCollection();
        PromptPointOptions pPtOpts = new PromptPointOptions("");
     
        // Prompt for the first point
        pPtOpts.Message = "\nSpecify first point: ";
        pPtRes = acDoc.Editor.GetPoint(pPtOpts);
        colPt.Add(new Point2d(pPtRes.Value.X, pPtRes.Value.Y));
     
        // Exit if the user presses ESC or cancels the command
        if (pPtRes.Status == PromptStatus.Cancel) return;
     
        int nCounter = 1;
     
        while (nCounter <= 4)
        {
            // Prompt for the next points
            switch(nCounter)
            {
                case 1:
                    pPtOpts.Message = "\nSpecify second point: ";
                    break;
                case 2:
                    pPtOpts.Message = "\nSpecify third point: ";
                    break;
                case 3:
                    pPtOpts.Message = "\nSpecify fourth point: ";
                    break;
                case 4:
                    pPtOpts.Message = "\nSpecify fifth point: ";
                    break;
            }
     
            // Use the previous point as the base point
            pPtOpts.UseBasePoint = true;
            pPtOpts.BasePoint = pPtRes.Value;
     
            pPtRes = acDoc.Editor.GetPoint(pPtOpts);
            colPt.Add(new Point2d(pPtRes.Value.X, pPtRes.Value.Y));
     
            if (pPtRes.Status == PromptStatus.Cancel) return;
     
            // Increment the counter
            nCounter = nCounter + 1;
        }
     
        // Create a polyline with 5 points
        using (Polyline acPoly = new Polyline())
        {
            acPoly.AddVertexAt(0, colPt[0], 0, 0, 0);
            acPoly.AddVertexAt(1, colPt[1], 0, 0, 0);
            acPoly.AddVertexAt(2, colPt[2], 0, 0, 0);
            acPoly.AddVertexAt(3, colPt[3], 0, 0, 0);
            acPoly.AddVertexAt(4, colPt[4], 0, 0, 0);
     
            // Close the polyline
            acPoly.Closed = true;
     
            // Query the area of the polyline
            Application.ShowAlertDialog("Area of polyline: " +
                                        acPoly.Area.ToString());
     
            // Dispose of the polyline
        }
    }

#### VB.NET
    
    
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    Imports Autodesk.AutoCAD.EditorInput
    Imports Autodesk.AutoCAD.Runtime
     
    <CommandMethod("CalculateDefinedArea")> _
    Public Sub CalculateDefinedArea()
        '' Prompt the user for 5 points
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
     
        Dim pPtRes As PromptPointResult
        Dim colPt As Point2dCollection = New Point2dCollection
        Dim pPtOpts As PromptPointOptions = New PromptPointOptions("")
     
        '' Prompt for the first point
        pPtOpts.Message = vbLf & "Specify first point: "
        pPtRes = acDoc.Editor.GetPoint(pPtOpts)
        colPt.Add(New Point2d(pPtRes.Value.X, pPtRes.Value.Y))
     
        '' Exit if the user presses ESC or cancels the command
        If pPtRes.Status = PromptStatus.Cancel Then Exit Sub
     
        Dim nCounter As Integer = 1
     
        While (nCounter <= 4)
            '' Prompt for the next points
            Select Case nCounter
                Case 1
                    pPtOpts.Message = vbLf & "Specify second point: "
                Case 2
                    pPtOpts.Message = vbLf & "Specify third point: "
                Case 3
                    pPtOpts.Message = vbLf & "Specify fourth point: "
                Case 4
                    pPtOpts.Message = vbLf & "Specify fifth point: "
            End Select
     
            '' Use the previous point as the base point
            pPtOpts.UseBasePoint = True
            pPtOpts.BasePoint = pPtRes.Value
     
            pPtRes = acDoc.Editor.GetPoint(pPtOpts)
            colPt.Add(New Point2d(pPtRes.Value.X, pPtRes.Value.Y))
     
            If pPtRes.Status = PromptStatus.Cancel Then Exit Sub
     
            '' Increment the counter
            nCounter = nCounter + 1
       End While
     
        '' Create a polyline with 5 points
        Using acPoly As Polyline = New Polyline()
            acPoly.AddVertexAt(0, colPt(0), 0, 0, 0)
            acPoly.AddVertexAt(1, colPt(1), 0, 0, 0)
            acPoly.AddVertexAt(2, colPt(2), 0, 0, 0)
            acPoly.AddVertexAt(3, colPt(3), 0, 0, 0)
            acPoly.AddVertexAt(4, colPt(4), 0, 0, 0)
     
            '' Close the polyline
            acPoly.Closed = True
     
            '' Query the area of the polyline
            Application.ShowAlertDialog("Area of polyline: " & _
                                        acPoly.Area.ToString())
     
            '' Dispose of the polyline
        End Using
    End Sub

### VBA/ActiveX Code Reference

This example prompts the user to enter five points. A polyline is then created out of the points entered. The polyline is closed, and the area of the polyline is displayed in a message box. Unlike the AutoCAD .NET API examples, the polyline is not created in memory but as a database resident object and added to Model space. So after the area of the polyline is obtained, it is removed. 
    
    
    Sub CalculateDefinedArea()
        Dim p1 As Variant
        Dim p2 As Variant
        Dim p3 As Variant
        Dim p4 As Variant
        Dim p5 As Variant
     
        ' Get the points from the user
        p1 = ThisDrawing.Utility.GetPoint(, vbCrLf & "Specify first point: ")
        p2 = ThisDrawing.Utility.GetPoint(p1, vbCrLf & "Specify second point: ")
        p3 = ThisDrawing.Utility.GetPoint(p2, vbCrLf & "Specify third point: ")
        p4 = ThisDrawing.Utility.GetPoint(p3, vbCrLf & "Specify fourth point: ")
        p5 = ThisDrawing.Utility.GetPoint(p4, vbCrLf & "Specify fifth point: ")
     
        ' Create the 2D polyline from the points
        Dim polyObj As AcadLWPolyline
        Dim vertices(0 To 9) As Double
        vertices(0) = p1(0): vertices(1) = p1(1)
        vertices(2) = p2(0): vertices(3) = p2(1)
        vertices(4) = p3(0): vertices(5) = p3(1)
        vertices(6) = p4(0): vertices(7) = p4(1)
        vertices(8) = p5(0): vertices(9) = p5(1)
        Set polyObj = ThisDrawing.ModelSpace.AddLightWeightPolyline _
                          (vertices)
        polyObj.Closed = True
     
        ' Display the area for the polyline
        MsgBox "The area defined by the points is " & _
               polyObj.Area, , "Calculate Defined Area"
     
        ' Remove the polyline
        polyObj.Delete
    End Sub
