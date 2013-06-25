from datetime import datetime

# change to K for 1000, Ki for 1024
units="Ki" 

def humanreadable(amt):
    if units=="Ki":
        return humanreadableKi(amt)
    else:
        return humanreadableK(amt)

def humanreadableK(amt):
    if amt<1000000:
        return "%2.2f KB" % (amt/1000.0,)
    if amt<1000000000:
        return "%2.2f MB" %  (amt/1000000.0,)
    return "%2.2f GB" % (amt/1000000000.0,)

def humanreadableKi(amt):
    if amt<2**20:
        return "%2.2f KiB" % (amt/2**10.0,)
    if amt<2**30:
        return "%2.2f MiB" %  (amt/2**20.0,)
    return "%2.2f GiB" % (amt/2**30.0,)


def getdtfromtimestamp(timestamp):
    year = int(timestamp[0:4])
    month = int(timestamp[4:6])
    day = int(timestamp[6:8])
    hour = int(timestamp[8:10])
    minute = int(timestamp[10:12])
    return datetime(year, month, day, hour, minute)

class reportbatcher(object):
    
    def __init__(self, csv_input_flo):
        self.hours = {}
        skip = 1
        for line in csv_input_flo:
            skip = skip - 1
            if skip < 0:
                line = line.rstrip()
                fields = line.split(",")
                down = float(fields[1])
                up = float(fields[2])
                self.tally(entry(fields[0], down, up))
        self.report(self.hours)
        
    def report(self, hourdata):
        print "Internet bandwidth usage report"
        print "%20s%20s%20s" % ("Hour Beginning","Download","Upload")
        for hourlist in sorted(hourdata):
            down, up = self.computetrafficforhour(hourlist)
            print "%20s%20s%20s" % (hourlist, humanreadable(down), humanreadable(up))
        
        
    def tally(self, entry):
        key = entry.timestamp[0:10] # up to and including the hour
        if not key in self.hours:
            self.hours[key] = [entry]
        else:
            self.hours[key].append(entry)
            
    def computetrafficforhour(self, key):
        if not key in self.hours:
            return 0
        if len(self.hours[key])==1: # only got value at minute 2
            return 0
        startdown = self.hours[key][0].downstream
        startup  = self.hours[key][0].upstream
        total_down = 0
        total_up = 0
        accumulator_down = -startdown
        accumulator_up = -startup
        lastdownstream = startdown
        lastupstream = startup
        checksum = 0
        checksum_up = 0
        for entry in self.hours[key][1:]:
            # downstream
            if entry.downstream >= lastdownstream:
                checksum += entry.downstream-lastdownstream
                lastdownstream = entry.downstream
                total_down = entry.downstream
            else:
                # logout during hour?
                accumulator_down += lastdownstream
                lastdownstream = entry.downstream
                total_down += entry.downstream
            # upstream
            if entry.upstream >= lastupstream:
                checksum_up += entry.upstream-lastupstream
                lastupstream = entry.upstream
                total_up = entry.upstream
            else:
                # amount dropped, so we rebooted somewhere
                accumulator_up += lastupstream
                lastupstream = entry.upstream
                total_up += entry.upstream 
        return (total_down + accumulator_down, total_up + accumulator_up)
        
class entry(object):
    
    def __init__(self, timestamp, downstream, upstream):
        self.timestamp = timestamp
        self.downstream = downstream
        self.upstream = upstream
        self.dt = getdtfromtimestamp(self.timestamp)
    
    def __repr__(self):
        return "%s\tDown:%s\tUp:%s" % (self.dt, humanreadable(self.downstream), humanreadable(self.upstream))
        

batcher = reportbatcher(open("/home/steven/bandwidth.csv","r"))

