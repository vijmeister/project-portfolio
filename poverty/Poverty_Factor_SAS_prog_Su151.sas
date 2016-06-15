*;
*;
* Poverty - Principal Components Analysis;
*;
    ods graphics on;
	ods pdf file= "C:\Users\Vijay\Documents\poverty_fa___.pdf";

*;
options ls=80 ps=50 nodate pageno=1;
*;
Title 'Poverty EFA';

* Input Poverty ;
*;
Data Poverty;
Infile 'C:\Users\Vijay\Downloads\poverty3.txt' DLM = '09'X TRUNCOVER;
Input ID X1 X2 X3 X4 X5 X6 X7 X8 X9 X10 X11 X12 X13 X14 X15;
*;
Data Poverty;
	Set Poverty (Keep = X4 X5 X6 X7 X8 X9 X10 X11 X12 X13 X14 X15);
	Label X4 = 'X4 - Rural_urban_Continuum_Code_2003'
          X5 = 'X5 - Urban_influence_Code_2003'
          X6 = 'X6 - Rural_urban_Continuum_Code_2013'
          X7 = 'X7 - Urban_Influence_Code_2013'
		  X8 = 'X8 - PCTPOVALL_2013'
		  X9 = 'X9 - PCTPOV017_2013'
		  X10 = 'X10 - PCTPOV517_2013'
		  X11 = 'X11 - MEDHHINC_2013'
		  X12 = 'X12 - Unemployment rate'
		  X13 = 'X13 - Percentage of people without High school Diploma'
		  X14 = 'X14 - Average Household Size'
		  X15 = 'X15 - Population Size';
*;
Proc Print Data = Poverty;
*;
* Principal Components Analysis - All Variables;
*;
Proc Princomp Data = Poverty Plots = ALL;
    Var X6 X7 X12 X13 X14 X15;
*;
*;
************ All Variables - Method=Principal Rotation: None and Varimax ****************;
*;
* Exploratory Factor Analysis Rotate=NONE All Variables ;
*;
Proc Factor Data = Poverty Method=Principal Rotate=None NFactors=3 Simple MSA Plots = Scree MINEIGEN=0 Reorder;
    Var X6 X7 X12 X13 X14 X15;
*;
	* Exploratory Factor Analysis Rotate=NONE All Variables-  X13 Deleted ;
*;
Proc Factor Data = Poverty Method=Principal Rotate=None NFactors=3 Simple MSA Plots = Scree MINEIGEN=0 Reorder;
    Var X6 X7 X12 X14 X15;
*;
* Exploratory Factor Analysis Rotate=Varimax All Variables- X13 Deleted ;
*;
Proc Factor Data = Poverty Method=Principal Rotate=Varimax NFactors=3 Print Score Simple MSA Plots = Scree MINEIGEN=0 Reorder;
    Var X6 X7 X12 X14 X15;
*;
*EFA Quartimax;
*Proc Factor Data = Poverty Method=Principal Rotate=Quartimax NFactors=4 Print Score Simple Corr MSA Plots = ALL MINEIGEN=0 Reorder;
   	*Var X11 X17 X23 X26;
* Equamax;
*Proc Factor Data = Poverty Method=Principal Rotate=Equamax NFactors=4 Print Score Simple Corr MSA Plots = ALL MINEIGEN=0 Reorder;
   	*Var X11 X17 X23 X26;
*Promax;
*Proc Factor Data = Poverty Method=Principal Rotate=Promax(3) NFactors=3 Print Score Simple Corr MSA Plots = ALL MINEIGEN=0 Reorder;
   	*Var X6 X7 X12 X14 X15;
*;
************  Compute Factor and Summated Scores****************; 
*;
Proc Factor Data = Poverty Outstat=FactOut Method=Principal Rotate=Varimax NFactors=3 Print Score Simple MSA Plots = ALL MINEIGEN=0 Reorder;
    Var X6 X7 X12 X14 X15;
Proc Score Data=Poverty Score=FactOut Out=FScore;
    Var X6 X7 X12 X14 X15;
*;
Proc Print Data = FactOut;
*;
Proc Print Data = FScore;
*;
Data FScore;
	Set FScore;
	*Label SumScale1 = 'SumScale1 - Urban and Rural Influence with population adjusted'
	      SumScale2 = 'SumScale2 - unemployment rate'
          SumScale3 = 'SumScale3 - Average Household Size'
	SumScale1 = (X7 + X6 + ) / 3;
	*SumScale2 = X15;
	*SumScale3 = X14;
*;
Proc Print Data = FScore;
*;
Proc Means Data = FScore;
   Var Factor1 Factor2 Factor3; *SumScale1 SumScale2 SumScale3; 
*;
*;
************  Compute Factor and Summated Correlations ****************; 
*;
Proc Corr Data = FScore;
  Var Factor1 Factor2 Factor3; *SumScale1 SumScale2 SumScale3; 
*;
*;
Run;
Quit;
ods pdf close;
