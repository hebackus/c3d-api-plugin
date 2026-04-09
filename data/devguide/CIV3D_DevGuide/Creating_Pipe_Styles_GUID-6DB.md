<!-- Developer's Guide > API Developer's Guide > Pipe Networks > Pipes > Creating Pipe Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-6DBF9EA6-1DC2-4151-939F-9633099CFC7C.htm -->

# Creating Pipe Styles

A pipe style controls the visual appearance of pipes in a document. All pipe style objects in a document are stored in the CivilDocument.PipeStyles collection. Pipe styles have four display methods and three hatch methods for controlling general appearance attributes and three properties for controlling display attributes that are specific to pipes. The methods GetDisplayStyleProfile|Section|Plan(), and GetHatchStyleProfile() all take a parameter describing the feature being modified, and return a reference to the DisplayStyle or HatchDisplayStyle object controlling common display attributes, such as line styles and color. The methods GetDisplayStyleModel(), GetHatchStylePlan(), and GetHatchStyleSection() do not take a component parameter.

The properties PlanOption and ProfileOption set the size of the inner wall, outer wall, and end lines according to either the physical properties of the pipe, custom sizes using drawing units, or a certain percentage of its previous drawing size. The HatchOption property sets the area of the pipe covered by any hatching used. A pipe object is given a style by assigning the Pipe.Style property to a PipeStyle object.

This sample attempts to create a new pipe style object and set some of its properties. If a style already exists with the same name, it sets the properties on the existing style:
    
    
    Public Function CreatePipeStyle(ByVal sStyleName As String) As PipeStyle
        Dim oPipeStyleId As ObjectId
        Dim oPipeStyle As PipeStyle
        Dim trans As Transaction = tm.StartTransaction()
        Try
            oPipeStyleId = g_oDocument.Styles.PipeStyles.Add(sStyleName)
        Catch
        End Try
        If (oPipeStyleId = ObjectId.Null) Then
            Try
                oPipeStyleId = g_oDocument.Styles.PipeStyles.Item(sStyleName)
            Catch
            End Try
            If (oPipeStyleId = ObjectId.Null) Then
                MsgBox("Could not create or use a pipe style with the name:" & sStyleName)
                CreatePipeStyle = Nothing
                Exit Function
            End If
        End If
        oPipeStyle = trans.GetObject(oPipeStyleId, OpenMode.ForWrite)
        ' Set the display size of the pipes in plan view.  We will
        ' use absolute drawing units for the inside, outside, and
        ' ends of each pipe.
        ' enter a value greater than or equal to 0.000mm and less than or equal to 1000.000mm
        oPipeStyle.PlanOption.InnerDiameter = 0.0021
        oPipeStyle.PlanOption.OuterDiameter = 0.0024
        ' Indicate that we will use our own measurements for the inside
        ' and outside of the pipe, and not base drawing on the actual
        ' type of pipe.
        oPipeStyle.PlanOption.WallSizeType = PipeWallSizeType.UserDefinedWallSize
        ' Inidcate what kind of custom sizing to use.
        oPipeStyle.PlanOption.WallSizeOptions = PipeUserDefinedType.UseDrawingScale
        oPipeStyle.PlanOption.EndLineSize = 0.0021
        ' Indicate that we will use our own measurements for the end 
        'line of the pipe, and not base drawing on the actual type
        ' of pipe.
        oPipeStyle.PlanOption.EndSizeType = PipeEndSizeType.UserDefinedEndSize
        ' Inidcate what kind of custom sizing to use.
        oPipeStyle.PlanOption.EndSizeOptions = PipeUserDefinedType.UseDrawingScale
        '
        ' Modify the colors of pipes using this style, as shown 
        'in plan view.
        oPipeStyle.GetDisplayStylePlan(PipeDisplayStylePlanType.OutsideWalls).Color = Color.FromRgb(255, 191, 0)  ' orange, ColorIndex = 40
        oPipeStyle.GetDisplayStylePlan(PipeDisplayStylePlanType.InsideWalls).Color = Color.FromRgb(191, 0, 255) ' violet, ColorIndex = 200
        oPipeStyle.GetDisplayStylePlan(PipeDisplayStylePlanType.EndLine).Color = Color.FromRgb(191, 0, 255) ' violet, ColorIndex = 200
        '
        ' Set the hatch style for pipes using this style, as shown 
        'in plan view.
        oPipeStyle.GetHatchStylePlan().Pattern = "DOTS"
        oPipeStyle.GetHatchStylePlan().HatchType = Autodesk.Civil.DatabaseServices.Styles.HatchType.PreDefined
        oPipeStyle.GetHatchStylePlan().UseAngleOfObject = False
        oPipeStyle.GetHatchStylePlan().ScaleFactor = 9.0#
        oPipeStyle.GetDisplayStylePlan(PipeDisplayStylePlanType.Hatch).Color = Color.FromRgb(0, 255, 191) ' turquose, ColorIndex = 120
        oPipeStyle.GetDisplayStylePlan(PipeDisplayStylePlanType.Hatch).Visible = True
        oPipeStyle.PlanOption.HatchOptions = PipeHatchType.HatchToInnerWalls
        trans.Commit()
        ed.WriteMessage("Create PipeStyle succeeded." + Convert.ToChar(10))
        CreatePipeStyle = oPipeStyle
    End Function ' CreatePipeStyle
