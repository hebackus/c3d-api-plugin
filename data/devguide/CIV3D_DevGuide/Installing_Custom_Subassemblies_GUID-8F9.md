<!-- Developer's Guide > API Developer's Guide > Creating Custom Subassemblies Using .NET > Installing Custom Subassemblies -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-8F9A5C64-4EBE-433E-89B8-92F776DBACFD.htm -->

# Installing Custom Subassemblies

Once you’ve created a custom subassembly, you can install it on other Autodesk Civil 3D users’ machines.

Note:

It’s simpler to create a subassembly package file to distribute to users than to install custom subassemblies manually. See [Exporting Subassemblies Using a Package File](<GUID-B749C4D6-7EAC-42EA-89EB-25178126DF4D.htm>).

To install a custom subassembly:

  1. Copy the compiled Autodesk Civil 3D subassembly _.dll_ library to its destination directory. By default, libraries are located in _< Autodesk Civil 3D Install Directory>\Sample\Civil 3D API\C3DstockSubAssemblies_. 
  2. Copy the tool catalog _.atc_ files to its destination directory. The tool catalog files are normally located in the directory. For information about creating these, see [Creating a Tool Catalog ATC File](<GUID-40C8020C-6B2F-4C8E-BC44-59CDEDD5C550.htm>). 
  3. Copy optional files such as the image file representing the subassemblies or the help file to their destination directory. Images are normally located in , and help files are normally located in , although these can be any directory as long as the _.atc_ file has the correct relative path information. For information about creating help files, see [Creating Subassembly Help Files](<GUID-D08C5392-0E8E-423D-A160-9849F3FDF241.htm>)
  4. Copy the catalog cover page _.html_ file to its destination. Usually this is the same location as the _.atc_ file, although it can be any directory as long as the _.atc_ file has the correct relative path information. For information about creating cover pages, see [Creating a Tool Catalog Cover Page](<GUID-DAA35D43-162C-419E-931A-AC1D27568B3F.htm>).
  5. Register the tool catalog using a registry (_.reg_) file. This _.reg_ file must have the correct paths to the _.atc_ file and the catalog image file from steps 2) and 3). For information about creating registry files, see [Creating a Tool Catalog Registry File](<GUID-7D8F6D79-5662-4793-AB30-769A5C384CFF.htm>)
