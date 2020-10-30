from __future__ import print_function

from pdbfixer import PDBFixer
from simtk.openmm.app.pdbfile import PDBFile
from simtk.openmm import app
import simtk.openmm.app.data
import simtk.openmm.app.data.charmm36
from simtk.unit import *
from sys import stdout
import parmed as pmd
import numpy as np
import time
import os


def fix_pdb(pdb_id):
    path = os.getcwd()
    if len(pdb_id) != 4:
        print("Creating PDBFixer...")
        fixer = PDBFixer(pdb_id)
        print("Finding missing residues...")
        fixer.findMissingResidues()

        chains = list(fixer.topology.chains())
        keys = fixer.missingResidues.keys()
        for key in list(keys):
            chain = chains[key[0]]
            if key[1] == 0 or key[1] == len(list(chain.residues())):
                print("ok")
                del fixer.missingResidues[key]

        print("Finding nonstandard residues...")
        fixer.findNonstandardResidues()
        print("Replacing nonstandard residues...")
        fixer.replaceNonstandardResidues()
        print("Removing heterogens...")
        fixer.removeHeterogens(keepWater=True)

        print("Finding missing atoms...")
        fixer.findMissingAtoms()
        print("Adding missing atoms...")
        fixer.addMissingAtoms()
        print("Adding missing hydrogens...")
        fixer.addMissingHydrogens(7)
        print("Writing PDB file...")

        PDBFile.writeFile(
            fixer.topology,
            fixer.positions,
            open(os.path.join(path, "%s_fixed_pH_%s.pdb" % (pdb_id.split('.')[0], 7)),
                 "w"),
            keepIds=True)
        return "%s_fixed_pH_%s.pdb" % (pdb_id.split('.')[0], 7)


fix_pdb('2h6o.pdb')
