#!/usr/bin/env python
# -*- coding: utf-8 -*-


def main(filename=None):
    xdata      = []
    xdata1     = []
    xdata2     = []
    xdata3     = []

    BufferSize = []
    FrameTime =  []
    DrainEncodermOutputStream = []
    CreateTime = []

    if filename is None:
        filename = "data/sample.txt"

    fd = open(filename, 'r')
    i = 0
    j = 0
    k = 0
    g = 0
 
    while 1:
        line = fd.readline()
        if not line:
            break
        else:
            sl = line.split("reInint:0, drainEncoder bufferSize: ")
            if len(sl) > 1:                
                BufferSize.append(int((sl[1]).strip()))
                # xdata.append((line.split("\t")[0]).strip())
                xdata.append(i)
                i += 1

            sl = line.split("create per frame time:")
            if len(sl) > 1:
                CreateTime.append(int((sl[1]).strip()))
                # xdata1.append((line.split("\t")[0]).strip())
                xdata1.append(g)
                g += 1

            sl = line.split("frame to frame time:")
            if len(sl) > 1:
                FrameTime.append(int((sl[1]).strip()))
                # xdata1.append((line.split("\t")[0]).strip())
                xdata2.append(j)
                j += 1

            sl = line.split("drainEncoder mOutputStream write time:")
            if len(sl) > 1:
                DrainEncodermOutputStream.append(int((sl[1].split("ms")[0]).strip()))
                # xdata1.append((line.split("\t")[0]).strip())
                xdata3.append(k)
                k += 1

    fd.close()
    
    if DrainEncodermOutputStream == []:
        DrainEncodermOutputStream = [0] * len(BufferSize)
        xdata3 = xdata

    o = {
        "xdata":xdata,
        "xdata1":xdata1,
        "xdata2":xdata2,
        "xdata3":xdata3,
        "BufferSize":BufferSize,
        "CreateTime":CreateTime,
        "FrameTime":FrameTime,
        "DrainEncodermOutputStream":DrainEncodermOutputStream        
    }

    import json

    s = json.dumps(o, indent=2)

    s = "var data_from_log = " + s

    fd = open("static/data/data.js", 'w')
    fd.write(s)
    fd.close()

    import os
    now_dir = os.getcwd()

    file_path = os.path.join(now_dir, "index.html")

    url = "file://" + file_path

    import webbrowser

    webbrowser.open_new_tab(url)


if __name__ == '__main__':
    import sys, os
    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            main(sys.argv[1])
        else:
            main()
    else:
        main()