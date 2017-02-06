from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import pandas as pd
from sklearn import preprocessing

Base = automap_base()

engine = create_engine("postgresql://mimic_user@localhost:5432/mimic")

# reflect the tables
Base.prepare(engine, reflect=True, schema='mimiciii')

# mapped classes are now created with names by default
# matching that of the table name.
Admission = Base.classes.admissions
Patient = Base.classes.patients

session = Session(engine)

admission_query = session.query(Admission)

df = pd.read_sql(admission_query.statement, admission_query.session.bind)
# admission_type, hospital_expire_flag

# expiry = df[['admission_type', 'hospital_expire_flag']]
expiry = df.loc[:, ['admission_type', 'hospital_expire_flag']]

at_le = preprocessing.LabelEncoder()
at_le.fit(['ELECTIVE', 'URGENT', 'NEWBORN', 'EMERGENCY'])

expiry['admission_type_encoded'] = at_le.transform(expiry['admission_type'])

import pdb
pdb.set_trace()

# rudimentary relationships are produced
# session.add(Address(email_address="foo@bar.com", user=User(name="foo")))
# session.commit()

# collection-based relationships are by default named
# "<classname>_collection"
print (u1.address_collection)
