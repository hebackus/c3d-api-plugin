<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Getting Started with Microsoft Visual Studio (.NET) > Work with Microsoft Visual Studio Projects (.NET) > Work with Multiple Projects in a Solution (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-28A97A98-26CD-422E-813B-29F77B773D67.htm -->

# Work with Multiple Projects in a Solution (.NET)

A solution can contain multiple projects. Working with multiple projects is not much different than working with a single project. Use the Solution Explorer to navigate between the projects in the current solution. 

## Add a project to a solution

You might add a project to a solution to copy code between projects. You might want to reference the procedures, functions and classes in one project and use them in another project. By adding multiple projects to a single solution, it allows you to use a project as a set of common utilities that you might use with more than one project. 

## Unload a project from a solution

Projects can be unloaded from a solution when they are no longer needed. If you no longer want a project to load with a solution, you can unload the project and then reference the compiled DLL assembly of the project instead. Working with the compiled DLL helps to prevent accidental edits to the source code. 

## Procedures

**To add a project to a solution**

  * In Microsoft Visual Studio, do one of the following: 
    * Click File menu  Add  New Project to create a new project and add it to the current solution. 
    * Click File menu  Add  Existing Project to display the Add Existing Project dialog box and add an existing project to the current solution. In the Add Existing Project dialog box, browse to and select the project to add to the current solution. 

**To unload a project from a solution**

  * In Microsoft Visual Studio, Solution Explorer, right-click the project you want to unload from the current solution and click Unload Project. 

**To close a solution**

  * Click File menu  Close Solution.
