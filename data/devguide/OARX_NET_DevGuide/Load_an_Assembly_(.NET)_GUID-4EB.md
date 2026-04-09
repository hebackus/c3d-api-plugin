<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Getting Started with Microsoft Visual Studio (.NET) > Load an Assembly (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-4EB83A6B-9903-4BF7-9F19-767A4D419CE3.htm -->

# Load an Assembly (.NET)

Once a solution and project are created, a namespace and class are defined, and one or more command or AutoLISP® function structures are implemented, you can use the NETLOAD command to load a .NET assembly. 

## Use the Debug Environment

Prior to loading a .NET assembly, you should determine if you need to use the Debug environment of Microsoft Visual Studio to test any logic defined in the procedures and functions you might have created. The Debug environment allows you to step through the code in the .NET assembly as it is being executed in real-time. As the code is being executed, you are able to check the values of variables and watch which logic paths of the program are executed. 

For more information on using the Debug environment, see the documentation that comes with your development environment. 

## Procedures

**To load a .NET Assembly through Debug Mode**

Note: Debug features are not available in Microsoft Visual Studio Express. 

  1. In Microsoft Visual Studio, Solution Explorer, right-click the project you want to load. Click Properties. 
  2. In the <Project> Properties tab, click the Debug tab. 
  3. On the Debug tab, under Start Action, click Start External Program and then click the ellipsis button to the right of the text box. 
  4. In the Select File dialog box, browse to _C:\Program Files\Autodesk\ <release>_ and select _acad.exe_. Click Open. 
  5. With the project selected in the Solution Explorer, click Debug menu  Start Debugging. 
  6. In AutoCAD, at the Command prompt, enter **netload**. 
  7. In the Choose .NET Assembly dialog box, browse to the debug version of the assembly file. Click Open. 

Tip: The location of the built assembly file is in the Output pane in Microsoft Visual Studio. 

By default, the debug version is located under the _\bin\debug_ folder; while the release version can be found under the _\bin\release_ folder. 

  8. At the Command prompt, enter the name of the command or AutoLISP function and any required parameters. 

**To load a .NET assembly with NETLOAD**

  1. In Microsoft Visual Studio, with a solution or project open, click Build menu  Build Solution or Build _< Project name>_. 
  2. In AutoCAD, at the Command prompt, enter **netload**. 
  3. In the Choose .NET Assembly dialog box, browse to the built assembly file. Click Open. 

Tip: The location of the built assembly file is in the Output pane in Microsoft Visual Studio. 

By default, the debug version is located under the _\bin\debug_ folder; while the release version can be found under the _\bin\release_ folder. 

  4. At the Command prompt, enter the name of the command or AutoLISP function and any required parameters.
