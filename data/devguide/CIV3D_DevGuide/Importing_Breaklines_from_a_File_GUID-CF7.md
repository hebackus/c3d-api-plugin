<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Working with TIN Surfaces > Adding a Breakline to a TIN Surface > Importing Breaklines from a File -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-CF7DE6F7-EE67-450C-888C-7C9175731D1C.htm -->

# Importing Breaklines from a File

You can import breaklines from a file in .FLT format, using AeccSurfaceBreaklines.AddBreaklineFromFile(). When you import the file, you need to specify whether to maintain the file link, or break the link: 

  * aeccBreaklineFileMaintainLink: Reads the breaklines from the FLT file when they are added and when the surface is rebuilt. 
  * aeccBreaklineFileBreakLink: All breaklines in the FLT file are copied into the surface as Add Breakline operations. 

For more information about these options, see [To Import Breaklines from a File](<https://beehive.autodesk.com/community/service/rest/cloudhelp/resource/cloudhelpchannel/guidcrossbook/?v=2026&p=CIV3D&l=ENU&accessmode=live&guid=GUID-BD2BC12A-465D-4F7F-A678-4A1569804524>). 

This sample shows how to import breaklines from a file named eg1.flt, and to get the first newly created breakline: 
    
    
    Dim oBrkLine As AeccSurfaceBreakline 
    Set oBrkLine = brkLines.AddBreaklineFromFile("New Breakline", "C:\eg1.flt", 10#, aeccBreaklineFileBreakLink)(0)
