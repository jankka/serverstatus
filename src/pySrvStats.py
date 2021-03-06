'''
Created on 31.7.2013

@author: janmatilainen
'''
import subprocess

class SrvStats(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def cpu(self, appname):
        self.appname = appname
        """Return float containing CPU -usage used by defined application name."""

        self.process = subprocess.Popen("ps -o pcpu -p `ps -ef | grep -i %s | grep -v grep |grep -v Users| awk '{ print $2 }'`"
                                        % self.appname,
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        )
        self.cpu = self.process.communicate()[0].split('\n')
        #print self.cpu
        if len(self.cpu) >= 1:
            return float(self.cpu[1])
        else:
            return "NO CPU INFO FOR " + str(self.appname)
    def top(self):
        """ Returns 10 most memory consuming applications on the host """
        """ OS X TOP Uses different syntax and parameters than linux"""

        self.process = subprocess.Popen("top -stats pid,rsize,vsize,cpu,th,pstate,time,command -o cpu -O +rsize -s 2 -n 10 -l 2| grep -A10 PID",
#     OSX top -line is commented. Uncomment in case running in OSX
        #self.process = subprocess.Popen("top -b -n 2 | grep -A10 PID",
                                        shell=True,
                                        stdout=subprocess.PIPE)
        self.top = self.process.communicate()[0].split('\n')
        """ Since the first captured top output does not contain the wanted data, we remove the first 13 elements"""
        for x in xrange(12):
            del self.top[0]
        return self.top

    def appTop(self,appname):
                """ Returns TOP -information from the system """
                """ PID,USER      PR  NI  VIRT  RES  SHR S  %CPU %MEM    TIME+  COMMAND"""
                """ @TODO: Change the way to get the pid. There should be function for that"""
        self.appname = appname
        #print self.appname
        self.app = subprocess.Popen("ps -ef | grep -i %s " % self.appname,
                                        shell=True,
                                        stdout=subprocess.PIPE)
        self.appPid = self.app.communicate()[0].split()
        #print self.appPid

###        self.process = subprocess.Popen("top -pid %s -stats pid,rsize,vsize,cpu,th,pstate,time,command -o cpu -O +rsize -s 2 -n 1 -l 2| grep -A10 PID" % self.appPid[1],
###     OSX top -line is commented. Uncomment in case running in OSX
        self.process = subprocess.Popen("top -p%s -b -n 1 | grep -A10 PID" % self.appPid[1],
                                        shell=True,
                                        stdout=subprocess.PIPE)
        self.appTop = self.process.communicate()[0].split('\n')
        #print self.appTop[1]
        return self.appTop[1]

    def mem(self, appname):
        self.appname = appname

        self.app = subprocess.Popen("ps -ef | grep -i %s | awk '{ print $2 }'" % self.appname,
                                        shell=True,
                                        stdout=subprocess.PIPE)
        self.appPid = self.app.communicate()[0].split('\n')
        #print self.appPid[0]

        """OSX top -line is commented. Uncomment in case running in  OSX"""
#        self.meminfo = subprocess.Popen("top -pid %s -stats rsize,vsize -s 2 -n 1 -l 2| grep -A2 RSIZE" % self.appPid[0],

        self.meminfo = subprocess.Popen("top -p%s -b -n 1| grep -A2 PID" % self.appPid[0],
                                        shell=True,
                                        stdout=subprocess.PIPE)
        self.appMem = self.meminfo.communicate()[0].split('\n')
        #print self.appMem
        return self.appMem[1]

    def threads(self, appname):
        self.appname = appname
        self.app = subprocess.Popen("ps -ef | grep -i %s | awk '{ print $2 }'" % self.appname,
                                        shell=True,
                                        stdout=subprocess.PIPE)
        self.appPid = self.app.communicate()[0].split('\n')
        #print self.appPid[0]

        self.threadInfo = subprocess.Popen("lsof -p %s | wc -l" % self.appPid[0],
                                        shell=True,
                                        stdout=subprocess.PIPE)
        self.appThreads = self.threadInfo.communicate()[0].split('\n')
        myThreads = str(self.appThreads[0]).split()

        return myThreads[0]

