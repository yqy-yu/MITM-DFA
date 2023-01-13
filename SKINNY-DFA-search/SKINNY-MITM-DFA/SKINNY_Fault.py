from CPFault import *
from gurobipy import *

class Vars_generator:
    @staticmethod
    def genVars_input_of_SC(r):
        return ['X_' + str(j) + '_r' + str(r) for j in range(16)]

    @staticmethod
    def genVars_input_of_SR(r):
        return ['Y_' + str(j) + '_r' + str(r) for j in range(16)]

    @staticmethod
    def genVars_input_of_MC(r):
        return ['Z_' + str(j) + '_r' + str(r) for j in range(16)]

    @staticmethod
    def genVars_output_of_matching(r):
        return ['match_' + str(j) + '_r' + str(r) for j in range(16)]

    def genVars_input1_of_SC(r):
        return ['IS1_' + str(j) + '_r' + str(r) for j in range(16)]
    def genVars_input2_of_SC(r):
        return ['IS2_' + str(j) + '_r' + str(r) for j in range(16)]

    @staticmethod
    def genVars_input1_of_SR(r):
        return ['SR1_' + str(j) + '_r' + str(r) for j in range(16)]
    @staticmethod
    def genVars_input2_of_SR(r):
        return ['SR2_' + str(j) + '_r' + str(r) for j in range(16)]

    def genVars_input1_of_MC(r):
        return ['M1_' + str(j) + '_r' + str(r) for j in range(16)]
    def genVars_input2_of_MC(r):
        return ['M2_' + str(j) + '_r' + str(r) for j in range(16)]

    def genVars_Keyguess():
        return ['KG_'+str(j) for j in range(16)]

    def genVars_Keyguess1():
        return ['KG1_'+str(j) for j in range(16)]

    def genVars_Keyguess2():
        return ['KG2_'+str(j) for j in range(16)]

    def genVars_KeyguessBlue():
        return ['KGB_'+str(j) for j in range(16)]

    def genVars_KeyguessRed():
        return ['KGR_'+str(j) for j in range(16)]

    def genVars_KeyguessN():
        return ['KGN_'+str(j) for j in range(16)]


class Constraints_generator():

    def __init__(self, total_round, match_round):
        self.mat_r = match_round
        self.TR = total_round


    def genConstraints_of_encrypt(self,r):
        input_sc = Vars_generator.genVars_input_of_SC(r)
        input_sr = Vars_generator.genVars_input_of_SR(r)
        input_mc = Vars_generator.genVars_input_of_MC(r)
        output_round = Vars_generator.genVars_input_of_SC(r+1)

        constr = []
        #constraints for SC
        for i in range(16):
            constr = constr + [input_sc[i] + ' - ' + input_sr[i] + ' = 0']

        #constraints for SR
        constr = constr + MITMPreConstraints.equalConstraints(SR(input_sr),input_mc)

        #constraints for MC
        for i in range(4):
            constr = constr + MITMPreConstraints.MC_constraint(input_mc[i],input_mc[4+i],input_mc[8+i],input_mc[12+i],
                                                               output_round[i],output_round[4+i],output_round[8+i],output_round[12+i])
        return constr

    def genConstraints_of_matchinground(self):
        input_sc = Vars_generator.genVars_input_of_SC(self.mat_r - 1)
        input_sr = Vars_generator.genVars_input_of_SR(self.mat_r - 1)
        input_mc = Vars_generator.genVars_input_of_MC(self.mat_r - 1)
        output_match = Vars_generator.genVars_output_of_matching(self.mat_r)
        output1_sc = Vars_generator.genVars_input1_of_SC(self.mat_r)
        output2_sc = Vars_generator.genVars_input2_of_SC(self.mat_r)

        constr = []
        # constraints for SC
        for i in range(16):
            constr = constr + [input_sc[i] + ' - ' + input_sr[i] + ' = 0']

        # constraints for SR
        constr = constr + MITMPreConstraints.equalConstraints(SR(input_sr), input_mc)

        # constraints for MC
        for i in range(4):
            constr = constr + MITMPreConstraints.Match_constraint(input_mc[i],input_mc[4+i],input_mc[8+i],input_mc[12+i],
                                                               output_match[i],output_match[4+i],output_match[8+i],output_match[12+i])

        #matching column
        for i in range(4):
            constr = constr + MITMPreConstraints.split_constraint(output_match[i],output_match[4+i],output_match[8+i],output_match[12+i],
                                                                  output1_sc[i],output1_sc[4+i],output1_sc[8+i],output1_sc[12+i],
                                                                  output2_sc[i],output2_sc[4+i],output2_sc[8+i],output2_sc[12+i])

        constr = constr + [BasicTools.plusTerm(output1_sc) + ' >= 1']
        return constr

    def genConstraints_of_decrypt(self, r):
        input1_sc = Vars_generator.genVars_input1_of_SC(r)
        input2_sc = Vars_generator.genVars_input2_of_SC(r)

        input1_at = Vars_generator.genVars_input1_of_SR(r)
        input2_at = Vars_generator.genVars_input2_of_SR(r)

        input1_mc = Vars_generator.genVars_input1_of_MC(r)
        input2_mc = Vars_generator.genVars_input2_of_MC(r)

        output1_sc = Vars_generator.genVars_input1_of_SC(r+1)
        output2_sc = Vars_generator.genVars_input2_of_SC(r+1)

        constr = []
        #SC
        for i in range(8):
            constr = constr + [input1_sc[i] + ' - ' + input1_at[i] + ' = 0']
            constr = constr + [input2_sc[i] + ' - ' + input2_at[i] + ' = 0']
        for i in range(8):
            constr = constr + [input1_at[8+i] + ' = 0']
            constr = constr + [input2_at[8+i] + ' = 0']
        #SR
        constr = constr + MITMPreConstraints.equalConstraints(SR(input1_sc), input1_mc)
        constr = constr + MITMPreConstraints.equalConstraints(SR(input2_sc), input2_mc)
        #MC
        for i in range(4):
            constr = constr + MITMPreConstraints.MCguess_constraint(input1_mc[i], input1_mc[4+i], input1_mc[8+i], input1_mc[12+i],
                                                                    output1_sc[i], output1_sc[4+i], output1_sc[8+i], output1_sc[12+i])
            constr = constr + MITMPreConstraints.MCguess_constraint(input2_mc[i], input2_mc[4 + i], input2_mc[8 + i],
                                                                    input2_mc[12 + i],
                                                                    output2_sc[i], output2_sc[4 + i], output2_sc[8 + i],
                                                                    output2_sc[12 + i])
        return constr


    def genConstraints_keyguess(self):
        KG1 = Vars_generator.genVars_Keyguess1()
        KG2 = Vars_generator.genVars_Keyguess2()

        SR1 = []
        SR2 = []
        constr = []
        for r in range(self.mat_r, self.TR):
            SR1.append(Vars_generator.genVars_input1_of_SR(r))
            SR2.append(Vars_generator.genVars_input2_of_SR(r))

        for r in range(self.mat_r, self.TR):
            for i in range(0, self.TR-1-r):
                SR1[r - self.mat_r] = key_perm(SR1[r - self.mat_r])
                SR2[r - self.mat_r] = key_perm(SR2[r - self.mat_r])

        for r in range(self.mat_r, self.TR):
            SR1[r - self.mat_r] = lastroundtotk(SR1[r - self.mat_r])
            SR2[r - self.mat_r] = lastroundtotk(SR2[r - self.mat_r])

        for i in range(0, 16):
            X = []
            for r in range(self.mat_r,self.TR):
                X.append(SR1[r-self.mat_r][i])
            constr = constr + MITMPreConstraints.OR_constraint(X,KG1[i])

        for i in range(0, 16):
            X = []
            for r in range(self.mat_r,self.TR):
                X.append(SR2[r-self.mat_r][i])
            constr = constr + MITMPreConstraints.OR_constraint(X,KG2[i])

        return constr


    def genConstraints_total(self):
        inputsc = Vars_generator.genVars_input_of_SC(0)
        KG1 = Vars_generator.genVars_Keyguess1()
        KG2 = Vars_generator.genVars_Keyguess2()
        KGB = Vars_generator.genVars_KeyguessBlue()
        KGR = Vars_generator.genVars_KeyguessRed()
        KGN = Vars_generator.genVars_KeyguessN()
        KG = Vars_generator.genVars_Keyguess()
        constr = []
        constr = constr + [BasicTools.plusTerm(inputsc)+' = 1']
        for r in range(0, self.mat_r-1):
            constr = constr + self.genConstraints_of_encrypt(r)
        constr = constr + self.genConstraints_of_matchinground()
        for r in range(self.mat_r, self.TR):
            constr = constr + self.genConstraints_of_decrypt(r)

        constr = constr + self.genConstraints_keyguess()

        for i in range(16):
            constr = constr + MITMPreConstraints.ORm_constraint(KG1[i], KG[i], KGB[i])
            constr = constr + MITMPreConstraints.ORm_constraint(KG2[i], KG[i], KGR[i])

        for i in range(16):
            constr = constr + MITMPreConstraints.OR_constraint([KGB[i], KGR[i]], KGN[i])

        constr = constr + ['Deg1' + ' - ' + BasicTools.MinusTerm(KGB) + ' = 0']
        constr = constr + ['Deg2' + ' - ' + BasicTools.MinusTerm(KGR) + ' = 0']
        constr = constr + ['DegG' + ' + ' + BasicTools.plusTerm(KGN) + ' + ' + BasicTools.plusTerm(KG) + ' = 16']

        return constr



    def genModel(self, filename):
        V = set([])
        constr = list([])
        constr = constr + self.genConstraints_total()

        constr = constr + ['DObj - Deg1 >= 0']
        constr = constr + ['DObj - Deg2 >= 0']
        constr = constr + ['DObj <= 5']
        V = BasicTools.getVariables_From_Constraints(constr)

        fid = open('./skinny/TR' + str(self.TR) + '_matr' + str(self.mat_r) + '.lp', 'w')

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
    TR = 9
    mat_r = 6
    name = './skinny/TR' + str(TR) + '_matr' + str(mat_r)
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
        if (v.VarName[0:3]=='KG_'):
            v.ub = 0
    m.update()
    while counter < 16:
        m.optimize()
        m.write(name + '_' + str(inject_num) +'.sol')
        solFile = open('./' + name + '_' + str(inject_num) + '.sol', 'r')
        Sol = dict()

        for line in solFile:
            if line[0] != '#':
                temp = line
                temp = temp.replace('-', ' ')
                temp = temp.split()
                # Sol[temp[0]] = float(temp[1]+'0')
                Sol[temp[0]] = float(temp[1])
        # Gurobi syntax: m.Status == 2 represents the model is feasible.
        if m.Status == 2:
            inject_num += 1
            fault = []
            KG1 = []
            KG2 = []
            M1 = []
            M2 = []
            varn = []
            for v in m.getVars():
                if (v.x == 1) and (v.VarName[0:3]=='KGB'):
                    KG1.append(v.VarName)
                if (v.x == 1) and (v.VarName[0:3]=='KGR'):
                    KG2.append(v.VarName)
                if (v.VarName[0:3] == 'IS1') and (v.VarName[len(v.VarName)-1] == str(mat_r)) and (v.x == 1):
                    M1.append(v.VarName)
                if (v.VarName[0:3] == 'IS2') and (v.VarName[len(v.VarName)-1] == str(mat_r)) and (
                        v.x == 1):
                    M2.append(v.VarName)
                if (v.x == 1) and (v.VarName[0:2] == 'X_') and (v.VarName[len(v.VarName)-1] == '0'):
                    #v.ub = 1
                    fault.append(v.VarName)
                if (v.x == 1) and (v.VarName[0:3] == 'KGN'):
                    counter += 1
                    if (len(v.VarName)==5):
                        varn.append('KG_' + str(v.VarName[4]))
                    if (len(v.VarName) == 6):
                        varn.append('KG_' + str(v.VarName[4:6]))
            for u in varn:
                for v in m.getVars():
                    if (v.VarName == u):
                        v.ub = 1
            m.update()
            Fault.append(fault)
            KGB.append(KG1)
            KGR.append(KG2)
            MB.append(M1)
            MR.append(M2)
        elif m.Status == 3:
            break


    fileobj = open(name+'result.txt', "w")
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













