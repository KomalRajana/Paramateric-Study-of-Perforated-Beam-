#Project: Perforated Steel Beam: 
#Python script for allowing the parameterisation of cellular steel beams.
#Paper ref: https://doi.org/10.1016/j.tws.2020.106955
#MSc(Eng) Thesis: https://osf.io/fhzjv/

##The parameterized variables are: the thickness of the flange (TF), web (TW), global (GI) and local (LI) geometrical imperfection, steel yield strength (FY), ultimate strength (FU) and final strain of the steel (FS).  

*PARAMETER
TF = <1.0>
TW =<1.0>
GI = <1.0>
LI=<1.0>
FY= <1.0>
FU=<1.0>
FS=<1.0>

#Create parametric study
Buckling Study=Par Study (‘TW’,‘TF’, ‘GI’ , ‘LI’ ‘FY’, ‘FU’,’FS’, name= ‘NLB’, verbose= ON , directory= OFF)

#Define Parameters 
BucklingStudy.define(DISCRETE, par='TF',domain=(15,20,25))
BucklingStudy.define(DISCRETE, par='TW',domain=(9,12,15))
BucklingStudy.define(DISCRETE, par='GI',domain=(2.1,2.625,3.5))
BucklingStudy.define(DISCRETE, par='LI',domain=(0.268441358,0.5368827,0.675))
BucklingStudy.define (DISCRETE, par= ‘FY’ , domain = (355))
BucklingStudy.define (DISCRETE, par= ‘FU’ , domain = (510))
BucklingStudy.define (DISCRETE, par= ‘FS’ , domain = (0.126175))

#Sample Parameters 
BucklingStudy.sample (INTERVAL, par = 'TF', interval = 1)
BucklingStudy.sample (INTERVAL, par = 'TW', interval = 1)
BucklingStudy.sample (INTERVAL, par = 'LI', interval = 1)
BucklingStudy.sample (INTERVAL, par = 'GI', interval=1)
BucklingStudy.sample (INTERVAL, par = 'FY', interval = 1)
BucklingStudy.sample (INTERVAL, par = 'FU', interval = 1)
BucklingStudy.sample (INTERVAL, par = 'FS', interval=1)

#Combined Parameters
# PS: parametric study 
Buckling Study.combine(MESH, name = PS) 

##Constrain the designs
#FY*FU*ST= 355*510*0.126175 =22843.9837500
#FY*FU*ST= 235 * 360 * 0.156775= 13263.16500
#FY*FU*ST= 440 * 550 * 0.1122 = 27152.400
BucklingStudy.constrain(‘‘FY*FU*ST=22843.9837500’’ )              
BucklingStudy.constrain(‘’FY*FU*ST=13263.16500’’)     
BucklingStudy.constrain(‘’FY*FU*ST=22843.9837500’’ ) 

#Generate design and submit the analysis                
BucklingStudy.generate (template = 'NLB1’)

#Execute the analysis jobs
BucklingStudy.execute(ALL)

#Output the results  
  #For elastic analysis: 
BucklingStudy.output(step=1, instance= ‘Final’, file=Fil, request=FIELD) 
  #For Inelastic analysis:
BucklingStudy.output(step=2, instance= ‘Final’, file=ODB, request=HISTORY)

#Gather the results
  #For elastic buckling:
BucklingStudy.gather (results='elastic-load', variable='MODAL', mode=1,  step=1)

  #For inelastic buckling:
BucklingStudy.gather(results='lpf',variable='LPF', step=2, inc=LAST)

#Report the results with variables
  #For elastic request:
BucklingStudy.report(FILE,results=('elastic-load'),par=('TF','TW'), truncation=OFF, file='output-E.psr')

  #For inelastic request:
BucklingStudy.report(FILE,results=('lpf'),par=('TF','TW','GI','LI','FY','FU','FS'), truncation=OFF, file='output-InE.psr')






