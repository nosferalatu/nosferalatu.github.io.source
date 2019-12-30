Title: Sculpting And Simulations with 6DoF Controllers
Date: 2019-12-30 14:00
Tags: Programming, OculusMedium
Category: Blog
Slug: SculptingAndSimulations
Author: David Farrell
Summary: Tech talk about sculpting, simulations, and 6DoF controllers
<IMG src="https://user-images.githubusercontent.com/6667377/55200209-5d055000-517a-11e9-8f6d-476a58e19509.gif">

At VRDC 2019 I gave the talk "Sculpting and Simulations with 6DoF Controllers". The talk covers using 6DoF controllers to guide mesh deformation in Oculus Medium and using Kelvinlets in a lightweight physically based simulation. Topics include representing a controller's position and orientation as a rigid translation and a displacement gradient tensor, using that representation to feed a Kelvinlets simulation, and using adaptive integrators to efficiently deform a mesh's vertices.

The slides are available here (be sure to read the speaker notes!):

[Sculpting And Simulations Slides](https://github.com/fbsamples/sculpting-and-simulations-sample/releases/latest/download/SculptingAndSimulations.pptx)

Additional notes that didn't make it into the presentation can be found at:

[ODE Solvers](https://github.com/fbsamples/sculpting-and-simulations-sample/blob/master/NotesOnODESolvers.pdf?raw=true)

[Calibrating Kelvinlets](https://github.com/fbsamples/sculpting-and-simulations-sample/blob/master/KelvinletsCalibration.pdf?raw=true)

Sample source code was released by Facebook/Oculus under the BSD license to supplement the talk. The sample code shows how to deform meshes using regularized Kelvinlets as well as with affine transformations. It compiles in both C++ and GLSL and consists of only header files. The code is available at the fbsamples Github site:

[Sculpting And Simulations Sample](https://github.com/fbsamples/sculpting-and-simulations-sample)


