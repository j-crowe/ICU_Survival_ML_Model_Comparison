# MIMICIII-Investigation
A probe into the MIMIC III dataset. Used as an investigatory project and proposal alongside Udacity capstone.

## Goal:
The goal of this project is to probe some basic information from the MIMIC III dataset. This project is an investigation to aid in deciding upon a useful capstone project in the Udacity Machine Learning Engineer Nanodegree program. 

This repository also includes the capstone project proposal to go along with this basic data probe.

## The data:
MIMIC-III (Medical Information Mart for Intensive Care III) is a large, freely-available database comprising deidentified health-related data associated with over forty thousand patients who stayed in critical care units of the Beth Israel Deaconess Medical Center between 2001 and 2012.

The database includes information such as demographics, vital sign measurements made at the bedside (~1 data point per hour), laboratory test results, procedures, medications, caregiver notes, imaging reports, and mortality (both in and out of hospital).

MIMIC supports a diverse range of analytic studies spanning epidemiology, clinical decision-rule improvement, and electronic tool development. It is notable for three factors:

* it is freely available to researchers worldwide
* it encompasses a diverse and very large population of ICU patients
* it contains high temporal resolution data including lab results, electronic documentation, and bedside monitor trends and waveforms.

Citation: https://mimic.physionet.org/about/mimic/ 

## The Proposal:
For a more detailed description of the proposal please see the .tex file or .pdf file that will be included in the repo once the proposal has been completed.

Sepsis is a serious, life threatening condition that is caused by an overwhelming immune resp onse to an infection. Infection is often bacterial however it is possible for sepsis to be associated with: fungal, viral, parasitic, as well as bacterial infections. 

Sepsis is due to the body's response, not only the effects of the infection itself. White blo o d cells release an array of chemicals to fight the infection which trigger systemic inflammation, vaso dilation, permeability of vessels, and intracellular fluid build up. These "leaky vessels" use up the body's supply of coagulation factors. The increased fluid build up and decreased blood pressure result in a lack of oxygenation of tissue, known as shock. 

If sepsis is not treated quickly or with enough direct care, multiple organ dysfunction can occur which can result in kidney failure, liver failure, heart failure, acute respiratory distress, etc... The speed at which treatment is administered and types of treatments are directly correlated with survivability of this severe condition. The speed of treatment has been found to be more important than the age of the patient. Each hour of delay in antimicrobial administration over the initial 6 hours is associated with an average decrease in survival rate of 7.6%. 

Certain treatments may be highly effective, therefore it is important to pay special attention to several things: the type of infection and type of antibiotics used, the blood pressure and whether or not vasopressors were used, correct amount of IV fluid provided to patient. The correct type of antibiotic and appropriate administering of vasopressors can reduce the chance of organ failure and mortality greatly.

The goal of this project is to predict the survivability of patients based off of demographic information along with speed of treatment, type of infection, type of antimicrobial treatment, as well as other drugs and vital information. While sepsis is well studied, it is still partially responsible for ~6% of all deaths in the United States. More information and a better understanding of tailoring individual treatments for patients may improve its survivability.

## Learn More:
To gain access to this dataset for your own project visit: https://mimic.physionet.org

A short course is required to gain permission to the dataset.

## Citations:
MIMIC-III, a freely accessible critical care database. Johnson AEW, Pollard TJ, Shen L, Lehman L, Feng M, Ghassemi M, Moody B, Szolovits P, Celi LA, and Mark RG. Scientific Data (2016). DOI: 10.1038/sdata.2016.35. Available from: http://www.nature.com/articles/sdata201635

Goldberger AL, Amaral LAN, Glass L, Hausdorff JM, Ivanov PCh, Mark RG, Mietus JE, Moody GB, Peng C-K, Stanley HE. PhysioBank, PhysioToolkit, and PhysioNet: Components of a New Research Resource for Complex Physiologic Signals. Circulation 101(23):e215-e220 [Circulation Electronic Pages; http://circ.ahajournals.org/content/101/23/e215.full]; 2000 (June 13).
