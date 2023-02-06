Title: Derivatives, Logarithms, and Transforms
Date: 2023-01-14 16:00
Tags: Programming
Category: Blog
Slug: DerivativesLogarithmsTransforms
Author: David Farrell
Summary: Understanding derivatives and logarithms of transforms
Status: draft

Given a transform $T$ and a point x, we can find the transformed point with $T * x$. But what if we want to smoothly interpolate $T$ so it moves $x$ along the path from its initial position to its position transformed by $T$? 

What we want to find is the point $x$ at time $t$:

$x(t) = T(t) * x(0)$

where $x(0)$ is the point's initial position, and $T(t)$ is the transform at time $t$. Since we have only a single transform $T$, we need to find a way to interpolate it over time.

One way to accomplish this is to raise $T$ to the power of $t$, which can be done using the exponential and logarithm of the transform. Interestingly, the logarithm of a transform can also be used to easily find the velocity of a point $x$ in space: the velocity vector (also called the tangent vector) is just $log(T) * x$. This blog post shows the relationship between the logarithm and velocity.

### Example

Check out this interactive example to see how the vector field changes as you manipulate the gizmo to translate and rotate the transform. The vector field represents the velocity vector at each point in space during the transformation.

As you move the gizmo, you'll notice a white curve that traces the path from the origin to the gizmo's transform. Along this curve, you'll see the interpolated transform as it travels from the origin to the gizmo. As you can see, the interpolation follows the flow of the velocity vector field. The applet's code is using the exponential and logarithm of the transform to compute the curve, interpolated transform, and vector field.

<body>
  <!-- <div id="canvas" style="width: 256px; max-width: 256px; height: 512px; max-height: 512px;"></div> -->
  <div>
   <div id="canvas-gui-container" style="position:absolute;"></div>
   <canvas id="canvas" width="512" height="512"></canvas>
  </div>
</body>

<script src="/js/three.js/three.min.js"></script>
<script src="/js/three.js/OrbitControls.js"></script>
<script src="/js/three.js/TransformControls.js"></script>
<script type="module" src="/js/three.js/VRButton.js"></script>
<script src="/js/lil-gui/lil-gui@0.17.umd.js"></script>
<script src="/js/VectorField.js"></script>

The source code for the applet can be found [here](../../js/VectorField.js), which includes an implementation of closed-form log() and exp() for rigid body transforms.

Next, I'll describe how to compute the interpolated transform and the velocity vector field you see in this example.

### What's $T(t)$?
We have $T$, but not $T(t)$, which changes with time. Assuming that multiplying two transforms represents the composition of those transforms, we can find $T(t)$ by saying

$T(0) = I$ (the identity transform)

$T(1) = T$

$T(2) = T * T$

$T(3) = T * T * T$

More generally, we can find $T$ at any time by saying

$T(t) = T^t$.

The above trick is from a blog post by Fabian Giesen [here](https://fgiesen.wordpress.com/2012/08/24/quaternion-differentiation/) but works for any transform that uses multiplication for composition.

Now that we know $T(t) = T^t$, the original equation can be rearranged to

$x(t) = T^t * x(0)$.

### What's $T^t$?

To compute $T^t$, we need to use the matrix exponential and matrix logarithm.

Let's start with two facts about a matrix X:

$e^{log(X)} = X$ and

$log(X^y) = log(X) * y$.

Put together, we can say that

$T^t = e^{log(T^t)} = e^{log(T)*t}$

which we can plug into the earlier equation, giving us

$x(t) = e^{log(T) * t} * x(0)$.

This says that to find the point x at time t, find the transform at time t using $e^{log(T) * t}$, and use that to transform the point at its initial position (at time 0).

### What's the derivative? {#WhatsTheDerivative}

In calculus, we learned that

$\dfrac{d}{dt}e^{a t} = a e^{a t}$

which holds true for matrices as well:

$\dfrac{d}{dt}e^{A t} = A e^{A t}$

This relationship is explained in more detail in the section [the derivative of the matrix exponential](#DerivativeOfMatrixExponential).

We can use this property to find the derivative of our earlier equation $x(t) = e^{log(T)t} x(0)$ with respect to t:

$\dfrac{d}{dt}x(t) = log(T) e^{log(T) t} x(0)$.

This equation states that to find the first derivative (the velocity vector, also called the tangent vector) of the point at time t, you first transform the point's initial position $x(0)$ with the interpolated transform $e^{log(T)t}$ and then multiply it by the logarithm of the transform $log(T)$. This expression follows the right-to-left convention of column vectors, so you would start with the initial position $x(0)$, then apply the interpolated transform $e^{log(T)t}$, and finally multiply by the logarithm $log(T)$.

$e^{log(T) t}$ acts as an operator that maps points from their initial position to their new position at time t. The matrix exponential can be thought of as like integration. At time 0, $e^{log(T) t}$ is the identity matrix ($e^0=I$ for matrix exponentials), and at time 1.0, $e^{log(T) t}$ is equal to the original transform matrix T ($e^{log(T)}=T$).

### What's this all mean?

If we take the equation at the end of "What's $T^t$?"

$x(t) = e^{log(T) t} x(0)$

and substitute that into the equation at the end of "What's the derivative?"

$\dfrac{d}{dt}x(t) = log(T) e^{log(T) t} x(0)$,

then we have:

$\dfrac{d}{dt}x(t) = log(T) x(t)$.

This relates the derivative of a moving point to the logarithm of the transformation moving that point.

One way to think of $log(T)$ is as a vector field of tangent vectors for the transformation. In other words, it's the field of first derivatives. This vector field is independent of time and shows the velocity for every point in space.

That equation is saying that if you transform any point in space by the logarithm of the transform, you will get the first derivative at that point. The first derivative is the velocity, so $log(T)$ defines the velocity field (the field of tangent vectors at every point in space). 

As a point moves through space by the transform, it forms a curve. The tangent vector at time t is tangent to the point's position on the curve at time t.

You can think of the logarithm of a matrix as the velocity field of the action performed by that matrix. The velocity field visualized in the interactive example above is this field.

A more informal way of looking at this is to say

$velocity = log(transform) * position$

meaning, to understand how a point will move in time, look at the vector field of the log of the transform as a velocity field. As the point flows along that velocity field, it moves in time.

### What's the differential equation?

We can also reformulate all of this as a differential equation. Earlier, we had

$\dfrac{d}{dt} x(t) = log(T) x(t)$

which is a differential equation. Because $log(T)$ is a matrix, it is more specifically a matrix differential equation.

Scalar ordinary differential equations of the form

$y'(t)=ay(t)$

have the general solution

$y(t)=e^{at}y(0)$.

Similarly, matrix differential equations of the form

$x'(t)=Ax(t)$

have the general solution

$x(t)=e^{At}x(0)$.

Therefore, given our equation from earlier

$\dfrac{d}{dt} x(t) = log(T) x(t)$

we have the solution

$x(t) = e^{log(T) t} x(0)$.

This is the same as our original equation, but we started with a differential equation and found a solution. To prove this solution is correct, just take the derivative of it, which is what we did earlier in the [What's the derivative?](#WhatsTheDerivative) section.

### The exponential map and logarithm map

The exponential map is defined as the infinite series

$$e^{A t} = I + A t + \frac{1}{2}(A t)^2 + \frac{1}{3!}(A t)^3 + ... = \sum_{i=0}^{\infty} \frac{(At)^i}{i!}$$

and can be used to find the exponential of real numbers, complex numbers, quaternions, matrices, and more. For example, when square matrices are plugged in to the series, the result is called the [matrix exponential](https://en.wikipedia.org/wiki/Matrix_exponential).

Similarly, the logarithm is defined as the infinite series

$$log(A) = \sum_{i=1}^{\infty} (-1)^{i+1} \frac{(A - I)^i}{i}$$

If you want to know more, search for the exponential map and logarithm map. You'll find that these are important concepts in Lie group theory. The exponential map and logarithm map are inverses of each other. In Lie theory, the exponential map maps a tangent vector at a point p to a point on the manifold. The logarithm map does the opposite, mapping a point on the manifold back to the tangent vector at p.

When reading about Lie groups, you'll come across many different kinds of groups. There are only a few groups that are related to transforms, though. **SO(3)** is a 3D rotation matrix, **SU(2)** is a quaternion, **SE(3)** is a 3D rigid body transform (rotation and translation), **SIM(3)** is rotation, translation, and (positive) uniform scale, and **GL(n)** is an nxn matrix.

There are several options for how to practically compute the exponential and logarithm map for a matrix or other object:

1) Use a math library like Eigen or Armadillo. These have functions to compute the matrix exponential and matrix logarithm.

2) The library Sophus has code for a closed form exp/log for the groups SO(3), SE(3), and SIM(3). Beware that it clamps its quaternions to a 3D rotation angle in -$\pi$ ... +$\pi$ though.

3) There is an excellent PDF at the web site of Ethan Eade [here](https://ethaneade.com/lie.pdf) which contains the closed form equations for the groups SO(3), SE(3), and SIM(3).

4) Compute the matrix exponential and logarithm by using the infinite series definitions above, and truncating after some number of terms. In my experience, this is not robust when working with floating point numbers, as you quickly start to deal with very small and very large numbers, depending on your input matrix.

5) Compute the exponential with numerical integration. Given a starting point $x$, integrating it for time t is the same thing as the exponential. There are many ways to compute numerical integration, from Euler to Runge-Kutta to adaptive methods.

### Pitfalls

There are a few issues that you should be aware of.

#### Pitfall #1

The logarithm of a rotation matrix will return a 3D rotation angle in -$\pi$ ... +$\pi$. More technically, there are an infinite number of logarithms for a matrix, each corresponding to a rotation angle that is  2$\pi$ greater than the previous one. Generally matrix logarithm code will return the principal logarithm, which is the logarithm in -$\pi$ ... +$\pi$. This can lead to discontinuities when interpolating transforms with rotations in them, such rotations from human joints (you can move your head from looking over your left shoulder to over your right shoulder and rotate a little more than 180 degrees).

On the other hand, the logarithm of a quaternion returns a 3D rotation angle in the larger range of -2$\pi$ ... +2$\pi$, which makes quaternions nicer to work with.

#### Pitfall #2

When working with logarithms, be aware that that the property

$log(AB) = log(A) + log(B)$

is _only_ true when A and B commute, which is not the case for most transforms. Real numbers always commute, though, so the property does apply to them. It's tempting to apply the property to transforms, but it's important to remember it only applies when A and B commute.

For example, interpolating a transform by using log(rotation) plus log(translation) will result in a straight path between the start and end transform, but the correct result is a helical, screw path that is obtained by using log(rotation*translation).

#### Pitfall #3

Related to pitfall #2, you might want to interpolate two transforms A and B with

$interpolate(A, B, t) = e^{(1-t)*log(A) + t*log(B)}$

But be careful: this only works if A and B commute, which is not usually the case for transforms. Otherwise, this interpolation is neither shortest path nor constant speed.

Instead, interpolate the relative (also called delta) transform from A to B, like this:

$interpolate(A, B, t) = e^{log(B A^{-1}) t} A$

However, this method only works for interpolating between two transforms and not for blending more than two transforms.

### Visualizing a matrix as a vector field

If you are wondering how you can visualize a matrix as a vector field, an eloquent explanation is in 3Blue1Brown's video about matrix exponentiation. This part about matrices as vector fields explains that very well:

<iframe width="560" height="315" src="https://www.youtube.com/embed/O85OWBJ2ayo?start=1331" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### The derivative of the matrix exponential {#DerivativeOfMatrixExponential}

Earlier we used the property $\dfrac{d}{dt}e^{A t} = A e^{A t}$. It's not obvious why this property is true, but it's an important part of unlocking all of this.

A good reference for this derivation is in the textbook Modern Robotics. [A free copy of that book can be found here](http://hades.mech.northwestern.edu/index.php/Modern_Robotics). See equation (3.43) in that book.

The matrix exponential is defined as

$e^{A t} = I + A t + \frac{1}{2}(A t)^2 + \frac{1}{3!}(A t)^3 + ...$

What then is $\dfrac{d}{dt}e^{A t}$? If we take the derivative of each term of the matrix exponential's expanded definition, we have

$\dfrac{d}{dt}e^{A t} = 0 + A + A^2 t + \frac{1}{2} A^3 t^2 + ...$

Pull out A, and then we have

$\dfrac{d}{dt}e^{A t} = A*(I + A t + \frac{1}{2} (A t)^2 + ...) = A e^{A t}$.

It's worth noting that the matrix $A$ can go on the left or right, and it always holds true that

$Ae^{A t} = e^{A t}A$

for any square matrix, as stated in equation (3.44) in Modern Robotics.
