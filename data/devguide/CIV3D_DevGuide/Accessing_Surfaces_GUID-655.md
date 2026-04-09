<!-- Developer's Guide > API Developer's Guide > Surfaces > Accessing Surfaces -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-655D3624-20DD-4E47-B0ED-484AA43FAB8B.htm -->

# Accessing Surfaces

There are many ways to access the surfaces objects in a drawing. All the surfaces contained by a Document can be obtained using the CivilDocument.GetSurfaceIds() method, which returns an ObjectIdCollection. 
    
    
    ObjectIdCollection SurfaceIds = doc.GetSurfaceIds();
    foreach (ObjectId surfaceId in SurfaceIds)
    {
        CivSurface oSurface = surfaceId.GetObject(OpenMode.ForRead) as CivSurface;
        editor.WriteMessage("Surface: {0} \n  Type: {1}", oSurface.Name, oSurface.GetType().ToString());
    
    }
    

Note that there is also a Surface class in the Autodesk.AutoCAD.DatabaseServices namespace, which will conflict with Autodesk.Civil.DatabaseServices.Surface if you use both namespaces. In this case you can fully qualify the Surface object, or use a "using" alias directive to disambiguate the reference. For example: 
    
    
    using CivSurface = Autodesk.Civil.DatabaseServices.Surface;

And then use the alias like this: 
    
    
    CivSurface oSurface = surfaceId.GetObject(OpenMode.ForRead) as CivSurface;

You can also prompt a user to select a specific surface type, such as a TIN Surface, and then get the surface ID from the selection: 
    
    
    private ObjectId promptForTinSurface(String prompt)
    {
        PromptEntityOptions options = new PromptEntityOptions(
            String.Format("\n{0}: ", prompt));
        options.SetRejectMessage(
            "\nThe selected object is not a TIN Surface.");
        options.AddAllowedClass(typeof(TinSurface), true);
    
        PromptEntityResult result = editor.GetEntity(options);
        if (result.Status == PromptStatus.OK)
        {
            // We have the correct object type
            return result.ObjectId;
        }
        return ObjectId.Null;   // Indicating error.
    }
