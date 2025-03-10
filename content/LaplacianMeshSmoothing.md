Title: Laplacian Mesh Smoothing by Throwing Vertices
Date: 2025-3-9 21:00
Tags: Programming
Category: Blog
Slug: LaplacianMeshSmoothing
Author: David Farrell
Summary: Laplacian Mesh Smoothing by Throwing Vertices

In this blog post, I'll talk about smoothing and blurring 3D meshes using Laplacian mesh smoothing. A good example of where this is useful is Adobe Substance 3D Modeler's [smooth tool](https://helpx.adobe.com/substance-3d-modeler/create-with-clay/tools/smooth-tool.html) which I implemented using Laplacian mesh smoothing. Laplacian mesh smoothing works by iteratively shifting each vertex towards the average position of that vertex's neighbors. The math formula for this is:

$$v_i = \frac{1}{N} \sum_{j=1}^{N} v_j$$

which we can implement in code as:

```cpp
for (const Vertex& vertex : mesh.vertices)
{
    vec3 avrgPosition = vec3(0);
    for (const Vertex& vertexNeighbor : neighbors(vertex))
    {
        avrgPosition += vertexNeighbor;
    }
    avrgPosition /= numNeighbors(vertex);
}
```

Run that a few times, and the mesh smooths out like magic. It's important to note that this process only changes the vertex data of the mesh; the connectivity (triangle indices) are unchanged.

The above is straightforward except that we need the `neighbors()` and `numNeighbors()` functions. While one approach is to build a half-edge mesh data structure, which gives us information about the connectivity of the mesh, this blog post will show two alternative methods that can be used when the mesh is two-manifold (where each edge connects exactly two triangles).

### The One Pass Trick: Throwing Vertices

Forget about neighbor lookups. Instead, we'll iterate over the triangle faces directly, leveraging the fact that every edge in a two-manifold mesh connects exactly two triangles. Instead of precomputing neighbors, we accumulate neighbor positions on the fly in a single pass over the faces.

This process is often called _throwing vertices_, a term used in libraries like libigl. It refers to accumulating vertex positions at their connected neighbors and then averaging them. For a triangle formed by vertices A, B, and C, we define three directed half-edges: `A->B`, `B->C`, and `C->A`. As we traverse these half-edges, we accumulate the source vertex position at the destination vertex position and count how many times each vertex gets updated. This effectively computes the sum of all neighboring vertex positions for each vertex. Once we have this sum, we divide by the count to get the new, smoothed position.

Here's the implementation:

```cpp
std::vector<vec3> accumulated(mesh.vertices.size(), 0);
std::vector<int> numNeighbors(mesh.vertices.size(), 0);

for (const auto& triangle : mesh.triangles)
{
    int vertexIndex0 = triangle.index0;
    int vertexIndex1 = triangle.index1;
    int vertexIndex2 = triangle.index2;

    // vertexIndex0 -> vertexIndex1
    accumulated[vertexIndex1] += mesh.vertices[vertexIndex0];
    numNeighbors[vertexIndex1]++;

    // vertexIndex1 -> vertexIndex2
    accumulated[vertexIndex2] += mesh.vertices[vertexIndex1];
    numNeighbors[vertexIndex2]++;
    
    // vertexIndex2 -> vertexIndex0
    accumulated[vertexIndex0] += mesh.vertices[vertexIndex2];
    numNeighbors[vertexIndex0]++;
}

for (int i=0; i<mesh.vertices.size(); i++)
{
    mesh.vertices[i] = accumulated[i] / numNeighbors[i];
}
```

And there you go: a Laplacian smoothing pass without needing to precompute any data, or create a half-edge data structure.

If you want to make the mesh smoother, just apply more passes of the above. And if you want to slow down the smoothing process, just use a fractional pass:

```cpp
mesh.vertices[i] = lerp(mesh.vertices[i], accumulated[i]/numNeighbors[i], fractionalAmount);
```

This method is simple and effective.

### Squeezing Out Performance with Parallelism

The above approach works well in single threaded scenarios but doesn't work in multithreading code or on GPUs. The problem is the simultaneous writes to the `accumulated` and `numNeighbors` arrays by different threads.  This falls into the problematic category of mutable, shared data. For example, if different threads process separate triangles, they may concurrently modify the same vertex shared by those triangles.

#### Atomic Mayhem: Things Get MESI

```cpp
std::vector<std::atomic<vec3>> accumulated(mesh.vertices.size());
std::vector<std::atomic<int>> numNeighbors(mesh.vertices.size());
```

This works to allow multiple threads to run the smoothing code in parallel. However, atomic operations aren't free, and cache contention will slow this down on both CPUs and GPUs. In my own tests on CPUs, I've found that using this with multiple threads is slower than the single-threaded non-atomic version. That may or may not apply to your case, so please profile your situation before/after you try this.

#### A Cleaner Way: Precompute Neighbors

A better solution is to precompute the neighbor list once and reuse it across multiple smoothing passes. That looks like this:

```cpp
// Find the number of neighbors of each vertex
std::vector<int> numNeighbors(mesh.vertices.size(), 0);
int totalNeighbors = 0;

for (const auto& triangle : mesh.triangles)
{
    numNeighbors[triangle.index0]++;
    numNeighbors[triangle.index1]++;
    numNeighbors[triangle.index2]++;
    totalNeighbors += 3;
}

// Prefix sum
std::vector<int> neighborsStartIndex(mesh.vertices.size(), 0);
int currentIndex = 0;

for (int i=0; i<numNeighbors.size(); i++)
{
    neighborsStartIndex[i] = currentIndex;
    currentIndex += numNeighbors[i];
}

// Populate the neighbors array
std::vector<int> neighbors(totalNeighbors, 0);
std::fill(numNeighbors.begin(), numNeighbors.end(), 0);

for (const auto& triangle : mesh.triangles)
{
    // vertexIndex0 -> vertexIndex1
    neighbors[neighborsStartIndex[triangle.index1] + numNeighbors[triangle.index1]] = triangle.index0;
    numNeighbors[triangle.index1]++;

    // vertexIndex1 -> vertexIndex2
    neighbors[neighborsStartIndex[triangle.index2] + numNeighbors[triangle.index2]] = triangle.index1;
    numNeighbors[triangle.index2]++;

    // vertexIndex2 -> vertexIndex0
    neighbors[neighborsStartIndex[triangle.index0] + numNeighbors[triangle.index0]] = triangle.index2;
    numNeighbors[triangle.index0]++;
}
```

With this, a smoothing pass can process each vertex in parallel.

```cpp

std::vector<vec3> result(mesh.vertices.size(), 0);

// this for() loop can now operate on each vertex in parallel;
// the result[] array holds the new mesh vertices
for (int i=0; i<mesh.vertices.size(); i++)
{
    for (int j=0; j<numNeighbors[i]; j++)
    {
        int neighborIndex = neighbors[neighborStartIndex[i] + j];
        result[i] += mesh.vertices[neighborIndex] / numNeighbors[i];
    }
}
```

Once the `neighbors` and `numNeighbors` list is built, we never have to touch it again.

### Vertex Normals

Once the vertices are smoothed, vertex normals will need to be recomputed. That can be done with the same trick: iterate over faces, compute the face normal, and throw to that face's vertices.

```cpp
std::vector<vec3> accumulated(mesh.vertices.size(), 0);

for (const auto& triangle : mesh.triangles)
{
    vec3 v0 = mesh.vertices[triangles.index0];
    vec3 v1 = mesh.vertices[triangles.index1];
    vec3 v2 = mesh.vertices[triangles.index2];
    vec3 faceNormal = normalize(cross(v1-v0, v2-v0));

    accumulated[triangles.index0] += faceNormal;
    numNeighbors[triangles.index0]++;

    accumulated[triangles.index1] += faceNormal;
    numNeighbors[triangles.index1]++;

    accumulated[triangles.index2] += faceNormal;
    numNeighbors[triangles.index2]++;
}

for (int i=0; i<mesh.vertices.size(); i++)
{
    mesh.vertices[i] = normalize(accumulated[i]);
}

```

If you want more accurate results, use angle- or area-weighted normals. That's another rabbit hole, but a good reference is at [Weighted Vertex Normals](http://www.bytehazard.com/articles/vertnorm.html). 

### Comments

Leave comments on this post with Github Issues [here](https://github.com/nosferalatu/nosferalatu.github.io/issues/3).
