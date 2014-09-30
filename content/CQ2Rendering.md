Title: Physically Based Deferred Rendering in Costume Quest 2
Date: 2014-9-24 12:00
Tags: Programming
Category: Blog
Slug: CQ2Rendering
Author: David Farrell
Summary: Rendering in Costume Quest 2
Status: draft

Developing the rendering tech for Double Fine's Costume Quest 2 was interesting because the game was developed in less than a year and released simultaneously on eight platforms: PS4, XBox One, PS3, XBox 360, WiiU, Windows, OSX, and Linux. It used Double Fine's proprietary game engine, named Buddha.

Much of the engineering schedule for Costume Quest 2 (CQ2) was taken up with resurrecting support for the old consoles and and bringing up the engine on new consoles. Unfortunately, that left little time for look dev in preproduction. Fortunately, CQ2 was a sequel, so the game's art style was a known quantity. Unfortunately, the CQ2 design was more ambitious than the original Costume Quest, including levels in a swampy bayou in New Orleans and a dystopic future where you have to save Halloween from an evil time-travelling dentist.

We knew we could use the old graphics tech from the original game, but of course, we wanted to improve on the past and do a bit better. However, we also knew we had to scale from last gen consoles all the way up to modern consoles and modern desktop PC's.

### Physically Based Rendering

You might be wondering how physically based rendering applies to the Costume Quest universe, since Costume Quest's aesthetics are inspired more by a comic book art style than the physical constraints of the real world. Actually, the game has two separate styles of rendering; the first is for the toon-shaded characters, and the second is for the more traditionally rendered world.

The first style of rendering is for the characters, which use a toon shader and a cel outline effect. That's not even vaguely physically based; if we had more graphics dev time on CQ2, I would have looked into developing an energy conserving toon shader effect. Instead, the toon shader is a simple 1D lookup texture based on the NdotL of a single light direction. That's also the same effect that was used in the original Costume Quest.

The second style of rendering is for the rest of the world, which uses an energy conserving Blinn-Phong BRDF lit by a primary shadow-casting sunlight, additional point lights, and a hemisphere light for ambient lighting. All lighting was dynamic, except for prebaked per-vertex ambient occlusion. The Blinn Phong BRDF was based on [Tri-Ace's work](http://renderwonk.com/publications/s2010-shading-course/gotanda/course_note_practical_implementation_at_triace.pdf). We dropped the Fresnel factor, which doesn't match the real world but doesn't break energy conservation. The Fresnel effect didn't fit the art style, and it was a bit cheaper to drop the calculation.

There are two aspects of physically based rendering which are very useful even for games that use nonphotorealistic materials. One aspect is energy conservation, meaning that a surface emits no more light than it receives. This is important because you want materials that work independently of the lighting environment and avoid the production problem of reworking materials after you do a lighting pass and vice versa. When renderers don't obey energy conservation, such as with unnormalized Blinn-Phong, you often have to manually adjust the specular color, gloss, and perhaps other ad-hoc factors whenever the lighting changes. Another useful aspect of physically based rendering is that it produces more consistent results by following a few constraints. The number and range of material attributes is better defined, which helped us reason about about which values were important to Costume Quest 2 and how best to pack them into a deferred renderer's gbuffer.

CQ2 strayed from realism in many ways but kept those two aspects of physically based rendering. For instance:

* We removed support for metallic materials. There's no support for a specular color vector, and the specular intensity scalar is in the range [0.0, 0.1]. This was done to fit into the small gbuffer, and there are few metals in the CQ2 universe.
* Even though [everything is shiny](http://filmicgames.com/archives/547) in the real world, many of the materials are purely diffuse with a specular intensity value of 0.0. 
* We removed the Fresnel effect, which doesn't match the real world, but isn't necessary for energy conservation. The effect looked out of place with CQ2's aesthetics and was slightly cheaper to compute.
* Our point lights used a color inside an inner radius and a different color inside an outer radius, which isn't possible in the real world, but the important aspect of energy conservation (basically, that the light exiting a surface is less than or equal to the light illuminating the surface) was still maintained.

### Deferred Rendering

We faced many constraints when targeting so many platforms. We knew we wanted to support a large number of point lights, so a deferred renderer of some kind made sense. However, we also knew that we needed to run on the XBox 360 with its 10 MB of EDRAM, and we wanted to use as much of the same rendering code as possible. We chose a gbuffer format of two RGBA8888 render targets (plus the depth buffer) to fit in EDRAM and run well everywhere. This fit neatly into the 360's EDRAM (well, with a bit of adjustment to resolution), and also fit into the 32 MB ESRAM of the XBox One.

One of the advantages of physically based rendering, as I mentioned above, is that materials produce more consistent results by following a few constraints. Most materials are either metallic or dielectrics, and with some simplification, the constraints can be summarized as this:

* Non-metals (dielectrics) have an albedo color and monochromatic specular in the range (0.02, 0.08)
* Metals have no albedo color and a specular color value in (0.5, 1.0)

A minimal Blinn-Phong BRDF will use an albedo color, specular color, gloss scalar, and normal vector. That's 10 components, which would be tricky to fit into the smaller gbuffer format. CQ2 additionally needed to store ambient occlusion and emissive values in the gbuffer, making it even more difficult to fit.

The paper [Physically Based Shading at Disney](http://disney-animation.s3.amazonaws.com/library/s2012_pbs_disney_brdf_notes_v2.pdf) is interesting because it takes advantage of the constraints of physically based materials. They use a metallic texture to indicate whether a material is a dielectric or metal; in the case of a dielectric, they use the albedo color directly along with a scalar specular intensity, and for metals, they repurpose the albedo color as the specular color and use an all-black albedo for lighting. A similar technique is also used by [Unreal 4](https://docs.unrealengine.com/latest/INT/Engine/Rendering/Materials/PhysicallyBased/index.html). The metallic value helps a lot with packing values into a gbuffer because you no longer need to store a specular color in 3 components. A possible gbuffer layout would look like this:


```
albedo R         | albedo G        | albedo B        | metal
normal X         | normal Y        | spec. intensity | gloss
```

That's close to what we want with Costume Quest 2, but we have nowhere to put the ambient occlusion and emissive value. As mentioned above, we decided to drop support for metallic materials. We don't need the metal component, but it's also useful to remember the specular intensity for dielectrics is in the range [0.0,0.1] and doesn't need much precision. We pack the specular intensity with the emissive, and place the ambient occlusion into a separate channel.

That gets us to the layout we used for CQ2:

```
albedo R         | albedo G        | albedo B                   | ambient occlusion
normal X         | normal Y        | spec. intensity / emissive | gloss / cel shaded 
```

The ambient occlusion stored the per-vertex AO. This needed to be in its own channel (not packed with anything else) because screen-space ambient occlusion blended with this value. Additionally, the character drop shadows would blend with the ambient occlusion channel.

The albedo had to be stored in gamma space as this was an eight bit per channel format. Our pipeline is gamma correct, meaning it does all lighting and blending in linear space, so we had to be sure to convert the albedo colors to sRGB before we wrote them to the framebuffer. Not all platforms had support for per-render-target sRGB writes, so this was done manually.

The specular intensity and emissive were packed together using four bits each. The specular intensity represented a value in the range [0, 0.1], and the emissive was in the range [0, 8].

The gloss (AKA roughness, or smoothness) was in the range [0, 2048] and stored in 7 bits, and we used the top bit to store the cel shaded bit.
