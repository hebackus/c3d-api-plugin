<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Viewports (.NET) > Use Shaded Viewports (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-32466B8D-60A0-4964-90D8-01C4B6A48FB8.htm -->

# Use Shaded Viewports (.NET)

If your drawing contains 3D faces, meshes, surfaces, or solids, you can control how the 3D objects appear when outputting a layout. A viewport can be set to use a visual style, render preset, one of the other values defined by the ShadePlotStype enum. Shaded and rendered viewports are previewed, plotted, and plotted to file with full shading and rendering. Use the SetShadePlot method and ShadePlot property of the Viewport object to query and set the option for plotting a shaded viewport. 

When outputting a layout, you can override the ShadePlot property of all the viewports on a Layout object by using the layout's ShadePlot property and control the shaded quality using the ShadePlotResLevel property. 

Note: The hidden lines for the objects in a Viewport object can be enabled with the HiddenLinesRemoved property. This property takes a boolean value: TRUE to remove hidden lines or FALSE to draw them. 

## Assign a visual style or render preset to a viewport

This example creates two new viewports (rectangular and nonrectangular, and assigns a visual style to one and a render preset to another. A help function is used to create a render preset that can then be assigned to the viewport. 

### C#
    
    
    // Standard .NET namespaces
    using System;
    using System.Runtime.InteropServices;
    
    // Main AutoCAD namespaces
    using Autodesk.AutoCAD;
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    using Autodesk.AutoCAD.PlottingServices;
    using Autodesk.AutoCAD.GraphicsInterface;
    using Autodesk.AutoCAD.EditorInput;
    
    // Used to create a rectangular and nonrectangular viewports - RapidRT example
    [CommandMethod("RRTCreatViewportsAndSetShadePlot")]
    public void RRTCreatViewportsAndSetShadePlot()
    {
        // Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Block table for read
            BlockTable acBlkTbl= acTrans.GetObject(acCurDb.BlockTableId,
                                                   OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Paper space for write
            BlockTableRecord acBlkTblRec =
                acTrans.GetObject(acBlkTbl[BlockTableRecord.PaperSpace],
                                  OpenMode.ForWrite) as BlockTableRecord;
    
            // Create a Viewport
            using (Autodesk.AutoCAD.DatabaseServices.Viewport acVport1 =
                       new Autodesk.AutoCAD.DatabaseServices.Viewport())
            {
                // Set the center point and size of the viewport
                acVport1.CenterPoint = new Point3d(3.75, 4, 0);
                acVport1.Width = 7.5;
                acVport1.Height = 7.5;
    
                // Lock the viewport
                acVport1.Locked = true;
    
                // Set the scale to 1" = 4'
                acVport1.CustomScale = 48;
    
                // Set visual style
                DBDictionary vStyles =
                    acTrans.GetObject(acCurDb.VisualStyleDictionaryId,
                                      OpenMode.ForRead) as DBDictionary;
    
                acVport1.SetShadePlot(ShadePlotType.VisualStyle,
                                      vStyles.GetAt("Sketchy"));
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acVport1);
                acTrans.AddNewlyCreatedDBObject(acVport1, true);
    
                // Change the view direction
                acVport1.ViewDirection = new Vector3d(-1, -1, 1);
    
                // Create a rectangular viewport to change to a non-rectangular viewport
                using (Autodesk.AutoCAD.DatabaseServices.Viewport acVport2 =
                           new Autodesk.AutoCAD.DatabaseServices.Viewport())
                {
                    acVport2.CenterPoint = new Point3d(9, 6.5, 0);
                    acVport2.Width = 2.5;
                    acVport2.Height = 2.5;
    
                    // Set the scale to 1" = 8'
                    acVport2.CustomScale = 96;
    
                    // Set render preset
                    DBDictionary namedObjs =
                        acTrans.GetObject(acCurDb.NamedObjectsDictionaryId,
                                          OpenMode.ForRead) as DBDictionary;
    
                    // Check to see if the Render Settings dictionary already exists
                    DBDictionary renderSettings;
                    if (namedObjs.Contains("ACAD_RENDER_RAPIDRT_SETTINGS") == true)
                    {
                        renderSettings = acTrans.GetObject(
                            namedObjs.GetAt("ACAD_RENDER_RAPIDRT_SETTINGS"),
                            OpenMode.ForWrite) as DBDictionary;
                    }
                    else
                    {
                        // If it does not exist, create it and add it to the drawing
                        acTrans.GetObject(acCurDb.NamedObjectsDictionaryId, OpenMode.ForWrite);
                        renderSettings = new DBDictionary();
                        namedObjs.SetAt("ACAD_RENDER_RAPIDRT_SETTINGS", renderSettings);
                        acTrans.AddNewlyCreatedDBObject(renderSettings, true);
                    }
    
                    // Create a new render preset and assign it to the new viewport
                    RapidRTRenderSettings renderSetting;
    
                    if (renderSettings.Contains("MyPreset") == false)
                    {
                        renderSetting = new RapidRTRenderSettings();
                        renderSetting.Name = "MyPreset";
                        renderSetting.Description = "Custom new render preset";
    
                        renderSettings.SetAt("MyPreset", renderSetting);
                        acTrans.AddNewlyCreatedDBObject(renderSetting, true);
                    }
                    else
                    {
                        renderSetting = (RapidRTRenderSettings)acTrans.GetObject(
                            renderSettings.GetAt("MyPreset"), OpenMode.ForRead);
                    }
    
                    acVport2.SetShadePlot(ShadePlotType.RenderPreset,
                                          renderSetting.ObjectId);
                    renderSetting.Dispose();
    
                    // Create a circle
                    using (Circle acCirc = new Circle())
                    {
                        acCirc.Center = acVport2.CenterPoint;
                        acCirc.Radius = 1.25;
    
                        // Add the new object to the block table record and the transaction
                        acBlkTblRec.AppendEntity(acCirc);
                        acTrans.AddNewlyCreatedDBObject(acCirc, true);
    
                        // Add the new object to the block table record and the transaction
                        acBlkTblRec.AppendEntity(acVport2);
                        acTrans.AddNewlyCreatedDBObject(acVport2, true);
    
                        // Clip the viewport using the circle  
                        acVport2.NonRectClipEntityId = acCirc.ObjectId;
                        acVport2.NonRectClipOn = true;
                    }
    
                    // Change the view direction
                    acVport2.ViewDirection = new Vector3d(0, 0, 1);
    
                    // Enable the viewports
                    acVport1.On = true;
                    acVport2.On = true;
                }
            }
    
            // Save the new objects to the database
            acTrans.Commit();
        }
    
        // Switch to the last named layout
        acDoc.Database.TileMode = false;
    }

### VB.NET
    
    
    ' Standard .NET namespaces
    Imports System.Runtime.InteropServices
    
    ' Main AutoCAD namespaces
    Imports Autodesk.AutoCAD
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    Imports Autodesk.AutoCAD.PlottingServices
    Imports Autodesk.AutoCAD.GraphicsInterface
    
    ' Used to create a rectangular and nonrectangular viewports - RapidRT example
    <CommandMethod("RRTCreatViewportsAndSetShadePlot")> _
    Public Sub RRTCreatViewportsAndSetShadePlot()
        ' Get the current document and database, and start a transaction
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            ' Open the Block table for read
            Dim acBlkTbl As BlockTable = acTrans.GetObject(acCurDb.BlockTableId,
                                                           OpenMode.ForRead)
    
            ' Open the Block table record Paper space for write
            Dim acBlkTblRec As BlockTableRecord =
                acTrans.GetObject(acBlkTbl(BlockTableRecord.PaperSpace),
                                  OpenMode.ForWrite)
    
            ' Create a Viewport
            Using acVport1 As Autodesk.AutoCAD.DatabaseServices.Viewport =
                           New Autodesk.AutoCAD.DatabaseServices.Viewport()
                ' Set the center point and size of the viewport
                acVport1.CenterPoint = New Point3d(3.75, 4, 0)
                acVport1.Width = 7.5
                acVport1.Height = 7.5
    
                ' Lock the viewport
                acVport1.Locked = True
    
                ' Set the scale to 1" = 4'
                acVport1.CustomScale = 48
    
                ' Set visual style
                Dim vStyles As DBDictionary =
                    acTrans.GetObject(acCurDb.VisualStyleDictionaryId,
                                      OpenMode.ForRead)
    
                acVport1.SetShadePlot(ShadePlotType.VisualStyle,
                                      vStyles.GetAt("Sketchy"))
    
                ' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acVport1)
                acTrans.AddNewlyCreatedDBObject(acVport1, True)
    
                ' Change the view direction
                acVport1.ViewDirection = New Vector3d(-1, -1, 1)
    
                ' Create a rectangular viewport to change to a non-rectangular viewport
                Using acVport2 As Autodesk.AutoCAD.DatabaseServices.Viewport =
                           New Autodesk.AutoCAD.DatabaseServices.Viewport()
    
                    acVport2.CenterPoint = New Point3d(9, 6.5, 0)
                    acVport2.Width = 2.5
                    acVport2.Height = 2.5
    
                    ' Set the scale to 1" = 8'
                    acVport2.CustomScale = 96
    
                    ' Set render preset
                    Dim namedObjs As DBDictionary =
                        acTrans.GetObject(acCurDb.NamedObjectsDictionaryId,
                                          OpenMode.ForRead)
    
                    ' Check to see if the Render Settings dictionary already exists
                    Dim renderSettings As DBDictionary
                    If (namedObjs.Contains("ACAD_RENDER_RAPIDRT_SETTINGS") = True) Then
                        renderSettings = acTrans.GetObject(
                            namedObjs.GetAt("ACAD_RENDER_RAPIDRT_SETTINGS"),
                            OpenMode.ForWrite)
                    Else
                        ' If it does not exist, create it and add it to the drawing
                        acTrans.GetObject(acCurDb.NamedObjectsDictionaryId, OpenMode.ForWrite)
                        renderSettings = New DBDictionary()
                        namedObjs.SetAt("ACAD_RENDER_RAPIDRT_SETTINGS", renderSettings)
                        acTrans.AddNewlyCreatedDBObject(renderSettings, True)
                    End If
    
                    ' Create a new render preset and assign it to the new viewport
                    Dim renderSetting As RapidRTRenderSettings
    
                    If (renderSettings.Contains("MyPreset") = False) Then
                        renderSetting = New RapidRTRenderSettings()
                        renderSetting.Name = "MyPreset"
                        renderSetting.Description = "Custom new render preset"
    
                        renderSettings.SetAt("MyPreset", renderSetting)
                        acTrans.AddNewlyCreatedDBObject(renderSetting, True)
                    Else
                        renderSetting = acTrans.GetObject(
                                renderSettings.GetAt("MyPreset"), OpenMode.ForRead)
                    End If
    
                    acVport2.SetShadePlot(ShadePlotType.RenderPreset,
                                          renderSetting.ObjectId)
                    renderSetting.Dispose()
    
                    ' Create a circle
                    Using acCirc As Circle = New Circle()
                        acCirc.Center = acVport2.CenterPoint
                        acCirc.Radius = 1.25
    
                        ' Add the new object to the block table record and the transaction
                        acBlkTblRec.AppendEntity(acCirc)
                        acTrans.AddNewlyCreatedDBObject(acCirc, True)
    
                        ' Add the new object to the block table record and the transaction
                        acBlkTblRec.AppendEntity(acVport2)
                        acTrans.AddNewlyCreatedDBObject(acVport2, True)
    
                        ' Clip the viewport using the circle  
                        acVport2.NonRectClipEntityId = acCirc.ObjectId
                        acVport2.NonRectClipOn = True
                    End Using
    
                    ' Change the view direction
                    acVport2.ViewDirection = New Vector3d(0, 0, 1)
    
                    ' Enable the viewports
                    acVport1.On = True
                    acVport2.On = True
                End Using
            End Using
    
            ' Save the new objects to the database
            acTrans.Commit()
        End Using
    
        ' Switch to the last named layout
        acDoc.Database.TileMode = False
    End Sub

## Assign a visual style or render preset to a viewport (AutoCAD 2015-based and earlier products)

This example creates two new viewports (rectangular and nonrectangular, and assigns a visual style to one and a render preset to another. A help function is used to create a render preset that can then be assigned to the viewport. 

Note: The following example code is maintained for backwards compatibility. Starting with AutoCAD 2016-based products, rendering settings are represented by the RapidRTRenderSettings class and not the MentalRayRenderSettings class used in earlier releases. 

### C#
    
    
    // Standard .NET namespaces
    using System;
    using System.Runtime.InteropServices;
    
    // Main AutoCAD namespaces
    using Autodesk.AutoCAD;
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    using Autodesk.AutoCAD.PlottingServices;
    using Autodesk.AutoCAD.GraphicsInterface;
    using Autodesk.AutoCAD.EditorInput;
    
    // Used to create a rectangular and nonrectangular viewports - MentalRay example
    [CommandMethod("MRCreatViewportsAndSetShadePlot")]
    public void MRCreatViewportsAndSetShadePlot()
    {
        // Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            // Open the Block table for read
            BlockTable acBlkTbl= acTrans.GetObject(acCurDb.BlockTableId,
                                                   OpenMode.ForRead) as BlockTable;
    
            // Open the Block table record Paper space for write
            BlockTableRecord acBlkTblRec =
                acTrans.GetObject(acBlkTbl[BlockTableRecord.PaperSpace],
                                  OpenMode.ForWrite) as BlockTableRecord;
    
            // Create a Viewport
            using (Autodesk.AutoCAD.DatabaseServices.Viewport acVport1 = 
                       new Autodesk.AutoCAD.DatabaseServices.Viewport())
            {
                // Set the center point and size of the viewport
                acVport1.CenterPoint = new Point3d(3.75, 4, 0);
                acVport1.Width = 7.5;
                acVport1.Height = 7.5;
    
                // Lock the viewport
                acVport1.Locked = true;
    
                // Set the scale to 1" = 4'
                acVport1.CustomScale = 48;
    
                // Set visual style
                DBDictionary vStyles =
                    acTrans.GetObject(acCurDb.VisualStyleDictionaryId,
                                      OpenMode.ForRead) as DBDictionary;
    
                acVport1.SetShadePlot(ShadePlotType.VisualStyle,
                                      vStyles.GetAt("Sketchy"));
    
                // Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acVport1);
                acTrans.AddNewlyCreatedDBObject(acVport1, true);
    
                // Change the view direction and enable the viewport
                acVport1.ViewDirection = new Vector3d(-1, -1, 1);
                acVport1.On = true;
    
                // Create a rectangular viewport to change to a non-rectangular viewport
                using (Autodesk.AutoCAD.DatabaseServices.Viewport acVport2 = 
                           new Autodesk.AutoCAD.DatabaseServices.Viewport())
                {
                    acVport2.CenterPoint = new Point3d(9, 6.5, 0);
                    acVport2.Width = 2.5;
                    acVport2.Height = 2.5;
    
                    // Set the scale to 1" = 8'
                    acVport2.CustomScale = 96;
    
                    // Set render preset
                    DBDictionary namedObjs =
                        acTrans.GetObject(acCurDb.NamedObjectsDictionaryId,
                                          OpenMode.ForRead) as DBDictionary;
    
                    // Check to see if the Render Settings dictionary already exists
                    DBDictionary renderSettings; 
                    if (namedObjs.Contains("ACAD_RENDER_PLOT_SETTINGS") == true)
                    {
                        renderSettings = acTrans.GetObject(
                            namedObjs.GetAt("ACAD_RENDER_PLOT_SETTINGS"),
                            OpenMode.ForWrite) as DBDictionary;
                    }
                    else
                    {
                        // If it does not exist, create it and add it to the drawing
                        acTrans.GetObject(acCurDb.NamedObjectsDictionaryId, OpenMode.ForWrite);
                        renderSettings = new DBDictionary();
                        namedObjs.SetAt("ACAD_RENDER_PLOT_SETTINGS", renderSettings);
                        acTrans.AddNewlyCreatedDBObject(renderSettings, true);
                    }
    
                    // Create the new render preset, based on the settings
                    // of the Medium render preset
                    MentalRayRenderSettings renderSetting = new MentalRayRenderSettings();
    
                    GetDefaultRenderPreset(ref renderSetting, "Medium");
    
                    renderSetting.Name = "Medium";
                    renderSettings.SetAt("Medium", renderSetting);
                    acTrans.AddNewlyCreatedDBObject(renderSetting, true);
    
                    acVport2.SetShadePlot(ShadePlotType.RenderPreset,
                                          renderSetting.ObjectId);
                    renderSetting.Dispose();
    
                    // Create a circle
                    using (Circle acCirc = new Circle())
                    {
                        acCirc.Center = acVport2.CenterPoint;
                        acCirc.Radius = 1.25;
    
                        // Add the new object to the block table record and the transaction
                        acBlkTblRec.AppendEntity(acCirc);
                        acTrans.AddNewlyCreatedDBObject(acCirc, true);
    
                        // Add the new object to the block table record and the transaction
                        acBlkTblRec.AppendEntity(acVport2);
                        acTrans.AddNewlyCreatedDBObject(acVport2, true);
    
                        // Clip the viewport using the circle  
                        acVport2.NonRectClipEntityId = acCirc.ObjectId;
                        acVport2.NonRectClipOn = true;
                    }
    
                    // Change the view direction
                    acVport2.ViewDirection = new Vector3d(0, 0, 1);
    
                    // Enable the viewport
                    acVport2.On = true;
                }
            }
    
            // Save the new objects to the database
            acTrans.Commit();
        }
    
        // Switch to the previous Paper space layout
        acCurDb.TileMode = false;
    }
    
    // Method used to populate a MentalRayRenderSettings object with the
    // same settings used by the standard render presets
    private static void GetDefaultRenderPreset(
                   ref MentalRayRenderSettings renderPreset,
                   string name)
    {
        // Set the values common to multiple default render presets
        renderPreset.BackFacesEnabled = false;
        renderPreset.DiagnosticBackgroundEnabled = false;
        renderPreset.DiagnosticBSPMode =
            DiagnosticBSPMode.Depth;
        renderPreset.DiagnosticGridMode =
            new MentalRayRenderSettingsTraitsDiagnosticGridModeParameter(
                DiagnosticGridMode.Object, (float)10.0);
    
        renderPreset.DiagnosticMode =
            DiagnosticMode.Off;
        renderPreset.DiagnosticPhotonMode =
            DiagnosticPhotonMode.Density;
        renderPreset.DisplayIndex = 0;
        renderPreset.EnergyMultiplier = (float)1.0;
        renderPreset.ExportMIEnabled = false;
        renderPreset.ExportMIFileName = "";
        renderPreset.FGRayCount = 100;
    
        // FGSampleRadius cannot be set, it returns invalid input
        renderPreset.FGSampleRadiusState =
            new MentalRayRenderSettingsTraitsBoolParameter(
                false, false, false);
    
        renderPreset.FinalGatheringEnabled = false;
        renderPreset.FinalGatheringMode =
            FinalGatheringMode.FinalGatherOff;
        renderPreset.GIPhotonsPerLight = 1000;
        renderPreset.GISampleCount = 500;
        renderPreset.GISampleRadius = 1.0;
        renderPreset.GISampleRadiusEnabled = false;
        renderPreset.GlobalIlluminationEnabled = false;
        renderPreset.LightLuminanceScale = 1500.0;
        renderPreset.MaterialsEnabled = true;
        renderPreset.MemoryLimit = 1048;
    
        renderPreset.PhotonTraceDepth =
            new MentalRayRenderSettingsTraitsTraceParameter(
                5, 5, 5);
        renderPreset.PreviewImageFileName = "";
        renderPreset.RayTraceDepth =
            new MentalRayRenderSettingsTraitsTraceParameter(
                3, 3, 3);
        renderPreset.RayTracingEnabled = false;
        renderPreset.Sampling =
            new MentalRayRenderSettingsTraitsIntegerRangeParameter(
                -2, -1);
        renderPreset.SamplingContrastColor =
            new MentalRayRenderSettingsTraitsFloatParameter(
                (float)0.1, (float)0.1, (float)0.1, (float)0.1);
        renderPreset.SamplingFilter =
            new MentalRayRenderSettingsTraitsSamplingParameter(
                Filter.Box, 1.0, 1.0);
    
        renderPreset.ShadowMapsEnabled = false;
        renderPreset.ShadowMode = ShadowMode.Simple;
        renderPreset.ShadowSamplingMultiplier =
            ShadowSamplingMultiplier.SamplingMultiplierZero;
        renderPreset.ShadowsEnabled = true;
        renderPreset.TextureSampling = false;
        renderPreset.TileOrder = TileOrder.Hilbert;
        renderPreset.TileSize = 32;
    
        switch (name.ToUpper()) {
            // Assigns the values to match the Draft render preset
    	case "DRAFT":
                renderPreset.Description =
                    "The lowest rendering quality which entails no raytracing, " +
                    "no texture filtering and force 2-sided is inactive.";
                renderPreset.Name = "Draft";
                break;
            case "LOW":
                renderPreset.Description =
                    "Rendering quality is improved over Draft. " +
                    "Low anti-aliasing and a raytracing depth of 3 " +
                    "reflection/refraction are processed.";
                renderPreset.Name = "Low";
    
                renderPreset.RayTracingEnabled = true;
    
                renderPreset.Sampling =
                    new MentalRayRenderSettingsTraitsIntegerRangeParameter(
                        -1, 0);
                renderPreset.SamplingContrastColor =
                    new MentalRayRenderSettingsTraitsFloatParameter(
                        (float)0.1, (float)0.1, (float)0.1, (float)0.1);
                renderPreset.SamplingFilter =
                    new MentalRayRenderSettingsTraitsSamplingParameter(
                        Filter.Triangle, 2.0, 2.0);
    
                renderPreset.ShadowSamplingMultiplier =
                    ShadowSamplingMultiplier.SamplingMultiplierOneFourth;
                break;
            case "MEDIUM":
                renderPreset.BackFacesEnabled = true;
                renderPreset.Description =
                    "Rendering quality is improved over Low to include " +
                    "texture filtering and force 2-sided is active. " +
                    "Moderate anti-aliasing and a raytracing depth of " +
                    "5 reflections/refractions are processed.";
    
                renderPreset.FGRayCount = 200;
                renderPreset.FinalGatheringMode =
                    FinalGatheringMode.FinalGatherAuto;
                renderPreset.GIPhotonsPerLight = 10000;
    
                renderPreset.Name = "Medium";
                renderPreset.RayTraceDepth =
                    new MentalRayRenderSettingsTraitsTraceParameter(
                        5, 5, 5);
                renderPreset.RayTracingEnabled = true;
                renderPreset.Sampling =
                    new MentalRayRenderSettingsTraitsIntegerRangeParameter(
                        0, 1);
                renderPreset.SamplingContrastColor =
                    new MentalRayRenderSettingsTraitsFloatParameter(
                        (float)0.05, (float)0.05, (float)0.05, (float)0.05);
                renderPreset.SamplingFilter =
                    new MentalRayRenderSettingsTraitsSamplingParameter(
                        Filter.Gauss, 3.0, 3.0);
    
                renderPreset.ShadowSamplingMultiplier =
                    ShadowSamplingMultiplier.SamplingMultiplierOneHalf;
                renderPreset.TextureSampling = true;
                break;
            case "HIGH":
                renderPreset.BackFacesEnabled = true;
                renderPreset.Description =
                    "Rendering quality is improved over Medium. " +
                    "High anti-aliasing and a raytracing depth of 7 " +
                    "reflections/refractions are processed.";
    
                renderPreset.FGRayCount = 500;
                renderPreset.FinalGatheringMode =
                    FinalGatheringMode.FinalGatherAuto;
                renderPreset.GIPhotonsPerLight = 10000;
    
                renderPreset.Name = "High";
                renderPreset.RayTraceDepth =
                    new MentalRayRenderSettingsTraitsTraceParameter(
                        7, 7, 7);
                renderPreset.RayTracingEnabled = true;
                renderPreset.Sampling =
                    new MentalRayRenderSettingsTraitsIntegerRangeParameter(
                        0, 2);
                renderPreset.SamplingContrastColor =
                    new MentalRayRenderSettingsTraitsFloatParameter(
                        (float)0.05, (float)0.05, (float)0.05, (float)0.05);
                renderPreset.SamplingFilter =
                    new MentalRayRenderSettingsTraitsSamplingParameter(
                        Filter.Mitchell, 4.0, 4.0);
    
                renderPreset.ShadowSamplingMultiplier =
                    ShadowSamplingMultiplier.SamplingMultiplierOne;
                renderPreset.TextureSampling = true;
                break;
            case "PRESENTATION":
                renderPreset.BackFacesEnabled = true;
                renderPreset.Description =
                    "Rendering quality is improved over High. " +
                    "Very high anti-aliasing and a raytracing depth of 9 " +
                    "reflections/refractions are processed.";
    
                renderPreset.FGRayCount = 1000;
                renderPreset.FinalGatheringMode =
                    FinalGatheringMode.FinalGatherAuto;
                renderPreset.GIPhotonsPerLight = 10000;
    
                renderPreset.Name = "Presentation";
                renderPreset.RayTraceDepth =
                    new MentalRayRenderSettingsTraitsTraceParameter(
                        9, 9, 9);
                renderPreset.RayTracingEnabled = true;
                renderPreset.Sampling =
                    new MentalRayRenderSettingsTraitsIntegerRangeParameter(
                        1, 2);
                renderPreset.SamplingContrastColor =
                    new MentalRayRenderSettingsTraitsFloatParameter(
                        (float)0.05, (float)0.05, (float)0.05, (float)0.05);
                renderPreset.SamplingFilter =
                    new MentalRayRenderSettingsTraitsSamplingParameter(
                        Filter.Lanczos, 4.0, 4.0);
    
                renderPreset.ShadowSamplingMultiplier =
                    ShadowSamplingMultiplier.SamplingMultiplierOne;
                renderPreset.TextureSampling = true;
                break;
        }
    }

### VB.NET
    
    
    ' Standard .NET namespaces
    Imports System.Runtime.InteropServices
    
    ' Main AutoCAD namespaces
    Imports Autodesk.AutoCAD
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    Imports Autodesk.AutoCAD.PlottingServices
    Imports Autodesk.AutoCAD.GraphicsInterface
    
    ' Used to create a rectangular and nonrectangular viewports - MentalRay example
    <CommandMethod("MRCreatViewportsAndSetShadePlot")> _
    Public Sub MRCreatViewportsAndSetShadePlot()
        ' Get the current document and database, and start a transaction
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            ' Open the Block table for read
            Dim acBlkTbl As BlockTable = acTrans.GetObject(acCurDb.BlockTableId,
                                                           OpenMode.ForRead)
    
            ' Open the Block table record Paper space for write
            Dim acBlkTblRec As BlockTableRecord =
                acTrans.GetObject(acBlkTbl(BlockTableRecord.PaperSpace),
                                  OpenMode.ForWrite)
    
            ' Create a Viewport
            Using acVport1 As Autodesk.AutoCAD.DatabaseServices.Viewport =
                       New Autodesk.AutoCAD.DatabaseServices.Viewport()
                ' Set the center point and size of the viewport
                acVport1.CenterPoint = New Point3d(3.75, 4, 0)
                acVport1.Width = 7.5
                acVport1.Height = 7.5
    
                ' Lock the viewport
                acVport1.Locked = True
    
                ' Set the scale to 1" = 4'
                acVport1.CustomScale = 48
    
                ' Set visual style
                Dim vStyles As DBDictionary =
                    acTrans.GetObject(acCurDb.VisualStyleDictionaryId,
                                      OpenMode.ForRead)
    
                acVport1.SetShadePlot(ShadePlotType.VisualStyle,
                                      vStyles.GetAt("Sketchy"))
    
                ' Add the new object to the block table record and the transaction
                acBlkTblRec.AppendEntity(acVport1)
                acTrans.AddNewlyCreatedDBObject(acVport1, True)
    
                ' Change the view direction and enable the viewport
                acVport1.ViewDirection = New Vector3d(-1, -1, 1)
                acVport1.On = True
    
                ' Create a rectangular viewport to change to a non-rectangular viewport
                Using acVport2 As Autodesk.AutoCAD.DatabaseServices.Viewport =
                           New Autodesk.AutoCAD.DatabaseServices.Viewport()
                    acVport2.CenterPoint = New Point3d(9, 6.5, 0)
                    acVport2.Width = 2.5
                    acVport2.Height = 2.5
    
                    ' Set the scale to 1" = 8'
                    acVport2.CustomScale = 96
    
                    ' Set render preset
                    Dim namedObjs As DBDictionary =
                        acTrans.GetObject(acCurDb.NamedObjectsDictionaryId,
                                          OpenMode.ForRead)
    
                    ' Check to see if the Render Settings dictionary already exists
                    Dim renderSettings As DBDictionary
                    If namedObjs.Contains("ACAD_RENDER_PLOT_SETTINGS") = True Then
                        renderSettings = acTrans.GetObject(
                            namedObjs.GetAt("ACAD_RENDER_PLOT_SETTINGS"),
                            OpenMode.ForWrite)
                    Else
                        ' If it does not exist, create it and add it to the drawing
                        acTrans.GetObject(acCurDb.NamedObjectsDictionaryId, OpenMode.ForWrite)
                        renderSettings = New DBDictionary()
                        namedObjs.SetAt("ACAD_RENDER_PLOT_SETTINGS", renderSettings)
                        acTrans.AddNewlyCreatedDBObject(renderSettings, True)
                    End If
    
                    ' Create the new render preset, based on the settings
                    ' of the Medium render preset
                    Dim renderSetting As MentalRayRenderSettings = New MentalRayRenderSettings
    
                    GetDefaultRenderPreset(renderSetting, "Medium")
    
                    renderSetting.Name = "Medium"
                    renderSettings.SetAt("Medium", renderSetting)
                    acTrans.AddNewlyCreatedDBObject(renderSetting, True)
    
                    acVport2.SetShadePlot(ShadePlotType.RenderPreset,
                                          renderSetting.ObjectId)
                    renderSetting.Dispose()
    
                    ' Create a circle
                    Using acCirc As Circle = New Circle()
                        acCirc.Center = acVport2.CenterPoint
                        acCirc.Radius = 1.25
    
                        ' Add the new object to the block table record and the transaction
                        acBlkTblRec.AppendEntity(acCirc)
                        acTrans.AddNewlyCreatedDBObject(acCirc, True)
    
                        ' Add the new object to the block table record and the transaction
                        acBlkTblRec.AppendEntity(acVport2)
                        acTrans.AddNewlyCreatedDBObject(acVport2, True)
    
                        ' Clip the viewport using the circle  
                        acVport2.NonRectClipEntityId = acCirc.ObjectId
                        acVport2.NonRectClipOn = True
                    End Using
    
                    ' Change the view direction
                    acVport2.ViewDirection = New Vector3d(0, 0, 1)
    
                    ' Enable the viewport
                    acVport2.On = True
                End Using
            End Using
    
            ' Save the new objects to the database
            acTrans.Commit()
        End Using
    
        ' Switch to the previous Paper space layout
        acCurDb.TileMode = False
    End Sub
    
    ' Method used to populate a MentalRayRenderSettings object with the
    ' same settings used by the standard render presets
    Private Shared Sub GetDefaultRenderPreset( _
                       ByRef renderPreset As MentalRayRenderSettings, _
                       ByVal name As String)
        ' Set the values common to multiple default render presets
        renderPreset.BackFacesEnabled = False
        renderPreset.DiagnosticBackgroundEnabled = False
        renderPreset.DiagnosticBSPMode = _
            DiagnosticBSPMode.Depth
        renderPreset.DiagnosticGridMode = _
            New MentalRayRenderSettingsTraitsDiagnosticGridModeParameter( _
                DiagnosticGridMode.Object, 10.0)
    
        renderPreset.DiagnosticMode = _
            DiagnosticMode.Off
        renderPreset.DiagnosticPhotonMode = _
            DiagnosticPhotonMode.Density
        renderPreset.DisplayIndex = 0
        renderPreset.EnergyMultiplier = 1.0
        renderPreset.ExportMIEnabled = False
        renderPreset.ExportMIFileName = ""
        renderPreset.FGRayCount = 100
    
        ' FGSampleRadius cannot be set, it returns invalid input
        renderPreset.FGSampleRadiusState = _
            New MentalRayRenderSettingsTraitsBoolParameter( _
                False, False, False)
    
        renderPreset.FinalGatheringEnabled = False
        renderPreset.FinalGatheringMode = _
            FinalGatheringMode.FinalGatherOff
        renderPreset.GIPhotonsPerLight = 1000
        renderPreset.GISampleCount = 500
        renderPreset.GISampleRadius = 1.0
        renderPreset.GISampleRadiusEnabled = False
        renderPreset.GlobalIlluminationEnabled = False
        renderPreset.LightLuminanceScale = 1500.0
        renderPreset.MaterialsEnabled = True
        renderPreset.MemoryLimit = 1048
    
        renderPreset.PhotonTraceDepth = _
            New MentalRayRenderSettingsTraitsTraceParameter( _
                5, 5, 5)
        renderPreset.PreviewImageFileName = ""
        renderPreset.RayTraceDepth = _
            New MentalRayRenderSettingsTraitsTraceParameter( _
                3, 3, 3)
        renderPreset.RayTracingEnabled = False
        renderPreset.Sampling = _
            New MentalRayRenderSettingsTraitsIntegerRangeParameter( _
                -2, -1)
        renderPreset.SamplingContrastColor = _
            New MentalRayRenderSettingsTraitsFloatParameter( _
                0.1, 0.1, 0.1, 0.1)
        renderPreset.SamplingFilter = _
            New MentalRayRenderSettingsTraitsSamplingParameter( _
                Filter.Box, 1.0, 1.0)
    
        renderPreset.ShadowMapsEnabled = False
        renderPreset.ShadowMode = ShadowMode.Simple
        renderPreset.ShadowSamplingMultiplier = _
            ShadowSamplingMultiplier.SamplingMultiplierZero
        renderPreset.ShadowsEnabled = True
        renderPreset.TextureSampling = False
        renderPreset.TileOrder = TileOrder.Hilbert
        renderPreset.TileSize = 32
    
        Select Case name.ToUpper()
            ' Assigns the values to match the Draft render preset
            Case "DRAFT"
                renderPreset.Description = _
                    "The lowest rendering quality which entails no raytracing, " & _
                    "no texture filtering and force 2-sided is inactive."
                renderPreset.Name = "Draft"
            Case ("LOW")
                renderPreset.Description = _
                    "Rendering quality is improved over Draft. " & _
                    "Low anti-aliasing and a raytracing depth of 3 " & _
                    "reflection/refraction are processed."
                renderPreset.Name = "Low"
    
                renderPreset.RayTracingEnabled = True
    
                renderPreset.Sampling = _
                    New MentalRayRenderSettingsTraitsIntegerRangeParameter( _
                        -1, 0)
                renderPreset.SamplingContrastColor = _
                    New MentalRayRenderSettingsTraitsFloatParameter( _
                        0.1, 0.1, 0.1, 0.1)
                renderPreset.SamplingFilter = _
                    New MentalRayRenderSettingsTraitsSamplingParameter( _
                        Filter.Triangle, 2.0, 2.0)
    
                renderPreset.ShadowSamplingMultiplier = _
                    ShadowSamplingMultiplier.SamplingMultiplierOneFourth
            Case "MEDIUM"
                renderPreset.BackFacesEnabled = True
                renderPreset.Description = _
                    "Rendering quality is improved over Low to include " & _
                    "texture filtering and force 2-sided is active. " & _
                    "Moderate anti-aliasing and a raytracing depth of " & _
                    "5 reflections/refractions are processed."
    
                renderPreset.FGRayCount = 200
                renderPreset.FinalGatheringMode = _
                    FinalGatheringMode.FinalGatherAuto
                renderPreset.GIPhotonsPerLight = 10000
    
                renderPreset.Name = "Medium"
                renderPreset.RayTraceDepth = _
                    New MentalRayRenderSettingsTraitsTraceParameter( _
                        5, 5, 5)
                renderPreset.RayTracingEnabled = True
                renderPreset.Sampling = _
                    New MentalRayRenderSettingsTraitsIntegerRangeParameter( _
                        0, 1)
                renderPreset.SamplingContrastColor = _
                    New MentalRayRenderSettingsTraitsFloatParameter( _
                        0.05, 0.05, 0.05, 0.05)
                renderPreset.SamplingFilter = _
                    New MentalRayRenderSettingsTraitsSamplingParameter( _
                        Filter.Gauss, 3.0, 3.0)
    
                renderPreset.ShadowSamplingMultiplier = _
                    ShadowSamplingMultiplier.SamplingMultiplierOneHalf
                renderPreset.TextureSampling = True
            Case "HIGH"
                renderPreset.BackFacesEnabled = True
                renderPreset.Description = _
                    "Rendering quality is improved over Medium. " & _
                    "High anti-aliasing and a raytracing depth of 7 " & _
                    "reflections/refractions are processed."
    
                renderPreset.FGRayCount = 500
                renderPreset.FinalGatheringMode = _
                    FinalGatheringMode.FinalGatherAuto
                renderPreset.GIPhotonsPerLight = 10000
    
                renderPreset.Name = "High"
                renderPreset.RayTraceDepth = _
                    New MentalRayRenderSettingsTraitsTraceParameter( _
                        7, 7, 7)
                renderPreset.RayTracingEnabled = True
                renderPreset.Sampling = _
                    New MentalRayRenderSettingsTraitsIntegerRangeParameter( _
                        0, 2)
                renderPreset.SamplingContrastColor = _
                    New MentalRayRenderSettingsTraitsFloatParameter( _
                        0.05, 0.05, 0.05, 0.05)
                renderPreset.SamplingFilter = _
                    New MentalRayRenderSettingsTraitsSamplingParameter( _
                        Filter.Mitchell, 4.0, 4.0)
    
                renderPreset.ShadowSamplingMultiplier = _
                    ShadowSamplingMultiplier.SamplingMultiplierOne
                renderPreset.TextureSampling = True
            Case "PRESENTATION"
                renderPreset.BackFacesEnabled = True
                renderPreset.Description = _
                    "Rendering quality is improved over High. " & _
                    "Very high anti-aliasing and a raytracing depth of 9 " & _
                    "reflections/refractions are processed."
    
                renderPreset.FGRayCount = 1000
                renderPreset.FinalGatheringMode = _
                    FinalGatheringMode.FinalGatherAuto
                renderPreset.GIPhotonsPerLight = 10000
    
                renderPreset.Name = "Presentation"
                renderPreset.RayTraceDepth = _
                    New MentalRayRenderSettingsTraitsTraceParameter( _
                        9, 9, 9)
                renderPreset.RayTracingEnabled = True
                renderPreset.Sampling = _
                    New MentalRayRenderSettingsTraitsIntegerRangeParameter( _
                        1, 2)
                renderPreset.SamplingContrastColor = _
                    New MentalRayRenderSettingsTraitsFloatParameter( _
                        0.05, 0.05, 0.05, 0.05)
                renderPreset.SamplingFilter = _
                    New MentalRayRenderSettingsTraitsSamplingParameter( _
                        Filter.Lanczos, 4.0, 4.0)
    
                renderPreset.ShadowSamplingMultiplier = _
                    ShadowSamplingMultiplier.SamplingMultiplierOne
                renderPreset.TextureSampling = True
        End Select
    End Sub
