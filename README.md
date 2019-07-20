# ROBOT BASIC 

## Introduction

A BASIC script used for robot control. <br>
Original check readme.org.md to learn supported syntax. <https://github.com/richpl/PyBasic> <br>
New added functions:<br>

```
10 rem minit  -- motion init
10 rem moveto -- moveto(x,y,z,speed)
10 rem movepre -- moverel(x,y,z,speed)
20 i1 = minit()
30 i2 = moveto(10,10,10,30)
40 i3 = moverel(10,10,10,30)
50 print i1
60 print i2
70 print i3
```

