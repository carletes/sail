sail
====

Sailing simulator in Kivy. allows you to sail around a racecourse in wind and tide.

Zeroeth version: boat object with properties compass and position. interally we work in theta using mathmatical conventions. Boat has move and steer methods.

First version: one boat motors around, can be steered by buttons which adjust compass course to port or starboard by 10 degree increments.

Boat represented by circle with a radius drawn in a different color to indicate compass course.

TODO
====
more tests of conversion between coordinate systems
test initialise with silly values (compass = 2000)

boat
 add polars tables

model environment
 wind and tide layers
 return conditions at pos and time
 initally assume 

