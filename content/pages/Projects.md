Title: Projects
Date: 2019-12-29 12:00
Tags: Projects
Category: Blog
Slug: Projects
Author: David Farrell
Summary: Projects

These are some things I've worked on over the years:

### Medium (Adobe / 2020 )

Medium was acquired by Adobe at the end of 2019: [Adobe Acquisition](https://theblog.adobe.com/adobe-accelerates-3di-efforts-through-medium-acquisition/)

At Adobe, I work in the 3D&Immersive group, where I'm continuing to work on Medium and developing innovative sculpting and modeling software.

![test image]({static}../images/oculusmedium5.jpg)

![test image]({static}../images/oculusmedium4.jpg)

![test image]({static}../images/oculusmedium6.jpg)

### Medium (Oculus / 2016 )

[Oculus Medium](https://www.oculus.com/medium/) is a digital sculpting application that works with virtual reality headsets and 6DoF controllers to let you sculpt, model, paint, and create solid-feeling objects in a VR environment.

I led the graphics team at Facebook/Oculus that developed Medium from before the initial release to the Adobe acquisition. I made core contributions to Medium's sculpting technology, such as the SDF sparse data structures, the real-time stamp brushes, and the move tool, as well as the Vulkan rendering backend and Transvoxel renderer.
 
![test image]({static}../images/oculusmedium_orc.jpg)

![test image]({static}../images/oculusmedium2.jpg)

![test image]({static}../images/oculusmedium3.jpg)

### Headlander (Double Fine / 2016 / Windows, PS4, XBox One)

After Massive Chalice and through preproduction of Headlander, I worked as Double Fine's technical director to update the Buddha engine. We switched to LuaJIT, replaced Scaleform with an in-house UI library, and revised the level editing framework to combine in-game editing with a standalone Python/C++ app. The latter used a Redis database to arbitrate changes between users to allow concurrent editing. During Headlander's preproduction, I helped develop the post processing effects that gave Headlander its unique visual style.

![test image]({static}../images/headlander1.jpg)

![test image]({static}../images/headlander2.jpg)

![test image]({static}../images/headlander3.jpg)


### Massive Chalice (Double Fine / 2015 / Windows, XBox One)

Massive Chalice was a Kickstarter funded game. I contributed to the graphics and systems software, particularly the Windows and XBox One support. The game shipped on XBox One at 60 Hz at 1600x900 using a deferred renderer similar to Costume Quest 2's. 

![test image]({static}../images/massivechalice1.jpg)

![test image]({static}../images/massivechalice2.jpg)

![test image]({static}../images/massivechalice3.jpg)

### Costume Quest 2 (Double Fine / 2014 / Windows, OSX, Linux, PS4, XBox One, WiiU, PS3, XB360)

Costume Quest 2 shipped simultaneously on eight platforms. Much of the engineering schedule was devoted on platform work, but we were able to add a few nice features, such as deferred rendering using tiled lighting, where the light/tile intersections were found using [the projection of a sphere](http://jcgt.org/published/0002/02/05/). I wrote a bit about the deferred renderer on my blog.

![test image]({static}../images/costumequest2_1.jpg)

![test image]({static}../images/costumequest2_2.jpg)

![test image]({static}../images/costumequest2_3.jpg)

### My Alien Buddy (Double Fine and Japan Studios / PS4 / 2013)

Double Fine worked with Japan Studios in Tokyo to create this augmented reality experience. We contributed one room to The Playroom, which ships with every PS4. This project had many challenges; it was our first experience with the PS4, we were using Sony's engine, and we were working with a team many time zones away in Tokyo. The engine was particularly challenging for me as the sole programmer on the project, because although the code itself was in English, the comments were in Japanese (and I do not know Japanese). Nevertheless, in four months we developed many prototypes, made a simple level editor out of Unity which exported into Sony's engine, integrated Lua, added some rendering features such as instancing, and developed a mass/spring simulation for the alien's squishy skin.

![test image]({static}../images/myalienbuddy1.jpg)

![test image]({static}../images/myalienbuddy2.jpg)

![test image]({static}../images/myalienbuddy3.png)

### Steed (Double Fine / 2014 / Amnesia Fornight Prototype)

I was the lead programmer on this two week project and wrote the grass simulation and rendering. This heavily used geometry instancing and noise to randomly distribute and animate the grass blades. I switched the renderer from forward rendering to a deferred system to help deal with the overdraw, and developed a dynamic heightmap that the horse would render into so that you could leave trails in the grass.

![test image]({static}../images/steed1.png)

![test image]({static}../images/steed2.jpg)

![test image]({static}../images/steed3.jpg)

### The Cave (Double Fine / 2012 / Windows, WiiU, PS3, XB360)
My primary contribution to The Cave was working on the Windows and WiiU SKUs of the game.

![test image]({static}../images/thecave1.png)

![test image]({static}../images/thecave2.png)

![test image]({static}../images/thecave3.png)

### Black Lake (Double Fine / 2012 / Amnesia Fortnight Prototype)

For this two week Amnesia Fortnight prototype, I changed the Double Fine's hybrid forward/deferred renderer to correctly handle diffuse and specular color (and gamma correct, at that). This allowed the player to carry a lantern which illuminated a dark forest. I also wrote a system to procedurally animate thorns winding out of the ground, although in hindsight, the time constraints of the project were too short to fully develop that system.

![test image]({static}../images/blacklake1.jpg)

![test image]({static}../images/blacklake2.jpg)

![test image]({static}../images/blacklake3.jpg)

### PC Ports (Brutal Legend, Stacking, Iron Brigade, Costume Quest) (Double Fine / 2011-2012)

I ported several of Double Fine's back catalog of PS3/XB360 games to Windows and Steam. I used my knowledge of those consoles to adapt the Buddha engine to DX9 and Windows. Brutal Legend was enhanced to run at 60 Hz. \m/ 

![test image]({static}../images/brutallegend1.jpg)

![test image]({static}../images/brutallegend2.jpg)

![test image]({static}../images/brutallegend3.jpg)

### Kinect Party (Double Fine / 2012 / XB360)

I did a lot of optimization work to Kinect Party and a few shaders here and there. I wrote a dynamic heightmap simulation that ran on the XB360's GPU for the Bath Tub activity. The players' positions from the Kinect would intersect with the heightmap, causing ripples and waves in the water sim. I also added instancing, which was very useful in the Castle Builder and Voxel Runner activities.

![test image]({static}../images/kinectparty-bath.png)

![test image]({static}../images/kinectparty-castle.jpeg)

![test image]({static}../images/kinectparty-voxelrunner.jpg)

### Zombie Apocalypse (Nihilistic Software / 2009 / PS3, XB360)

This game reused the Conan engine and was a lot of fun. The biggest rendering feature of this game was the blood splatter on the ground, which we made by projecting particles into a deferred decal buffer.

![test image]({static}../images/zombieapocalypse-1.jpg)

![test image]({static}../images/zombieapocalypse-2.jpg)

![test image]({static}../images/zombieapocalypse-3.jpg)

### Conan (Nihilistic Software / 2007 / PS3, XB360)

Conan was Nihilistic's first PS3 and XB360 game. I played a core role in the team that wrote a new PS3/360 renderer for Nihilistic's engine, including a data driven shader pipeline, dynamic lighting, and an SPU job system. After Conan shipped, we refined the renderer to use the Cell's SPU's for a variety of work, such as deferred lighting (where the Cell would do the lighting and the RSX would do the shadow mapping) and geometry processing.

I added support for cheap static branches in the PS3's fragment shaders by using SPU's to scan the patched RSX microcode for branches using immediate values, pruning out blocks that the branch skipped, and replacing the branch instruction itself with a NOP. Although the RSX supported branching in fragment shaders, it was very slow, even when branching on an immediate value. This technique avoided the slow runtime branch, and was shared with Sony, who released a version of the technique in the PS3 SDK.

![test image]({static}../images/conan1.jpg)

![test image]({static}../images/conan2.jpg)

![test image]({static}../images/conan3.jpg)

### Demon Stone (Stormfront Studios / 2004 / PS2)

Demon Stone refined the PS2 engine developed for The Two Towers. I continued to write a lot of VU1 code, and implemented a neat notation to pack vertex data into various formats for the VIF/VU1 to unpack. I implemented compressed textures on the PS2 for this project by separating the high frequency luminance from the low frequency color and using the PS2's fast GS to blend them together.

![test image]({static}../images/demonstone0.jpg)

![test image]({static}../images/demonstone1.jpg)

![test image]({static}../images/demonstone2.jpg)

### Lord of the Rings: The Two Towers (Stormfront Studios / 2001 / PS2)

Looking back, we packed a lot of game into a PS2. Most challenging was the Battle of Helm's Deep at the end of the game, where up to 20 skinned characters were visible at a time, including their shadows. I was particulary happy with the shadows at the time, as they were implemented using a stencil shadow technique, even though the PS2 had no stencil hardware (but it could blend in add/subtract modes to a single color channel, which was enough). The silhouette edges of the shadows were computed on the VU0 which were then passed through the CPU to the VU1.

I wrote the VU1 microcode that performed the world and skinned character rendering. This included variants to do six plane clipping in VU1 code. I also wrote a high performance animation system using the CPU and VU0 running in parallel. The CPU would fetch data for the next bone from memory, and in parallel, the VU0 would calculate the previous bone's matrices.

![test image]({static}../images/lotr0.jpg)

![test image]({static}../images/lotr1.jpg)

![test image]({static}../images/lotr2.jpg)

### Rendition

A long time ago I worked at Rendition in their DirectX driver group. I learned a great deal about how to debug software and about how hardware works. 

![test image]({static}../images/v2200agp_fhq.jpg)

![test image]({static}../images/verite2100.jpg)

### Any Channel

My first game dev job. I moved to California and started writing games. Any Channel had their own proprietary, first person, software rendered game engine.

![test image]({static}../images/any_channel.jpg)

![test image]({static}../images/vigilance1.JPG)
