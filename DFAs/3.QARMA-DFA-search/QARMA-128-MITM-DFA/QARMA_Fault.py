from CPFault import *
from gurobipy import *

class Vars_generator:
    def genVars_input_of_SB(r):
        return ['X_' + str(j) + '_r' + str(r) for j in range(16)]

    def genVars_input_of_MC(r):
        return ['Y_' + str(j) + '_r' + str(r) for j in range(16)]

    def genVars_input_of_SC(r):
        return ['Z_' + str(j) + '_r' + str(r) for j in range(16)]

    def genVars_input1_of_SB(r):
        return ['IS1_' + str(j) + '_r' + str(r) for j in range(16)]
    def genVars_input2_of_SB(r):
        return ['IS2_' + str(j) + '_r' + str(r) for j in range(16)]

    @staticmethod
    def genVars_input1_of_MC(r):
        return ['MC1_' + str(j) + '_r' + str(r) for j in range(16)]
    @staticmethod
    def genVars_input2_of_MC(r):
        return ['MC2_' + str(j) + '_r' + str(r) for j in range(16)]

    def genVars_input1_of_SC(r):
        return ['SC1_' + str(j) + '_r' + str(r) for j in range(16)]
    def genVars_input2_of_SC(r):
        return ['SC2_' + str(j) + '_r' + str(r) for j in range(16)]

    def genVars_Keyguess():
        return ['KG_' + str(j) for j in range(32)]

    def genVars_Keyguess1():
        return ['KG1_' + str(j) for j in range(32)]

    def genVars_Keyguess2():
        return ['KG2_' + str(j) for j in range(32)]

    def genVars_KeyguessBlue():
        return ['KGB_' + str(j) for j in range(32)]

    def genVars_KeyguessRed():
        return ['KGR_' + str(j) for j in range(32)]

    def genVars_KeyguessN():
        return ['KGN_' + str(j) for j in range(32)]


class Constraints_generator():

    def __init__(self, total_round, match_round):
        self.mat_r = match_round
        self.TR = total_round


    def genConstraints_of_encrypt(self,r):
        input_sb = Vars_generator.genVars_input_of_SB(r)
        input_mc = Vars_generator.genVars_input_of_MC(r)
        input_sc = Vars_generator.genVars_input_of_SC(r)
        output_round = Vars_generator.genVars_input_of_SB(r+1)

        constr = []
        #constraints for SB
        constr = constr + MITMPreConstraints.equalConstraints(input_sb,input_mc)

        #constraints for MC
        for i in range(4):
            constr = constr + MITMPreConstraints.MC_constraint(input_mc[i], input_mc[4+i], input_mc[8+i], input_mc[12+i],
                                                               input_sc[i], input_sc[4+i], input_sc[8+i], input_sc[12+i])

        #constraints for SC
        constr = constr + MITMPreConstraints.equalConstraints(SC_inv(input_sc), output_round)

        return constr

    def genConstraints_of_matchinground(self):
        input_sb = Vars_generator.genVars_input_of_SB(self.mat_r)
        input_mc = Vars_generator.genVars_input_of_MC(self.mat_r)
        input_sc = Vars_generator.genVars_input_of_SC(self.mat_r)
        input1_sc = Vars_generator.genVars_input1_of_SC(self.mat_r)
        input2_sc = Vars_generator.genVars_input2_of_SC(self.mat_r)
        output1_round = Vars_generator.genVars_input1_of_SB(self.mat_r+1)
        output2_round = Vars_generator.genVars_input2_of_SB(self.mat_r + 1)


        constr = []
        # constraints for SB
        constr = constr + MITMPreConstraints.equalConstraints(input_sb, input_mc)

        # constraints for Match
        for i in range(4):
            constr = constr + MITMPreConstraints.Match_constraint(input_mc[i],input_mc[4+i],input_mc[8+i],input_mc[12+i],
                                                                  input_sc[i],input_sc[4+i],input_sc[8+i],input_sc[12+i])

        constr = constr + [BasicTools.plusTerm(input_sc) + ' = 2']

        # split
        for i in range(4):
            constr = constr + MITMPreConstraints.split_constraint(input_sc[i],input_sc[4+i],input_sc[8+i],input_sc[12+i],
                                                                  input1_sc[i],input1_sc[4+i],input1_sc[8+i],input1_sc[12+i],
                                                                  input2_sc[i],input2_sc[4+i],input2_sc[8+i],input2_sc[12+i])

        #SC
        constr = constr + MITMPreConstraints.equalConstraints(SC_inv(input1_sc), output1_round)
        constr = constr + MITMPreConstraints.equalConstraints(SC_inv(input2_sc), output2_round)
        return constr

    def genConstraints_of_decrypt(self, r):
        input1_sb = Vars_generator.genVars_input1_of_SB(r)
        input2_sb = Vars_generator.genVars_input2_of_SB(r)

        input1_mc = Vars_generator.genVars_input1_of_MC(r)
        input2_mc = Vars_generator.genVars_input2_of_MC(r)

        input1_sc = Vars_generator.genVars_input1_of_SC(r)
        input2_sc = Vars_generator.genVars_input2_of_SC(r)

        output1_round = Vars_generator.genVars_input1_of_SB(r+1)
        output2_round = Vars_generator.genVars_input2_of_SB(r+1)

        constr = []
        #SB
        constr = constr + MITMPreConstraints.equalConstraints(input1_sb, input1_mc)
        constr = constr + MITMPreConstraints.equalConstraints(input2_sb, input2_mc)

        #MC
        for i in range(4):
            constr = constr + MITMPreConstraints.MCguess_constraint(input1_mc[i],input1_mc[4+i],input1_mc[8+i],input1_mc[12+i],
                                                                    input1_sc[i],input1_sc[4+i],input1_sc[8+i],input1_sc[12+i])
            constr = constr + MITMPreConstraints.MCguess_constraint(input2_mc[i], input2_mc[4 + i], input2_mc[8 + i],
                                                                    input2_mc[12 + i],
                                                                    input2_sc[i], input2_sc[4 + i], input2_sc[8 + i],
                                                                    input2_sc[12 + i])

        #SC
        constr = constr + MITMPreConstraints.equalConstraints(SC_inv(input1_sc), output1_round)
        constr = constr + MITMPreConstraints.equalConstraints(SC_inv(input2_sc), output2_round)
        return constr


    def genConstraints_keyguess(self):
        KG1 = Vars_generator.genVars_Keyguess1()
        KG2 = Vars_generator.genVars_Keyguess2()

        K01 = []
        K02 = []

        constr = []
        for r in range(self.mat_r + 1,self.TR-1):
            K01.append(Vars_generator.genVars_input1_of_MC(r))
            K02.append(Vars_generator.genVars_input2_of_MC(r))

        '''
        for r in range(self.mat_r + 1, self.TR):
            for i in range(0, self.TR-1-r):
                K01[r - self.mat_r - 1] = tweak_perm(K01[r - self.mat_r - 1])
                K02[r - self.mat_r - 1] = tweak_perm(K02[r - self.mat_r - 1])
        '''

        K11 = Vars_generator.genVars_input1_of_MC(self.TR - 1)
        K12 = Vars_generator.genVars_input2_of_MC(self.TR - 1)
        for i in range(0,16):
            X=[]
            for v in K01:
                X.append(v[i])
            constr = constr + MITMPreConstraints.OR_constraint(X, KG1[i])

        for i in range(0,16):
            constr = constr + [K11[i] + ' - ' + KG1[16+i] + ' = 0']

        for i in range(0, 16):
            X = []
            for v in K02:
                X.append(v[i])
            constr = constr + MITMPreConstraints.OR_constraint(X, KG2[i])

        for i in range(0,16):
            constr = constr + [K12[i] + ' - ' + KG2[16+i] + ' = 0']

        return constr


    def genConstraints_total(self):
        inputsb = Vars_generator.genVars_input_of_SB(0)
        KG1 = Vars_generator.genVars_Keyguess1()
        KG2 = Vars_generator.genVars_Keyguess2()
        KGB = Vars_generator.genVars_KeyguessBlue()
        KGR = Vars_generator.genVars_KeyguessRed()
        KGN = Vars_generator.genVars_KeyguessN()
        KG = Vars_generator.genVars_Keyguess()
        constr = []
        constr = constr + [BasicTools.plusTerm(inputsb) + ' = 1']
        for r in range(0, self.mat_r):
            constr = constr + self.genConstraints_of_encrypt(r)
        constr = constr + self.genConstraints_of_matchinground()

        for r in range(self.mat_r + 1,self.TR):
            constr = constr + self.genConstraints_of_decrypt(r)

        constr = constr + self.genConstraints_keyguess()

        for i in range(32):
            constr = constr + MITMPreConstraints.ORm_constraint(KG1[i], KG[i], KGB[i])
            constr = constr + MITMPreConstraints.ORm_constraint(KG2[i], KG[i], KGR[i])

        for i in range(32):
            constr = constr + MITMPreConstraints.OR_constraint([KGB[i], KGR[i]], KGN[i])

        constr = constr + ['Deg1' + ' - ' + BasicTools.MinusTerm(KGB) + ' = 0']
        constr = constr + ['Deg2' + ' - ' + BasicTools.MinusTerm(KGR) + ' = 0']
        constr = constr + ['DegG' + ' + ' + BasicTools.plusTerm(KGN) + ' + ' + BasicTools.plusTerm(KG) + ' = 32']

        return constr



    def genModel(self,filename):
        V = set([])
        constr = list([])
        constr = constr + self.genConstraints_total()

        constr = constr + ['DObj - Deg1 >= 0']
        constr = constr + ['DObj - Deg2 >= 0']
        constr = constr + ['Deg1 + Deg2 >= 1']
        constr = constr + ['DObj <= 5']
        V = BasicTools.getVariables_From_Constraints(constr)

        fid = open('./qarma/TR' + str(self.TR) + '_matr' + str(self.mat_r) + '.lp', 'w')

        fid.write('Minimize' + '\n')
        fid.write('DObj + DegG' + '\n')
        fid.write('\n')
        fid.write('Subject To')
        fid.write('\n')
        for c in constr:
            fid.write(c)
            fid.write('\n')

        GV = []
        BV = []
        for v in V:
            if v[0] == 'D':
                GV.append(v)
            else:
                BV.append(v)

        fid.write('Binary' + '\n')
        for bv in BV:
            fid.write(bv + '\n')

        fid.write('Generals' + '\n')
        for gv in GV:
            fid.write(gv + '\n')

        fid.close()


def cmd():
    TR = 4
    mat_r = 1
    name = './qarma/TR' + str(TR) + '_matr' + str(mat_r)
    A = Constraints_generator(TR, mat_r)
    A.genModel('')
    counter = 0
    inject_num = 1
    Fault = []
    KGB = []
    KGR = []
    MB = []
    MR = []
    m = read(name + '.lp')
    for v in m.getVars():
        if (v.VarName[0:3] == 'KG_'):
            v.ub = 0
    m.update()
    while counter < 28:
        m.optimize()

        # Gurobi syntax: m.Status == 2 represents the model is feasible.
        if m.Status == 2:
            m.write(name + '_' + str(inject_num) + '.sol')
            solFile = open('./' + name + '_' + str(inject_num) + '.sol', 'r')
            Sol = dict()

            for line in solFile:
                if line[0] != '#':
                    temp = line
                    temp = temp.replace('-', ' ')
                    temp = temp.split()
                    # Sol[temp[0]] = float(temp[1]+'0')
                    Sol[temp[0]] = float(temp[1])

            inject_num += 1
            fault = []
            KG1 = []
            KG2 = []
            M1 = []
            M2 = []
            varn = []
            for v in m.getVars():
                if (v.x == 1) and (v.VarName[0:3] == 'KGB'):
                    KG1.append(v.VarName)
                if (v.x == 1) and (v.VarName[0:3] == 'KGR'):
                    KG2.append(v.VarName)
                if (v.VarName[0:3] == 'SC1') and (v.VarName[len(v.VarName) - 1] == str(mat_r)) and (v.x == 1):
                    M1.append(v.VarName)
                if (v.VarName[0:3] == 'SC2') and (v.VarName[len(v.VarName) - 1] == str(mat_r)) and (
                        v.x == 1):
                    M2.append(v.VarName)
                if (v.x == 1) and (v.VarName[0:2] == 'X_') and (v.VarName[len(v.VarName) - 1] == '0'):
                    vtemp = v
                    v.lb = 1
                    fault.append(v.VarName)
                if (v.x == 1) and (v.VarName[0:3] == 'KGN'):
                    counter += 1
                    if (len(v.VarName) == 5):
                        varn.append('KG_' + str(v.VarName[4]))
                    if (len(v.VarName) == 6):
                        varn.append('KG_' + str(v.VarName[4:6]))
            for u in varn:
                for v in m.getVars():
                    if (v.VarName == u):
                        v.ub = 1
                        v.lb = 1
            m.update()
            Fault.append(fault)
            KGB.append(KG1)
            KGR.append(KG2)
            MB.append(M1)
            MR.append(M2)
        elif m.Status == 3:
            if vtemp.lb == 1:
                vtemp.lb = 0
                vtemp.ub = 0
                m.update()
            else:
                break

    fileobj = open(name + 'result.txt', "w")
    fileobj.write("Fault\n")
    for h in Fault:
        fileobj.write(", ".join(h))
        fileobj.write("\n")
    fileobj.write("\nMB\n")
    for h in MB:
        fileobj.write(", ".join(h))
        fileobj.write("\n")
    fileobj.write("\nMR\n")
    for h in MR:
        fileobj.write(", ".join(h))
        fileobj.write("\n")
    fileobj.write("\nKGB\n")
    for h in KGB:
        fileobj.write(", ".join(h))
        fileobj.write("\n")
    fileobj.write("\nKGR\n")
    for h in KGR:
        fileobj.write(", ".join(h))
        fileobj.write("\n")

    fileobj.close()



if __name__== "__main__":
    cmd()













