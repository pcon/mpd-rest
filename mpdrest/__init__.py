def shutdown():
    cherrypy.enginer.exit()

def sig_handler(signum=None, frame=None):
    if type(signum) != type(None):
        print "Signal %i caught, saving and exiting..." % int(signum)
        shutdown()
    else:
        print "Got a nonetype signum"