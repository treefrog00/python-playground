import os


class MemoryMonitor:
    _scale = {'kB': 1024.0, 'mB': 1024.0 * 1024.0,
              'KB': 1024.0, 'MB': 1024.0 * 1024.0}

    _proc_status = '/proc/%d/status' % os.getpid()

    @classmethod
    def _vmb(cls, VmKey):
        """Private.
        """
        # get pseudo file  /proc/<pid>/status
        try:
            t = open(cls._proc_status)
            v = t.read()
            t.close()
        except:
            return 0.0  # non-Linux?
            # get VmKey line e.g. 'VmRSS:  9999  kB\n ...'
        i = v.index(VmKey)
        v = v[i:].split(None, 3)  # whitespace
        if len(v) < 3:
            return 0.0  # invalid format?
            # convert Vm value to bytes
        return (float(v[1]) * cls._scale[v[2]])

    @classmethod
    def peak(cls):
        t = open(cls._proc_status)
        v = t.read()
        t.close()
        i = v.index('VmPeak')
        v = v[i:].split(None, 3)
        return float(v[1])

    @classmethod
    def memory(cls, since=0.0):
        """Return memory usage in bytes.
        """
        return cls._vmb('VmSize:') - since

    @classmethod
    def resident(cls, since=0.0):
        """Return resident memory usage in bytes.
        """
        return cls._vmb('VmRSS:') - since

    @classmethod
    def stacksize(cls, since=0.0):
        """Return stack size in bytes.
        """
        return cls._vmb('VmStk:') - since

    @classmethod
    def print_mem(cls):
        print("Memory: {} MB".format(cls.memory() / 1024 / 1024))
        print("Resident: {} MB".format(cls.resident() / 1024 / 1024))
        print("Peak: {} MB".format(cls.peak() / 1024))  # this is in kb


def example():
    MemoryMonitor.print_mem()
