<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Getting Started with Microsoft Visual Studio (.NET) > Define the Components in a Project (.NET) > Per Document Data (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-B8F6FD9A-8FC2-47DF-BE26-11073EAF49D5.htm -->

# Per Document Data (.NET)

Global data can be temporally stored in memory at the document level. 

When the AutoCAD program loads a managed application, it queries the application's assembly for one or more PerDocumentClass custom attributes. If instances of this attribute are found, an instance of each attribute's associated type is created for each document open in the AutoCAD drawing environment. New instances of the types are then created for any documents that are opened thereafter. 

The type associated with a PerDocumentClass attribute must provide either a Public constructor that takes a document argument or a Public Static Create method that takes a document argument and returns an instance of the type. If the Create method exists, it will be used, otherwise the constructor will be used. The document that the type instance is being created for will be passed as the document argument so that the type instance knows with which document it is associated. 

The following procedure describes how to use the PerDocumentClass attribute. 

  1. In the assembly context, declare a PerDocumentClass attribute for each class that you want to be instantiated for each document. 
  2. Pass the type of the class to the PerDocumentClass attribute. 

Note: This attribute must be declared in the assembly context. 

## C#
    
    
    ...
    using Autodesk.AutoCAD.ApplicationServices;
    using Autodesk.AutoCAD.Runtime;
    
    [assembly: PerDocumentClass(typeof(CSPerDoc.PerDocData))]
    
    namespace CSPerDoc
    {
        // Defines a global class for constant values
        public static class CSPerDocConsts
        {
            public const string dbLocVarName = "dbLoc";
        }
    
        // Defines the main class
        public class PerDocCommands
        {
            // Creates a command that returns the current value of the per document data
            [CommandMethod("DatabaseLocation")]
            public void DatabaseLocation()
            {
                Document acDoc = Application.DocumentManager.MdiActiveDocument;
                PerDocData pDData = (PerDocData) acDoc.UserData[CSPerDocConsts.dbLocVarName];
                if (pDData == null) {
                    acDoc.Editor.WriteMessage("\nNo user data assigned.");
                } else {
                    acDoc.Editor.WriteMessage("\n" + pDData.DbLocation);
                }
            }
        }
    
        // Defines the class that wuill be used to initialize the per document data
        public class PerDocData
        {
            // Define the internal/member variables of the class
            private string _stDbLoc;
    
            // Expose a public property that returns the value of the internal variable
            public string DbLocation
            {
                get { return _stDbLoc; }
            }
    
            // Public constructor that requires a Document object
            // Created by AutoCAD when the application is loaded
            public PerDocData(Document acDoc)
            {
                _stDbLoc = @"";
                acDoc.UserData.Add(CSPerDocConsts.dbLocVarName, this);
            }
    
            // Create method: Required constructor for the class
            public static PerDocData Create(Document acDoc)
            {
                PerDocData pDData = new PerDocData(acDoc);
                pDData._stDbLoc = @"C:\\ABCApp\\ProjectData\\" + acDoc.Name.Remove(acDoc.Name.Length - 4) + ".db";
    
                return pDData;
            }
        }
    }

## VB.NET
    
    
    ...
    Imports Autodesk.AutoCAD.ApplicationServices
    Imports Autodesk.AutoCAD.Runtime
    
    <Assembly: PerDocumentClass(GetType(PerDocData))> 
    
    ' Defines a global class for constant values
    Public NotInheritable Class CSPerDocConsts
        Private Sub New()
        End Sub
    
        Public Const dbLocVarName As String = "dbLoc"
    End Class
    
    ' Defines the main class
    Public Class PerDocCommands
        ' Creates a command that returns the current value of the per document data
        <CommandMethod("DatabaseLocation")> _
        Public Sub DatabaseLocation()
            Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
            Dim pDData As PerDocData = DirectCast(acDoc.UserData(CSPerDocConsts.dbLocVarName), PerDocData)
            If pDData Is Nothing Then
                acDoc.Editor.WriteMessage(vbLf & "No user data assigned.")
            Else
                acDoc.Editor.WriteMessage(vbLf & pDData.DbLocation)
            End If
        End Sub
    End Class
    
    ' Defines the class that wuill be used to initialize the per document data
    Public Class PerDocData
        ' Define the internal/member variables of the class
        Private _stDbLoc As String
    
        ' Expose a public property that returns the value of the internal variable
        Public ReadOnly Property DbLocation() As String
            Get
                Return _stDbLoc
            End Get
        End Property
    
        ' Public constructor that requires a Document object
        ' Created by AutoCAD when the application is loaded
        Public Sub New(acDoc As Document)
            _stDbLoc = ""
            acDoc.UserData.Add(CSPerDocConsts.dbLocVarName, Me)
        End Sub
    
        ' Create method: Required constructor for the class
        Public Shared Function Create(acDoc As Document) As PerDocData
            Dim pDData As New PerDocData(acDoc)
            pDData._stDbLoc = "C:\ABCApp\Data\" & acDoc.Name.Remove(acDoc.Name.Length - 4) & ".db"
    
            Return pDData
        End Function
    End Class
