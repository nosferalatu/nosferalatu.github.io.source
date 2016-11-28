Title: Test
Date: 2014-5-26 12:00
Tags: Programming
Category: Blog
Slug: Test
Author: David Farrell
Summary: Testing Pelican
Status: draft

Specializing code at compile time is often useful for high performance code.

    :::
    int compute_sum(bool branch0, bool branch1, bool branch2)
    {
        int sum = 0;
        if (branch0)
           sum |= 1;
        if (branch1)
           sum |= 2;
        if (branch3)
           sum |= 4;
        return sum;
    }

C Preprocessor
==============

You can use the C preprocessor to generate the permutations by having one file contain code that is driven by `#define`'s, and a second file that `#include`'s the first file over and over again:

```
// FunctionKernel.h
int compute_sum_##FN_NAME()
{
    int sum = 0;
    #if BRANCH0
        sum |= 1;
    #endif
    #if BRANCH1
        sum |= 2;
    #endif
    #if BRANCH2
        sum |= 4;
    #endif
}
```

Math stuff
==========

Here's an equation: $e=mc^2$ and another one: $x^2$ and then a third one: $$x^2$$ and so on and on.

This is an identity matrix: $$\left[\begin{matrix} 1.0 & 0.0\\ 0.0 & 1.0\end{matrix} \right]$$

And a PDE: $\dfrac {\partial \phi } {\partial t} = 1$

The level set equation: $\dfrac {\partial \phi } {\partial t} + u \cdot \nabla \phi = 1$

An Eikonal: $\left| \nabla \phi \right| = 1$

with the source: $\left| \nabla \phi \right| = 1 $
