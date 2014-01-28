sail
====

Sailing simulator in Kivy. allows you to sail around a racecourse in wind and tide.

Zeroeth version: boat object with properties compass and position. interally we work in theta using mathmatical conventions. Boat has move and steer methods.

First version: one boat motors around, can be steered by buttons which adjust compass course to port or starboard by 10 degree increments.

Boat represented by circle with a radius drawn in a different color to indicate compass course.

TODO
====

boat
 add polars tables
 given a windangle and windspeed return the theoretical boatspeed
 first approximation: if no value in table for (wtheta,wspeed) then get value for 'nearest' windspeed and windangle in table. can do fancier interpolation later, or even fit a function to the table values and then use the function.

model environment
 wind and tide layers, start with just wind.
 return conditions at pos and time
 initally assume 

graphics rendering
 use kivy to render boat being steered around at constant speed

Hacking the code
================
Install [pyflakes](https://pypi.python.org/pypi/pyflakes) and then run `make`
to check your Python syntax and then run the unit tests.

