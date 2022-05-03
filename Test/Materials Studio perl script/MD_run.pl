#!perl
# This perl script must be run on Materials Studio to equilirate the configuration " XXX.xtd" and eventuallty apply the shear rate.
# The outputs needed to calculate DMA using python scripts, are .txt files
# This script is only an example, please change the parameters/variables according to your project

use strict;
use Getopt::Long;
use MaterialsScript qw(:all);

##########################################################

#Paramètres Forcite
Modules->Forcite->ChangeSettings([
	Quality=>'Medium',
	CurrentForcefield=>'COMPASSIII',
	'3DPeriodicvdWSummationMethod' => 'Atom based', 
	'3DPeriodicElectrostaticSummationMethod' => 'PPPM',
	Ensemble3D=>'NPT',
	InitialVelocities=>'Current',
	AssignFixedBonds => 'Yes',
	TimeStep=>2,
	TrajectoryFrequency=>5000000,
	EnergyDeviation=>5000000000000,
        Thermostat => 'Nose',
	WriteLevel=>'Silent']);                                                                                                                                                        
	
##########################################################


#Paramètres Forcite
#=======================Equilibration=================================

my $doc=$Documents{"FRAME2_compression.xtd"};
my $FileName=$doc->Name;
my @Temperatures;
Modules->Forcite->Dynamics->Run($doc, Settings([
	NumberOfSteps=>10,
	Temperature=>298]));


Modules->Forcite->Dynamics->Run($doc, Settings([ Ensemble3D=>'NPT',
	TrajectoryRestart=>'Yes',
	TimeStep=>2,
	AppendTrajectory=>'No',
	NumberOfSteps=>50,
	WriteStressData=>'No',
	Temperature=>298]));
Modules->Forcite->Dynamics->Run($doc, Settings([ Ensemble3D=>'NVT',
	TrajectoryRestart=>'Yes',
	AppendTrajectory=>'No',
	TimeStep=>2,
	NumberOfSteps=>20]));	
my $Trajectory = $doc->Trajectory;	

#===============Parameters========================================
  
my $x=0.25;  # Log(frequency) (1/ps) Example: if x=-2 (1.ps) => frequency = 10^(-2) (1.ps)      
my $N=5;    # Number of periods
my $M=100;  # Number of data frequency (Number of output data). Example: if N=10, and M=100. For 10 periods 100 data are saved. Or for each cycle (period) 10 data is saved
my $A=0.2;  # Strain Amplitude
my $time=2.0; # Time step
my $pi = 3.14159265358979;
my $SimulationTime=int($N*1000/($time*10**($x))); # Simulation time of "N" cycles with "x" frequency
my $DataOutput=int($SimulationTime/$M); # Example: if simulation time = 1 ns, and we want to have 1000 data, every 1ps, the data is saved.
        
print "log10(frequency) (1/ps) = " . $x . "\n";
print "Simulation Time = " . $SimulationTime . "\n";
print "Data output (fs) = " . $DataOutput . "\n";
my $sr = 0.0;
my $dp = 0;
        
#==========================MD simulation, Shear strain==================================        
for ( my $t1=0; $t1<=$SimulationTime; $t1 += $time){ # ; $t1 += $DataOutput

	#====Updating periodic shear rate====================================
	$sr += 10**($x)*2*$pi*$A*cos(2*$pi*10**($x)*($t1)*0.001);
	
	#=======================================================
	Modules->Forcite->ChangeSettings([
		Ensemble3D=>'NVT',
		InitialVelocities=>'Current',
		ShearRate=>$sr,
		TimeStep=>$time,
		ShearDirection=>'B (BC)',
		NumberOfSteps=>1,
		AppendTrajectory=>'No',
		UseMultipleTimeSteps=>'Yes',
	 	Thermostat => 'NHL',
		ElectrostaticKSpaceTimeStep => 4 ,
		WriteStressData=>'No',
		TrajectoryRestart=>'No',
		DataFrequency=> 0,
		WriteLevel=>'Silent']);
	
	#==============================================================
	my $results = Modules->Forcite->Shear->Run($doc);  
	

	if ( $t1 < $dp+1 && $t1 > $dp-1 ){
		print "data point= " . $dp . 
		print " shear rate = " . $sr . "\n";
			
		$dp += $DataOutput;
		Modules->Forcite->ChangeSettings([DataFrequency => "2",
			WriteStressData=>'Yes'])
	}else{
	 	Modules->Forcite->ChangeSettings([DataFrequency => 0,
			WriteStressData=>'No'])	
	}		
	#==============================================================
	Modules->Forcite->Dynamics->Run($doc, Settings([ Ensemble3D=>'NVT',
		TrajectoryRestart=>'No',
		AppendTrajectory=>'No',
		TimeStep=>$time,
		NumberOfSteps=>10,
		Temperature=>298]));                                                                                                                                                    
		
	##########################################################
	
}		




