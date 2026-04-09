<!-- Developer's Guide > API Developer's Guide > Surfaces > Working with TIN Surfaces > Adding A Breakline to a TIN Surface -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-4C3A98F1-B429-4052-9ACE-AFBB55E0E60A.htm -->

# Adding A Breakline to a TIN Surface

Breaklines are used to shape the triangulation of a TIN surface. Each TIN surface has a collection of breaklines contained in the TinSurface.BreaklinesDefinition property, which is a SurfaceDefinitionBreaklines object. There are different kinds of breaklines, and each is created in a slightly different way. 

Note: For more information about breakline types, see the Autodesk Civil 3D User’s Guide.

The SurfaceDefinitionBreaklines class allows you to add standard, non-destructive, and proximity breaklines in similar ways. Each breakline type has its own Add*() method (for example, AddStandardBreaklines for standard breaklines), and each method has three versions, depending on the type of object you are creating a breakline from. You can add breaklines from a Point2dCollection, a Point3dCollection, or an ObjectIdCollection that contains one or more 3D lines, grading feature lines, splines, or 3D polylines. Each type of breakline requires a specified mid-ordinate distance parameter, which determines how curves are tessellated. 

A **standard breakline** consists of an array of 3D lines or polylines. Each line endpoint becomes a point in the surface and surface triangles around the breakline are redone. The AddStandardBreaklines() method requires that you specify the maximum distance, weeding distance and weeding angle, in addition to the mid-ordinate distance. The maximumDistance parameter corresponds to the Supplementing Distance in the Autodesk Civil 3D GUI, while weedingDistance and weedingAngle correspond to the weeding distance and angle, respectively. 

A **proximity breakline** does not add new points to a surface. Instead, the nearest surface point to each breakline endpoint is used. The triangles that make up a surface are then recomputed making sure those points are connected. 

A **non-destructive breakline** does not remove any triangle edges. It places new points along the breakline at each intersection with a triangle edge and new triangles are computed. 

This example illustrates how to add standard, non-destructive and proximity breaklines: 
    
    
    [CommandMethod("SurfaceBreaklines")]
    public void SurfaceBreaklines()
    {
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            // Prompt the user to select a TIN surface and a polyline, and create a breakline from the polyline
    
            ObjectId surfaceId = promptForEntity("Select a TIN surface to add a breakline to", typeof(TinSurface));
            ObjectId lineId = promptForEntity("Select a 3D polyline to use as the breakline", typeof(Polyline3d));
            TinSurface oSurface = surfaceId.GetObject(OpenMode.ForWrite) as TinSurface;
            ObjectId[] lines = { lineId };
    
            PromptKeywordOptions pKeyOpts = new PromptKeywordOptions("");
            pKeyOpts.Message = "\nEnter the type of breakline to create: ";
            pKeyOpts.Keywords.Add("Standard");
            pKeyOpts.Keywords.Add("Non-Destructive");
            pKeyOpts.Keywords.Add("Proximity");
            pKeyOpts.Keywords.Default = "Standard";
            pKeyOpts.AllowNone = true;
            PromptResult pKeyRes = editor.GetKeywords(pKeyOpts);
    
            try
            {
                switch (pKeyRes.StringResult)
                {
                    case "Non-Destructive":
                        oSurface.BreaklinesDefinition.AddNonDestructiveBreaklines(new ObjectIdCollection(lines), 1);
                        break;
                    case "Proximity":
                        oSurface.BreaklinesDefinition.AddProximityBreaklines(new ObjectIdCollection(lines), 1);
                        break;
                    case "Standard":
                    default:
                        oSurface.BreaklinesDefinition.AddStandardBreaklines(new ObjectIdCollection(lines), 10, 5, 5, 0);
                        break;
                }
            }
    
            catch (System.Exception e)
            {
                editor.WriteMessage("Operation failed: {0}", e.Message);
            }
    
            // commit the transaction
            ts.Commit();
        }
    }
