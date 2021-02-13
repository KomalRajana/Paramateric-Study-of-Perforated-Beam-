#Project: Parametric study of the elastic and inelastic buckling of cellular beams 
#Python script for allowing the parameterisation of cellular steel beams.
#Paper ref: https://doi.org/10.1016/j.tws.2020.106955
#: MSc(Eng) Thesis: https://osf.io/fhzjv/

#The ABAQUS input file was parameterised and submitted to the solver with seven variables: the thickness of the flange (TF), web (TW), global (GI) and local (LI) geometrical imperfection, steel yield strength (FY), ultimate strength (FU), and final strain of the steel (FS).  The command below was inserted at the beginning of the input file to initiate the parametric study

*PARAMETER
TF = <1.0>
TW =<1.0>
GI = <1.0>
LI=<1.0>
FY= <1.0>
FU=<1.0>
FS=<1.0>

#It was required to add a command in the input file in order to extract and save the Eigen modes and Eigen values for the non-linear analysis as shown below: 
#NODE FILE, 
GLOBAL=YES
U

### Parametric script with variables 
#Create parametric study
Buckling Study=Par Study (‘TW’,‘TF’, ‘GI’ , ‘LI’ ‘FY’, ‘FU’,’FS’, name= ‘NLB’, verbose= ON , directory= OFF)
#Define parameters
BucklingStudy.define(DISCRETE, par='TF',domain=(15,20,25))
BucklingStudy.define(DISCRETE, par='TW',domain=(9,12,15))
BucklingStudy.define(DISCRETE, par='GI',domain=(2.1,2.625,3.5))
BucklingStudy.define(DISCRETE, par='LI',domain=(0.268441358,0.5368827,0.675))
BucklingStudy.define (DISCRETE, par= ‘FY’ , domain = (235,355,440))
BucklingStudy.define (DISCRETE, par= ‘FU’ , domain = (360,510,550))
BucklingStudy.define(DISCRETE, par= ‘FS’ , domain = (0.156775,0.126175,0.1122))

#Sample of the parameters. 
BucklingStudy.sample (INTERVAL, par = 'TF', interval = 1)
BucklingStudy.sample (INTERVAL, par = 'TW', interval = 1)
BucklingStudy.sample (INTERVAL, par = 'LI', interval = 1)
BucklingStudy.sample (INTERVAL, par = 'GI', interval=1)
BucklingStudy.sample (INTERVAL, par = 'FY', interval = 1)
BucklingStudy.sample (INTERVAL, par = 'FU', interval = 1)
BucklingStudy.sample (INTERVAL, par = 'FS', interval=1)

#Combined parameters
Buckling Study.combine(MESH, name = PS1)

#The constrain command was used to ensure the steel tensile yield stress, the ultimate stress and strains for a specific strength class was used.  The command was based on the following multiplication: 
#FY*FU*ST= 355*510*0.126175 =22843.9837500
#FY*FU*ST= 235 * 360 * 0.156775= 13263.16500
#FY*FU*ST= 440 * 550 * 0.1122 = 27152.400
#The steel strength class of S355 would only be active when the multiplication of FY * FU * ST = 22843.9837500.
BucklingStudy.constrain(“FY*FU*ST=22843.9837500”)
BucklingStudy.constrain(“FY*FU*ST=13263.16500”) 
BucklingStudy.constrain(“FY*FU*ST=22843.9837500”)

#Generate design and submit analysis
BucklingStudy.generate (template = 'NLB1’)

#Execute all analyses
BucklingStudy.execute(ALL)

#Results output for elastic and inelastic analysis 
BucklingStudy.output(step=1, instance= ‘Final’, file=Fil, request=FIELD)
BucklingStudy.output(step=2, instance= ‘Final’, file=ODB, request=HISTORY)

#Extract results for both the elastic and inelastic analyses 
BucklingStudy.gather (results='elastic-load', variable='MODAL', mode=1, step=1)
BucklingStudy.gather(results='lpf', variable='LPF', step=2, inc=LAST)

#Organise the output variable 
BucklingStudy.report(FILE,results=('elastic-load'),par=('TF','TW'), truncation=OFF, file='output-E.psr')
BucklingStudy.report(FILE,results=('lpf'),par=('TF','TW','GI','LI','FY','FU','FS'),truncation=OFF,file='output-InE.psr')

#The analyses were then submitted via the ABAQUS command prompt by recalling the Python script (.psf). as “ABAQUS SCRIPT=NLB1.psf”.


