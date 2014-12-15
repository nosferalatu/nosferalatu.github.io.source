Title: Shader Generation
Date: 2014-11-19 12:00
Tags: Programming
Category: Blog
Slug: ShaderGeneration
Author: David Farrell
Summary: Shader Generation
Status: draft

Earlier this year, we decided to rewrite our shader generation system at Double Fine. This has been used in Massive Chalice, Costume Quest 2, and our Amnesia Fortnight projects. Its goals were to be as data driven as possible, emit correct error line numbers, and facilitate generation of many variants of the same shader.

The data flow looks like this: `(.fx, .fx.lua)` -> `ShaderCompiler.exe` -> `platform shader compiler` -> `.fxo`

* `.fx` files are written in standard HLSL
* `.fx.lua` files are written in Lua and specify shader metadata and a specialization function (the .fx and .fx.lua files correspond one-to-one to each other)
* `ShaderCompiler.exe` is the Double Fine shader generator program (it doesn't do any real compiling; it delegates that work to the platform shader compiler)
* `Platform shader compiler` is whatever shader compiler is used for the target platform, such as FXC.EXE for Windows
* `.fxo` files are loaded by the game

Here's a simple example of a shader that outputs a green triangle. The first block is an .fx file and the second is the corresponding .fx.lua file:

```cpp
float4 SimpleShaderVS(int vertexid : SV_VERTEXID) : SV_POSITION
{
    float4 pos[] = { {0,0,0,1}, {1,0,0,1}, {1,1,0,1} };
    return pos[vertexid];
}

float4 SimpleShaderPS()
{
    return float4(0,1,0,1);
}
```

```lua
local shader = Shader("MyNewSimpleShader")
shader.Technique.VertexShader = "SimpleShaderVS"
shader.Technique.PixelShader = "SimpleShaderPS"
```

Lua is used for offline shader generation and not used at runtime. Lua was our choice because of its easy interop with C code, its malleable nature to work as a data definition language, and that it was already deeply embedded in our existing C codebase. Lua is trivial to parse (just execute the Lua code!) and you have an expressive programming language at your fingertips. Many other languages, particularly dynamic languages such as Python, have similar properties and would also work well.

In this example, we can see how we set up render state to turn on alpha blending for the shader. The .fx file is the same, but the .fx.lua has changed:

```lua
local shader = Shader("MyNewSimpleShader")
shader.Technique.VertexShader = "SimpleShaderVS"
shader.Technique.PixelShader = "SimpleShaderPS"
shader.Technique.RenderState.AlphaBlendEnable = true
shader.Technique.RenderState.SrcBlend = BlendMode.SrcAlpha
shader.Technique.RenderState.DstBlend = BlendMode.InvSrcAlpha
```

### Shader Specialization

First, a few definitions of the terms we'll use below:

* `shader` means a collection of techniques and branches. This is what the game engine uses to associate a mesh with a shader
* `technique` means a vertex/pixel shader pair and render state. The word pipeline can also be used to describe a technique. A shader has 1 or more techniques (actually, 2^N, where N=the number of branches)
* `branch` means a boolean value that is evaluated either statically at shader generation time or dynamically by the GPU at runtime. These appear as global boolean parameters in the HLSL code

At runtime, the game sets which shader to use and sets the values of the branch booleans. The rendering code then uses the boolean values to select which technique in the shader should be used by the GPU.

In the example above, the shader code has exactly one technique because it has no branches. Here's an example of a shader that has one branch and outputs either green or blue:

```cpp
bool g_bOutputBlue;

float4 SimpleShaderVS(int vertexid : SV_VERTEXID) : SV_POSITION
{
    float4 pos[] = { {0,0,0,1}, {1,0,0,1}, {1,1,0,1} };
    return pos[vertexid];
}

float4 SimpleShaderPS()
{
    if (g_bOutputBlue)
        return float4(0,0,1,1);
    else
        return float4(0,1,0,1);
}
```

```lua
local shader = Shader("MyNewSimpleShader")
shader.Branches = { "g_bOutputBlue" }
shader.Specialize = function(permutation)
    local technique = Technique()
    technique.VertexShader = "SimpleShaderVS"
    technique.PixelShader = "SimpleShaderPS"

    return technique, permutation
end
```

The above .fx has one branch (g_bOutputBlue) and so it has 2^N = 2^1 = 2 different shader variants that are compiled. The first variant is compiled with g_bOutputBlue set to false, and the second variant has g_bOutputBlue set to true. We *specialize* the .fx shader code by substituting the text `g_bOutputBlue` for the text `true` or the text `false`, depending on which variant we are compiling, before we send that shader variant to the platform shader compiler.

If we want to evaluate the branch at runtime by the GPU, rather than at compile time, all we have to do is remove `g_bOutputBlue` from the list of branches in the .fx.lua file. The `g_bOutputBlue` stays with the shader as a global boolean parameter and becomes a runtime branch. This is very useful for experiments to determine if it's worthwhile to trade off memory and more shader program switches for a more specialized shader, or if the cost of shader specialization is too high. The code is also much easier to read than using C preprocessor macros and sprinkling lots of `#if LOTS_OF_CPP_DEFINE_TESTING` all over the place. It does rely on the platform shader compiler to do deadcode elimination, but that's true of all the compilers I've seen, even when their other optimization passes aren't as solid.

### Better Shader Specialization

A real life shader often has many branches, and 2^N different variants can quickly become prohibitively expensive. Often, though, shader variants can be combined together, or are mutually exclusive. We can specify a shader specialization function in Lua which, given a particular set of branch values, outputs a different set of branch values. This can mean the difference between millions of shader variants and only a few hundred.

The important thing to note is that for N boolean branches, we have 2^N permutations, each of which are mapped through the specialization function, which returns a (possibly different) permutation. We find the unique permutations from that set and send those to the platform-specific shader compiler.

Here's an example from Massive Chalice, where we have 14 different branches for our main mesh shader, but fewer actual variants:

```lua
local shader = Shader("RenderMesh")
shader.Branches = {
    "g_bBinaryAlpha",
    "g_bBloom",
    "g_bDebug",
    "g_bDepth",
    "g_bDepthAsColor",
    "g_bMultiLayer",
    "g_bFoliage",
    "g_bForwardLighting",
    "g_bShadowCast",
    "g_bShadowCastDepthAsColor",
    "g_bShadowRec",
    "g_bShadowProjected",
    "g_bSkinning",
    "g_bTransparent",
}
shader.Specialize = function(permutation)
    local specializedtechnique = Technique()
    specializedtechnique.VertexShader = "RenderMeshVS"
    specializedtechnique.PixelShader = "RenderMeshPS"
    specializedtechnique.RenderState = DefaultRenderState

    if permutation.g_bSkinning then
        permutation.g_bFoliage = false
    end

    if permutation.g_bFoliage then
        permutation.g_bMultiLayer = false
    end

    -- only RENDERER_DX9 uses DepthAsColor/ShadowCastDepthAsColor. Other platforms use Depth/ShadowCast.
    if not RENDERER_DX9 then
        permutation.g_bDepth = permutation.g_bDepth or permutation.g_bDepthAsColor
        permutation.g_bDepthAsColor = false
        permutation.g_bShadowCast = permutation.g_bShadowCast or permutation.g_bShadowCastDepthAsColor
        permutation.g_bShadowCastDepthAsColor = false
    end
    
    if permutation.g_bDepth or permutation.g_bDepthAsColor then
        specializedtechnique.VertexShader = "RenderMeshVSDepth"
        specializedtechnique.PixelShader = "RenderMeshPSDepth"

        permutation.g_bShadowCast = false
        permutation.g_bShadowCastDepthAsColor = false
        permutation.g_bBloom = false
        permutation.g_bMultiLayer = false
        permutation.g_bForwardLighting = false
        permutation.g_bShadowRec = false
        permutation.g_bTransparent = false

        if not permutation.g_bDepthAsColor then
            specializedtechnique.RenderState.ColorWriteState = ColorWriteState.____
        end
    elseif permutation.g_bShadowCast or permutation.g_bShadowCastDepthAsColor then
        specializedtechnique.VertexShader = "RenderMeshVSDepth"
        specializedtechnique.PixelShader = "RenderMeshPSDepth"

        permutation.g_bDepth = false
        permutation.g_bDepthAsColor = false
        permutation.g_bBloom = false
        permutation.g_bMultiLayer = false
        permutation.g_bForwardLighting = false
        permutation.g_bShadowRec = false
        permutation.g_bTransparent = false
		permutation.g_bShadowProjected = false

        if not permutation.g_bShadowCastDepthAsColor then
            specializedtechnique.RenderState.ColorWriteState = ColorWriteState.____
        end
    else
        permutation.g_bShadowCast = false
        permutation.g_bShadowCastDepthAsColor = false
        permutation.g_bDepth = false
        permutation.g_bDepthAsColor = false

        if permutation.g_bTransparent then
            specializedtechnique.RenderState = AlphaBlendRenderState
            permutation.g_bForwardLighting = true
        else
            permutation.g_bForwardLighting = false
        end
    end

	if permutation.g_bSkinning then
		specializedtechnique.VertexFormat = "kVERTTYPE_Skin_Compact"
	end

    return specializedtechnique, permutation
end
```

When rendering depth-only passes, such as to shadow maps, we can disable (set to false) many of the shader branches such as `g_bBloom`, `g_bMultiLayer`, etc. Similarly, when rendering lit passes, we can disable `g_bDepth`, `g_bShadowCast`, etc. When rendering transparent passes, we can enable the forward lighting branch.

The `Specialize()` function returns a Technique, so it can customize the shader stages to use, the render state, etc. It also returns a modified set of branch values, which are later substituted into the HLSL source code.

The platform shader compilation proceeds in this order:

- Run the Specialize() function to get all the techniques
- Find the unique set of vertex and pixel shaders from those techniques
- For each vertex and pixel shader:
    - Run the C preprocessor over the HLSL code
    - Substitute that technique's branch values into the preprocessed HLSL code
    - Call the platform shader compiler on that preprocessed, specialized code
- Gather the results and package everything into a .fxo file

When we look at calling the platform shader compiler as a pure function: `fn(preprocessed/specialized HLSL, compiler and dll's) -> shader binary` we can cache the results of shader compilation. 

A pure function is a function that, given an input, always produces the same output. It has no side effects and no external state. The above Specialize() function should be a pure function.

### Runtime

At runtime, we set the branch values:

```
pRenderContext->SetShaderBool(g_bShadowCast, false);
pRenderContext->SetShaderBool(g_bSkinning, mesh->has_skinning_data());
...
```

Then we set the shader and draw:

```
pRenderContext->SetShader(MeshShader);
pRenderContext->Draw(mesh);
```

When we draw a mesh, we use the state of the boolean branch values to construct an index into an array of techniques for that shader. Each branch gets one bit in the index. The techniques can be stored as an array for fast lookup but at the cost of more memory, or you can put the techniques into a hash table where the key=index and value=technique, or whatever scheme you want. We look up that technique, set its render state, its shaders, and finally issue the draw calls for the mesh.

### Locking Lua down

Although Lua is easy to use to define data, you need to do some extra work to enforce that tables contain only valid values. For example, the Shader.Technique.RenderState table only has fields for render state that we support, and new entries in that table aren't allowed. When you assign a value to one of the entries in the table, we make sure that value is valid (so you can only assign true/false to AlphaBlendEnable, and not assign true/false to AlphaBlendFunc).

We can use Lua's metatables to manage access to the table. Here's some code to create read-only enums:

```lua
-- Redefine pairs() and ipairs() to call the metatable's __pairs/__ipairs function, if they exist
-- By default, pairs/ipairs will not call the metatable's __index field, which doesn't work with
-- our controlled-access tables.
rawpairs, rawipairs = pairs, ipairs
function pairs(t)
  local mt=getmetatable(t)
  return (mt and mt.__pairs or rawpairs)(t)
end
function ipairs(t)
  local mt=getmetatable(t)
  return (mt and mt.__ipairs or rawipairs)(t)
end

-- Return a read-only enum. Keys can be read, but neither created nor changed. The keys and values are both strings.
-- The input should be a table of strings, one for each enum type.
function ReadOnlyEnum(table)
    for k,v in pairs(table) do if type(v) ~= "string" then error ("Enum entries must be strings in quotes", 2) end end

    local __table = {}
    for k,v in pairs(table) do __table[v] = v end

    local newtable_mt = {}
	newtable_mt.__newindex = function(t,k,v) error("Attempt to modify an enum", 2) end
	newtable_mt.__index = function(t,k) if getmetatable(t).__table[k] ~= nil then return getmetatable(t).__table[k] else error("Unknown enum value '" .. tostring(k) .. "'", 2) end end
    newtable_mt.__pairs = function(t) return pairs(getmetatable(t).__table) end
    newtable_mt.__ipairs = function(t) return ipairs(getmetatable(t).__table) end
    newtable_mt.__table = __table

	local newtable = {}
	setmetatable(newtable, newtable_mt)
	return newtable
end
```

The above function can be used like this:

```lua
FillMode = ReadOnlyEnum
{
    "Solid",
    "Wireframe"
}

CullMode = ReadOnlyEnum
{
    "CW",
    "CCW",
    "None"
}

ComparisonFunc = ReadOnlyEnum
{
    "Never",
    "Less",
    "Equal",
    "LEqual",
    "Greater",
    "NotEqual",
    "GEqual",
    "Always"
}
```

### C Preprocessor

It's worth pointing out that we use [mcpp](http://mcpp.sourceforge.net/) to preprocess the shaders. 