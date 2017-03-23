Project Name: Survivability of ICU Patients with Severe Sepsis/Septic Shock
Author: Jeremy B. Crowe

Description: The following project an analysis and model comparison in
predicting the survivability of sepsis using patient vitals within the
first 24 hours from ICU admission.

Dataset: The dataset is the MIMIC-III dataset provided by MIT with data from
the Beth Israel Deaconess Medical center in Boston Massachusetts.
This dataset requires completion of a short certification course detailing the
ethical guidelines in dealing with de-identified patient information. This
dataset was suggested for use by Udacity and can be obtained from the following
url: mimic.physionet.org

Files: The project contains several files including two jupyter notebooks and
a helper python file. Here they will be described.

    * Septic Feature Probe.ipynb: This notebook contains much of the initial
        analysis, preprocessing, and visualizations on the dataset. It contains
        much of the interesting work including feature comparison and
        correlational analysis.

    * Sepsis Model Comparison.ipynb: This notebook also contains data
        pre-processing in much the same way as the previous notebook however
        most of the work goes into model training, tweaking, and testing.
        Four different models are compared in this notebook.

    * mimicpreprocess.py: This is a helper python file that contains almost
        identical pre-processing work as in the first notebook. The purpose of
        offloading this was to keep the model comparison notebook concise and
        focused more on the model building and testing process itself.

Libraries: There were certain libraries used that were not standard throughout
the course. They will be briefly described here.
    * SQLAlchemy: With much of the data stored in a postgres database,
        sqlalchemy makes it very easy to access and query using its easy to use
        ORM. It was most definitely possible to just write raw sql but this
        library saved some time and was fun to learn.
    * Keras: Keras is a high-level neural network API, written in Python and
        runs on top of either TensorFlow or Theano. In this case, TensorFlow.
         It makes fast implementation and experimentation possible since TF or
         Theano require much more architecture and implementation time.
    * XGBoost: XGBoost is an optimized distributed gradient boosting library
        designed for efficiency. It implements machine learning algorithms
        under the Gradient Boosting framework. It has significant community
        support and is considered a best in class predictor.
    * Standard ML libraries: numpy, pandas, and scikitlearn
    * Standard visualization libraries: matplotlib, and seaborn for improved
        visuals.
