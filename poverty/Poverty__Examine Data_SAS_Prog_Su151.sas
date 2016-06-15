*;
*;
* Poverty - Examining Your Data PROC Univariate;
*;
    ods graphics on;
	ods pdf file= "C:\Users\Vijay\Documents\poverty_Ex_.pdf";
*;
options ls=80 ps=50 nodate pageno=1;
*;
Title 'Poverty Examine Data';
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
* 
*;
*;
*;
Proc Univariate Data = Poverty Normal Plot;
*    Var X6 X7 X8 X9 X10 X11 X12 X13 X14 X15 X16 X17 X18 X19 X20 X21 X22;
     Var X8 X11;
*;
*;
* X8 by X6;
Proc Sort Data = Poverty;
    By X6;
*;
Proc Univariate Data = Poverty Normal Plot;
    Var X8;
	By X6;
	ID X6;
*;
* X11 by X6;
	Proc Sort Data = Poverty;
    By X6;
*;
Proc Univariate Data = Poverty Normal Plot;
    Var X11;
	By X6;
	ID X6;
* X8 by X7;
Proc Sort Data = Poverty;
    By X7;

Proc Univariate Data = Poverty Normal Plot;
    Var X8;
	By X7;
	ID X7;
*;
*   Only X11 by X7 ;
*;
	Proc Sort Data = Poverty;
    By X7;
* ;
Proc Univariate Data = Poverty Normal Plot;
    Var X11;
	By X7;
	ID X7;
*;

* GLM ANOVA Analysis ;
* X8 by X6;
Proc GLM Data = Poverty;
    Class X6;
	Model X8 = X6;
	Means X6;
	Means X6 / hovtest = levene hovtest = bf hovtest = bartlett;
*;
*;

* X11 by X6 ;
	Proc GLM Data = Poverty;
    Class X6;
	Model X11 = X6;
	Means X6;
	Means X6 / hovtest = levene hovtest = bf hovtest = bartlett;

*  Only Var X8 By X7 Illustrated ;
Proc GLM Data = Poverty;
    Class X7;
	Model X8 = X7;
	Means X7;
	Means X7 / hovtest = levene hovtest = bf hovtest = bartlett;
*;
*;

* X11 by X7;
	Proc GLM Data = Poverty;
    Class X7;
	Model X11 = X7;
	Means X7;
	Means X7 / hovtest = levene hovtest = bf hovtest = bartlett;
*;
*;
*	ods graphics off;
*;
*;
Run;
Quit;
ods pdf close;
