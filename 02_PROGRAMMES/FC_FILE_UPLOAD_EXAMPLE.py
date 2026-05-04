import streamlit as PI_STREAMLIT
import polars as PI_POLARS
import numpy as PI_NUMPY
from datetime import date as PI_DATE, timedelta as PI_TIMEDELTA

from Z_SHARED_FUNCTIONS.FC_FILE_UPLOADER import FC_FILE_UPLOADER
from Z_SHARED_FUNCTIONS.FC_IMPORT import FC_IMPORT_TEXT

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
    ZV_DF = FC_IMPORT_TEXT(
        ZV_OB_UPLOADED_FILE,
        ZVFCI_ST_DELIMITER = ','
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

ZV_ST_FILTER_COLUMN = (
        PI_STREAMLIT.selectbox(
        'Select column to filter',
        ZV_DF.columns
    )
)    

ZV_LI_FILTER_VALUES = (
    ZV_DF
    .select(ZV_ST_FILTER_COLUMN)
    .unique()
    .sort(ZV_ST_FILTER_COLUMN)
    .to_series()
    .to_list()
)

ZV_LI_SELECTED_VALUES = (
        PI_STREAMLIT.multiselect(
        'Select values',
        ZV_LI_FILTER_VALUES,
        default=ZV_LI_FILTER_VALUES
    )
)

ZV_DF = (
    ZV_DF
    .filter(
        PI_POLARS.col(ZV_ST_FILTER_COLUMN).is_in(ZV_LI_SELECTED_VALUES)
    )
)

PI_STREAMLIT.dataframe(
    ZV_DF.to_dicts(),
    use_container_width=True,
    on_select='rerun',
    selection_mode='multi-row'    
)



# ------------------------
# COLUMN SELECTION
# ------------------------
ZV_LI_COLUMNS = [
    ZV_ST_COLUMN
    for ZV_ST_COLUMN in ZV_DF.columns
]

if len(ZV_LI_COLUMNS) > 0:

    ZV_ST_SELECTED_NUMERIC_COLUMN = PI_STREAMLIT.selectbox(
        'Select numeric column',
        ZV_LI_COLUMNS
    )

    ZV_LI_CATEGORY_COLUMNS = [
        ZV_ST_COLUMN
        for ZV_ST_COLUMN in ZV_LI_COLUMNS
        if ZV_ST_COLUMN != ZV_ST_SELECTED_NUMERIC_COLUMN
    ]

    ZV_ST_SELECTED_CATEGORY_COLUMN = PI_STREAMLIT.selectbox(
        'Select category column',
        ['None']+ZV_LI_CATEGORY_COLUMNS
    )

    ZV_LI_NUMERIC_COLUMNS_2 = [
        col for col in ZV_LI_COLUMNS
        if col != ZV_ST_SELECTED_NUMERIC_COLUMN
    ]    

    ZV_LI_CATEGORY_COLUMNS_2 = [
        col for col in ZV_LI_COLUMNS
        if col != ZV_ST_SELECTED_CATEGORY_COLUMN
    ]        

    ZV_ST_SELECTED_NUMERIC_COLUMN2 = PI_STREAMLIT.selectbox(
        'Select second numeric column to show scatter chart',
        ['None']+ZV_LI_NUMERIC_COLUMNS_2
    )

    ZV_ST_SELECTED_CATEGORY_COLUMN2 = PI_STREAMLIT.selectbox(
        'Select second category column to show heat map',
        ['None']+ZV_LI_CATEGORY_COLUMNS_2
    )         

    ZV_LI_CAST_EXPRESSIONS = [
        PI_POLARS.col(ZV_ST_SELECTED_NUMERIC_COLUMN)
        .cast(PI_POLARS.Float64, strict=False)
        .alias(ZV_ST_SELECTED_NUMERIC_COLUMN)
    ]

    if ZV_ST_SELECTED_NUMERIC_COLUMN2 != 'None':
        ZV_LI_CAST_EXPRESSIONS.append(
            PI_POLARS.col(ZV_ST_SELECTED_NUMERIC_COLUMN2)
            .cast(PI_POLARS.Float64, strict=False)
            .alias(ZV_ST_SELECTED_NUMERIC_COLUMN2)
        )

    ZV_DF = (
        ZV_DF
        .with_columns(ZV_LI_CAST_EXPRESSIONS)
    )

    # ------------------------
    # SIMPLE CHART
    # ------------------------

    if ZV_ST_SELECTED_CATEGORY_COLUMN == 'None':

        PI_STREAMLIT.subheader('Simple Charts - choose a category to see charts grouped per category')

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

    elif (ZV_ST_SELECTED_CATEGORY_COLUMN != 'None'):

        PI_STREAMLIT.subheader('Charts for numeric and category selection')

        # Grouped data
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
            use_container_width=True,
            on_select='rerun',
            selection_mode='multi-row'             
        )

        # Stacked bar chart 
        PI_STREAMLIT.vega_lite_chart(
            ZV_DF.to_dicts(),
            {
                'title': 'Bar chart',
                'mark': 'bar',
                'encoding': {
                    'x': {'field': ZV_ST_SELECTED_CATEGORY_COLUMN, 'type': 'nominal'},
                    'y': {'aggregate': 'sum', 'field': ZV_ST_SELECTED_NUMERIC_COLUMN},
                    'color': {'field': 'Category', 'type': 'nominal'}
                }
            },
            use_container_width=True
        )

        PI_STREAMLIT.vega_lite_chart(
            ZV_DF_GROUPED.to_dicts(),
            {
                'title': 'Line chart by category',
                'mark': {'type': 'line', 'point': True, 'tooltip': True},
                'encoding': {
                    'x': {'field': ZV_ST_SELECTED_CATEGORY_COLUMN, 'type': 'nominal'},
                    'y': {'field': ZV_ST_SELECTED_NUMERIC_COLUMN, 'type': 'quantitative'}
                }
            },
            use_container_width=True
        )

        PI_STREAMLIT.vega_lite_chart(
            ZV_DF_GROUPED.to_dicts(),
            {
                'title': 'Area chart by category',
                'mark': {'type': 'area', 'tooltip': True},
                'encoding': {
                    'x': {
                        'field': ZV_ST_SELECTED_CATEGORY_COLUMN,
                        'type': 'nominal'
                    },
                    'y': {
                        'field': ZV_ST_SELECTED_NUMERIC_COLUMN,
                        'type': 'quantitative'
                    }
                }
            },
            use_container_width=True
        )        

        # Donut
        PI_STREAMLIT.vega_lite_chart(
            ZV_DF_GROUPED.to_dicts(),
            {
                'title': 'Donut',
                'mark': {'type': 'arc', 'innerRadius': 50, 'tooltip': True},
                'encoding': {
                    'theta': {'field': ZV_ST_SELECTED_NUMERIC_COLUMN, 'type': 'quantitative'},
                    'color': {'field': ZV_ST_SELECTED_CATEGORY_COLUMN, 'type': 'nominal'}
                }
            },
            use_container_width=True
        )

        if (
            (ZV_ST_SELECTED_CATEGORY_COLUMN != 'None') and
            (ZV_ST_SELECTED_CATEGORY_COLUMN2 != 'None')
        ):
            
            ZV_DF_HEATMAP = (
                ZV_DF
                .with_columns(
                    PI_POLARS.col(ZV_ST_SELECTED_CATEGORY_COLUMN2)
                    .cast(PI_POLARS.Utf8)
                    .alias(ZV_ST_SELECTED_CATEGORY_COLUMN2)
                )
            )            
            
            # Heat map
            PI_STREAMLIT.vega_lite_chart(
                ZV_DF_HEATMAP
                .to_dicts(),
                {
                    'title':'Heat map',
                    'mark': 'rect',
                    'encoding': {
                        'x': {'field': ZV_ST_SELECTED_CATEGORY_COLUMN, 'type': 'nominal'},
                        'y': {'field': ZV_ST_SELECTED_CATEGORY_COLUMN2, 'type': 'nominal'},
                        'color': {
                            'aggregate': 'sum',
                            'field': ZV_ST_SELECTED_NUMERIC_COLUMN,
                            'type': 'quantitative'                            
                        }
                    }
                },
                use_container_width=True
            )        

        # Box plot
        PI_STREAMLIT.vega_lite_chart(
            ZV_DF.to_dicts(),
            {
                'title':'Boxplot',
                'mark': 'boxplot',
                'encoding': {
                    'y': {
                        'field': ZV_ST_SELECTED_NUMERIC_COLUMN,
                        'type': 'quantitative'
                    },
                    'x': {
                        'field': ZV_ST_SELECTED_CATEGORY_COLUMN,
                        'type': 'nominal'
                    } if ZV_ST_SELECTED_CATEGORY_COLUMN != 'None' else {}
                }
            },
            use_container_width=True
        )        

    if (
        (ZV_ST_SELECTED_CATEGORY_COLUMN != 'None') and 
        (ZV_ST_SELECTED_NUMERIC_COLUMN2 != 'None')
    ):

        # Scatter chart
        PI_STREAMLIT.vega_lite_chart(
            ZV_DF.to_dicts(),
            {
                'title':'Scatter chart',                
                'mark': {'type': 'point', 'tooltip': True},
                'encoding': {
                    'x': {'field': ZV_ST_SELECTED_NUMERIC_COLUMN, 'type': 'quantitative'},
                    'y': {'field': ZV_ST_SELECTED_NUMERIC_COLUMN2, 'type': 'quantitative'},
                    'color': {'field': ZV_ST_SELECTED_CATEGORY_COLUMN, 'type': 'nominal'} if ZV_ST_SELECTED_CATEGORY_COLUMN != 'None' else {}
                }
            },
            use_container_width=True
        )


else:
    PI_STREAMLIT.warning('No numeric columns found in dataset.')