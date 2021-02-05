README
FAST clock file

Clock file in TEMPO2 format:</br>
https://crafts.bao.ac.cn/pub/fast/time/fast2gps.clk

Clock file in TEMPO format:</br>
https://crafts.bao.ac.cn/pub/fast/time/time_fast.dat



FAST 台站更新 201909/19 </br>
-1668557.0      5506838.0      2744934.0        FAST                fast

https://crafts.bao.ac.cn/pub/fast/time/fast-coord.txt



How to change to TEMPO2 clock file in PINT</br>

Find the file `pint/observatory/observatories.py` and edit it.</br>

Here's the example setting for FAST.</br>

```python
 TopoObs(
     "fast",
     tempo_code="k",
     itoa_code="FA",
     clock_fmt="tempo2",
     clock_dir="TEMPO2",
     clock_file="fast2gps.clk",
     itrf_xyz=[-1668557.0, 5506838.0, 2744934.0]
```

Here's the clock difference plot.</br>
![clockDiff](https://github.com/NAOC-pulsar/FAST_ClockFile/blob/master/clockDiff.png)


> It is straight forward to get (X,Y,Z)=(−1668557.2070983793,5506838.5266271923,2744934.9655897617). This value is consistent with that used by PINT, (X,Y,Z)=(−1668557.0,5506838.0,2744934.0), which is provided by Youling Yue, one of the authors. We think the FAST coordinate used by PINT is OK. [link](http://blog.sciencenet.cn/blog-117333-1262557.html)

This means you need to update the coordinates of FAST in tempo2
