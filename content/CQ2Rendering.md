Title: Physically Based Deferred Rendering in Costume Quest 2
Date: 2014-9-24 12:00
Tags: Programming
Category: Blog
Slug: CQ2Rendering
Author: David Farrell
Summary: Rendering in Costume Quest 2
Status: draft

Developing the rendering tech for Double Fine's Costume Quest 2 was interesting because the game released simultaneously on eight platforms: XBox 360, PS3, WiiU, Windows, OSX, Linux, XBox One, and PS4. It uses Double Fine's proprietary 3D engine, Buddha, originally written for the XBox 360 and PS3 for the game Brutal Legend. We've extended Buddha and ported it to many new platforms since then.

The engineering schedule for CQ2 was taken up almost entirely with merging branches, resurrecting support for the old consoles, and bringing up the new consoles. Unfortunately, that left little more than two weeks of my time for look dev in preproduction. Fortunately, this was a sequel, so the game's art style was a known quantity. Unfortunately, the CQ2 design was more ambitious than the original Costume Quest, including levels in a swampy bayou in New Orleans and a dystopic future where an evil dentist has travelled through time to eradicate Halloween. Fortunately, we had very talented tech artists who nailed down the graphics requirements in preproduction so that we could make good use of those two weeks of look dev.

In that context, what changes did we make to the Buddha renderer for Costume Quest 2?

Physically Based Rendering
==========================

Physically based rendering in a Costume Quest universe? Isn't Costume Quest inspired more by a comic book art style and less by the physical constraints of the real world? Yes, but Costume Quest has two separate styles of rendering; the first is for the toon-shaded characters, and the second is for the more traditionally rendered world.

The first style of rendering is for the characters, which use a toon shader and a cel outline effect. That's not even vaguely physically based; if we had more graphics dev time on CQ2, I would have looked into developing an energy conserving toon shader effect. Instead, the toon shader is a simple 1D lookup texture based on the NdotL of a single light direction. That's also the same effect that was used in the original Costume Quest, and we didn't want to stray far from that established look.

The second style of rendering is for the rest of the world, which uses an energy conserving Blinn-Phong BRDF lit by a primary shadow-casting sunlight, additional point lights, and a hemisphere light for ambient lighting. All lighting was dynamic, except for some prebaked per-vertex ambient occlusion. The Blinn Phong BRDF was based on [Tri-Ace's work](http://renderwonk.com/publications/s2010-shading-course/gotanda/course_note_practical_implementation_at_triace.pdf). For the sake of speed, we dropped the Fresnel factor, which doesn't match the real world but doesn't break energy conservation. GGX is very popular now, but we continued to use Blinn-Phong as it was cheaper to compute.

There are two properties of physically based rendering that are very useful even for games that aren't set in the real world. One property is energy conservation, which is useful becauase lighting and materials can be created independently. That helps avoid the problem of having to rework the materials after you do a lighting pass and vice versa, and lets materials be reusable in different lighting conditions. Another useful property is that the range of values used by materials is better defined, which helps when packing values into a deferred renderer's gbuffer.

CQ2 strayed from realism in many ways but kept those two properties of physically based rendering. We dropped support for metallic materials; there's no support for a specular color vector, and the specular intensity scaler is capped at 0.1. This was done to fit into the small gbuffer. Many of our materials have no specular lighting at all and are purely diffuse with a specular intensity of 0.0, even though [everything is shiny](http://filmicgames.com/archives/547) in the real world. There's no change in lighting from the Fresnel effect, which doesn't match the real world, but doesn't break energy conservation and was cheaper on the GPU. Our point lights would have a color inside an inner radius and a different color inside an outer radius, and light in the real world doesn't change colors by itself. 

Deferred Rendering
==================

We faced many constraints when targeting so many platforms. We knew we wanted to support a large number of point lights, so a deferred renderer of some kind made sense. However, we also knew that we needed to run on the XBox 360 with its 10 MB of EDRAM, and we wanted to use as much of the same rendering code as possible. We chose a gbuffer format of two RGBA8888 render targets (plus the depth buffer) to fit in EDRAM and run well everywhere. This fit neatly into the 360's EDRAM (well, with a bit of adjustment to resolution), and also fit into the 32 MB ESRAM of the XBox One and WiiU.

One of the advantages of physically based rendering, as I mentioned above, is that the range of possible values for a material is better defined. Most materials are either metallic or dielectrics, which with some simplification can be summarized as this:

* Dielectrics (most non-metals) have a albedo color and monochromatic specular in the range (0.02, 0.08)
* Metals have no albedo color and a specular color value in (0.5, 1.0)

A minimal Blinn-Phong BRDF will use an albedo color, specular color, gloss scalar, and normal vector. That's 10 components, which would be tricky to fit into the smaller gbuffer format. And, actually, CQ2 also needed to store ambient occlusion and emissive values in the gbuffer, making it even more difficult to fit.

We looked at [Disney's principled BRDF](http://disney-animation.s3.amazonaws.com/library/s2012_pbs_disney_brdf_notes_v2.pdf) which uses a metallic texture to indicate whether a material is a dielectric or material. In the case of a dielectric, it uses the albedo color directly and a scalar specular intensity; for metals, it repurposes the albedo color as the specular color, and uses an all-black albedo for lighting. This is also used by [Unreal 4](https://docs.unrealengine.com/latest/INT/Engine/Rendering/Materials/PhysicallyBased/index.html). The metallic value helps a lot with packing values into a gbuffer because you no longer need to store a specular color in 3 components. A possible gbuffer layout would look like this:


```
albedo R         | albedo G        | albedo B        | metal
normal X         | normal Y        | spec. intensity | gloss
```

That's close, but we have nowhere to put the ambient occlusion and emissive value. The specular intensity certainly doesn't need eight bits, so we could stuff the emissive value into there, but we would still need to put the ambient occlusion somewhere (and we want it in its own channel so that we can splat the character drop shadows and SSAO into it).

As mentioned above, we decided to drop support for metallic materials. That meant that we could use the above laytout but drop the metal channel. That gets us to the layout we used for CQ2:

```
albedo R         | albedo G        | albedo B                   | ambient occlusion
normal X         | normal Y        | spec. intensity / emissive | gloss / cel shaded 
```

The ambient occlusion stored the per-vertex AO. Screen-space ambient occlusion also blended with this value, and the character drop shadows blended with it as well. Additionally, the character drop shadows would blend with the ambient occlusion channel.

The albedo had to be stored in gamma space as this was an eight bit per channel format. Our pipeline is gamma correct, meaning it does all lighting and blending in linear space, so we had to be sure to convert the albedo colors to sRGB before we wrote them to the framebuffer. Not all platforms had support for per-render-target sRGB writes, so this was done manually.

The specular intensity and emissive were packed together using four bits each. The specular intensity represented a value in the range [0, 0.1], and the emissive was in the range [0, 8].

The gloss (AKA gloss, or smoothness) was in the range [0, 2048] was stored in 7 bits, and we used the top bit to store the cel shaded bit.

