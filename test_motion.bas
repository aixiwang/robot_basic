10 print "start test ..."
20 ret = slp(1000)
30 print "time:",ret
40 ret = checkonline()
50 print "checkonline:",ret
60 ret = getloc(1)
70 print "getloc:",ret
100 let ret = clrloc()
110 print "clrloc:",ret
150 let ret = setparam(1,20,4000,200)
160 print "setparam axis 1:",ret
170 let ret = setparam(2,20,4000,200)
180 print "setparam axis 2:",ret
190 let ret = setparam(3,20,4000,200)
200 print "setparam axis 3:",ret
210 let ret = setparam(4,20,4000,200)
220 print "setparam axis 4:",ret
230 let ret = setparam(5,20,4000,200)
240 print "setparam axis 5:",ret
250 let ret = setparam(6,20,4000,200)
260 print "setparam axis 6:",ret
270 print "---------------------------"
280 print "test moverel =>"
290 ret = moverel(1,0,200)
300 t = slp(1000)
310 print "test moverelmulti =>"
320 ret1 = MOVERELPRE(1,0,500)
321 ret2 = MOVERELPRE(2,1,500)
330 ret3 = MOVERELMULTI(3)
340 t = slp(1000)
350 loc1 = getloc(1)
360 loc2 = getloc(2)
370 print "loc1:",loc1," loc2:",loc2
380 print "t:",t," ret3:",ret3
390 rem if loc1 < 19000 then 280 else 800
800 rem stop
810 goto 280
