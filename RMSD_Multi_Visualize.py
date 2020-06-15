import numpy as npfrom MDAnalysis.analysis.rms import rmsdimport MDAnalysisimport matplotlibimport matplotlib.pyplot as plt############################# INPUTS #############################################topology = ['protein.pdb','protein2.pdb']trajectory = ['50_frame.dcd', 'fram2.dcd']def RMSD(top, trj, ax, color_id):    u = MDAnalysis.Universe(top, trj)    # one AtomGroup per domain    domains = {        'Calpha RMSD': u.select_atoms("protein and (name C or name N or name CA)"),        'All Atom RMSD (noH)': u.select_atoms("protein and not name H*"),        }    colors = {'Calpha RMSD': 'green', 'All Atom RMSD (noH)': 'red'}    u.trajectory[0]   # rewind trajectory    xref0 = dict((name, g.positions - g.center_of_mass()) for name, g in domains.items())    nframes = len(u.trajectory)    results = dict((name, np.zeros((nframes, 2), dtype=np.float64)) for name in domains)    for iframe, ts in enumerate(u.trajectory):        for name, g in domains.items():            results[name][iframe, :] = (u.trajectory.frame,                                        rmsd(g.positions, xref0[name],                                             center=True, superposition=True))    # fig = plt.figure(figsize=(5,5))    #    # ax = fig.add_subplot(111)    from matplotlib.cm import get_cmap    name = "Accent"    cmap = get_cmap(name)    colors = cmap.colors    for name in "Calpha RMSD", "All Atom RMSD (noH)":        print(name)        label_ID = str(top.split('.')[0])+"/ "+name        data = results[name]        ax.plot(data[:,0], data[:,1], linestyle="-", color=colors[color_id], lw=2, label=label_ID)    ax.legend(loc="best")    ax.set_xlabel("Frame")    ax.set_ylabel(r"RMSD of Backbone ($\AA$)")    return name, results, colors, axfig = plt.figure(figsize=(5,5))ax = fig.add_subplot(111)for i in range(len(topology)):    name, results, colors, ax = RMSD(topology[i],trajectory[i],ax, i)    ax.plot()plt.show()