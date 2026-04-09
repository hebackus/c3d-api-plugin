<!-- Developer's Guide > API Developer's Guide > Root Objects and Common Concepts > Name API 'ExportTo' using C++ -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-C97275B0-B2D8-4973-901C-E499B9454242.htm -->

# Name API 'ExportTo' using C++

Below is an example how you can change the API to 'ExportTo' using C++. 

For more information on the ExportTo Method, see [ExportTo Method. ](<https://help.autodesk.com/view/CIV3D/2021/ENU/?guid=2efdddc4-7813-8c83-fa66-315b3a895ca7>)
    
    
            public void StyleExportTest()
            {
                try
                {
                    var dwgPathAndName = @"C:\STYLES_2021.dwg";
                    if (!System.IO.File.Exists(dwgPathAndName))
                    {
                        Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage("No source file.\n");
                    }
                    var dbFrom = new Database(false, true);
                    dbFrom.ReadDwgFile(dwgPathAndName, FileOpenMode.OpenForReadAndAllShare, false, null);
                    var civDocFrom = CivilDocument.GetCivilDocument(dbFrom);
                    var dbTo = HostApplicationServices.WorkingDatabase;
    
                    using (var tr = dbTo.TransactionManager.StartOpenCloseTransaction())
                    {
                        try
                        {
                            var lineStyles = civDocFrom.Styles.LabelStyles.GeneralLineLabelStyles;
                            var curveStyles = civDocFrom.Styles.LabelStyles.GeneralCurveLabelStyles;
    
                            ObjectIdCollection idsExport = new ObjectIdCollection(); ;
                            foreach (ObjectId id in lineStyles)
                                idsExport.Add(id);
    
                            foreach (ObjectId id in curveStyles)
                                idsExport.Add(id);
    
                            Autodesk.Civil.DatabaseServices.Styles.StyleBase.ExportTo(idsExport, dbTo, Autodesk.Civil.StyleConflictResolverType.Override);
                            tr.Commit();
                        }
                        catch (System.Exception ex)
                        {
                            Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage(ex.Message + "Export failed.\n");
                        }
                    }
                }
                catch (System.Exception ex)
                {
                    Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage(ex.Message + "Export failed.\n");
                }
            }
