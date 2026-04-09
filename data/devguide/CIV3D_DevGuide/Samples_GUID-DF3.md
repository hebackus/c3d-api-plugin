<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Creating Client Applications > Samples -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-DF3E8C70-B59F-44BD-B92F-1091F2509F47.htm -->

# Samples

All of the following are located in the **< installation-directory>\Sample\Civil 3D API\COM** directory.

## C++ Using COM

**.\VC++\COM C++\ProjectStats.vcproj**

Directly launches Autodesk Civil 3D and creates a dialog box that displays some information about the current drawing or adds sample lines into the alignments of any selected sites.

## Managed C++

**.\VC++\Managed C++\C3DManagedExample.vcproj**

Using COM interops, launches Autodesk Civil 3D and creates a dialog box that displays some information about the current drawing or adds sample lines into the alignments of any selected sites.

## C++ Using CustomDraw

**.\VC++\CustomDraw\Sample\C3DCustomDraw.vcproj**

Demonstrates accessing the CustomDraw API. This project overrides how triangles in TIN surfaces are drawn so that they’re numbered. It requires the Autodesk ObjectARX libraries.

## C++ Using Custom Events

**.\VC++\CustomEvent\Sample\C3DCustomEvent.vcproj**

Demonstrates using custom events. This project recieves notification just before and just after a corridor is rebuilt. It requires the Autodesk ObjectARX libraries.

## C++ Using Custom UI

**.\VC++\CustomEvent\Sample\C3DCustomUI.vcproj**

Demonstrates UI customization. This project adds a button to the Properties Property sheet that opens a custom dialog for TIN surfaces. It requires the Autodesk ObjectARX libraries.

## C++ Client Sample

**.\VC++\VcClient\VcClientSamp.vcproj**

Creates a dialog box that lets you launch Autodesk Civil 3D and determine simple information about the current drawing.

## C# 

**.\CSharp\CSharpClient\CSharpClientSample.csproj**

Creates a dialog box that lets you launch Autodesk Civil 3D and determine simple information about the current drawing.

## Visual Basic .NET

**.\VB_NET\VbDotNetClient\VBDotNetClientSample.vbproj**

Creates a dialog box that lets you launch Autodesk Civil 3D and determine simple information about the current drawing.
