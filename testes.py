import tclab

TCLab = tclab.setup(connected=False, speedup=10)

with TCLab() as lab:
    h = tclab.Historian(lab.sources)
    def log_values():
        for t in tclab.clock(20):
            lab.Q1(100 if t <= 15 else 0)
            print("Time:", t, 'seconds')
            print("T1:",lab.T1)
            h.update(t)
    log_values()

    
 