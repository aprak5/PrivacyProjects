"""
File: ModelInversionAttack.py
Author: Amit Prakash
Purpose: Use a given model to determine sensitive information such as genotype and dosage infotmation for warfarin.
"""

# Import all necessary modules/libraries
from math import isclose

"""
Compute genotypes (sensitive attribute) using different characteristics and known correlations.
"""
def computeGenotypes(warfarin_dosage, age, height, weight, asian, black, mixed_unknown, enzyme_inducer_status, amiodarone):
        VKORC1_dict = {'VKORC1 A/G': -0.8677, 'VKORC1 A/A': -1.6974, 'VKORC1 Unknown': -0.4854, 'VKORC1 Not Present': 0}
        CYP2C9_dict = {'CYP2C9 *1/*2': -0.5211, 'CYP2C9 *1/*3': -0.9357, 'CYP2C9 *2/*2': -1.0616, 
                       'CYP2C9 *2/*3': -1.9206, 'CYP2C9 *3/*3': -2.3312, 'CYP2C9 unknown': -0.2188, 'CYP2C9 Not Present': 0}
        genotype_warfarin_dosage = 5.6044
        genotype_warfarin_dosage -= (0.2614 * age)
        genotype_warfarin_dosage += (0.0087 * height)
        genotype_warfarin_dosage += (0.0128 * weight)
        genotype_warfarin_dosage -= (0.1092 * asian)
        genotype_warfarin_dosage -= (0.2760 * black)
        genotype_warfarin_dosage -= (0.1032 * mixed_unknown)
        genotype_warfarin_dosage += (1.1816 * enzyme_inducer_status)
        genotype_warfarin_dosage -= (0.5503 * amiodarone)
        for k, v in VKORC1_dict.items():
            for l, w in CYP2C9_dict.items():
                if(isclose(warfarin_dosage, ((genotype_warfarin_dosage + v + w)**2), abs_tol=1e-1)):
                    return [k, l, ((genotype_warfarin_dosage + v + w)**2)]

"""
Populate with numbers associated with the different variables and give an exact dose with the genotypes.
"""
def main():
    outputList = computeGenotypes(21, 5, 175, 72, 0, 0, 0, 1, 1)
    print("The genotypes are " + str(outputList[0]) + " and " + str(outputList[1]) + " with an exact dosage of " + str(outputList[2]) + " mg/week.")

# Run the main method
if __name__ == "__main__":
    main()