<!-- Developer's Guide > API Developer's Guide > Sections Overview -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-18800A23-76CA-40DC-9B53-8E9CF2E12DD5.htm -->

# Sections Overview

The .NET API exposes classes and methods to access and create Sample Lines, Sections, and Section Views. Sample Lines are encapsulated by the SampleLine object, and related SampleLine objects are organized in a SampleLineGroup collection. SampleLineGroup objects are associated with Alignments.

Sections are the surfaces, corridor models, or pipe networks that intersect the vertical plane defined by a sample line. In the .NET API, these surfaces are represented by SectionSource objects. SectionSource objects are held in a SampleLineGroup's SectionSourceCollection.

Section Views are encapsulated by the SectionView object. A SectionView is associated with (and created from) a related SampleLine. The features shown in a section view are determined by the Sections sampled.
