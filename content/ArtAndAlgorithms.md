Title: Art+Algorithms
Date: 2019-12-30 12:00
Tags: Programming, OculusMedium
Category: Blog
Slug: Art+Algorithms
Author: David Farrell
Summary: Art+Algorithms: Developing Oculus Medium in VR
I spoke at Oculus Connect 4 about how we use VR in the development of Oculus Medium. I demonstrated several of our debugging visualizations that become very powerful when combined with VR manipulation. This works well for the same reason that sculpting in VR works so well: each hand can control a 3D transformation, and your head can also control a 3D transformation. This enables you to manipulate 3D objects and visualizations more quickly then with a keyboard, mouse, and 2D monitor.

Much of this presentation was delivered from within a VR headset. I modified Medium so that there was a camera object in VR that I could place in the scene and point at me. The image from that camera object was then mirrored on a desktop window, which could be seen by the audience. That was a much more pleasant experience for the audience than watching a shaky first-person point of view. Also, I placed the camera object in the headset roughly where the audience was, so I knew which direction to look at while in VR.

In hindsight, we don't take advantage of the Studio Share (networked connection of two Medium instances) feature for development as much as I thought we would. All of our debugging visualizations work over Studio Share, but there's still quite a bit of friction to jump into VR and establish a Studio Share connection. Still, it is used from time to time; for example, Medium's UI system can be hot reloaded, and two developers can quickly develop and critique UI by editing files from within a Studio Share session.

<iframe width="560" height="315" src="https://www.youtube.com/embed/oXtspak9aVU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
