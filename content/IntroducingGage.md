Title: Introducing GAGE
Date: 2014-11-30 12:00
Tags: Programming
Category: Blog
Slug: IntroGage
Author: David Farrell
Summary: Introducing GAGE

I've started development on a small game engine for experimenting, researching, and prototyping. I'm calling it GAGE,
short for the Great American Graphics Engine. It's a joke about how instead of writing the [the Great American
Novel](http://en.wikipedia.org/wiki/Great_American_Novel) I'm writing the Great American Graphics Engine. Alternatively,
I could have used the name 'DX11Testbed', but GAGE is shorter and has more panache.

The project is hosted [here on Github](http://github.com/nosferalatu/gage).

This project is meant to be an environment to quickly test out rendering ideas, not to be a full fledged game
engine. Currently it displays Crytek's Sponza model and has a compute shader based GPU particle simulation. The shader
generation and parameter management are some of the more interesting parts of the code.

### Build

To build GAGE, you need:

* the Visual Studio 2010 compiler (I want to upgrade this to at least 2012)
* the DirectX June 2010 SDK (I am using some D3DX functions to load textures)
* Python 2.7 (for the shader compiler)

Open `[project]\Build\gage.sln` and build. Press F5 in Visual Studio, or run `[project]\Build\Debug\gage.exe` or
`[project]\Build\Release\gage.exe`. The game will find the project root by searching backwards from the .exe for the
`.git` directory.

### Notes

You translate with WASD, and you rotate by mousing with the right mouse button down. You can also use a gamepad if it
supports XInput. Space will reload shaders, and you can pop the left gamestick to reset the camera. 

Lua is compiled in the engine, and more of the C++ code will be connected to Lua soon.

The shader generation system is an experiment with using Python as an effect file format, similar to [Lua as an effect
file format](http://prideout.net/blog/?p=1). The idea is to have a Python file sitting side-by-side the HLSL file,
where the Python file will specify the technique names, render state, sampler state, and other meta information about the
HLSL code. For an example, see `[project]\Shaders\Mesh.fx` and `[project]\Shaders\Mesh.py`.

The `ShaderCompiler` directory contains `sc.py` and `d3dcompiler.py`, which drive the shader generation. `sc.py` will
import the shader's .py file (e.g. `Mesh.py`) and look at that module's dictionary to extract the techniques and
samplers. It then calls `fxc.exe` to compile the technique's shaders, and writes out the data into a binary `.fxo`
file that is loaded by GAGE.

The `.fxo` data is relocatable, meaning that the C++ code loads it and patches its pointers in-place. The `blob` class
in sc.py manages writing relocatable data; the `FixupHeader` class in shader.cpp does the corresponding pointer fixup.

The code in `shadercompiler\d3dcompiler.py` uses Python's ctypes library to wrap around the D3D11 reflection
interface. I think that's fragile, especially the code in the Python class ID3D11ShaderReflection, which jumps through
hoops to call C++ vtable methods. It might be better to write a custom DLL in C++ that wraps around the D3D11 shader
reflection API rather than have Python do the C++ interop directly. Nevertheless, the current system works in just 591
lines of Python code.

There's a simple compute shader based GPU particle system which you can see in the center of the screenshot below.

![gage sponza]({filename}images/IntroGageSponza.jpg)
