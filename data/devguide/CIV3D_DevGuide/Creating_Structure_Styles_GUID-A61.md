<!-- Developer's Guide > API Developer's Guide > Pipe Networks > Structures > Creating Structure Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-A61D50BF-6687-4631-A8EB-0445EA9FBE54.htm -->

# Creating Structure Styles

A structure style controls the visual appearance of structures in a document. All structure style objects are stored in the CivilDocument.Styles.StructureStyles property. Structure styles have four methods for controlling general appearance attributes and three properties for controlling display attributes that are specific to structures. The methods GetDisplayStylePlan|Profile|Section() and GetHatchStyleProfile() all take a parameter describing the feature being modified and return a reference to the DisplayStyle or HatchDisplayStyle object controlling common display attributes such as line styles and color. The properties PlanOption, ProfileOption, SectionOption, and ModelOption set the display size of the structure and whether the structure is shown as a model of the physical object or only symbolically. A structure object is given a style by assigning the Structure.StyleId or Structure.StyleName property to a StructureStyle object.

This sample attempts to create a new structure style object and set some of its properties. If the style already exists, it changes the existing style:
    
    
    Public Function CreateStructureStyle(ByVal sStyleName As String) As StructureStyle
        Dim oStructureStyle As StructureStyle
        Dim oStructureStyleId As ObjectId
        Dim trans As Transaction = tm.StartTransaction()
        Try
            oStructureStyleId = g_oDocument.Styles.StructureStyles.Add(sStyleName)
        Catch
        End Try
        If (oStructureStyleId = ObjectId.Null) Then
            Try
                oStructureStyleId = g_oDocument.Styles.StructureStyles.Item(sStyleName)
            Catch
            End Try
            If (oStructureStyleId = ObjectId.Null) Then
                MsgBox("Could not create or use a structure style with the name:" & sStyleName)
                CreateStructureStyle = Nothing
                Exit Function
            End If
        End If
        oStructureStyle = trans.GetObject(oStructureStyleId, OpenMode.ForWrite)
        oStructureStyle.GetDisplayStylePlan(StructureDisplayStylePlanType.Structure).Color = Color.FromRgb(255, 191, 0) ' orange
        oStructureStyle.GetDisplayStylePlan(StructureDisplayStylePlanType.Structure).Visible = True
        oStructureStyle.PlanOption.MaskConnectedObjects = False
        oStructureStyle.PlanOption.SizeType = StructureSizeOptionsType.UseDrawingScale
        oStructureStyle.PlanOption.Size = 0.0035
        oStructureStyle.GetDisplayStyleSection(StructureDisplayStylePlanType.Structure).Visible = False
        oStructureStyle.GetDisplayStyleSection(StructureDisplayStylePlanType.StructureHatch).Visible = False
        oStructureStyle.GetDisplayStylePlan(StructureDisplayStylePlanType.StructureHatch).Visible = False
        oStructureStyle.GetDisplayStyleProfile(StructureDisplayStylePlanType.Structure).Visible = False
        oStructureStyle.GetDisplayStyleProfile(StructureDisplayStylePlanType.StructureHatch).Visible = False
        trans.Commit()
        ed.WriteMessage("Create StructureStyle Successful." + Convert.ToChar(10))
        CreateStructureStyle = oStructureStyle
    End Function ' CreateStructureStyle
