import streamlit as PI_STREAMLIT
import polars as PI_POLARS
import numpy as PI_NUMPY
from datetime import date as PI_DATE, timedelta as PI_TIMEDELTA

from Z_SHARED_FUNCTIONS.FC_FILE_UPLOADER import FC_FILE_UPLOADER

PI_STREAMLIT.set_page_config(page_title='Upload files, tables and graphs demo', layout='wide')
PI_STREAMLIT.title('Upload files, tables and graphs demo')

try:
    from FC_APP_CONFIG import ZV_BO_USE_WIDTH
except ImportError:
    ZV_BO_USE_WIDTH = True

ZV_NU_ROWS = PI_STREAMLIT.slider('Number of random rows', 10, 500, 100)
ZV_NU_MULTIPLIER = PI_STREAMLIT.number_input('Multiplier variable', min_value=1, max_value=20, value=5)

# ------------------------
# DATA SOURCE
# ------------------------
ZV_OB_UPLOADED_FILE = FC_FILE_UPLOADER(
    ZVFCI_LI_ALLOWED_TYPES = ['csv'],
    ZVFCI_BO_ACCEPT_MUL_FILES = False,
    ZVFCI_ST_KEY = 'UPLOAD_CSV_01',  
    ZVFCI_BO_USE_WIDTH = ZV_BO_USE_WIDTH
)

if ZV_OB_UPLOADED_FILE is not None:
    ZV_DF = PI_POLARS.read_csv(
        ZV_OB_UPLOADED_FILE,
        try_parse_dates=True
    )

    PI_STREAMLIT.success('Using uploaded CSV file')

else:
    PI_NUMPY.random.seed(42)

    ZV_DT_START = PI_DATE.today()
    ZV_DF = PI_POLARS.DataFrame({
        'Date': [
            ZV_DT_START + PI_TIMEDELTA(days=i)
            for i in range(ZV_NU_ROWS)
        ],
        'Sales': PI_NUMPY.random.randint(100, 1000, ZV_NU_ROWS),
        'Costs': PI_NUMPY.random.randint(50, 700, ZV_NU_ROWS),
        'RiskScore': PI_NUMPY.random.rand(ZV_NU_ROWS) * ZV_NU_MULTIPLIER,
        'Category': PI_NUMPY.random.choice(['Low', 'Medium', 'High'], ZV_NU_ROWS)
    })

    PI_STREAMLIT.info('Using random demo data')


PI_STREAMLIT.subheader('Data Preview')

PI_STREAMLIT.dataframe(
    ZV_DF.to_dicts(),
    use_container_width=True
)


# ------------------------
# COLUMN SELECTION
# ------------------------
ZV_LI_NUMERIC_COLUMNS = [
    ZV_ST_COLUMN
    for ZV_ST_COLUMN, ZV_OB_DTYPE in zip(ZV_DF.columns, ZV_DF.dtypes)
    if ZV_OB_DTYPE.is_numeric()
]

ZV_LI_CATEGORY_COLUMNS = [
    ZV_ST_COLUMN
    for ZV_ST_COLUMN, ZV_OB_DTYPE in zip(ZV_DF.columns, ZV_DF.dtypes)
    if ZV_OB_DTYPE in [
        PI_POLARS.String,
        PI_POLARS.Categorical,
        PI_POLARS.Date,
        PI_POLARS.Datetime
    ]
]


if len(ZV_LI_NUMERIC_COLUMNS) > 0:

    ZV_ST_SELECTED_NUMERIC_COLUMN = PI_STREAMLIT.selectbox(
        'Select numeric column',
        ZV_LI_NUMERIC_COLUMNS
    )

    ZV_ST_SELECTED_CATEGORY_COLUMN = PI_STREAMLIT.selectbox(
        'Select category column (optional)',
        ['None'] + ZV_LI_CATEGORY_COLUMNS
    )


    # ------------------------
    # SIMPLE CHART
    # ------------------------
    if ZV_ST_SELECTED_CATEGORY_COLUMN == 'None':

        PI_STREAMLIT.subheader('Simple Charts')

        ZV_OB_COL1, ZV_OB_COL2 = PI_STREAMLIT.columns(2)

        with ZV_OB_COL1:
            PI_STREAMLIT.line_chart(
                ZV_DF
                .select(ZV_ST_SELECTED_NUMERIC_COLUMN)
                .to_dicts()
            )

        with ZV_OB_COL2:
            PI_STREAMLIT.bar_chart(
                ZV_DF
                .select(ZV_ST_SELECTED_NUMERIC_COLUMN)
                .to_dicts()
            )

        PI_STREAMLIT.area_chart(
            ZV_DF
            .select(ZV_ST_SELECTED_NUMERIC_COLUMN)
            .to_dicts()
        )


    # ------------------------
    # GROUPED CHART
    # ------------------------
    else:

        PI_STREAMLIT.subheader('Grouped Chart')

        ZV_DF_GROUPED = (
            ZV_DF
            .group_by(ZV_ST_SELECTED_CATEGORY_COLUMN)
            .agg(
                PI_POLARS.col(ZV_ST_SELECTED_NUMERIC_COLUMN).sum()
            )
            .sort(ZV_ST_SELECTED_CATEGORY_COLUMN)
        )

        PI_STREAMLIT.write('Aggregated data')

        PI_STREAMLIT.dataframe(
            ZV_DF_GROUPED.to_dicts(),
            use_container_width=True
        )

        PI_STREAMLIT.bar_chart(
            ZV_DF_GROUPED
            .to_dicts(),
            x=ZV_ST_SELECTED_CATEGORY_COLUMN,
            y=ZV_ST_SELECTED_NUMERIC_COLUMN
        )

        PI_STREAMLIT.line_chart(
            ZV_DF_GROUPED
            .to_dicts(),
            x=ZV_ST_SELECTED_CATEGORY_COLUMN,
            y=ZV_ST_SELECTED_NUMERIC_COLUMN
        )

else:
    PI_STREAMLIT.warning('No numeric columns found in dataset.')