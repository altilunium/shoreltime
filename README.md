# shoreltime (Shalat's Relative-Time)
How close are we to the next adzan?

![alt text](https://github.com/altilunium/shoreltime/blob/main/demo.png?raw=true "Logo Title Text 1")

61 means "61% percent completion" from the last adzan to the next adzan. 

## Installation Guide (Windows)
1. Install Python 3
2. Open the source code
3. Modify the coordinate and timezone based on your location.  `lamd : longitude, phi : latitude, td : UTC offset (i.e. 7,-5)` 
5. Open command prompt, type `pip install pystray`. Then `pip install Pillow`
7. Rename `sy.py` to `sy.pyw`
8. Press WIN+R, type "shell:startup". Copy `sy.pyw` there.
9. Double click the `sy.pyw`


## Algorithm
The prayer times calculation algorithm is based from [Djamaluddin (1990)](https://tdjamaluddin.wordpress.com/2010/12/09/program-jadwal-shalat/) by using solar position algorithm of [Astronomical Almanac for Computer](https://tdjamaluddin.wordpress.com/2010/12/09/program-jadwal-shalat/#comment-11720).

Then, today's prayer times (+ midnight time) is stored inside an array. `checkpoints = [subuh,zuhur,ashar,magrib,isya,midnight]`. 

If right now is 14.00 , then we calculate the time difference between 14.00 and zuhur `progress = now - zuhur`, calculate the time difference between zuhur and ashar `complete_progress = ashar - zuhur`, calculate the progress (in percent) `percentageProgress = (progress / complete_progress) * 100`.

