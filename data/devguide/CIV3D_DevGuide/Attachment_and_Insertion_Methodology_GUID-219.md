<!-- Developer's Guide > API Developer's Guide > Creating Custom Subassemblies Using .NET > Designing Custom Subassemblies > Attachment and Insertion Methodology -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-219E43E2-9ECA-40B4-B454-CC2FB3C5F1AF.htm -->

# Attachment and Insertion Methodology

Most subassembly components have a single point of attachment and extend in one direction or the other from that point. However, there are some exceptions to this general rule.

The list below describes the attachment and insertion methodology for three categories of subassemblies: medians, components joining two roadways, and rehabilitation and overlay.

  * **Medians.** Medians tend to be inserted in both the left and right directions simultaneously about a centerline (which is not necessarily the corridor baseline alignment). Furthermore, the attachment point may not be a point on the median surface links. For example, the attachment point for a depressed median subassembly may be above the median ditch at the elevation of the inside edges-of-traveled-way.
  * **Components Joining Two Roadways.** When modeling separated roadways in a single corridor model, it is often necessary to insert intersection fill slopes, or to connect from one edge-of-roadway to another. Typically, you assemble the components for as much of the first roadway as possible, switch baselines and assemble the components for the second roadway, then use special subassemblies to connect between the two roadways. In this case, two attachment points are needed. Do this by creating a subassembly with a normal attachment point on one side, and which attaches to a previously defined marked point on the other.
  * **Rehabilitation and Overlay.** Typically, subassemblies that are used to strip pavement, level, and overlay existing roads are placed based on calculations involving the shape of the existing roadway section, rather than using a design centerline alignment and profile. For example, a pavement overlay subassembly may require a minimum vertical distance from the existing pavement for a given design slope. A lane-widening subassembly may need to attach to the existing edge-of-traveled-way and match the existing lane slope.
