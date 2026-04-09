<!-- Developer's Guide > API Developer's Guide > Creating Custom Subassemblies Using .NET > Exporting Custom Subassemblies Using a Package File -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-B749C4D6-7EAC-42EA-89EB-25178126DF4D.htm -->

# Exporting Custom Subassemblies Using a Package File

You can share custom subassemblies with others by copying the required files to a package file. 

Custom subassemblies that have been created using .NET or VBA can be exported and imported using a package file. A package file contains all the files necessary for the custom subassemblies to work. Once the package file is created, users can import the package file into Autodesk Civil 3D, and then copy the custom subassemblies directly into a tool palette or catalog. For more information about importing subassembly package files, see [To Access and Share Subassemblies](<https://beehive.autodesk.com/community/service/rest/cloudhelp/resource/cloudhelpchannel/guidcrossbook/?v=2026&p=CIV3D&l=ENU&accessmode=live&guid=GUID-1A37AF5A-BEA8-4C25-893B-635ABF2DC63C>). 

To create a package file, you must copy all of the files that make up the custom subassembly or subassemblies into a folder. Create a _.zip_ file of that folder, and then change the file extension from _.zip_ to _.pkt_. 

Note: Subassemblies created from polylines cannot be included in a package file. Package files are intended for sharing custom subassemblies that have been created using .NET or VBA. 

## Naming the Package File

If you are sharing a single subassembly, it is recommended that you name the package file the same name as the subassembly. For example, if you plan to export a subassembly named OpenChannel, name the package file _OpenChannel.pkt_. If you plan to export multiple subassemblies in a single package file, give the folder a name that easily identifies the types of subassemblies that are contained in it. For example, _DitchSubassemblies.pkt_. 

## Required Subassembly Files

The following table describes the files that must be included in a package file to successfully export and import one or more subassemblies. 

File  | Description   
---|---  
_.atc_ file(s)  | A valid _.atc_ file that defines the shape and behavior of the subassembly or subassemblies is required. You can have one or more _.atc_ files included in the package file. For example, you can have one _.atc_ file that defines one or more subassemblies, or you can have multiple _.atc_ files, each of which defines one or more subassemblies. If the package file contains multiple _.atc_ files, each _.atc_ file must have a unique name. All the paths referenced in .atc file must be relative paths, if they point to files in the same .pkt file.   
_.dll_ or _.dvb_ file(s)  | A _.dll_ file is required for subassemblies that are defined using .NET. A _.dvb_ file is required for subassemblies that are defined using VBA. A package file can contain both _.dll_ and _.dvb_ files.   
Help file(s)  | A Help file is not required in order for a subassembly to function properly. However, the Help file is needed for others to understand how to use the subassembly. Therefore, it is recommended that you always include a Help file with each subassembly. For more information, see [Creating Subassembly Help Files](<GUID-D08C5392-0E8E-423D-A160-9849F3FDF241.htm>).   
Image file(s)  | An image file for each is displayed on the tool palette and is used to provide a conceptual graphical representation of the subassembly shape.
