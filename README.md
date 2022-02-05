# Map-Coloring-Visualization

A Python application which demonstrates the "domain reduction algorithim" for coloring a map of ajacent regions with a fixed number of colors such that no 
region shares colors wiith an ajacent region. This algorithim utilizes contraint propagaton upon each depth first search assignment (rotating color choice), 
propogating through various extents through the maps regions, reducing the domain of remaining viable color options for each region, and back-tracking when a
region among those concidered no longeer has no reminaing color options.  

This "domain reduction algorithim" was presented by Patrick Winston in his Artificial Itelligence course at MIT. 
[This lecture is avalible online via MIT OpenCourseWare](https://youtu.be/dARl_gGrS4o)


![](https://github.com/mcmoffat/Map-Coloring-Visualization/blob/main/mapColoringDemo.gif)
