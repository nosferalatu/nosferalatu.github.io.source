Title: Derivatives, Logarithms, and Transforms
Date: 2022-08-01 21:00
Tags: Programming
Category: Blog
Slug: DerivativesLogarithmsTransforms
Author: David Farrell
Summary: Understanding derivatives and logarithms of transforms
Status: draft

Given a transform matrix $T$ and a point x, we can find the transformed point with $T * x$. Multiply the point x by the matrix $T$, and out pops a new point.

But what if we want to smoothly interpolate $T$ so it moves x along the path from its initial position to its position transformed by $T$? What we want is 

$x(t) = T(t) * x(0)$

meaning, to find the point x at time t, we multiply the point's initial position ($x(0)$) by the transform at time t ($T(t)$). But since we only have a single matrix $T$, we need to find a way to interpolate that matrix in time.

I want to show how to do that, and also share some interesting insights I learned along the way.

### What's $T(t)$?
We have $T$, but not $T(t)$, which changes with time. Assuming that multiplying two transforms represents the composition of those transforms, we can find $T(t)$ by saying

$T(0) = I$ (the identity transform)

$T(1) = T$

$T(2) = T * T$

$T(3) = T * T * T$

More generally, we can find $T$ at any time by saying

$T(t) = T^t$.

The above trick is from a blog post by Fabien Geisen [here](https://fgiesen.wordpress.com/2012/08/24/quaternion-differentiation/) but works for any transform that uses multiplication for composition.

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

### What's this all mean?

The equation

$\dfrac{d}{dt}x(t) = log(T) e^{log(T) t} x(0)$

(which is the same as $\dfrac{d}{dt}x(t) = log(T) x(t)$)

can be read as: to find the first derivative (tangent vector) of the point at time t, start with the initial position of the point, transform it with the interpolated transform at time t, and then multiply it by the log of the transform. This is using column vector notation, so you should read the operations right-to-left, so the initial position of the point is $x(0)$, the interpolated transform is $e^{log(T) t}$, and the log of the transform is $log(T)$.

You can think of $e^{log(T) t}$ as a kind of operator that maps points from their initial position to their new position at time t. I like to think of the matrix exponential as like integration. At time 0, $e^{log(T) t}$ is the identity matrix (because $e^0=I$ for matrix exponentials); at time 1.0, $e^{log(T) t}$ is the original transform matrix T (because $e^{log(T)}=T$).

And, you can think of $log(T)$ as the vector field of tangent vectors of that transform. In other words, it's the field of first derivatives. This vector field is constant with respect to t; it's the same field, regardless of what time is. The vector field shows what the velocity is for every point in space.

That equation is saying that if you transform any point in space by the logarithm of the transform, you will get the first derivative at that point. The first derivative is the velocity, so $log(T)$ defines the velocity field (the field of tangent vectors at every point in space). 

As x moves through space by the transform matrix, it forms a curve; the tangent vector at time t is tangent to the x's position on the curve at time t.

This insight is really neat: The logarithm of a transform matrix is another matrix that maps positions in space to tangent vectors.

By analogy, taking the logarithm of a transform matrix is kind of like producing the assembly instructions for that transform. If the transform matrix is like a high level representation of a transform, then the logarithm of the transform matrix is a bunch of tangent vectors which are like low level assembly code. You can take the exponent of the logarithm of the transform matrix, or numerically integrate a point using the log(transform), or solve the matrix exponent directly, or even find a closed form solution for log() and exp() for certain groups of transforms. These have very different meanings for computation, but conceptually, the log of a transform matrix-- really, the log of any matrix-- can be thought of as the velocity field of the action performed by that matrix.

How can we think of a matrix as a vector field? An eloquent explanation is in 3Blue1Brown's video about matrix exponentiation. This part about matrices as vector fields explains that very well:

<iframe width="560" height="315" src="https://www.youtube.com/embed/O85OWBJ2ayo?start=1331" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Another way of looking at our equation above is to say

$velocity = log(transform) * position$

meaning, to understand how a point will move in time, look at the vector field of the log of the transform as a velocity field. As the point flows along that velocity field, it moves in time.



### What's the ODE?

The above can also be rearranged as

$\dfrac{d}{dt} x(t) = log(T) x(t)$

which is a matrix differential equation. $log(T)$ is just a matrix.

Just as scalar ordinary differential equations of the form $y'(t)=ay(t)$ have the solution $y(t)=e^{at}y(0)$, matrix differential equations of the form $x'(t)=Ax(t)$ have the general solution $x(t)=e^{At}x(0)$.

That means that the solution to the matrix differential equation above is

$x(t) = e^{log(T) t} x(0)$.

### Deriving the derivative of the matrix exponential

_Be careful below. The chain rule is correct here, but it only applies in certain circumstances: [A Remark on the Chain Rule for Exponential Matrix Functions](https://www.maa.org/sites/default/files/liu03010328120.pdf)_

Let's find the derivative of that equation. Starting with

$\dfrac{d x(t)}{dt} = (e^{A t} x(0))'$

we can pull out the constant $x(0)$

$\dfrac{d x(t)}{dt} = (e^{A t})' x(0)$

and then apply the chain rule

$\dfrac{d x(t)}{dt} = (A t)' e^{A t} x(0)$

The derivative of $A t$ with respect to $t$ is just $A$, leaving us with 

$\dfrac{d x(t)}{dt} = A e^{A t} x(0)$.

### Deriving the derivative of the matrix exponential, another way

The matrix exponential is defined as

$e^{A t} = I + A t + \frac{1}{2}(A t)^2 + \frac{1}{3!}(A t)^3 + ...$

What then is $\dfrac{d}{dt}e^{A t}$? If we take the derivative of each term of the matrix exponential's expanded definition, we have

$\dfrac{d}{dt}e^{A t} = 0 + A + A^2 t + \frac{1}{2} A^3 t^2 + ...$

Pull out A, and then we have

$\dfrac{d}{dt}e^{A t} = A*(I + A t + \frac{1}{2} (A t)^2 + ...) = A e^{A t}$.

If we plug that into the equation

$\dfrac{d}{dt}x(t) = (e^{A t} x(0))'$

and pull out the constant $x(0)$, the result is

$\dfrac{d}{dt}x(t) = A e^{A t} x(0)$.




### Example: Rotation

That differential equation is saying that if you transform any point in space by the logarithm of the transform, you will get the first derivative at that point. The first derivative is the velocity, so $log(T)$ defines the velocity field (the field of tangent vectors at every point in space).

One way to see this is to consider rotation matrices. Imagine we have a rotation matrix R and a point x. Then we have

$\dfrac{d x(t)}{dt} = log(R) * R^t * x(0)$

which can be read as: starting with the initial point x, rotate it for t units of time, which results in a new point at position x(t). Then, multiply that new point by the the logarithm of $R$. That returns the first derivative (the tangent vector) at that new point. Note that $log(R)$ is independent of time; it returns a different tangent vector for each point in space, but it doesn't return a different tangent vector at different times.

The logarithm of a rotation matrix is a skew symmetric matrix that corresponds to angular velocity. If you are using an axis-angle representation for rotation, the angular velocity vector is $\omega$, which is a vector pointing in the direction of the axis of rotation with a length equal to the angle of rotation.



### WebGL

<body>
  <!-- <div id="canvas" style="width: 256px; max-width: 256px; height: 512px; max-height: 512px;"></div> -->
  <canvas id="canvas" width="512" height="512"></canvas>
  <div id="overlay">
    <div>slider <input id="slider" type="range" min="-1" max="2" step="0.01" value="0" /></div>
    <div>Time: <span id="time"></span></div>
    <div>Slider Value: <span id="sliderValue"></span></div>
  </div>
</body>

<!-- <script type="text/javascript" src="/js/testClearToRed.js"></script> -->
<script src="/js/three.js/three.min.js"></script>
<script src="/js/three.js/OrbitControls.js"></script>
<script type="module" src="/js/VectorField.js"></script>


# Miscellaneous

At time 0, we have $T(0) = I$ (the identity transform).

At time 1, we have $T(1) = T$.


$10x^9$

rocket




