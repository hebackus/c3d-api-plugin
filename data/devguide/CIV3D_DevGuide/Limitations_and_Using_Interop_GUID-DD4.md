<!-- Developer's Guide > API Developer's Guide > Getting Started > Migrating COM code to .NET > Limitations and Using Interop -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-DD447A5A-DF8B-4905-8BFC-4CBFA1C7C121.htm -->

# Limitations and Using Interop

The .NET API does not expose all the functionality of Autodesk Civil 3D, and it exposes less than the COM API. The following areas are not yet exposed in .NET: 

  * Sites and Parcels 
  * Data Bands 
  * Some labels 

In addition, there are some areas in implemented functionality that are not yet complete: 

  * Pipes: interference checks (except interference check styles) 

If you require this functionality in your .NET project, you can use the corresponding COM objects. 

To use Autodesk Civil 3D COM APIs from .NET

  1. Create a .NET solution and project. 
  2. Select Add Reference from the Project menu or Solution Explorer. 
  3. On the Browse tab, browse to the Civil 3D install directory, and select the following COM interop DLLs, where <domain> is the Civil domain you want to use (Land, Roadway, Pipe, or Survey): 
     * Autodesk.AEC.Interop.Base 
     * Autodesk.AEC.Interop.UiBase 
     * Autodesk.AutoCAD.Interop 
     * Autodesk.AutoCAD.Interop.Common 
     * Autodesk.AECC.Interop.<domain>
     * Autodesk.AECC.Interop.Ui<domain>
  4. Select the references above, and set the "Copy Local" property to true, as this will embed all referenced types into your target assembly, and the referenced interop DLLs are therefore not required at runtime. 
  5. Add the Autodesk.AutoCAD.Interop and Autodesk.AECC.Interop.Ui<domain> namespaces to your using or Imports statement. 

Note:

You may see warnings about types not being found in various Autodesk.AutoCAD.Interop namespaces (warning type 1684). To disable these warnings, enter 1684 under Supress Warnings on the Build tab of the project’s properties. 

Here is a C# example of getting a count of point groups and surfaces from a document using COM interop: 
    
    
    string m_sAcadProdID = "AutoCAD.Application";
    string m_sAeccAppProgId = "AeccXUiLand.AeccApplication.10.3";
    ...
    private void useCom()
    {
        //Construct AeccApplication object, Document and Database objects
        m_oAcadApp = (IAcadApplication)System.Runtime.InteropServices.Marshal.GetActiveObject(m_sAcadProdID);     
        if (m_oAcadApp != null)
        {
            m_oAeccApp = (IAeccApplication)m_oAcadApp.GetInterfaceObject(m_sAeccAppProgId);
            m_oAeccDoc = (IAeccDocument)m_oAeccApp.ActiveDocument;
            
            
            // get the Database object via a late bind
            m_oAeccDb = (Autodesk.AECC.Interop.Land.IAeccDatabase)m_oAeccDoc.GetType().GetProperty("Database").GetValue(m_oAeccDoc, null);
            long lCount = m_oAeccDb.PointGroups.Count;
            m_sMessage += "Number of PointGroups = " + lCount.ToString() + "\n";
            lCount = m_oAeccDb.Surfaces.Count;
            m_sMessage += "Number of Surfaces = " + lCount.ToString() + "\n\n";
            MessageBox.Show(m_sMessage);
            m_sMessage = "";
            
        }
    }
    

For more interoprability examples, see the CSharpClient and VbDotNetClient sample projects located in <Install directory>\Sample\Autodesk Civil 3D\COM\.
