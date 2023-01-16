Title: Derivatives, Logarithms, and Transforms
Date: 2023-01-14 16:00
Tags: Programming
Category: Blog
Slug: DerivativesLogarithmsTransforms
Author: David Farrell
Summary: Understanding derivatives and logarithms of transforms
Status: draft

Given a transform matrix $T$ and a point x, we can find the transformed point with $T * x$. Multiply the point $x$ by the matrix $T$, and out pops a new point.

But what if we want to smoothly interpolate $T$ so it moves $x$ along the path from its initial position to its position transformed by $T$? What we want is 

$x(t) = T(t) * x(0)$

meaning, to find the point $x$ at time $t$, we multiply the point's initial position ($x(0)$) by the transform at time t ($T(t)$). But since we only have a single matrix $T$, we need to find a way to interpolate that matrix in time.

One way to do that is to raise $T$ to the power of $t$, which can be done with the matrix exponential and matrix logarithm. Interestingly, the matrix logarithm of a transform matrix can also be used to easily find the velocity of a point $x$ in space: the velocity vector (or tangent vector) is just $log(T) * x$. This blog post shows how the logarithm and velocity are related.

### Example

To start with, here is an interactive example. As you use the gizmo to rotate and translate the transform, you can see the vector field change. The vector field can be interpreted as the the velocity vector at every point in space as the point is being transformed.

As you move the gizmo, you can see a white curve from the origin to the gizmo's transform. Along that curve, you can also see the interpolated transform as it travels from the origin to the gizmo. As you can see, the interpolation follows the flow of the velocity vector field. The code is using the exponential and logarithm of the transform to compute the curve and interpolated transform.

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

To compute $T^t$, we need to use matrix exponentials and matrix logarithms.

Let's start with two facts about a matrix X:

$e^{log(X)} = X$ and

$log(X^y) = log(X) * y$.

Put together, we can say that

$T^t = e^{log(T^t)} = e^{log(T)*t}$

which we can plug into the earlier equation, giving us

$x(t) = e^{log(T) * t} * x(0)$.

This says that to find the point x at time t, find the transform at time t using $e^{log(T) * t}$, and use that to transform the point at its initial position (at time 0).

### What's the derivative?

In calculus, we learned that

$\dfrac{d}{dt}e^{a t} = a e^{a t}$

which is also true for matrices:

$\dfrac{d}{dt}e^{A t} = A e^{A t}$

Using that, we can find the derivative of our earlier equation $x(t) = e^{log(T)t} x(0)$ with respect to t:

$\dfrac{d}{dt}x(t) = log(T) e^{log(T) t} x(0)$.

This can be read as: to find the first derivative (tangent vector) of the point at time t, start with the initial position of the point, transform it with the interpolated transform at time t, and then multiply it by the log of the transform. This is using column vector notation, so you should read the operations as happening right-to-left: the initial position of the point is $x(0)$, the interpolated transform is $e^{log(T) t}$, and the log of the transform is $log(T)$.

$e^{log(T) t}$ is a kind of operator that maps points from their initial position to their new position at time t. I like to think of the matrix exponential as like integration. At time 0, $e^{log(T) t}$ is the identity matrix (because $e^0=I$ for matrix exponentials); at time 1.0, $e^{log(T) t}$ is the original transform matrix T (because $e^{log(T)}=T$).

### What's this all mean?

If we take the equation at the end of "What's $T^t$?"

$x(t) = e^{log(T) t} x(0)$

and substitute that into the equation at the end of "What's the derivative?"

$\dfrac{d}{dt}x(t) = log(T) e^{log(T) t} x(0)$,

then we have:

$\dfrac{d}{dt}x(t) = log(T) x(t)$.

This relates the derivative of a moving point to the logarithm of the transformation moving that point.

One way to think of $log(T)$ is as the vector field of tangent vectors of that transform. In other words, it's the field of first derivatives. This vector field is independent of time. It's constant with respect to t. The vector field shows what the velocity is for every point in space.

That equation is saying that if you transform any point in space by the logarithm of the transform, you will get the first derivative at that point. The first derivative is the velocity, so $log(T)$ defines the velocity field (the field of tangent vectors at every point in space). 

As x moves through space by the transform matrix, it forms a curve; the tangent vector at time t is tangent to the x's position on the curve at time t.

This insight is really neat: The logarithm of a transform matrix is another matrix that maps positions in space to tangent vectors. You can think of the log of a matrix as the velocity field of the action performed by that matrix.

The vector field visualized in the interactive example above is this velocity field.

A more informal way of looking at the equation $\dfrac{d}{dt}x(t) = log(T) x(t)$ is to say

$velocity = log(transform) * position$

meaning, to understand how a point will move in time, look at the vector field of the log of the transform as a velocity field. As the point flows along that velocity field, it moves in time.

### What's the differential equation?

Let's look at this in a different way-- from the perspective of differential equations. Earlier, we had
$\dfrac{d}{dt} x(t) = log(T) x(t)$
which is a differential equation, and because $log(T)$ is a matrix, it is more specifically a matrix differential equation.

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

This is the same as our original equation, but from the opposite direction.

### Visualizing a matrix as a vector field

If you are wondering how you can visualize a matrix as a vector field, an eloquent explanation is in 3Blue1Brown's video about matrix exponentiation. This part about matrices as vector fields explains that very well:

<iframe width="560" height="315" src="https://www.youtube.com/embed/O85OWBJ2ayo?start=1331" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### The derivative of the matrix exponential

Earlier we used the property $\dfrac{d}{dt}e^{A t} = A e^{A t}$. It's not obvious why this property is true, but it's an important part of unlocking all of this.

A good reference for this derivation is in the textbook Modern Robotics. [A free copy of that book can be found here](http://hades.mech.northwestern.edu/index.php/Modern_Robotics). See equation (3.43) in that book.

The matrix exponential is defined as

$e^{A t} = I + A t + \frac{1}{2}(A t)^2 + \frac{1}{3!}(A t)^3 + ...$

What then is $\dfrac{d}{dt}e^{A t}$? If we take the derivative of each term of the matrix exponential's expanded definition, we have

$\dfrac{d}{dt}e^{A t} = 0 + A + A^2 t + \frac{1}{2} A^3 t^2 + ...$

Pull out A, and then we have

$\dfrac{d}{dt}e^{A t} = A*(I + A t + \frac{1}{2} (A t)^2 + ...) = A e^{A t}$.

Interestingly, note that $A$ can go on the left or the right. It is always true that

$Ae^{A t} = e^{A t}A$

for any square matrix (equation (3.44) in Modern Robotics). 