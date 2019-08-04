10 rem==========================
20 rem init
30 rem==========================
31 print 'start test ...'
40 ret = checkonline()
50 print 'checkonline:',ret
60 ret = closelocnoti()
70 print 'closelocnoti:',ret
80 ret = stopall()
90 print 'stopall:',ret
100 ret = clrloc()
110 print 'clrloc:',ret
120 rem==========================
130 rem set axis 1-6 parameter
140 rem==========================
150 ret = setparam(1,20,4000,200);
160 print 'setparam axis 1:',ret
170 ret = setparam(2,20,4000,200);
180 print 'setparam axis 2:',ret
190 ret = setparam(3,20,4000,200);
200 print 'setparam axis 3:',ret
210 ret = setparam(4,20,4000,200);
220 print 'setparam axis 4:',ret
230 ret = setparam(5,20,4000,200);
240 print 'setparam axis 5:',ret
250 ret = setparam(6,20,4000,200);
260 print 'setparam axis 6:',ret
270 print 'moverel test ...'
280 for i = 1 to 3
290 ret = moverel(1,0,200)
300 print 'moverel:',ret,' cnt:',i
310 delay(1000)
320 next i   
330 print 'end of test ...'
run

