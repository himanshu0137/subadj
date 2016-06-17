#Written by Himanshu Bansal
from sys import argv
if len(argv) == 1:
	print "No argument supplied"
	exit()
if len(argv) > 6:
	print "Too many arguments"
	exit()
if argv[1] == "-help" or argv[1] == "/?":
	print "Subtitle adjustment program written in python by Himanshu Bansal."
	print "Usage is -\n\tpython {} [file location] [adjustment in minutes] [adjustment in seconds] [adjustment in miliseconds]".format(argv[0])
	exit()
u = argv[1].replace("\\","\\\\")
try:
	f = repr(open(u,"r").read().decode("utf-8-sig").encode("utf-8")).strip("'")
except:
	print "File not found or incorrect path"
	exit()

e = open(u[:-4]+"new.srt","w")
l = f.split("\\n\\n")[:-1]                   #Every subtitle is separeted by 2 new lines
adj = [0]+map(int,argv[2:])                  #Adjustments
h = [0,60,60,1000]                           #array used for time formulation
n = 1
for i in l:
	q = i.split("\\n")                         #Each subtitle is divided in 3 parts
	#print q[0],q[1],q[2:]                     #serial number of subtitle,duration,lines 
	se = q[1].split(" --> ")                   #duration have 2 parts start time and end time
	time = ""
	t = [[0]*4,[0]*4]                          #array row 1 start time h,m,s,ms elements
	for j in [0,1]:                            #array row 2 end time h,m,s,ms elements
		a,b = se[j].split(",")
		t[j][3] = int(b)
		t[j][0],t[j][1],t[j][2] = map(int,a.split(":"))
	
		for k in [3,2,1]:                       #no adjustment for hours..... you know why
			t[j][k] += adj[k]
			if t[j][k] >= h[k]:
				t[j][k-1] += 1
				t[j][k] -= h[k]
			if t[j][k] < 0:
				t[j][k-1] -= 1
				t[j][k] += h[k]
		
		time += "{:2}:{:2}:{:2},{:3}".format(t[j][0],t[j][1],t[j][2],t[j][3]).replace(" ","0")
		if j == 0:
			time += " --> "
	subtitle = str(n)+"\n"+time+"\n"
	for v in q[2:]:
		subtitle += v.replace("\\","")+"\n"
	e.write(subtitle+"\n")
	n += 1
print "\nNew adjusted subtitle are placed in the same folder as provided in the argument with the same name just added \"new\" in the last."
e.close()
#print l,len(l)