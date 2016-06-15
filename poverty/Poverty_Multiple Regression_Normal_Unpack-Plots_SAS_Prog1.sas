*;
*;
* Poverty - Multiple Regression Analysis;
*;
    ods graphics on;
	ods pdf file= "C:\Users\Vijay\Documents\poverty_reg___.pdf";
*;
options ls=80 ps=50 nodate pageno=1;
*;
Title 'Poverty Regression';
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
*;
* Correlation Matrix - All Variables;
*;
Proc Corr Data = Poverty;
    Var X6 X7 X8 X12 X13 X14 X15;
*;
*;
* Simple Regression Analysis of best variable X4;
*;
Proc Reg Data = Poverty plots(unpack);
	Model X8 = X13 / STB Influence P R VIF Tol;
	Plot NQQ.*R. NPP.*R.;
*;
*;
* Stepwise Regression Analysis ;
*;
*;
Proc Reg Data = Poverty Corr Simple plots(unpack);
	Model X8 = X6 X7 X12 X13 X14 X15 / Selection=Stepwise SLEntry=0.05 STB Influence P R VIF Tol;
	Plot NQQ.*R. NPP.*R.;
*;
* Performing a full model confirmatory analysis;
Proc Reg Data = Poverty Corr Simple plots(unpack);
	Model X8 = X6 X7 X12 X13 X14 X15 /STB Influence P R VIF Tol;
	Plot NQQ.*R. NPP.*R.;
*	ods graphics off;
*;
* Adding other dependent variables to the best subset of the stepwise analysis;
Proc Reg Data = Poverty Corr Simple plots(unpack);
	Model X8 = X11 X7 X12 X13 /STB Influence P R VIF Tol;
	Plot NQQ.*R. NPP.*R.;
Run;
Quit;
ods pdf close;
