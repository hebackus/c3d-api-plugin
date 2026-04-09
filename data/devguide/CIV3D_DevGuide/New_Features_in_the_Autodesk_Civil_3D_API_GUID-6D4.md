<!-- Developer's Guide > API Developer's Guide > About the Developer's Guide > New Features in the Autodesk Civil 3D API -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-6D41D043-4958-40B7-9C7E-45A6D780955B.htm -->

# New Features in the Autodesk Civil 3D API

##  .NET Changes in Autodesk Civil 3D 

This section covers changes to the Autodesk Civil 3D .NET API for Autodesk Civil 3D. 

### New in 2026.2

Updates to the API have been made in the following feature areas: 

Catchments

  * Exposed the Runoff method to Catchment .Net APIs 

Channels

  * Added Channel.ByFeatureLine to create a channel from a feature line. 
  * Added Channel.ByAlignmentProfile to create a channel from an alignment profile 
  * Added the ability to Choose Channel Section Type on creation. 

Ponds

  * Added new API classes for creating and editing ponds 
    * Pond 
    * PondContour 
    * PondContourCollection 
  * Added PondStyle and PondStyleCollection classes for managing pond styles. 

### New in 2026.1

Updates to the API have been made in the following feature areas: 

Alignments

  * Added SettingsTag.SettingsCreation and SettingsTag.SettingsRenumbering to automatically renumber alignment tags based on station order. 

Labels

  * Added LabelStyle.GetDescendantIds() and LabelStyleCollection.GetDescendantIds() to get the objectId collection of all descendant label style objects. 
  * Added the LabelBase.ApplicableLabelStyleIds property, allowing Label and LabelGroup objects to directly access their associated LabelStyleCollection. 

Model Viewer

  * Added ModelViewerSetObjects to specify a set of objects to display in the model viewer. 

Pressure Networks

  * Added PressurePart.GetPartSize() to get the part size used to create the pressure part. Null is returned if the part size cannot be found in the parts list. 
  * Added PressurePartSize.PartListId to get the ObjectId of the PressurePartList object that owns the part size. 
  * Added Part.GetPartSizeId() to get the ObjectId of the PartSize used to create the part. ObjectId.Null is returned if the part size cannot be found in the parts list set to the network. 

Surfaces

  * Added SurfaceOperation.Guid to retrieve the GUID of a surface operation. 
  * Added SurfaceOperationCollection.get(GUID) to retrieve an operation from the collection based on its GUID. 
  * Added a SurfaceOperationCollection.Remove(GUID) to remove an operation with a specified GUID from the collection. 

### New in 2026

Updates to the API have been made in the following feature areas: 

Rail design

  * Added API that gets the minimum distance between tracks of two alignments. [Learn more](<GUID-749BD054-DCAA-4D73-AB87-2BC7A8A7C8EB.htm>). 
    * Alignment.TrackDistanceToAlignment(double startStationOnThisAlignment, double endStationOnThisAlignment, double? gaugeForThisAlignment, ObjectId otherAlignmentId, double? gaugeForOtherAlignment, TrackDistanceCalculationMode trackDistanceCalculationMode) 
  * Added API that gets the distance between tracks of two alignments. [Learn more](<GUID-749BD054-DCAA-4D73-AB87-2BC7A8A7C8EB.htm>). 
    * Alignment.TrackDistanceToAlignment(double stationOnThisAlignment, double? gaugeForThisAlignment, ObjectId otherAlignmentId, double? gaugeForOtherAlignment, TrackDistanceCalculationMode trackDistanceCalculationMode). 
  * Added API that gets the distance between tracks of two alignments. [Learn more](<GUID-749BD054-DCAA-4D73-AB87-2BC7A8A7C8EB.htm>). 
    * Alignment.TrackDistanceToAlignment(List<double> stationListOnThisAlignment, double? gaugeForThisAlignment, ObjectId otherAlignmentId, double? gaugeForOtherAlignment, TrackDistanceCalculationMode trackDistanceCalculationMode). 
  * Added API that gets the station set according to the station type, intervals, and station range. 
    * Alignment.GetStationSet(StationTypes stationType, double majorInterval, double minorInterval, double startStation, double endStation). 

Surfaces

  * Added API that gets origination type which indicates the surface is created from a Corridor or Grading. 
    * Surface.OriginationType() 

Partial surface reference

  * Updated API Surface.Operations(). InvalidOperationException will be thrown when it is a referenced surface. 
  * Added API property bool to query if a current entity is a partial reference object. 
    * Entity.IsPartialReferenceObject 
Added API that creates a partial reference surface with a specified boundary in the host drawing according to the host database, source drawing file name, surface name, and boundary object ID. 
    * DataShortcuts.CreatePartialReferenceSurface(Database hostDrawing, String sourceDrawingFilename, String surfaceName, ObjectId refBoundaryId). 
  * Added API that updates a partial reference surface in the host database after editing (adds, deletes, or changes) the reference boundary. 
    * DataShortcuts.UpdatePartialReferenceSurface(Database hostDrawing, ObjectId refSurfaceId) 
  * Added API that creates a partial reference surface with a specified boundary in the host drawing according to the host database, source drawing file name, surface name, and boundary object ID. 
    * DataShortcuts.DataShortcutManager.CreatePartialReferenceSurface(int index, Database hostDrawing, ObjectId dRefBoundaryId) 
  * Added API that provides access to the manager for partial reference boundaries. 
    * Surface.PartialReferenceBoundaryManager() 
  * Added API that retrieves all reference boundary object IDs. 
    * SurfacePartialReferenceBoundaryMgr.ReferenceBoundaryIds() 
  * Added API that adds a reference boundary to the partial reference surface. 
    * SurfacePartialReferenceBoundaryMgr.AddBoundary(ObjectId refBoundaryId) 
  * Added API that deletes a reference boundary from the partial reference surface. 
    * SurfacePartialReferenceBoundaryMgr.DeleteBoundary(ObjectId refBoundaryId) 

Autodesk Construction Cloud

  * [ Data Shortcut APIs](<https://help.autodesk.com/view/CIV3D/2026/ENU/?guid=299173e1-d4f1-a572-539d-f800a22b7cd8>) are now available to Autodesk Construction Cloud workflows. This functionality requires access to [Autodesk Collaboration for Civil 3D](<https://beehive.autodesk.com/community/service/rest/cloudhelp/resource/cloudhelpchannel/guidcrossbook/?v=2026&p=CIV3D&l=ENU&accessmode=live&guid=GUID-6C3CD2CD-4ABC-4A33-A9FF-5EBD6E67A8CC>).
