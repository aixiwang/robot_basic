#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------------------
# lib for serial port based motion controller
#
# Apache v2 license is applied to this code
# Copyright by Aixi Wang (aixi.wang@hotmail.com)
#---------------------------------------------------------------------------------------------
# v1 2019-08-03
#--------------------
# * initial checkin
# known issues(could be hardware issue): 
#    mc_move doesn't work, 
#    mc_move_rel_multi completion checking dosn't work
#    mc_get_cur_loc can't work for every signal axis, only support all axis
#---------------------------------------------------------------------------------------------

import serial
import sys,time

import sys
if sys.version_info[0] < 3:
    py2_flag = 1
else:
    py2_flag = 0
    
SERIAL_TIMEOUT = 1
s = None

#serialport_port = '/dev/ttyUSB0'
serialport_port = 'COM5'
serialport_baud = 115200

#-------------------------
# to_bytes
#-------------------------
def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode() # uses 'utf-8' for encoding
    else:
        value = bytes_or_str
    return value # Instance of bytes
    
#-------------------------
# int_to_bytes
#-------------------------
def int_to_bytes(i):
    return i.to_bytes(2,byteorder='little',signed=False)[0:1]
    
#-------------------------
# to_str
#-------------------------  
def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode() # uses 'utf-8' for encoding
    else:
        value = bytes_or_str
    return value # Instance of str

#-------------------------
# to_hex
#-------------------------      
def to_hex(bytes_or_str):
    return to_bytes(bytes_or_str).hex()

#-------------------------
# from_hex
#-------------------------    
def from_hex(bytes_or_str):
    return bytes.fromhex(to_str(bytes_or_str))
    
    
#-------------------------
# open_serial
#-------------------------    
def open_serial():
    global s
    s = serial.Serial(serialport_port,serialport_baud,parity=serial.PARITY_NONE,timeout=SERIAL_TIMEOUT)


#-------------------------
# decode_mc
#-------------------------
def decode_mc(data):
    #print('decode_mc hex_str:',data.encode('hex'))
    
    #data = to_str(data_b)
    len_2 = len(data)
    if  len_2!= 8:
        #print('decode_mc fail 1')
        return -1,0,None
        
    if (data[0]) != 0xa3:
        #print('decode_mc fail 2')
        return -1,0,None

    # check checksum
    cs = 0
    for i in range(0,len_2-1):
        #print hex((data[i]))
        cs += (data[i])
        
    #print 'cs 1:',hex(cs)
    cs = cs % 256
    #print 'cs 2:',hex(cs)

    if cs != data[len_2-1]:
        #print('decode_mc fail 3')
        return -1,0,None   

    return 0, (data[1]),data[2:7]

#-------------------------
# encode_mc
#------------------------- 
def encode_mc(cmd,axis,data):
    if axis == None and data == None:
        s1 = b'\x3a' + int_to_bytes(cmd)
    elif axis != None and data == None:
        s1 = b'\x3a' + int_to_bytes(cmd) + int_to_bytes(axis)
    else:
        s1 = b'\x3a' + int_to_bytes(cmd) + int_to_bytes(axis) + to_bytes(data)
    #s1 = '\x3a'
    #print('s1(hex):',to_hex(s1))
    # caculate cs
    cs = 0
    len_1 = len(s1)
    #print('len:',len_1)
    for i in range(0,len_1):
        cs += s1[i]
        #print('cs:',cs)
    cs = cs % 256
    #print('cs:',cs, 's1:',to_hex(s1))
    s1 = s1 + int_to_bytes(cs)

    #print('s1(hex):',to_hex(s1))
    return s1
    
#------------------
# mc_online_check
#------------------
def mc_online_check():
    global s
    open_serial()
    
    out_str = encode_mc(0x55,None,None)
    #print('write:',to_hex(out_str))
    s.write(out_str)

    time.sleep(0.01)
    resp = s.read(8)
    #print('read:',resp.hex())
    retcode,func,data = decode_mc(resp)
    s.close()    
    #print(retcode,func,data)
    if retcode == 0 and func == 0xaa:
        return 0
    else:
        return -1

#------------------
# mc_stop_rt_loc
#------------------
def mc_stop_rt_loc():
    global s
    open_serial()

    out_str = encode_mc(0xd4,None,None)
    #print('write:',out_str.encode('hex'))
    s.write(out_str)
    s.close()
    return 0

        
#------------------
# mc_get_cur_loc
#------------------
def mc_get_cur_loc(axis):
    global s
    open_serial()
    
    out_str = encode_mc(0xd2,(0xff),None)
    #print('write:',out_str.encode('hex'))
    s.write(out_str)

    time.sleep(0.01)
    resp = s.read(64)
    #print('read:',resp.encode('hex'))
    s.close()
    
    p_all = []
    i = 0
    while i < (8*8):
        retcode,func,data = decode_mc(resp[i:i+8])
        if retcode == 0:
            p = ((data[1]) << 24) + ((data[2]) << 16) + ((data[3]) << 8) + ((data[4]))
            if (data[0]) == 1:
                p = p * (-1)
            p_all.append(p)
        else:
            return -1
    
    
        i += 8
   
    return p_all[(axis-1)]
    
    
#------------------
# mc_get_axis_sts
#------------------
def mc_get_axis_sts(axis_i):
    global s
    open_serial()
    
    out_str = encode_mc(0xd6,(1 << (axis_i-1)),None)
    #print('write:',out_str.encode('hex'))
    s.write(out_str)

    time.sleep(0.01)
    resp = s.read(64)
    s.close()
    #print('read:',resp.encode('hex'))
    
    

    i = 0

    retcode,func,data = decode_mc(resp[i:i+8])
    if retcode == 0 and func == 0xb6 and (data[0]) == (1 << (axis_i-1)):
        p = ((data[1]) << 24) + ((data[2]) << 16) + ((data[3]) << 8) + ((data[4]))
        #if (data[0]) == 1:
        #    p = p * (-1)
    else:
        return -1

   
    return p

#------------------
# mc_clr_cur_loc
#------------------
def mc_clr_cur_loc():
    global s
    open_serial()
    out_str = encode_mc(0xd3,(0xff),None)
    #print('write:',out_str.encode('hex'))
    s.write(out_str)

    time.sleep(0.01)
    resp = s.read(64)
    s.close()    
    #print('read:',resp.encode('hex'))
    
    return 0

    
#------------------
# mc_get_param
#------------------
def mc_get_param(axis_i,p_n):
    global s
    open_serial()
    out_str = encode_mc(0xd5,(0xff),None)
    #print('write:',out_str.encode('hex'))
    s.write(out_str)

    time.sleep(0.01)
    resp = s.read(8*3*8)
    s.close()    
    #print('read:',resp.encode('hex'))

    p_all = []
    p = 0
    i = 0
    while i < (8*3*8):
        retcode,func,data = decode_mc(resp[i:i+8])
        if retcode == 0:
            p = ((data[1]) << 24) + ((data[2]) << 16) + ((data[3]) << 8) + ((data[4]))
            p_all.append(p)
        else:
            return -1

        i += 8
    
    return p_all[(p_n-1)*8 + (axis_i - 1)]

#---------------------
# mc_set_param
# p1 = low_speed (pulse/sec)
# p2 = speed (pulse/sec)
# p3 = accel_time (0.01s)
#---------------------
def mc_set_param(axis_i,p1,p2,p3):
    global s
    open_serial()
     
    data = int_to_bytes((p1 >> 24) & 0xff) + int_to_bytes((p1 >> 16) & 0xff) + int_to_bytes((p1 >> 8) & 0xff) + int_to_bytes(p1 & 0xff)
    data += int_to_bytes((p2 >> 24) & 0xff) + int_to_bytes((p2 >> 16) & 0xff) + int_to_bytes((p2 >> 8) & 0xff) + int_to_bytes(p2 & 0xff)   
    data += int_to_bytes((p3 >> 24) & 0xff) + int_to_bytes((p3 >> 16) & 0xff) + int_to_bytes((p3 >> 8) & 0xff) + int_to_bytes(p3 & 0xff)
    
    out_str = encode_mc(0xda,(1 << (axis_i-1)),data)
    #print('write:',out_str.encode('hex'))
    s.write(out_str)
    s.close()    
    return 0
    
#---------------------
# mc_set_param_save
# p1 = low_speed (pulse/sec)
# p2 = speed (pulse/sec)
# p3 = accel_time (0.01s)
#---------------------
def mc_set_param_save(axis_i,p1,p2,p3):
    global s
    open_serial()
     
    data = int_to_bytes((p1 >> 24) & 0xff) + int_to_bytes((p1 >> 16) & 0xff) + int_to_bytes((p1 >> 8) & 0xff) + int_to_bytes(p1 & 0xff)
    data += int_to_bytes((p2 >> 24) & 0xff) + int_to_bytes((p2 >> 16) & 0xff) + int_to_bytes((p2 >> 8) & 0xff) + int_to_bytes(p2 & 0xff)   
    data += int_to_bytes((p3 >> 24) & 0xff) + int_to_bytes((p3 >> 16) & 0xff) + int_to_bytes((p3 >> 8) & 0xff) + int_to_bytes(p3 & 0xff)
    
    out_str = encode_mc(0xdd,(1 << (axis_i-1)),data)
    #print('write:',out_str.encode('hex'))
    s.write(out_str)
    s.close()    
    return 0
    
#---------------------
# mc_stop_all
#---------------------
def mc_stop_all():
    global s
    open_serial()
    out_str = encode_mc(0xfc,0xff,b'\x4a')
    #print('write:',out_str.encode('hex'))
    s.write(out_str)
    
    time.sleep(0.01)
    resp = s.read(8)
    s.close()    
    #print('read:',resp.encode('hex'))
    retcode,func,data = decode_mc(resp)
    #print(retcode,func,data.encode('hex'))
    #if retcode == 0 and func == 0xb5:
    #    return 0
    #else:
    #    return -1

    
    return 0


#---------------------
# mc_stop_all_e
#---------------------   
def mc_stop_all_e():
    global s
    open_serial()
    out_str = encode_mc(0xfc,0xff,b'\x49')
    #print('write:',out_str.encode('hex'))
    s.write(out_str)
    time.sleep(0.01)
    resp = s.read(8)
    s.close()    
    #print('read:',resp.encode('hex'))
    retcode,func,data = decode_mc(resp)
    #print(retcode,func,data.encode('hex'))
    #if retcode == 0 and func == 0xb5:
    #    return 0
    #else:
    #    return -1
    return 0
 
#---------------------
# mc_move
#---------------------   
def mc_move(axis_i,n):
    global s
    open_serial()
    data = int_to_bytes((n >> 24) & 0xff) + int_to_bytes((n >> 16) & 0xff) + int_to_bytes((n >> 8) & 0xff) + int_to_bytes(n & 0xff)

    out_str = encode_mc(0xfb,(1 << (axis_i-1)),data)
    #print('write:',out_str.encode('hex'))
    s.write(out_str)
    s.close()    
    #time.sleep(0.01)
    #resp = s.read(8)
    #print('read:',resp.encode('hex'))    
    
    #i = 0
    #while i < tmt:
    #    print('waiting...')
    #    resp = s.read(8)
    #    if len(resp) == 8:
    #        print('read:',resp.encode('hex'))
    #        retcode,func,data = decode_mc(resp)
    #        print(retcode,func,data.encode('hex'))
    #        if retcode == 0 and func == 0xb5:
    #            return 0
    #        else:
    #            continue
    #    else:
    #        continue
    #    
    #    i += 1
    return 0
    
#---------------------
# mc_move_rel
#---------------------  
def mc_move_rel(axis_i,d,n):
    global s
    open_serial()
    data = int_to_bytes(d) + int_to_bytes((n >> 24) & 0xff) + int_to_bytes((n >> 16) & 0xff) + int_to_bytes((n >> 8) & 0xff) + int_to_bytes(n & 0xff)

    out_str = encode_mc(0xfa,(1 << (axis_i-1)),data)
    #print('write:',out_str.encode('hex'))
    s.write(out_str)
    s.close()    
    #time.sleep(0.01)
    #resp = s.read(8)
    #print('read:',resp.encode('hex'))    
    return 0
    
#---------------------
# mc_move_rel_pre
#---------------------  
def mc_move_rel_pre(axis_i,d,n):
    global s
    open_serial()
    data = int_to_bytes(d) + int_to_bytes((n >> 24) & 0xff) + int_to_bytes((n >> 16) & 0xff) + int_to_bytes((n >> 8) & 0xff) + int_to_bytes(n & 0xff)

    out_str = encode_mc(0x81,(1 << (axis_i-1)),data)
    #print('write:',out_str.encode('hex'))
    s.write(out_str)
    s.close()    
    return 0

#---------------------
# mc_move_rel_multi
#---------------------  
def mc_move_rel_multi(axis_mask):
    global s
    open_serial()

    out_str = encode_mc(0x82,(axis_mask),None)
    #print('write:',out_str.encode('hex'))
    s.write(out_str)
    s.close()
    if 0:
        i = 0
        while i < tmt:
            #print('waiting...')
            resp = s.read(8)
            if len(resp) == 8:
                #print('read:',resp.encode('hex'))
                retcode,func,data = decode_mc(resp)
                #print(retcode,func,data.encode('hex'))
                if retcode == 0 and func == 0xb8:
                    return 0
                else:
                    time.sleep(0.1)
                    continue
            else:
                time.sleep(0.1)
                continue
            
            i += 1
        
    return 0
    
    
    
#-------------------------
# main
#-------------------------
if __name__ == '__main__':

    try:
        serialport_port = sys.argv[1]
        serialport_baud = int(sys.argv[2])
        print('port:',serialport_port)
        print('baud:',serialport_baud)
        
        #s = serial.Serial(serialport_port,serialport_baud,parity=serial.PARITY_NONE,timeout=SERIAL_TIMEOUT)
        #print(s)

        print('-------------------------')       
        # test encode_mc
        s1 = encode_mc(0x55,None,None)
        if s1 == b'\x3a\x55\x8f':
            print('encode_mc passed')
        else:
            print('encode_mc failed')
            
        print('-------------------------')           
        # test decode_mc
        s1 = b'\xa3\xaa\x00\x00\x00\x00\x00\x4d'
        
        
        retcode,func,data = decode_mc(s1)
        if retcode == 0 and func == 0xaa and data == b'\x00\x00\x00\x00\x00':
            print('decode_mc passed')
        else:
            print('decode_mc failed')

        print('-------------------------')
        print('test:mc_stop_rt_loc')        
        print(mc_stop_rt_loc())
        
        time.sleep(1)
        # mc_is_online
        print('test:mc_is_online')
        print( mc_online_check())

        print('-------------------------')
        # mc_get_cur_loc(0)
        print('test:mc_get_cur_loc(1)')
        print(mc_get_cur_loc(1))

        print('-------------------------')
        # mc_clr_cur_loc(0)
        print('test:mc_clr_cur_loc')
        print(mc_clr_cur_loc())

        print('-------------------------')
        print('test:mc_get_param')
        print(mc_get_param(1,1))
        
        
        print('-------------------------')
        print('test:mc_get_axis_sts')
        print(mc_get_axis_sts(1))
          
        print('-------------------------')
        print('test:mc_set_param')
        print(mc_set_param(1,11,4000,31))
        
        #print('-------------------------')
        #print('test:mc_set_param_save')
        #print(mc_set_param_save(s,1,21,51,200))
        
        print('-------------------------')
        print('test:mc_stop_all')
        print(mc_stop_all())
        
        print('-------------------------')
        print('test:mc_stop_all_e')
        print(mc_stop_all_e())        
        

        if 0:
            print('-------------------------')
            print('mc_move_rel')

            n = 10

            while n > 0:            
                #print(mc_move(s,1,off))
                print(mc_move_rel(1,0,200))
                time.sleep(1)
                off += 200
                n -=1
            print('off:',off)


        if 1:
            print('-------------------------')
            print('mc_move_rel_pre')

            
            n = 0
            while True:            
                print('mc_move_rel_multi:',n)
                print(mc_move_rel_pre(1,0,200))
                print(mc_move_rel_pre(2,0,200))
            
                print(mc_move_rel_multi(0x03))
                print('axis loc 1:',mc_get_cur_loc(1), ' axis loc 2:',mc_get_cur_loc(2))
                

                time.sleep(1)
                #off += 200                
                n += 1
                
        
    except Exception as e:
        print('init serial error!',str(e))
        sys.exit(-1)
