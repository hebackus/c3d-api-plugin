<!-- Developer's Guide > API Developer's Guide > Converting VBA Subassemblies to .NET > Procedure > Installing the New Subassembly -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-53C87771-7FE3-4BDB-BFE1-0321064AB18F.htm -->

# Installing the New Subassembly

The Autodesk Tool Catalog files (.atc files, found in ProgramData\Autodesk\C3D <version>\enu\Tool Catalogs\Road Catalog) need to be modified in order to list your new subassembly in the Civil 3D Subassembly Catalog. 

The .atc file format for .NET subassemblies is largely the same as for VBA subassemblies except that two new tags are used: 

<GeometryGenerateMode>UseDotNet</GeometryGenerateMode>
    

<GeometryGenerateMode> tells Civil 3D that you are using a .NET subassembly. It is placed within the <Tool> tag. 

<DotNetClass Assembly="%AECCCONTENT_DIR%\C3DStockSubassemblies.dll">Subassembly.NewCurb</DotNetClass>
    

<DotNetClass> is used instead of <Macro> tag when using .NET subassemblies
