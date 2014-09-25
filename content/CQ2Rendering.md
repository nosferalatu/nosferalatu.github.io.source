Title: Physically Based Deferred Rendering in Costume Quest 2
Date: 2014-9-24 12:00
Tags: Programming
Category: Blog
Slug: CQ2Rendering
Author: David Farrell
Summary: Rendering in Costume Quest 2
Status: draft

Developing the rendering tech for Double Fine's Costume Quest 2 was interesting because the game released simultaneously on eight platforms: XBox 360, PS3, WiiU, Windows, OSX, Linux, XBox One, and PS4. It uses Double Fine's proprietary 3D engine, Buddha, originally written for the XBox 360 and PS3 for the game Brutal Legend. We've extended Buddha and ported it to many new platforms since then.

I wouldn't recommend anyone try to release on eight platforms simultaneously. Think carefully about the costs of porting to additional platforms, especially if that work is concurrent with the game's development. Consider the cost of either creating different assets for different platforms or the cost of loss of game quality because you have to create your assets for the lowest common denominator.

Back To The Future
==================

At the beginning of Costume Quest 2 (CQ2) development, the programmers at Double Fine looked at the state of the Buddha engine. Our main branch was running on Windows (DX9 and OpenGL 2.1), and with some work, could build for OSX and Linux. Although Buddha was originally written for XBox 360 and PS3 and that code still existed in the mainline branch, those platforms hadn't been run in over a year and suffered greatly from bitrot. We had ported Buddha to WiiU for The Cave, but that code was sitting in a separate WiiU-specific branch. Finally, we weren't running 64-bit or on DirectX 11, much less on the XBox One and PS4.

The engineering schedule for CQ2 was taken up almost entirely with merging branches, resurrecting the old consoles, and bringing up the new consoles. Unfortunately, I could only spend about two weeks of time for look dev in preproduction. Fortunately, this was a sequel, so the game's art style was a known quantity. Unfortunately, the CQ2 design was more ambitious than the original Costume Quest, including levels in a swampy bayou in New Orleans and a Blade Runner inspired dystopic future. Fortunately, we had very talented tech artists who nailed down the graphics requirements in preproduction so that we could make good use of those two weeks of look dev.

In that context, how did we design rendering on Costume Quest 2 to look good across so many platforms and maximize productivity for the artists?

Physically Based Rendering
==========================

Physically based rendering in a Costume Quest universe? Isn't Costume Quest inspired more by a comic book art style and less by the physical constraints of the real world? Costume Quest has two separate styles of rendering. The first is for the toon-shaded characters, and the second is for the more traditionally rendered world.

The first style of rendering is for the characters, which use a toon shader and a cel outline effect. That's not even vaguely physically based; if we had more graphics dev time on CQ2, I would have looked into developing an energy conserving toon shader effect. Instead, the toon shader is a simple 1D lookup texture based on the NdotL of a single light direction. 

The second style of rendering is for the rest of the world, which uses an energy conserving Blinn-Phong BRDF lit by a primary shadow-casting sunlight, additional point lights, and a hemisphere light for ambient lighting. All lighting was dynamic, except for some prebaked per-vertex ambient occlusion.

The energy conserving Blinn-Phong BRDF was based on Tri-Ace's work.

We had already switched to phsyically based rendering for Massive Chalice, but Costume Quest 2 was the first project that's shipped with the tech. Artists didn't like it at first, but they like it now. 

Deferred Rendering
==================

The small gbuffer

Used physically based material constraints to fit needed material attributes into gbuffer
No metals, so no need for specular color. Specular reflectance was a scalar value in the range [0, .08]
Lots of emissive (AKA incandescence) was a scalar [0, 8] value which scaled the albedo color and used it as a self-illuminating light

Vertex AO, mixed with SSAO, and drop shadow AO

Decals blend with albedo

Two channel gbuffer layout:
```
albedo R             | albedo G             | albedo B                     | ambient occlusion
normal X             | normal Y             | spec. reflectance / emissive | roughness / cel shaded 
```

The ambient occlusion stored the per-vertex AO. Screen-space ambient occlusion also blended with this value. Additionally, the character drop shadows would blend with the ambient occlusion channel.

The albedo was stored in gamma space. Our pipeline is gamma correct, meaning it does all lighting and blending in linear space. The geometry pass uses sRGB albedo textures, uses linear per-vertex colors, and so forth to blend in linear space; therefore, we had to convert those linear albedo values to gamma space so that we could store in an eight-bit-per-channel render target without banding.

The specular reflectance and emissive were packed together using four bits each. The specular reflectance represented a value in the range [0, 0.08], so we rescaled that value to [0, 1], applied a curve (a square root) to get more precision in the low end, and stored it in he gbuffer using four bits. The emissive was prepared similarly; it had a range [0,  8], which we scaled to [0,  1], applied a square-root curve, and stored in four bits.

The roughness (AKA gloss) was in the range [0, 2048], so we took the exp2 and divided by N to get into the [0, 1] range. We stored the roughness in 7 bits, and used the top bit to store the cel shaded bit. Characters were considered cel shaded, but the world geometry was not.

