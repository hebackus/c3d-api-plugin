<!-- Developer's Guide > API Developer's Guide > Corridors > Assemblies and Subassemblies > Importing Assemblies -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-657B4322-7203-4E70-B22F-27D3789B8A73.htm -->

# Importing Assemblies

The CivilDocument.AssemblyCollection object exposes an ImportAssembly() method that allows you to import an Assembly from an Autodesk Tool Catalog (.atc) file, or from another drawing's database. 

Tool catalogs provide a mechanism to organize and share Assemblies and Subassemblies. To import from an ATC file, the ImportAssembly() method takes the name of the newly imported Assembly, the full path to an .atc file (including the file name), the itemId for a tool in the ATC file, and the location in the drawing to insert the Assembly as a Point3d. 

You can determine the correct ItemId for the tool by looking at the <ExternalDrawing> element, which indicates the name of the Assembly. Here is the BasicAssembly XML from the Imperial Assemblies ATC file as an illustration (several elements are removed for clarity): 
    
    
    <Tool Revision="20.0.0" option="0">
    	<ItemID idValue="{CD468306-4A39-4AF9-B723-0C82A9644B97}"/>	
    [elements removed]		
    	<Data>
    		<AeccDbAssembly>
    			<ExternalDrawing>%AECCCONTENT_DIR%\Assemblies\Imperial\Basic Assembly.dwg</ExternalDrawing>
    		</AeccDbAssembly>
    		<Units>foot</Units>
    	</Data>
    </Tool>
    

In the example below, the user is prompted to select a drawing location, and the BasicAssembly Assembly is inserted from the stock Imperial Assemblies ATC file shipped with Civil 3D. 
    
    
    try
    {
        // import an assembly from an ATC file                     
        string assemblyName = _editor.GetString("Enter assembly name.").StringResult;
        string atcFilePath = @"C:\Users\Admininistrator\AppData\Roaming\Autodesk\C3D 2014\enu\Support\ToolPalette\Palettes\Assemblies - Imperial.atc"; 
        string itemId = "CD468306-4A39-4AF9-B723-0C82A9644B97";
        Point3d location = _editor.GetPoint("Select import assembly location").Value;
    
        ObjectId assemblyId3 = _civilDoc.AssemblyCollection.ImportAssembly(assemblyName, atcFilePath, itemId, location);
    
        ts.Commit();
    }
    catch (System.Exception e) { _editor.WriteMessage(e.Message); }
    

To import an Assembly from another drawing's database, the ImportAssembly() method takes the name of the newly imported Assembly, the source drawing database, the name of the Assembly in the source database, and a Point3d location for the imported Assembly. In this example, the user is prompted for the name and location of the new Assembly, and it is imported from one of the Civil 3D tutorial drawings. 
    
    
    using (Transaction ts = _currentDb.TransactionManager.StartTransaction())
    {
        try
        {
            // get the currently opened drawing:
            CivilDocument currentCivilDoc = _civildoc;
    
            string assemblyName = _editor.GetString("Enter new assembly name.").StringResult;
            Point3d location = _editor.GetPoint("Select import assembly location").Value;
    
            // open a drawing from the civil tutorials folder         
            string drawingName=@"C:\Program Files\Autodesk\AutoCAD Civil 3D 2014\Help\Civil Tutorials\Drawings\Corridor-5b.dwg";
            Document drawingDoc = Application.DocumentManager.Open(drawingName, true);
            Database sourceDatabase = drawingDoc.Database;
            string sourceAssemblyName = "Assembly - (1)"; // Divided highway with no superelevation                    
    
            ObjectId assemblyId3 = _civildoc.AssemblyCollection.ImportAssembly(assemblyName, sourceDatabase, sourceAssemblyName, location);
    
            ts.Commit();
        }
        catch (System.Exception e) { _editor.WriteMessage(e.Message); }
    }
