Python Robotics Simulator
================================

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Once the dependencies are installed, simply run the `test.py` script to test out the simulator.


Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

# researchtrack_assignment_01
The code is organized as follows :
1. Initializing variables and set silver to True.
2. Defining the functions we need to use : `drive()` to drive the robot with a certain speed at a given time, `turn()` to allow the robot to turn (right or left), `find_golden_token()` to allow the robot to search for golden tokens, `find_silver_token()` to allow the robot to search for silver tokens, and `get_id` to get the id of tokens.
3. Main code : 
While true do the following :
* Search for a silver token.
* Grab the token using `grab()` function.
* Look for a Golden token.
* Drive the robot toward the golden token then release the silver token next to it.
* Repeat for all tokens.

Each time the box releases a silver token next to a golden one, we store the `id` of the golden token in an array `rs[i]` then we increament the value of `i`. For every iteration we check the current value of `rs[i]` with `rs[i-1]` to know if the robot has visited that box before or not. This helps the robot evoids releasing multiple silver tokens next to the same golden token more than once.

----------------------

The folder containts the code file `assignment.py` to run the code copy `python2 run.py assignment.py` on the cmd window.

Find the flowchart of the code on the `Flowchart` folder. You can open the flowchart diagram `flowchart.drawio` on Visual studio code using `draw.io` extention.
