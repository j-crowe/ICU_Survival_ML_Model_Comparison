from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from sklearn import preprocessing

import datetime


class DataHandler(object):
    """A data handler object for the MIMIC iii dataset

    Attributes:
        db_name: A string representing the database connection string
        db_schema: The schema to use in database queries
    """

    def __init__(self, name='postgresql://mimic_user@localhost:5432/mimic', schema='mimiciii'):
        """Return DataHandler object with name and schema assigned."""
        self.db_name = name
        self.db_schema = schema

        self.vital_ids = {
                50912: 'creatinine',  # creatinine levels indicate kidney issues
                50813: 'lactate',     # lactate levels indicate shock and cellular anirobic respiration
                50889: 'CRP',         # C-reactive protein systemic inflammation
                51300: 'WBC',         # White blood cell count indicates systemic reaction to infection
                51006: 'BUN',         # Blood Urea Nitrogen indicates kidney issues
                51288: 'ESR',         # erythrocyte sedimentation rate another inflammation test
                51265: 'platelet',    # decreased platelet counts parallel the severity of infection
                50825: 'tempurature', # tempurature is highly indicative of infection and/or immune response
                50816: 'oxygen',
                51275: 'PT',
                51274: 'PTT',
                51277: 'RBCDW',       # red blood cell distribution width
                51256: 'neutrophils',
                50818: 'pco2',
                50821: 'po2',
                50893: 'calcium',
                50931: 'glucose',
                51221: 'hematocrit',
                51222: 'hemoglobin',
                51244: 'lymphocytes',
                51248: 'MCH',
                51237: 'INR',
                50956: 'lipase',
                50878: 'AST',
                50867: 'amylase',
                50863: 'alkaline phosphatase',
                50820: 'PH',
                50882: 'bicarbonate'
            }

    def connect(self):
        """Connects to database and assigns proper ORM objects"""
        # Set up SQL Alchemy engine and session
        Base = automap_base()

        # Doing basic probes on data locally
        engine = create_engine("postgresql://mimic_user@localhost:5432/mimic")

        # Reflect the tables
        Base.prepare(engine, reflect=True, schema='mimiciii')

        # mapped classes are now created with names by default
        # matching that of the table name.
        self.Admission = Base.classes.admissions
        self.Patient = Base.classes.patients
        self.LabEvent = Base.classes.labevents
        self.BioEvent = Base.classes.microbiologyevents

        self.session = Session(engine)

    def period(self, row, period):
        """Creates period of study importance"""
        if row['deathtime'] is None:
            return 0
        elif row['deathtime'] - row['admittime'] > period:
            return 0
        else:
            return 1
        row['admittime']

    def age(self, row):
        """Calculates patient age"""
        possible_age = int((row['admittime'] - row['dob'])/pd.Timedelta('365 days'))
        # For those holder than 89, their ages have been removed and set
        # to 300 years prior to admission.
        if possible_age < 0:
            # 91.4 is the median age for those with removed ages. This is
            # what we will set all ages to that are older than 89
            possible_age = 91
        return possible_age

    def acquire_vitals(self, lab_events, patient_vitals, patient_info):
        # Cycle through data, check for appropriate data within time period, average values and store
        one_day = pd.Timedelta('1 days')
        # Each hospital stay, think of it as an individual patient (though technically not true)
        for hadm_id, group in lab_events:
            sub_groups = group.groupby('itemid')
            admittance_time = patient_info.loc[patient_info.hadm_id==hadm_id]['admittime'].values[0]
            # Each lab item type
            for lab_item, sub_group in sub_groups:
                day_results = sub_group[((sub_group.charttime - admittance_time) < one_day)]
                if len(day_results['valuenum'].values) == 0:
                    mean = np.nan
                    maximum = np.nan
                    minimum = np.nan
                else:
                    mean = day_results['valuenum'].values.mean()

                    maximum = day_results['valuenum'].values.max()
                    minimum = day_results['valuenum'].values.min()

                patient_vitals.set_value(hadm_id, self.vital_ids[lab_item], mean)

                # patient_vitals.set_value(hadm_id, self.vital_ids[lab_item] + '_max', maximum)
                # patient_vitals.set_value(hadm_id, self.vital_ids[lab_item] + '_min', minimum)

    def admissions_query(self):
        """Query and calculate period of interest for mortality. Append to df"""
        admission_query = self.session.query(self.Admission).filter_by(diagnosis='SEPSIS')
        df = pd.read_sql(admission_query.statement, admission_query.session.bind)
        df['death_period'] = df.apply(lambda row: self.period (row, pd.Timedelta('30 days')),axis=1)
        adm_col = ['subject_id', 'hadm_id', 'admittime', 'admission_type', 'insurance', 'ethnicity', 'death_period']
        return df[adm_col]

    def patient_query(self):
        """Obtain patient information and trim unnecessary information"""
        patient_query = self.session.query(self.Patient)
        patients = pd.read_sql(patient_query.statement, patient_query.session.bind)
        patients = patients[['subject_id', 'gender', 'dob']]
        return patients

    def lab_event_query(self, patient_info):
        # Query database labevents for all information related to all hospital admission ids we are interested in
        # along with all item types we are interested in, defined above
        patient_hadm_ids = patient_info.hadm_id.tolist()
        # Beautiful query /sarcasm
        lab_event_query = self.session.query(self.LabEvent).filter(self.LabEvent.hadm_id.in_(patient_hadm_ids)).filter(self.LabEvent.itemid.in_(self.vital_ids.keys()))
        lab_events = pd.read_sql(lab_event_query.statement, lab_event_query.session.bind).groupby('hadm_id')

        # Prepare joining copy of patient vitals
        patient_vitals = patient_info[['hadm_id']].copy()
        for value in self.vital_ids.values():
            patient_vitals[value] = np.nan

            # patient_vitals[value + "_max"] = np.nan
            # patient_vitals[value + "_min"] = np.nan


        patient_vitals = patient_vitals.set_index('hadm_id')

        self.acquire_vitals(lab_events, patient_vitals, patient_info)
        return patient_vitals

    def prior_hospital_stays(self, patient_info):

        patient_ids = patient_info.subject_id.tolist()
        patient_hadm_ids = patient_info.hadm_id.tolist()

        hadm_id_tuple_list = zip(patient_ids, patient_hadm_ids)

        prior_visits_query = self.session.query(self.Admission).filter(self.Admission.subject_id.in_(patient_ids))
        prior_visits = pd.read_sql(prior_visits_query.statement, prior_visits_query.session.bind).groupby('subject_id')

        patient_info['prior'] = np.nan

        for patient_id, group in prior_visits:
            patient_admissions = [item for item in hadm_id_tuple_list if item[0] == patient_id]

            for item in patient_admissions:
                admit_time = group.loc[group['hadm_id'] == item[1]].iloc[0]['admittime']
                priors = len(group[(group['admittime'] < admit_time)])
                patient_info.loc[patient_info.hadm_id == item[1], 'prior'] = priors
