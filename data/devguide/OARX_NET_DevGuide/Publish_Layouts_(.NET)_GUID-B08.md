<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Publish Layouts (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-B08B5173-0C17-4663-BD1C-A40E4C8F3A75.htm -->

# Publish Layouts (.NET)

Before you can publish multiple layouts, you need to gather information about each layout. You create a DsdEntry object for each layout to be published. A DsdEntry object contains the layout name, title, override page setup, and drawing file it is located in. DsdEntry objects are then added to a DsdEntryCollection object which is then added to a DsdData object with the SetDsdEntryCollection method. 

A DsdData object defines the settings that should be used to publish the specified layouts. After a DsdData object is defined, you can use the WriteDsd method to create a DSD file for use with the PUBLISH command or Publisher object. 

The Publisher object is used to output the layouts in a DSD file. Similar to the Publish dialog box, a layout can be output using its plot device and settings defined or you can use an override page setup in the DsdEntry object with the PublishDsd method. You can also override the device assigned to a layout with the PublishExecute method. 

Note: You should set the BACKGROUNDPLOT system variable to a value of 0 before publishing a DSD file with the PublishDsd method. 

## Publish layouts to a PDF file

This example publishes two layouts to a PDF file using the PublishExecute method. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.DatabaseServices;
    using Autodesk.AutoCAD.PlottingServices;
    
    // Publishes layouts to a PDF file
    [CommandMethod("PublishLayouts")]
    public static void PublishLayouts()
    {
        using (DsdEntryCollection dsdDwgFiles = new DsdEntryCollection())
        {
            // Define the first layout
            using (DsdEntry dsdDwgFile1 = new DsdEntry())
            {
                // Set the file name and layout
                dsdDwgFile1.DwgName = "C:\\AutoCAD\\Samples\\Sheet Sets\\Architectural\\A-01.dwg";
                dsdDwgFile1.Layout = "MAIN AND SECOND FLOOR PLAN";
                dsdDwgFile1.Title = "A-01 MAIN AND SECOND FLOOR PLAN";
    
                // Set the page setup override
                dsdDwgFile1.Nps = "";
                dsdDwgFile1.NpsSourceDwg = "";
    
                dsdDwgFiles.Add(dsdDwgFile1);
            }
    
            // Define the second layout
            using (DsdEntry dsdDwgFile2 = new DsdEntry())
            {
                // Set the file name and layout
                dsdDwgFile2.DwgName = "C:\\AutoCAD\\Samples\\Sheet Sets\\Architectural\\A-02.dwg";
                dsdDwgFile2.Layout = "ELEVATIONS";
                dsdDwgFile2.Title = "A-02 ELEVATIONS";
    
                // Set the page setup override
                dsdDwgFile2.Nps = "";
                dsdDwgFile2.NpsSourceDwg = "";
    
                dsdDwgFiles.Add(dsdDwgFile2);
            }
    
            // Set the properties for the DSD file and then write it out
            using (DsdData dsdFileData = new DsdData())
            {
                // Set the target information for publishing
                dsdFileData.DestinationName = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + "\\MyPublish2.pdf";
                dsdFileData.ProjectPath = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + "\\";
                dsdFileData.SheetType = SheetType.MultiPdf;
    
                // Set the drawings that should be added to the publication
                dsdFileData.SetDsdEntryCollection(dsdDwgFiles);
    
                // Set the general publishing properties
                dsdFileData.LogFilePath = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + "\\myBatch.txt";
    
                // Create the DSD file
                dsdFileData.WriteDsd(Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + "\\batchdrawings2.dsd");
    
                try
                {
                    // Publish the specified drawing files in the DSD file, and
                    // honor the behavior of the BACKGROUNDPLOT system variable
    
                    using (DsdData dsdDataFile = new DsdData())
                    {
                        dsdDataFile.ReadDsd(Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + "\\batchdrawings2.dsd");
    
                        // Get the DWG to PDF.pc3 and use it as a 
                        // device override for all the layouts
                        PlotConfig acPlCfg = PlotConfigManager.SetCurrentConfig("DWG to PDF.PC3");
    
                        Application.Publisher.PublishExecute(dsdDataFile, acPlCfg);
                    }
                }
                catch (Autodesk.AutoCAD.Runtime.Exception es)
                {
                    System.Windows.Forms.MessageBox.Show(es.Message);
                }
            }
        }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.DatabaseServices
    Imports Autodesk.AutoCAD.PlottingServices
    
    ' Publishes layouts to a PDF file
    <CommandMethod("PublishLayouts")> _
    Public Shared Sub PublishLayouts()
        Using dsdDwgFiles As New DsdEntryCollection
    
            ' Add first drawing file
            Using dsdDwgFile1 As New DsdEntry
    
                ' Set the file name and layout
                dsdDwgFile1.DwgName = "C:\AutoCAD\Samples\Sheet Sets\Architectural\A-01.dwg"
                dsdDwgFile1.Layout = "MAIN AND SECOND FLOOR PLAN"
                dsdDwgFile1.Title = "A-01 MAIN AND SECOND FLOOR PLAN"
    
                ' Set the page setup override
                dsdDwgFile1.Nps = ""
                dsdDwgFile1.NpsSourceDwg = ""
    
                dsdDwgFiles.Add(dsdDwgFile1)
            End Using
    
            ' Add second drawing file
            Using dsdDwgFile2 As New DsdEntry
    
                ' Set the file name and layout
                dsdDwgFile2.DwgName = "C:\AutoCAD\Samples\Sheet Sets\Architectural\A-02.dwg"
                dsdDwgFile2.Layout = "ELEVATIONS"
                dsdDwgFile2.Title = "A-02 ELEVATIONS"
    
                ' Set the page setup override
                dsdDwgFile2.Nps = ""
                dsdDwgFile2.NpsSourceDwg = ""
    
                dsdDwgFiles.Add(dsdDwgFile2)
            End Using
    
            ' Set the properties for the DSD file and then write it out
            Using dsdFileData As New DsdData
    
                ' Set the target information for publishing
                dsdFileData.DestinationName = Environment.GetFolderPath( _
                    Environment.SpecialFolder.MyDocuments) & "\MyPublish2.pdf"
                dsdFileData.ProjectPath = Environment.GetFolderPath( _
                    Environment.SpecialFolder.MyDocuments) & "\"
                dsdFileData.SheetType = SheetType.MultiPdf
    
                ' Set the drawings that should be added to the publication
                dsdFileData.SetDsdEntryCollection(dsdDwgFiles)
    
                ' Set the general publishing properties
                dsdFileData.LogFilePath = Environment.GetFolderPath( _
                    Environment.SpecialFolder.MyDocuments) & "\myBatch.txt"
    
                ' Create the DSD file
                dsdFileData.WriteDsd(Environment.GetFolderPath( _
                                     Environment.SpecialFolder.MyDocuments) & _
                                     "\batchdrawings2.dsd")
    
                Try
                    ' Publish the specified drawing files in the DSD file, and
                    ' honor the behavior of the BACKGROUNDPLOT system variable
                    Using dsdDataFile As New DsdData
                        dsdDataFile.ReadDsd(Environment.GetFolderPath( _
                                            Environment.SpecialFolder.MyDocuments) & _
                                            "\batchdrawings2.dsd")
    
                        ' Get the DWG to PDF.pc3 and use it as a 
                        ' device override for all the layouts
                        Dim acPlCfg As PlotConfig = _
                            PlotConfigManager.SetCurrentConfig("DWG to PDF.PC3")
    
                        Application.Publisher.PublishExecute(dsdDataFile, acPlCfg)
                    End Using
    
                Catch es As Autodesk.AutoCAD.Runtime.Exception
                    MsgBox(es.Message)
                End Try
            End Using
        End Using
    End Sub
