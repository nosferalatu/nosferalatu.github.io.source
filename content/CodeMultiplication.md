Title: Code Multiplication
Date: 2014-6-8 12:00
Tags: Programming
Category: Blog
Slug: CodeMultiplication
Author: David Farrell
Summary: Code Multiplication
Status: draft
Specializing code at compile time is often useful for high performance code. I've heard this specific technique referred to as *code multiplication*. A google search doesn't find anything with that name, so I'll describe it here.

Say you have some code that does different things based on N boolean parameters. What we want to do is create 2^N different permutations of that function, each one specialized for a specific set of input values. At runtime, we'll go through a jump table of functions to execute the permutation we want. I'll describe a couple of ways to do that. For the examples below, here's the function that we'll be specializing:

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

```
// Function.cpp
#define BRANCH0 0
#define BRANCH1 0
#define BRANCH2 0
#define FN_NAME FFF
#include "FunctionKernel.h"
#undef BRANCH0
#undef BRANCH1
#undef BRANCH2

#define BRANCH0 1
#define BRANCH1 0
#define BRANCH2 0
#define FN_NAME FFT
#include "FunctionKernel.h"
#undef BRANCH0
#undef BRANCH1
#undef BRANCH2

#define BRANCH0 0
#define BRANCH1 1
#define BRANCH2 0
#define FN_NAME FTF
#include "FunctionKernel.h"
#undef BRANCH0
#undef BRANCH1
#undef BRANCH2

#define BRANCH0 1
#define BRANCH1 1
#define BRANCH2 0
#define FN_NAME FTT
#include "FunctionKernel.h"
#undef BRANCH0
#undef BRANCH1
#undef BRANCH2

#define BRANCH0 0
#define BRANCH1 0
#define BRANCH2 1
#define FN_NAME TFF
#include "FunctionKernel.h"
#undef BRANCH0
#undef BRANCH1
#undef BRANCH2

#define BRANCH0 1
#define BRANCH1 0
#define BRANCH2 1
#define FN_NAME TFT
#include "FunctionKernel.h"
#undef BRANCH0
#undef BRANCH1
#undef BRANCH2

#define BRANCH0 0
#define BRANCH1 1
#define BRANCH2 1
#define FN_NAME TTF
#include "FunctionKernel.h"
#undef BRANCH0
#undef BRANCH1
#undef BRANCH2

#define BRANCH0 1
#define BRANCH1 1
#define BRANCH2 1
#define FN_NAME TTT
#include "FunctionKernel.h"
#undef BRANCH0
#undef BRANCH1
#undef BRANCH2

#define NUM_BRANCHES 3
int (*specialized_fn)() fn_table[1 << NUM_BRANCHES] = {
    &compute_sum_FFF,
    &compute_sum_FFT,
    &compute_sum_FTF,
    &compute_sum_FTT,
    &compute_sum_TFF,
    &compute_sum_TFT,
    &compute_sum_TTF,
    &compute_sum_TTT,
};

int compute_sum(bool branch0, bool branch1, bool branch2)
{
    int permutation = (branch0 << 0) |
                      (branch1 << 1) |
                      (branch2 << 2);
    return fn_table[permutation]();
}
```

Function Templates
==================

For C++ code, an alternative is to use *function templates* to have the compiler generate the permutations. For example:

```
template <bool branch0, bool branch1, bool branch2>
int compute_sum_fn()
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

#define NUM_BRANCHES 3
int (*specialized_fn)() fn_table[1 << NUM_BRANCHES] = {
    &compute_sum_fn<false, false, false>,
    &compute_sum_fn<false, false, true >,
    &compute_sum_fn<false, true,  false>,
    &compute_sum_fn<false, true,  true >,
    &compute_sum_fn<true,  false, false>,
    &compute_sum_fn<true,  false, true >,
    &compute_sum_fn<true,  true,  false>,
    &compute_sum_fn<true,  true,  true >,
};

int compute_sum(bool branch0, bool branch1, bool branch2)
{
    int permutation = (branch0 << 0) |
                      (branch1 << 1) |
                      (branch2 << 2);
    return fn_table[permutation]();
}
```

An optimizing compiler will see that the values in each `compute_sum_fn()` permutation are constant and remove the branches. 

I generally shy away from C++ class templates, but function templates can be very useful for code generation. In the above example, the function template version produces the same results as the C preprocessor version but with fewer lines of code.
