<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Visual Styles (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-C6DA4EF7-1DFE-4D7A-A55D-62EA06E44997.htm -->

# Visual Styles (.NET)

Visual styles allow you to control the way objects appear on screen and during output. Visual styles are stored in a drawing as part of the Visual Style dictionary and they can all be customized. Since all visual styles can be customized, you cannot expect each drawing contains all the standard visual styles that are part of the drawing templates that ship with AutoCAD. A visual style is represented by the DBVisualStyle class. 

## List the available visual styles

This example lists the visual styles that are stored in the current drawing. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Colors;
    using Autodesk.AutoCAD.GraphicsInterface;
    
    // Lists the available visual styles
    [CommandMethod("ListVisualStyle")]
    public static void ListVisualStyle()
    {
        // Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            DBDictionary vStyles = acTrans.GetObject(acCurDb.VisualStyleDictionaryId, 
                                                     OpenMode.ForRead) as DBDictionary;
    
            // Output a message to the Command Line history
            acDoc.Editor.WriteMessage("\nVisual styles: ");
    
            // Step through the dictionary
            foreach (DBDictionaryEntry entry in vStyles)
            {
                // Get the dictionary entry
                DBVisualStyle vStyle = vStyles.GetAt(entry.Key).GetObject(OpenMode.ForRead) as DBVisualStyle;
    
                // If the visual style is not marked for internal use then output its name
                if (vStyle.InternalUseOnly == false)
                {
                    // Output the name of the visual style
                    acDoc.Editor.WriteMessage("\n  " + vStyle.Name);
                }
            }
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Colors
    Imports Autodesk.AutoCAD.GraphicsInterface
    
    ' Lists the available visual styles
    <CommandMethod("ListVisualStyle")> _
    Public Shared Sub ListVisualStyle()
        ' Get the current document and database, and start a transaction
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            Dim vStyles As DBDictionary = _
                acTrans.GetObject(acCurDb.VisualStyleDictionaryId, _
                                  OpenMode.ForRead)
    
            ' Output a message to the Command Line history
            acDoc.Editor.WriteMessage(vbLf & "Visual styles: ")
    
            ' Step through the dictionary
            For Each entry As DBDictionaryEntry In vStyles
                ' Get the dictionary entry
                Dim vStyle As DBVisualStyle = _
                    vStyles.GetAt(entry.Key).GetObject(OpenMode.ForRead)
    
                ' If the visual style is not marked for internal use then output its name
                If vStyle.InternalUseOnly = False Then
                    ' Output the name of the visual style
                    acDoc.Editor.WriteMessage(vbLf & "  " & vStyle.Name)
                End If
            Next
        End Using
    End Sub

## Create or edit a visual style

This example creates or edits a visual style named MyVS. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Colors;
    using Autodesk.AutoCAD.GraphicsInterface;
    
    // Creates a new visual style
    [CommandMethod("CreateVisualStyle")]
    public static void CreateVisualStyle()
    {
        // Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            DBDictionary vStyles = acTrans.GetObject(acCurDb.VisualStyleDictionaryId,
                                                     OpenMode.ForRead) as DBDictionary;
    
            try
            {
                // Check to see if the "MyVS" exists or not
                DBVisualStyle vStyle = default(DBVisualStyle);
                if (vStyles.Contains("MyVS") == true)
                {
                    vStyle = acTrans.GetObject(vStyles.GetAt("MyVS"), OpenMode.ForWrite) as DBVisualStyle;
                }
                else
                {
                    acTrans.GetObject(acCurDb.VisualStyleDictionaryId, OpenMode.ForWrite);
    
                    // Create the visual style
                    vStyle = new DBVisualStyle();
                    vStyles.SetAt("MyVS", vStyle);
    
                    // Add the visual style to the dictionary
                    acTrans.AddNewlyCreatedDBObject(vStyle, true);
                }
    
                // Set the description of the visual style
                vStyle.Description = "My Visual Style";
                vStyle.Type = VisualStyleType.Custom;
    
                // Face Settings (Opacity, Face Style, Lighting Quality, Color, 
                //                Monochrome color, Opacity, and Material Display)
                vStyle.SetTrait(VisualStyleProperty.FaceModifier, (int)VSFaceModifiers.FaceOpacityFlag, VisualStyleOperation.Set);
                vStyle.SetTrait(VisualStyleProperty.FaceLightingModel, (int)VSFaceLightingModel.Gooch, VisualStyleOperation.Set);
                vStyle.SetTrait(VisualStyleProperty.FaceLightingQuality, (int)VSFaceLightingQuality.PerPixelLighting, VisualStyleOperation.Set);
                vStyle.SetTrait(VisualStyleProperty.FaceColorMode, (int)VSFaceColorMode.ObjectColor, VisualStyleOperation.Set);
                vStyle.SetTrait(VisualStyleProperty.FaceMonoColor, Color.FromColorIndex(ColorMethod.ByAci, 1), VisualStyleOperation.Set);
                vStyle.SetTrait(VisualStyleProperty.FaceOpacity, 0.5, VisualStyleOperation.Set);
                vStyle.SetTrait(VisualStyleProperty.DisplayStyle, (int)VSDisplayStyles.MaterialsFlag + (int)VSDisplayStyles.TexturesFlag, VisualStyleOperation.Set);
    
                // Lighting (Enable Highlight Intensity, 
                //           Highlight Intensity, and Shadow Display)
                vStyle.SetTrait(VisualStyleProperty.FaceModifier, (int)vStyle.GetTrait(VisualStyleProperty.FaceModifier) + (int)VSFaceModifiers.SpecularFlag, VisualStyleOperation.Set);
                vStyle.SetTrait(VisualStyleProperty.DisplayStyle, (int)vStyle.GetTrait(VisualStyleProperty.DisplayStyle) + (int)VSDisplayStyles.LightingFlag, VisualStyleOperation.Set);
                vStyle.SetTrait(VisualStyleProperty.FaceSpecular, 45.0, VisualStyleOperation.Set);
                vStyle.SetTrait(VisualStyleProperty.DisplayShadowType, (int)VSDisplayShadowType.Full, VisualStyleOperation.Set);
    
                // Environment Settings (Backgrounds)
                vStyle.SetTrait(VisualStyleProperty.DisplayStyle, (int)vStyle.GetTrait(VisualStyleProperty.DisplayStyle) + (int)VSDisplayStyles.BackgroundsFlag, VisualStyleOperation.Set);
    
                // Edge Settings (Show, Number of Lines, Color, and Always on Top)
                vStyle.SetTrait(VisualStyleProperty.EdgeModel, (int)VSEdgeModel.Isolines, VisualStyleOperation.Set);
                vStyle.SetTrait(VisualStyleProperty.EdgeIsolines, 6, VisualStyleOperation.Set);
                vStyle.SetTrait(VisualStyleProperty.EdgeColor, Color.FromColorIndex(ColorMethod.ByAci, 2), VisualStyleOperation.Set);
                vStyle.SetTrait(VisualStyleProperty.EdgeModifier, (int)vStyle.GetTrait(VisualStyleProperty.EdgeModifier) + (int)VSEdgeModifiers.AlwaysOnTopFlag, VisualStyleOperation.Set);
    
                // Occluded Edges (Show, Color, and Linetype)
                if (!(((int)vStyle.GetTrait(VisualStyleProperty.EdgeStyle) + (int)VSEdgeStyles.ObscuredFlag) > 0))
                {
                    vStyle.SetTrait(VisualStyleProperty.EdgeStyle, (int)vStyle.GetTrait(VisualStyleProperty.EdgeStyle) + (int)VSEdgeStyles.ObscuredFlag, VisualStyleOperation.Set);
                }
                vStyle.SetTrait(VisualStyleProperty.EdgeObscuredColor, Color.FromColorIndex(ColorMethod.ByAci, 3), VisualStyleOperation.Set);
                vStyle.SetTrait(VisualStyleProperty.EdgeObscuredLinePattern, (int)VSEdgeLinePattern.DoubleMediumDash, VisualStyleOperation.Set);
    
                // Intersection Edges (Color and Linetype)
                if (!(((int)vStyle.GetTrait(VisualStyleProperty.EdgeStyle) + (int)VSEdgeStyles.IntersectionFlag) > 0))
                {
                    vStyle.SetTrait(VisualStyleProperty.EdgeStyle, (int)vStyle.GetTrait(VisualStyleProperty.EdgeStyle) + (int)VSEdgeStyles.IntersectionFlag, VisualStyleOperation.Set);
                }
                vStyle.SetTrait(VisualStyleProperty.EdgeIntersectionColor, Color.FromColorIndex(ColorMethod.ByAci, 4), VisualStyleOperation.Set);
                vStyle.SetTrait(VisualStyleProperty.EdgeIntersectionLinePattern, (int)VSEdgeLinePattern.ShortDash, VisualStyleOperation.Set);
    
                // Silhouette Edges (Color and Width)
                if (!(((int)vStyle.GetTrait(VisualStyleProperty.EdgeStyle) + (int)VSEdgeStyles.SilhouetteFlag) > 0))
                {
                    vStyle.SetTrait(VisualStyleProperty.EdgeStyle, (int)vStyle.GetTrait(VisualStyleProperty.EdgeStyle) + (int)VSEdgeStyles.SilhouetteFlag, VisualStyleOperation.Set);
                }
                vStyle.SetTrait(VisualStyleProperty.EdgeSilhouetteColor, Color.FromColorIndex(ColorMethod.ByAci, 5), VisualStyleOperation.Set);
                vStyle.SetTrait(VisualStyleProperty.EdgeSilhouetteWidth, 2, VisualStyleOperation.Set);
    
                // Edge Modifiers (Enable Line Extensions, Enable Jitter, 
                //                 Line Extensions, Jitter, Crease Angle, 
                //                 and Halo Gap)
                if (!(((int)vStyle.GetTrait(VisualStyleProperty.EdgeModifier) + (int)VSEdgeModifiers.EdgeOverhangFlag) > 0))
                {
                    vStyle.SetTrait(VisualStyleProperty.EdgeModifier, (int)vStyle.GetTrait(VisualStyleProperty.EdgeModifier) + (int)VSEdgeModifiers.EdgeOverhangFlag, VisualStyleOperation.Set);
                }
                if (!(((int)vStyle.GetTrait(VisualStyleProperty.EdgeModifier) + (int)VSEdgeModifiers.EdgeJitterFlag) > 0))
                {
                    vStyle.SetTrait(VisualStyleProperty.EdgeModifier, (int)vStyle.GetTrait(VisualStyleProperty.EdgeModifier) + (int)VSEdgeModifiers.EdgeJitterFlag, VisualStyleOperation.Set);
                }
                vStyle.SetTrait(VisualStyleProperty.EdgeOverhang, 3, VisualStyleOperation.Set);
                vStyle.SetTrait(VisualStyleProperty.EdgeJitterAmount, (int)VSEdgeJitterAmount.JitterMedium, VisualStyleOperation.Set);
                vStyle.SetTrait(VisualStyleProperty.EdgeCreaseAngle, 0.3, VisualStyleOperation.Set);
                vStyle.SetTrait(VisualStyleProperty.EdgeHaloGap, 5, VisualStyleOperation.Set);
            }
            catch (Autodesk.AutoCAD.Runtime.Exception es)
            {
                System.Windows.Forms.MessageBox.Show(es.Message);
            }
            finally
            {
                acTrans.Commit();
            }
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Colors
    Imports Autodesk.AutoCAD.GraphicsInterface
    
    ' Creates a new visual style
    <CommandMethod("CreateVisualStyle")> _
    Public Shared Sub CreateVisualStyle()
        ' Get the current document and database, and start a transaction
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            Dim vStyles As DBDictionary = _
                acTrans.GetObject(acCurDb.VisualStyleDictionaryId, _
                                  OpenMode.ForRead)
    
            Try
                ' Check to see if the "MyVS" exists or not
                Dim vStyle As DBVisualStyle
                If vStyles.Contains("MyVS") = True Then
                    vStyle = acTrans.GetObject(vStyles.GetAt("MyVS"), _
                                               OpenMode.ForWrite)
                Else
                    acTrans.GetObject(acCurDb.VisualStyleDictionaryId, OpenMode.ForWrite)
    
                    ' Create the visual style
                    vStyle = New DBVisualStyle
                    vStyles.SetAt("MyVS", vStyle)
    
                    ' Add the visual style to the dictionary
                    acTrans.AddNewlyCreatedDBObject(vStyle, True)
                End If
    
                ' Set the description of the visual style
                vStyle.Description = "My Visual Style"
                vStyle.Type = VisualStyleType.Custom
    
                ' Face Settings (Opacity, Face Style, Lighting Quality, Color, 
                '                Monochrome color, Opacity, and Material Display)
                vStyle.SetTrait(VisualStyleProperty.FaceModifier, _
                                VSFaceModifiers.FaceOpacityFlag, _
                                VisualStyleOperation.Set)
                vStyle.SetTrait(VisualStyleProperty.FaceLightingModel, _
                                VSFaceLightingModel.Gooch, _
                                VisualStyleOperation.Set)
                vStyle.SetTrait(VisualStyleProperty.FaceLightingQuality, _
                                VSFaceLightingQuality.PerPixelLighting, _
                                VisualStyleOperation.Set)
                vStyle.SetTrait(VisualStyleProperty.FaceColorMode, _
                                VSFaceColorMode.ObjectColor, _
                                VisualStyleOperation.Set)
                vStyle.SetTrait(VisualStyleProperty.FaceMonoColor, _
                                Color.FromColorIndex(ColorMethod.ByAci, 1), _
                                VisualStyleOperation.Set)
                vStyle.SetTrait(VisualStyleProperty.FaceOpacity, 0.5, _
                                VisualStyleOperation.Set)
                vStyle.SetTrait(VisualStyleProperty.DisplayStyle, _
                                VSDisplayStyles.MaterialsFlag + _
                                VSDisplayStyles.TexturesFlag, _
                                VisualStyleOperation.Set)
    
                ' Lighting (Enable Highlight Intensity, 
                '           Highlight Intensity, and Shadow Display)
                vStyle.SetTrait(VisualStyleProperty.FaceModifier, _
                                vStyle.GetTrait(VisualStyleProperty.FaceModifier) + _
                                VSFaceModifiers.SpecularFlag, _
                                VisualStyleOperation.Set)
                vStyle.SetTrait(VisualStyleProperty.DisplayStyle, _
                                vStyle.GetTrait(VisualStyleProperty.DisplayStyle) + _
                                VSDisplayStyles.LightingFlag, _
                                VisualStyleOperation.Set)
                vStyle.SetTrait(VisualStyleProperty.FaceSpecular, _
                                45.0, VisualStyleOperation.Set)
                vStyle.SetTrait(VisualStyleProperty.DisplayShadowType, _
                                VSDisplayShadowType.Full, _
                                VisualStyleOperation.Set)
    
                ' Environment Settings (Backgrounds)
                vStyle.SetTrait(VisualStyleProperty.DisplayStyle, _
                                vStyle.GetTrait(VisualStyleProperty.DisplayStyle) + _
                                VSDisplayStyles.BackgroundsFlag, _
                                VisualStyleOperation.Set)
    
                ' Edge Settings (Show, Number of Lines, Color, and Always on Top)
                vStyle.SetTrait(VisualStyleProperty.EdgeModel, VSEdgeModel.Isolines, _
                                VisualStyleOperation.Set)
                vStyle.SetTrait(VisualStyleProperty.EdgeIsolines, _
                                6, VisualStyleOperation.Set)
                vStyle.SetTrait(VisualStyleProperty.EdgeColor, _
                                Color.FromColorIndex(ColorMethod.ByAci, 2), _
                                VisualStyleOperation.Set)
                vStyle.SetTrait(VisualStyleProperty.EdgeModifier, _
                                vStyle.GetTrait(VisualStyleProperty.EdgeModifier) + _
                                VSEdgeModifiers.AlwaysOnTopFlag, _
                                VisualStyleOperation.Set)
    
                ' Occluded Edges (Show, Color, and Linetype)
                If Not (vStyle.GetTrait(VisualStyleProperty.EdgeStyle) And _
                        VSEdgeStyles.ObscuredFlag) > 0 Then
                    vStyle.SetTrait(VisualStyleProperty.EdgeStyle, _
                                    vStyle.GetTrait(VisualStyleProperty.EdgeStyle) + _
                                    VSEdgeStyles.ObscuredFlag, _
                                    VisualStyleOperation.Set)
                End If
                vStyle.SetTrait(VisualStyleProperty.EdgeObscuredColor, _
                                Color.FromColorIndex(ColorMethod.ByAci, 3), _
                                VisualStyleOperation.Set)
                vStyle.SetTrait(VisualStyleProperty.EdgeObscuredLinePattern, _
                                VSEdgeLinePattern.DoubleMediumDash, _
                                VisualStyleOperation.Set)
    
                ' Intersection Edges (Color and Linetype)
                If Not (vStyle.GetTrait(VisualStyleProperty.EdgeStyle) And _
                        VSEdgeStyles.IntersectionFlag) > 0 Then
                    vStyle.SetTrait(VisualStyleProperty.EdgeStyle, _
                                    vStyle.GetTrait(VisualStyleProperty.EdgeStyle) + _
                                    VSEdgeStyles.IntersectionFlag, _
                                    VisualStyleOperation.Set)
                End If
                vStyle.SetTrait(VisualStyleProperty.EdgeIntersectionColor, _
                                Color.FromColorIndex(ColorMethod.ByAci, 4), _
                                VisualStyleOperation.Set)
                vStyle.SetTrait(VisualStyleProperty.EdgeIntersectionLinePattern, _
                                VSEdgeLinePattern.ShortDash, _
                                VisualStyleOperation.Set)
    
                ' Silhouette Edges (Color and Width)
                If Not (vStyle.GetTrait(VisualStyleProperty.EdgeStyle) And _
                        VSEdgeStyles.SilhouetteFlag) > 0 Then
                    vStyle.SetTrait(VisualStyleProperty.EdgeStyle, _
                                    vStyle.GetTrait(VisualStyleProperty.EdgeStyle) + _
                                    VSEdgeStyles.SilhouetteFlag, _
                                    VisualStyleOperation.Set)
                End If
                vStyle.SetTrait(VisualStyleProperty.EdgeSilhouetteColor, _
                                Color.FromColorIndex(ColorMethod.ByAci, 5), _
                                VisualStyleOperation.Set)
                vStyle.SetTrait(VisualStyleProperty.EdgeSilhouetteWidth, 2, _
                                VisualStyleOperation.Set)
    
                ' Edge Modifiers (Enable Line Extensions, Enable Jitter, 
                '                 Line Extensions, Jitter, Crease Angle, 
                '                 and Halo Gap)
                If Not (vStyle.GetTrait(VisualStyleProperty.EdgeModifier) And _
                        VSEdgeModifiers.EdgeOverhangFlag) > 0 Then
                    vStyle.SetTrait(VisualStyleProperty.EdgeModifier, _
                                    vStyle.GetTrait(VisualStyleProperty.EdgeModifier) + _
                                    VSEdgeModifiers.EdgeOverhangFlag, _
                                    VisualStyleOperation.Set)
                End If
                If Not (vStyle.GetTrait(VisualStyleProperty.EdgeModifier) And _
                        VSEdgeModifiers.EdgeJitterFlag) > 0 Then
                    vStyle.SetTrait(VisualStyleProperty.EdgeModifier, _
                                    vStyle.GetTrait(VisualStyleProperty.EdgeModifier) + _
                                    VSEdgeModifiers.EdgeJitterFlag, _
                                    VisualStyleOperation.Set)
                End If
                vStyle.SetTrait(VisualStyleProperty.EdgeOverhang, 3, _
                                VisualStyleOperation.Set)
                vStyle.SetTrait(VisualStyleProperty.EdgeJitterAmount, _
                                VSEdgeJitterAmount.JitterMedium, _
                                VisualStyleOperation.Set)
                vStyle.SetTrait(VisualStyleProperty.EdgeCreaseAngle, _
                                0.3, VisualStyleOperation.Set)
                vStyle.SetTrait(VisualStyleProperty.EdgeHaloGap, _
                                5, VisualStyleOperation.Set)
            Catch es As Autodesk.AutoCAD.Runtime.Exception
                MsgBox(es.Message)
            Finally
                acTrans.Commit()
            End Try
        End Using
    End Sub
