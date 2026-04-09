<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Use Events (.NET) > Register and Unregister Events (.NET) > Handle DocumentCollection Events (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-E619BB54-D531-4640-BB74-B61E6CA13238.htm -->

# Handle DocumentCollection Events (.NET)

DocumentCollection object events are used to respond to the open documents in the application. DocumentCollection events, unlike Document object events, remain registered until AutoCAD is shutdown or until they are unregistered. 

The following events are available for DocumentCollection objects: 

DocumentActivated
    

Triggered when a document window is activated. 

DocumentActivationChanged
    

Triggered after the active document window is deactivated or destroyed. 

DocumentBecameCurrent
    

Triggered when a document window is set current and is different from the previous active document window. 

DocumentCreated
    

Triggered after a document window is created. Occurs after a new drawing is created or an existing drawing is opened. 

DocumentCreateStarted
    

Triggered just before a document window is created. Occurs before a new drawing is created or an existing drawing is opened. 

DocumentCreationCanceled
    

Triggered when a request to create a new drawing or to open an existing drawing is cancelled. 

DocumentDestroyed
    

Triggered before a document window is destroyed and its associated database object is deleted. 

DocumentLockModeChanged
    

Triggered after the lock mode of a document has changed. 

DocumentLockModeChangeVetoed
    

Triggered after the lock mode change is vetoed. 

DocumentLockModeWillChange
    

Triggered before the lock mode of a document is changed. 

DocumentToBeActivated
    

Triggered when a document is about to be activated. 

DocumentToBeDeactivated
    

Triggered when a document is about to be deactivated. 

DocumentToBeDestroyed
    

Triggered when a document is about to be destroyed. 

## Enable a DocumentCollection object event

The following example uses the DocumentActivated event to indicate when a drawing window has been activated. A message box with the name of the drawing that is activated is displayed when the event occurs. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
     
    [CommandMethod("AddDocColEvent")]
    public void AddDocColEvent()
    {
      Application.DocumentManager.DocumentActivated +=
          new DocumentCollectionEventHandler(docColDocAct);
    }
     
    [CommandMethod("RemoveDocColEvent")]
    public void RemoveDocColEvent()
    {
      Application.DocumentManager.DocumentActivated -=
          new DocumentCollectionEventHandler(docColDocAct);
    }
     
    public void docColDocAct(object senderObj, 
                             DocumentCollectionEventArgs docColDocActEvtArgs)
    {
      Application.ShowAlertDialog(docColDocActEvtArgs.Document.Name +
                                  " was activated.");
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
     
    <CommandMethod("AddDocColEvent")> _
    Public Sub AddDocColEvent()
      AddHandler Application.DocumentManager.DocumentActivated, _
          AddressOf docColDocAct
    End Sub
     
    <CommandMethod("RemoveDocColEvent")> _
    Public Sub RemoveDocColEvent()
      RemoveHandler Application.DocumentManager.DocumentActivated, _
          AddressOf docColDocAct
    End Sub
     
    Public Sub docColDocAct(ByVal senderObj As Object, _
                            ByVal docColDocActEvtArgs As DocumentCollectionEventArgs)
      Application.ShowAlertDialog(docColDocActEvtArgs.Document.Name & _
                                  " was activated.")
    End Sub

### VBA/ActiveX Code Reference
    
    
    Private Sub AcadDocument_Activate()
        ' This example intercepts the Document Activate event.
     
        MsgBox ThisDrawing.Name & " was activated."
    End Sub
