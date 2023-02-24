import sys
import re

TR=9
mat=6

with open('TR'+str(TR)+'_matr'+str(mat)+'.sol') as out:
    lines = out.readlines()
su=[]
for line in lines:
    b=line.rstrip()
    a=b.split(' ')
    su = su +[a[0],a[1]]
m=len(su)
X1 = []
X2 = []
Y1 = []
Y2 = []
Z1 = []
Z2 = []
SC1 = []
SC2 = []
SR1 = []
SR2 = []
MC1 = []
MC2 = []

s1=[]
s2=[]
start1=[]
start2=[]
stk1=[]
stk2=[]


for i in range(m):
    if su[i][0] == 'X':
        X1 = X1 + [su[i]]
        X2 = X2 + [su[i+1]]
    elif su[i][0] == 'Y':
        Y1 = Y1 + [su[i]]
        Y2 = Y2 + [su[i + 1]]
    elif su[i][0] == 'Z':
        Z1 = Z1 + [su[i]]
        Z2 = Z2 + [su[i + 1]]
    elif su[i][0:2]=='IS':
        SC1 = SC1 + [su[i]]
        SC2 = SC2 + [su[i+1]]
    elif su[i][0:2]=='SR':
        SR1 = SR1 + [su[i]]
        SR2 = SR2 + [su[i+1]]
    elif su[i][0:1] == 'M':
        MC1 = MC1 + [su[i]]
        MC2 = MC2 + [su[i + 1]]


longx=len(X1)
X12=zip(X1,X2)
dict1=dict(X12)
L=list(dict1.items())
Xs=sorted(L,key=lambda i:(int(re.findall(r'(\d+)',i[0])[1]),int(re.findall(r'(\d+)',i[0])[0])))
Xcolor=[]

for i in range(0,longx):
    if Xs[i][1]=='0':
        Xcolor = Xcolor + ['white']
    elif Xs[i][1]=='1':
        Xcolor = Xcolor + ['gray']


longy=len(Y1)
Y12=zip(Y1,Y2)
dict1=dict(Y12)
L=list(dict1.items())
Ys=sorted(L,key=lambda i:(int(re.findall(r'(\d+)',i[0])[1]),int(re.findall(r'(\d+)',i[0])[0])))
Ycolor=[]

for i in range(0,longy):
    if Ys[i][1]=='0':
        Ycolor = Ycolor + ['white']
    elif Ys[i][1]=='1':
        Ycolor = Ycolor + ['gray']



longz=len(Z1)
Z12=zip(Z1,Z2)
dict1=dict(Z12)
L=list(dict1.items())
Zs=sorted(L,key=lambda i:(int(re.findall(r'(\d+)',i[0])[1]),int(re.findall(r'(\d+)',i[0])[0])))
# for i in ss:
    # print(i)
Zcolor=[]

for i in range(0,longz):
    if Zs[i][1]=='0':
        Zcolor = Zcolor + ['white']
    elif Zs[i][1]=='1':
        Zcolor = Zcolor + ['gray']




longsc=len(SC1)
SC1SC2=zip(SC1,SC2)
dict1=dict(SC1SC2)
L=list(dict1.items())
SCs=sorted(L,key=lambda i:(int(re.findall(r'(\d+)',i[0])[2]),int(re.findall(r'(\d+)',i[0])[1]),int(re.findall(r'(\d+)',i[0])[0])))
# for i in ss:
    # print(i)

sccolor=[]

for i in range(0,longsc,2):
    if SCs[i][1]=='0' and SCs[i+1][1] == '0':
        sccolor = sccolor + ['gray']
    elif SCs[i][1]=='1' and SCs[i+1][1] == '0':
        sccolor = sccolor + ['blue']
    elif SCs[i][1]=='0' and SCs[i+1][1] == '1':
        sccolor = sccolor + ['red']
    elif SCs[i][1]=='1' and SCs[i+1][1] == '1':
        sccolor = sccolor + ['orange']



longsr=len(SR1)
SR1SR2=zip(SR1,SR2)
dict1=dict(SR1SR2)
L=list(dict1.items())
SRs=sorted(L,key=lambda i:(int(re.findall(r'(\d+)',i[0])[2]),int(re.findall(r'(\d+)',i[0])[1]),int(re.findall(r'(\d+)',i[0])[0])))
# for i in ss:
    # print(i)

srcolor=[]

for i in range(0,longsr,2):
    if SRs[i][1]=='0' and SRs[i+1][1] == '0':
        srcolor = srcolor+['gray']
    elif SRs[i][1]=='1' and SRs[i+1][1] == '0':
        srcolor = srcolor+['blue']
    elif SRs[i][1]=='0' and SRs[i+1][1] == '1':
        srcolor = srcolor+['red']
    elif SRs[i][1]=='1' and SRs[i+1][1] == '1':
        srcolor = srcolor+['orange']


longmc=len(MC1)
MC1MC2=zip(MC1,MC2)
dict1=dict(MC1MC2)
L=list(dict1.items())
MCs=sorted(L,key=lambda i:(int(re.findall(r'(\d+)',i[0])[2]),int(re.findall(r'(\d+)',i[0])[1]),int(re.findall(r'(\d+)',i[0])[0])))
# for i in ss:
    # print(i)

mccolor=[]

for i in range(0,longmc,2):
    if MCs[i][1]=='0' and MCs[i+1][1] == '0':
        mccolor = mccolor+['gray']
    elif MCs[i][1]=='1' and MCs[i+1][1] == '0':
        mccolor = mccolor+['blue']
    elif MCs[i][1]=='0' and MCs[i+1][1] == '1':
        mccolor = mccolor+['red']
    elif MCs[i][1]=='1' and MCs[i+1][1] == '1':
        mccolor = mccolor+['orange']




f=open('SKINNY_TR'+str(TR)+'_mat_'+str(mat)+'.tex','w')
f.write(r'\documentclass{standalone}'+'\n'+r'\usepackage{tikz}'+'\n')
f.write(r'\usetikzlibrary{arrows}'+'\n'+r'\usetikzlibrary{calc}'+'\n'+r'\usetikzlibrary{positioning}'+'\n'+r'\usetikzlibrary{patterns}'+'\n')
f.write(r'\usetikzlibrary{crypto.symbols}'+'\n'+r'\tikzset{shadows=no} '+'\n'+r'\definecolor{orange}{rgb}{1,0.6,0.2}'+'\n')
f.write(r'\definecolor{blue}{rgb}{0,0.4,0.8}'+'\n'+r'\definecolor{red}{rgb}{0.9,0,0.4}'+'\n')
f.write(r'\definecolor{gray}{rgb}{0.7,0.7,0.7}'+'\n'+r'\definecolor{darkgreen}{rgb}{0,0.4,0.4}'+'\n\n'+r'\begin{document}'+'\n')
f.write(r'\begin{tikzpicture}[scale=0.6]'+'\n\n'+r'\everymath{\scriptstyle}'+'\n')

f.write(r'\tikzset{edge/.style=->, arrow head=1pt};'+'\n')


for r in range(0, mat):
    f.write(r'\begin{scope}[yshift=' + str(20-4*(r//2)) + 'cm]' + '\n' + r'   \begin{scope}[xshift=' + str(-10+ 9 * (r % 2)) + 'cm]' + '\n')
    f.write(r'\path (4,-0.5) node {\tiny round $R' + str(r+1-TR) + '$};' + '\n')
    f.write(r'\draw[->] (2,1.5) -- ++(1,0);' + '\n')
    f.write(r'\draw[fill=gray!10, rounded corners, font={\sffamily\slshape}] (2.25,0.8) rectangle++(0.5,1.4);'+'\n')
    f.write(r'\draw[thin] (2.5,1.5) -- node[above] {\tiny\tt SC} +(0,0);' + '\n')
    f.write(r'\draw[thin] (2.5,1.5) -- node[below] {\tiny\tt AC} +(0,0);' + '\n')
    f.write(r'\draw(1,0) node {$X_{R'+str(r+1-TR)+'}$};' + '\n')
    for i in range(0, 4):
        for j in range(0, 4):
            f.write(r'  \draw[fill=' + Xcolor[16 * r + 4 * i + j] + '] (' + str(j / 2) + ',' + str(
                2 - i / 2) + ') rectangle +(0.5,0.5);' + '\n')
    f.write(r'	\end{scope}' + '\n' + r'    \end{scope}' + '\n')


    f.write(r'\begin{scope}[yshift=' + str(20 - 4 * (r//2)) + 'cm]' + '\n' + r'   \begin{scope}[xshift=' + str(
        -7+9*(r % 2)) + 'cm]' + '\n')
    f.write(r'\draw[thin] (2.5,1.5) -- node[above] {\tiny\tt SR} +(0,0);' + '\n')
    f.write(r'\draw[->] (2,1.5) -- ++(1,0);' + '\n')
    f.write(r'\draw(1,0) node {$Y_{R' + str(r + 1 - TR) + '}$};' + '\n')
    for i in range(0, 4):
        for j in range(0, 4):
            f.write(r'  \draw[fill=' + Ycolor[16 * r + 4 * i + j] + '] (' + str(j / 2) + ',' + str(
                2 - i / 2) + ') rectangle +(0.5,0.5);' + '\n')
    f.write(r'	\end{scope}' + '\n' + r'    \end{scope}' + '\n')


    f.write(r'\begin{scope}[yshift=' + str(20 - 4 * (r//2)) + 'cm]' + '\n' + r'   \begin{scope}[xshift=' + str(
        -4 + 9 * (r%2)) + 'cm]' + '\n')
    f.write(r'\draw[thin] (2.5,1.5) -- node[above] {\tiny\tt MC} +(0,0);' + '\n')
    f.write(r'\draw[->] (2,1.5) -- ++(1,0);' + '\n')
    f.write(r'\draw(1,0) node {$Z_{R' + str(r + 1 - TR) + '}$};' + '\n')
    for i in range(0, 4):
        for j in range(0, 4):
            f.write(r'  \draw[fill=' + Zcolor[16 * r + 4 * i + j] + '] (' + str(j / 2) + ',' + str(
                2 - i / 2) + ') rectangle +(0.5,0.5);' + '\n')
    f.write(r'	\end{scope}' + '\n' + r'    \end{scope}' + '\n')


for r in range(mat, TR):
    f.write(r'\begin{scope}[yshift=' + str(20 - 4 * (mat//2-1)-7*((r-mat)//2+1)) + 'cm]' + '\n' + r'   \begin{scope}[xshift=' + str(
        -10+9*(r%2)) + 'cm]' + '\n')
    f.write(r'\path (4,-0.5) node {\tiny round $R' + str(r+1-TR) + '$};' + '\n')
    f.write(r'\draw[->] (3,1.5) -- ++(-1,0);' + '\n')
    f.write(r'\draw[fill=gray!10, rounded corners, font={\sffamily\slshape}] (2.25,0.8) rectangle++(0.5,1.4);'+'\n')
    f.write(r'\draw[thin] (2.5,1.5) -- node[above] {\tiny\tt SC} +(0,0);' + '\n')
    f.write(r'\draw[thin] (2.5,1.5) -- node[below] {\tiny\tt AC} +(0,0);' + '\n')
    f.write(r'\draw(1,0) node {$X_{R'+str(r+1-TR)+'}$};' + '\n')
    for i in range(0, 4):
        for j in range(0, 4):
            f.write(r'  \draw[fill=' + sccolor[16 * (r-mat) + 4 * i + j] + '] (' + str(j / 2) + ',' + str(
                2 - i / 2) + ') rectangle +(0.5,0.5);' + '\n')
    f.write(r'	\end{scope}' + '\n' + r'    \end{scope}' + '\n')

    f.write(r'\begin{scope}[yshift=' + str(20 - 4 * (mat//2-1)-7*((r-mat)//2+1)) + 'cm]' + '\n' + r'   \begin{scope}[xshift=' + str(
        -7+9*(r%2)) + 'cm]' + '\n')
    f.write(r'\draw[thin] (2.5,1.5) -- node[above] {\tiny\tt SR} +(0,0);' + '\n')
    f.write(r'\draw[->] (3,1.5) -- ++(-1,0);' + '\n')
    f.write(r'\draw(1,0) node {$Y_{R' + str(r + 1 - TR) + '}$};' + '\n')
    for i in range(0, 4):
        for j in range(0, 4):
            f.write(r'  \draw[fill=' + sccolor[16 * (r-mat) + 4 * i + j] + '] (' + str(j / 2) + ',' + str(
                2 - i / 2) + ') rectangle +(0.5,0.5);' + '\n')
    f.write(r'	\end{scope}' + '\n' + r'    \end{scope}' + '\n')

    f.write(r'\begin{scope}[yshift=' + str(
        23 - 4 * (mat // 2-1) - 7 * ((r - mat) // 2 + 1)) + 'cm]' + '\n' + r'   \begin{scope}[xshift=' + str(
        -7 + 9 * (r % 2)) + 'cm]' + '\n')
    f.write(r'\draw (3,1.5) node{\tiny {$TK1$}};' + '\n')
    f.write(r'\draw (1,0) node{\tiny $\oplus$};' + '\n')
    for i in range(0, 2):
        for j in range(0, 4):
            if srcolor[16 * (r - mat) + 4 * i + j] != 'gray':
                f.write(r'  \draw[draw=gray!80,fill=' + srcolor[16 * (r - mat) + 4 * i + j] + '] (' + str(j / 2) + ',' + str(2 - i / 2) + ') rectangle +(0.5,0.5);' + '\n')
            else:
                f.write(r'  \draw[draw=gray!80,pattern = north west lines, pattern color = darkgreen] (' + str(
                    j / 2) + ',' + str(2 - i / 2) + ') rectangle +(0.5,0.5);' + '\n')
    f.write(r'\draw[line width =1pt] (0,1.5) rectangle +(2,1);' + '\n')
    f.write(r'	\end{scope}' + '\n' + r'    \end{scope}' + '\n')

    f.write(r'\begin{scope}[yshift=' + str(20 - 4 * (mat//2-1)-7*((r-mat)//2+1)) + 'cm]' + '\n' + r'   \begin{scope}[xshift=' + str(
        -4+9*(r % 2)) + 'cm]' + '\n')
    f.write(r'\draw[thin] (2.5,1.5) -- node[above] {\tiny\tt MC} +(0,0);' + '\n')
    f.write(r'\draw[->] (3,1.5) -- ++(-1,0);' + '\n')
    f.write(r'\draw(1,0) node {$Z_{R' + str(r + 1 - TR) + '}$};' + '\n')
    for i in range(0, 4):
        for j in range(0, 4):
            f.write(r'  \draw[fill=' + mccolor[16 * (r-mat) + 4 * i + j] + '] (' + str(j / 2) + ',' + str(
                2 - i / 2) + ') rectangle +(0.5,0.5);' + '\n')
    f.write(r'	\end{scope}' + '\n' + r'    \end{scope}' + '\n')


f.write(r'\begin{scope}[shift={(-3,-5.5)}]'+'\n')
f.write(r'\draw[fill=gray]  (-7.5,0) rectangle ++(0.5,0.5);'+'\n')
f.write(r'\draw (-5,0.25) node {\small\tt Active Cell};'+'\n')
f.write(r'\draw[fill=white] (-2,0) rectangle ++(0.5,0.5);'+'\n')
f.write(r'\draw (1.5,0.25) node {\small\tt Inactive Cell};'+'\n')
f.write(r'\draw[fill=blue]  (4,0) rectangle ++(0.5,0.5);'+'\n')
f.write(r'\draw[fill=red]  (5,0) rectangle ++(0.5,0.5);')
f.write(r'\draw (9,0.25 ) node {\small\tt Value need to be guessed};'+'\n')
f.write(r'\draw[fill=orange]  (14,0) rectangle ++(0.5,0.5);'+'\n')
f.write(r'\draw (18,0.25) node {\small\tt Guessed in each direction};'+'\n')
f.write(r'\draw[pattern=north west lines, pattern color=darkgreen]  (22.5,0) rectangle ++(0.5,0.5);'+'\n')
f.write(r'\draw (28,0.25) node {\small\tt Subkey cells need not be guessed};'+'\n')


f.write(r'\end{scope}'+'\n')
f.write(r'  \end{tikzpicture}'+'\n'+r'\end{document}')

f.close()