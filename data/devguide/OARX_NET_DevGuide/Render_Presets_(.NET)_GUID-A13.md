<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Render Presets (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-A1309D38-A432-487C-B890-6666B891C701.htm -->

# Render Presets (.NET)

Render presets allow you to define the settings that should be used when rendering 3D objects on screen or during the output of a layout. 

## Set a render preset current

This example sets a render preset current 

### C#
    
    
    // Sets the Draft render preset current - RapidRT example
    [CommandMethod("RRTRenderPresetsSetCurrent")]
    public void RRTRenderPresetsSetCurrent()
    {
        foreach (System.ComponentModel.ICustomTypeDescriptor itemDesc in Application.UIBindings.Collections.RenderPresets)
        {
            String presetName = itemDesc.GetProperties().Find("Name", false).GetValue(itemDesc) as String;
    
            if (presetName.ToUpper() == "LOW")
            {
                Application.UIBindings.Collections.RenderPresets.CurrentItem = itemDesc;
            }
        }
    }

### VB.NET
    
    
    ' Sets the Draft render preset current - RapidRT example
    <CommandMethod("RRTRenderPresetsSetCurrent")> _
    Public Shared Sub RRTRenderPresetsSetCurrent()
        Dim itemDesc As ComponentModel.ICustomTypeDescriptor = Nothing
        For Each itemDesc In Application.UIBindings.Collections.RenderPresets
            Dim presetName As String = itemDesc.GetProperties.Find("Name", False).GetValue(itemDesc)
    
            If presetName.ToUpper() = "DRAFT" Then
                Application.UIBindings.Collections.RenderPresets.CurrentItem = itemDesc
    
                Exit For
            End If
        Next
    End Sub

## Set a render preset current (AutoCAD 2015-based and earlier products)

This example sets a render preset current 

### C#
    
    
    // Sets the Draft render preset current - MentalRay example
    [CommandMethod("MRRenderPresetsSetCurrent")]
    public void MRRenderPresetsSetCurrent()
    {
        Application.UIBindings.RenderEngineMR.CurrentRenderPresetName = "Draft";
    }

### VB.NET
    
    
    ' Sets the Draft render preset current - MentalRay example
    <CommandMethod("MRRenderPresetsSetCurrent")> _
    Public Shared Sub MRRenderPresetsSetCurrent()
        Application.UIBindings.RenderEngineMR.CurrentRenderPresetName = "Draft"
    End Sub

## List the available render presets

There are two types of render presets: standard and custom. The standard render presets (Low, Medium, High, Coffee-Break Quality, Lunch Quality, and Overnight Quality) cannot be modified as they are defined with the application. All render presets are stored in the “ACAD_RENDER_RAPIDRT_SETTINGS” named dictionary as RapidRTRenderSettings objects. 

A second named dictionary, “ACAD_RENDER_PLOT_SETTINGS”, is used to store a copy of a render preset so it can be assigned to a Viewport or PlotSettings object. 

This example lists the render presets that are stored in the current drawing. 

### C#
    
    
    // Standard .NET namespaces
    using System;
    using System.Runtime.InteropServices;
    
    // Main AutoCAD namespaces
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    using Autodesk.AutoCAD.PlottingServices;
    using Autodesk.AutoCAD.Windows;
    using Autodesk.AutoCAD.GraphicsInterface;
    
    // Lists the available render presets - RapidRT example
    [CommandMethod("RRTRenderPresetsList")]
    public void RRTRenderPresetsList()
    {
        // Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            DBDictionary namedObjs = acTrans.GetObject(acCurDb.NamedObjectsDictionaryId,
                                                       OpenMode.ForRead) as DBDictionary;
    
            try
            {
                // Step through and list each of the render presets
                RapidRTRenderSettings renderSetting = null;
    
                if (namedObjs.Contains("ACAD_RENDER_RAPIDRT_SETTINGS") == true)
                {
                    DBDictionary renderSettings = acTrans.GetObject(namedObjs.GetAt("ACAD_RENDER_RAPIDRT_SETTINGS"),
                                                                    OpenMode.ForRead) as DBDictionary;
    
                    acDoc.Editor.WriteMessage("\nRender presets: ");
    
                    foreach (DBDictionaryEntry entry in renderSettings)
                    {
                        renderSetting = acTrans.GetObject(entry.Value, OpenMode.ForRead) as RapidRTRenderSettings;
                        // Output the names of the available render preset
                        acDoc.Editor.WriteMessage("\n  " + renderSetting.Name);
                    }
                }
                else
                {
                    acDoc.Editor.WriteMessage("\nNo render presets available.");
                }
            }
            catch (Autodesk.AutoCAD.Runtime.Exception Ex)
            {
                Application.ShowAlertDialog("The following exception was caught:\n" +
                                            Ex.Message);
            }
            finally
            {
                // Discard any changes
                acTrans.Abort();
            }
        }
    }

### VB.NET
    
    
    ' Standard .NET namespaces
    Imports System
    Imports System.Runtime.InteropServices
    
    ' Main AutoCAD namespaces
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    Imports Autodesk.AutoCAD.PlottingServices
    Imports Autodesk.AutoCAD.Windows
    Imports Autodesk.AutoCAD.GraphicsInterface
    
    ' Lists the available render presets - RapidRT example
    <CommandMethod("RRTRenderPresetsList")> _
    Public Shared Sub RRTRenderPresetsList()
        ' Get the current document and database, and start a transaction
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            Dim namedObjs As DBDictionary = acTrans.GetObject(acCurDb.NamedObjectsDictionaryId, OpenMode.ForRead)
    
            Try
                ' Step through and list each of the render presets
                Dim renderSetting As RapidRTRenderSettings = Nothing
    
                If namedObjs.Contains("ACAD_RENDER_RAPIDRT_SETTINGS") = True Then
                    Dim renderSettings As DBDictionary = acTrans.GetObject(namedObjs.GetAt("ACAD_RENDER_RAPIDRT_SETTINGS"), OpenMode.ForRead)
    
                    acDoc.Editor.WriteMessage(vbLf & "Render presets: ")
    
                    For Each entry As DBDictionaryEntry In renderSettings
                        renderSetting = acTrans.GetObject(entry.Value, OpenMode.ForRead)
                        ' Output the names of the available render preset
                        acDoc.Editor.WriteMessage(vbLf & "  " & renderSetting.Name)
                    Next
                Else
                    acDoc.Editor.WriteMessage(vbLf & "No render presets available.")
                End If
            Catch es As Autodesk.AutoCAD.Runtime.Exception
    
            End Try
    
            ' Discard any changes
            acTrans.Abort()
        End Using
    End Sub

## List the available render presets (AutoCAD 2015-based and earlier products)

This example lists the render presets that are stored in the current drawing. 

The standard render presets (Draft, Low, Medium, High, and Presentation) cannot be modified as they are defined with the application. Custom render presets are stored in the “ACAD_RENDER_SETTINGS” named dictionary as MentalRayRenderSettings objects. 

Note: The following example code is maintained for backwards compatibility. Starting with AutoCAD 2016-based products, rendering settings are represented by the RapidRTRenderSettings class and not the MentalRayRenderSettings like in earlier releases. 

### C#
    
    
    // Standard .NET namespaces
    using System;
    using System.Runtime.InteropServices;
    
    // Main AutoCAD namespaces
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    using Autodesk.AutoCAD.PlottingServices;
    using Autodesk.AutoCAD.Windows;
    using Autodesk.AutoCAD.GraphicsInterface;
    
    // Lists the available render presets - MentalRay example
    [CommandMethod("MRRenderPresetsList")]
    public void MRRenderPresetsList()
    {
        // Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            DBDictionary namedObjs = acTrans.GetObject(acCurDb.NamedObjectsDictionaryId,
                                                       OpenMode.ForRead) as DBDictionary;
    
            try
            {
                acDoc.Editor.WriteMessage("\nDefault render presets: ");
    
                // List the default render presets
                acDoc.Editor.WriteMessage("\n  Draft");
                acDoc.Editor.WriteMessage("\n  Low");
                acDoc.Editor.WriteMessage("\n  Medium");
                acDoc.Editor.WriteMessage("\n  High");
                acDoc.Editor.WriteMessage("\n  Presentation");
    
                // Step through and list each of the custom render presets
                MentalRayRenderSettings renderSetting = null;
    
                if (namedObjs.Contains("ACAD_RENDER_SETTINGS") == true)
                {
                    DBDictionary renderSettings = acTrans.GetObject(namedObjs.GetAt("ACAD_RENDER_SETTINGS"),
                                                                    OpenMode.ForRead) as DBDictionary;
    
                    acDoc.Editor.WriteMessage("\nCustom render presets: ");
    
                    // Set the new render preset MyPreset current
                    foreach (DBDictionaryEntry entry in renderSettings)
                    {
                        renderSetting = acTrans.GetObject(entry.Value, OpenMode.ForRead) as MentalRayRenderSettings;
                        // Output the names of the available render preset
                        acDoc.Editor.WriteMessage("\n  " + renderSetting.Name);
                    }
                }
                else
                {
                    acDoc.Editor.WriteMessage("\nNo custom render presets available.");
                }
            }
            catch (Autodesk.AutoCAD.Runtime.Exception Ex)
            {
                Application.ShowAlertDialog("The following exception was caught:\n" +
                                            Ex.Message);
            }
            finally
            {
                // Discard any changes
                acTrans.Abort();
            }
        }
    }

### VB.NET
    
    
    ' Standard .NET namespaces
    Imports System
    Imports System.Runtime.InteropServices
    
    ' Main AutoCAD namespaces
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    Imports Autodesk.AutoCAD.PlottingServices
    Imports Autodesk.AutoCAD.Windows
    Imports Autodesk.AutoCAD.GraphicsInterface
    
    ' Lists the available render presets - MentalRay example
    <CommandMethod("MRRenderPresetsList")> _
    Public Shared Sub MRRenderPresetsList()
        ' Get the current document and database, and start a transaction
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            Dim namedObjs As DBDictionary = acTrans.GetObject(acCurDb.NamedObjectsDictionaryId, OpenMode.ForRead)
    
            Try
                acDoc.Editor.WriteMessage(vbLf & "Default render presets: ")
    
                ' List the default render presets
                acDoc.Editor.WriteMessage(vbLf & "  Draft")
                acDoc.Editor.WriteMessage(vbLf & "  Low")
                acDoc.Editor.WriteMessage(vbLf & "  Medium")
                acDoc.Editor.WriteMessage(vbLf & "  High")
                acDoc.Editor.WriteMessage(vbLf & "  Presentation")
    
                ' Step through and list each of the custom render presets
                Dim renderSetting As MentalRayRenderSettings = Nothing
    
                If namedObjs.Contains("ACAD_RENDER_SETTINGS") = True Then
                    Dim renderSettings As DBDictionary = acTrans.GetObject(namedObjs.GetAt("ACAD_RENDER_SETTINGS"), OpenMode.ForRead)
    
                    acDoc.Editor.WriteMessage(vbLf & "Custom render presets: ")
    
                    For Each entry As DBDictionaryEntry In renderSettings
                        renderSetting = acTrans.GetObject(entry.Value, OpenMode.ForRead)
                        ' Output the names of the available render preset
                        acDoc.Editor.WriteMessage(vbLf & "  " & renderSetting.Name)
                    Next
                Else
                    acDoc.Editor.WriteMessage(vbLf & "No custom render presets available.")
                End If
            Catch es As Autodesk.AutoCAD.Runtime.Exception
    
            End Try
    
            ' Discard any changes
            acTrans.Abort()
        End Using
    End Sub

## Create or edit a render preset

This example creates or edits a render preset named MyPreset. 

### C#
    
    
    // Standard .NET namespaces
    using System;
    using System.Runtime.InteropServices;
    
    // Main AutoCAD namespaces
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    using Autodesk.AutoCAD.PlottingServices;
    using Autodesk.AutoCAD.Windows;
    using Autodesk.AutoCAD.GraphicsInterface;
    
    // Creates a new render preset - RapidRT example
    [CommandMethod("RRTRenderPresetsCreate")]
    public void RRTRenderPresetsCreate()
    {
        // Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            DBDictionary namedObjs = acTrans.GetObject(acCurDb.NamedObjectsDictionaryId, 
                                                       OpenMode.ForRead) as DBDictionary;
    
            try
            {
                // Check to see if the Render Settings dictionary already exists or not
                DBDictionary renderSettings;
                if (namedObjs.Contains("ACAD_RENDER_RAPIDRT_SETTINGS") == true)
                {
                    renderSettings = acTrans.GetObject(namedObjs.GetAt("ACAD_RENDER_RAPIDRT_SETTINGS"),
                                                       OpenMode.ForWrite) as DBDictionary;
                }
                else
                {
                    acTrans.GetObject(acCurDb.NamedObjectsDictionaryId, OpenMode.ForWrite);
                    renderSettings = new DBDictionary();
                    namedObjs.SetAt("ACAD_RENDER_RAPIDRT_SETTINGS", renderSettings);
                    acTrans.AddNewlyCreatedDBObject(renderSettings, true);
                }
    
                // Create the new render preset, based on the settings of the Medium render preset
                if (renderSettings.Contains("MyPreset") == false)
                {
                    RapidRTRenderSettings renderSetting = new RapidRTRenderSettings();
                    renderSetting.Name = "MyPreset";
                    renderSetting.Description = "Custom new render preset";
    
                    // Set renderer settings
                    renderSetting.BackFacesEnabled = false;
                    renderSetting.MaterialsEnabled = false;
                    renderSetting.ShadowsEnabled = false;
                    renderSetting.TextureSampling = false;
    
                    // Set Rendering duration
                    renderSetting.RenderTarget = RapidRTRenderTarget.Level;
                    renderSetting.RenderLevel = 10;
    
                    // Set rendering accuracy
                    renderSetting.LightingModel = RapidRTLightingMode.Simplified;
    
                    // Material rendering settings
                    renderSetting.FilterHeight = 5;
                    renderSetting.FilterWidth = 5;
                    renderSetting.FilterType = RapidRTFilterType.Mitchell;
    
                    renderSetting.DisplayIndex = 20;
    
                    renderSettings.SetAt("MyPreset", renderSetting);
                    acTrans.AddNewlyCreatedDBObject(renderSetting, true);
                }
            }
            catch (Autodesk.AutoCAD.Runtime.Exception Ex)
            {
                Application.ShowAlertDialog("The following exception was caught:\n" +
                                            Ex.Message);
            }
            finally
            {
                // Discard any changes
                 acTrans.Commit();
            }
        }
    
        // Set the new render preset MyPreset current
        acDoc.Editor.Command("_-RENDERPRESETS", "_custom", "mypreset");
    }

### VB.NET
    
    
    ' Standard .NET namespaces
    Imports System
    Imports System.Runtime.InteropServices
    
    ' Main AutoCAD namespaces
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    Imports Autodesk.AutoCAD.PlottingServices
    Imports Autodesk.AutoCAD.Windows
    Imports Autodesk.AutoCAD.GraphicsInterface
    
    ' Creates a new render preset - RapidRT example
    <CommandMethod("RRTRenderPresetsCreate")> _
    Public Shared Sub RRTRenderPresetCreate()
        ' Get the current document and database, and start a transaction
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            Dim namedObjs As DBDictionary = acTrans.GetObject(acCurDb.NamedObjectsDictionaryId, OpenMode.ForRead)
    
            Try
                ' Check to see if the Render Settings dictionary already exists or not
                Dim renderSettings As DBDictionary
                If namedObjs.Contains("ACAD_RENDER_RAPIDRT_SETTINGS") = True Then
                    renderSettings = acTrans.GetObject(namedObjs.GetAt("ACAD_RENDER_RAPIDRT_SETTINGS"), OpenMode.ForWrite)
                Else
                    acTrans.GetObject(acCurDb.NamedObjectsDictionaryId, OpenMode.ForWrite)
                    renderSettings = New DBDictionary
                    namedObjs.SetAt("ACAD_RENDER_RAPIDRT_SETTINGS", renderSettings)
                    acTrans.AddNewlyCreatedDBObject(renderSettings, True)
                End If
    
                ' Create the new render preset, based on the settings of the Medium render preset
                If renderSettings.Contains("MyPreset") = False Then
                    Dim renderSetting As New RapidRTRenderSettings
                    renderSetting.Name = "MyPreset"
                    renderSetting.Description = "Custom new render preset"
    
                    ' Set renderer settings
                    renderSetting.BackFacesEnabled = False
                    renderSetting.MaterialsEnabled = False
                    renderSetting.ShadowsEnabled = False
                    renderSetting.TextureSampling = False
    
                    ' Set Rendering duration
                    renderSetting.RenderTarget = RapidRTRenderTarget.Level
                    renderSetting.RenderLevel = 10
    
                    ' Set rendering accuracy
                    renderSetting.LightingModel = RapidRTLightingMode.Simplified
    
                    ' Material rendering settings
                    renderSetting.FilterHeight = 5
                    renderSetting.FilterWidth = 5
                    renderSetting.FilterType = RapidRTFilterType.Mitchell
    
                    renderSetting.DisplayIndex = 20
    
                    renderSettings.SetAt("MyPreset", renderSetting)
                    acTrans.AddNewlyCreatedDBObject(renderSetting, True)
                End If
            Catch es As Autodesk.AutoCAD.Runtime.Exception
                MsgBox(es.Message)
            Finally
                acTrans.Commit()
            End Try
        End Using
    
        acDoc.Editor.Command("_-RENDERPRESETS", "_custom", "mypreset")
    End Sub

## Create or edit a render preset (AutoCAD 2015-based and earlier products)

This example creates or edits a render preset named MyPreset. A helper function named GetDefaultRenderPreset is defined and used to get the recreate the settings of one of the standard render presets. 

### C#
    
    
    // Standard .NET namespaces
    using System;
    using System.Runtime.InteropServices;
    
    // Main AutoCAD namespaces
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.Geometry;
    using Autodesk.AutoCAD.PlottingServices;
    using Autodesk.AutoCAD.Windows;
    using Autodesk.AutoCAD.GraphicsInterface;
    
    // Creates a new render preset - MentalRay example
    [CommandMethod("MRRenderPresetsCreate")]
    public void MRRenderPresetsCreate()
    {
        // Get the current document and database, and start a transaction
        Document acDoc = Application.DocumentManager.MdiActiveDocument;
        Database acCurDb = acDoc.Database;
    
        using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
        {
            DBDictionary namedObjs = acTrans.GetObject(acCurDb.NamedObjectsDictionaryId,
                                                       OpenMode.ForRead) as DBDictionary;
    
            try
            {
                // Check to see if the Render Settings dictionary already exists or not
                DBDictionary renderSettings;
                if (namedObjs.Contains("ACAD_RENDER_SETTINGS") == true)
                {
                    renderSettings = acTrans.GetObject(namedObjs.GetAt("ACAD_RENDER_SETTINGS"),
                                                       OpenMode.ForWrite) as DBDictionary;
                }
                else
                {
                    acTrans.GetObject(acCurDb.NamedObjectsDictionaryId, OpenMode.ForWrite);
                    renderSettings = new DBDictionary();
                    namedObjs.SetAt("ACAD_RENDER_SETTINGS", renderSettings);
                    acTrans.AddNewlyCreatedDBObject(renderSettings, true);
                }
    
                // Create the new render preset, based on the settings of the Medium render preset
                if (renderSettings.Contains("MyPreset") == false)
                {
                    MentalRayRenderSettings renderSetting = new MentalRayRenderSettings();
    
                    GetDefaultRenderPreset(ref renderSetting, "MyPreset");
                    renderSetting.Description = "Custom new render preset";
                    renderSettings.SetAt("MyPreset", renderSetting);
                    acTrans.AddNewlyCreatedDBObject(renderSetting, true);
                }
    
                // Set the new render preset as current with the Render Engine
                Application.UIBindings.RenderEngineMR.CurrentRenderPresetName = "MyPreset";
            }
            catch (Autodesk.AutoCAD.Runtime.Exception Ex)
            {
                Application.ShowAlertDialog("The following exception was caught:\n" +
                                            Ex.Message);
            }
            finally
            {
                // Commit any changes
                acTrans.Commit();
            }
        }
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
    
        switch (name.ToUpper())
        {
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
    Imports System
    Imports System.Runtime.InteropServices
    
    ' Main AutoCAD namespaces
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.Geometry
    Imports Autodesk.AutoCAD.PlottingServices
    Imports Autodesk.AutoCAD.Windows
    Imports Autodesk.AutoCAD.GraphicsInterface
    
    ' Creates a new render preset - MentalRay example
    <CommandMethod("MRRenderPresetsCreate")> _
    Public Shared Sub MRRenderPresetCreate()
        ' Get the current document and database, and start a transaction
        Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
        Dim acCurDb As Database = acDoc.Database
    
        Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()
            Dim namedObjs As DBDictionary = acTrans.GetObject(acCurDb.NamedObjectsDictionaryId, OpenMode.ForRead)
    
            Try
                ' Check to see if the Render Settings dictionary already exists or not
                Dim renderSettings As DBDictionary
                If namedObjs.Contains("ACAD_RENDER_SETTINGS") = True Then
                    renderSettings = acTrans.GetObject(namedObjs.GetAt("ACAD_RENDER_SETTINGS"), OpenMode.ForWrite)
                Else
                    acTrans.GetObject(acCurDb.NamedObjectsDictionaryId, OpenMode.ForWrite)
                    renderSettings = New DBDictionary
                    namedObjs.SetAt("ACAD_RENDER_SETTINGS", renderSettings)
                    acTrans.AddNewlyCreatedDBObject(renderSettings, True)
                End If
    
                ' Create the new render preset, based on the settings of the Medium render preset
                If renderSettings.Contains("MyPreset") = False Then
                    Dim renderSetting As MentalRayRenderSettings = GetDefaultRenderPreset("Medium")
                    renderSetting.Name = "MyPreset"
                    renderSetting.Description = "Custom new render preset"
                    renderSettings.SetAt("MyPreset", renderSetting)
                    acTrans.AddNewlyCreatedDBObject(renderSetting, True)
                End If
    
                ' Set the new render preset as current with the Render Engine
                Application.UIBindings.RenderEngineMR.CurrentRenderPresetName = "MyPreset"
            Catch es As Autodesk.AutoCAD.Runtime.Exception
                MsgBox(es.Message)
            Finally
                acTrans.Commit()
            End Try
        End Using
    End Sub
    
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
