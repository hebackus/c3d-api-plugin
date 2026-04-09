<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > About .NET and the AutoCAD .NET API (.NET) > Components of the AutoCAD .NET API (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-8657D153-0120-4881-A3C8-E00ED139E0D3.htm -->

# Components of the AutoCAD .NET API (.NET)

The AutoCAD .NET API is made up of different DLL files that contain a wide range of classes, structures, methods, and events that provide access to objects in a drawing file or the application. Each DLL file defines different namespaces which are used to organize the components of the libraries based on functionality. 

The main DLL files of the AutoCAD .NET API that you will frequently use are: 

  * **AcCoreMgd.dll.** Use when working within the editor, publishing and plotting, and defining commands and functions that can be called from AutoLISP. 
  * **AcDbMgd.dll.** Use when working with objects stored in a drawing file. 
  * **AcMgd.dll.** Use when working with the application and user interface. 
  * **AcCui.dll.** Use when working with customization files. 

## Reference an AutoCAD .NET API DLL

Before classes, structures, methods, and events found in one of the AutoCAD .NET API related DLLs can be used, you must reference the DLL to a project. After a DLL is referenced to a project, you can utilize the namespaces and the components in the DLL file in your project. 

Once a AutoCAD .NET API DLL is referenced, you must set the Copy Local property of the referenced DLL to False. The Copy Local property determines if Microsoft Visual Studio creates a copy of the referenced DLL file and places it in the same directory as the _assembly file_ (or executable file) that is generated when building the project. Since the referenced files already ship with the product, creating copies of the referenced DLL files can cause unexpected results when you load your assembly file. 

An _assembly file_ is the source code from an Intermediate Language (IL) based program and is executed by invoking the .NET runtime; called the CLR, Common Language Runtime. The CLR compiles an assembly into native code right before it is executed by the operating system or another application. The process of compiling at runtime just before execution is often referred to as Just-In-Time (JIT) compiling. You can pre-compile an assembly using NGEN to create a native executable. Using NGEN can make your assembly more secure since it cannot be viewed using an IL disassembler. 

## Location of AutoCAD .NET API DLL Files

The AutoCAD .NET API DLL files can be located at _< drive>:\Program Files\Autodesk\<release>_ or as part of the latest _ObjectARX SDK_ which can be downloaded from _http://www.objectarx.com_ or the Autodesk Developer Network (ADN) website (_https://www.autodesk.com/adn_). 

After the ObjectARX SDK is installed, the DLL files can be found in the _inc_ folder under the main install folder. 

Note: The DLLs in the ObjectARX SDK are simplified versions of the same files that ship with AutoCAD, as they do not contain dependencies on the AutoCAD user interface. It is recommended that you download and install the ObjectARX SDK, and then reference the DLL files that come with the SDK instead of those that are found in the install directory of AutoCAD or the AutoCAD-based program. 

## Procedures

**To download and install the latest ObjectARX SDK**

  1. Launch your default Internet browser application and browse to _http://www.objectarx.com_. 
  2. On the Web page, click **Go to license agreement**. 
  3. Fill in the required fields and click **Submit**. 
  4. On the Download page, click the version of the ObjectARX SDK to download. 
  5. Click the download link to save it to your local drive. 
  6. Once the package file has been downloaded, browse to its location and double-click it. 

The install wizard is displayed. 

  7. In the ObjectARX _< Release>_ dialog box, specify a new install location or leave the default install location. Click **Install**. 

The install wizard closes after it is finished if no problems were encountered. 

**To install the Managed .NET project wizard**

  1. Launch your default Internet browser application and browse to _https://www.autodesk.com/developautocad_. 
  2. Download and unzip the _< release> .NET Wizards.zip_ file. 
  3. After browsing to the location of the unzipped files, double-click the _< release> dotNET Wizards.msi_ file. 
  4. In the AutoCAD .NET Wizards dialog box, click **Next**. 
  5. On the Select Installation Folder page, click Browse to specify a new installation location for the wizard or leave the default location. Click **Next**. 
  6. Click **Next** again to confirm installation of the wizard. 
  7. Click **Close** to close the installer. 

**To reference an AutoCAD .NET API DLL**

  1. In Microsoft Visual Studio, click View menu  Solution Explorer to display the Solution Explorer, if it is not already displayed. 
  2. In the Solution Explorer, on the toolbar along the top, click Show All Files. 
  3. Right-click over the Dependencies node and click choose Add COM Reference. 
  4. In the Reference Manager dialog box, Browse tab, select the DLL file that contains the library you want to use and click OK. 
  5. In the Solution Explorer, expand Dependencies  Assemblies. 
  6. Select the referenced library from the Assemblies node. 
  7. Right-click over the selected reference and click Properties. 
  8. In the Properties window, click the Copy Local field and select False from the drop-down list.
