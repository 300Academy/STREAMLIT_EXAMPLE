import streamlit as PI_STREAMLIT
import polars as PI_POLARS


from Z_SHARED_FUNCTIONS.FC_GET_EXCEL_BYTES import FC_GET_EXCEL_BYTES
from Z_SHARED_FUNCTIONS.FC_BTN_DOWNLOAD import FC_BTN_DOWNLOAD

ZV_LI_DI_TABLES = [
    {
        'title': 'Table 1 - Suppliers',
        'filename': 'suppliers',
        'dataframe': PI_POLARS.DataFrame({
            'Supplier': ['A100', 'B200'],
            'Amount': [1000, 2500]
        })
    },
    {
        'title': 'Table 2 - Customers',
        'filename': 'customers',
        'dataframe': PI_POLARS.DataFrame({
            'Customer': ['C100', 'C200'],
            'Amount': [500, 900]
        })
    }
]

for i, ZV_OB_TABLE in enumerate(ZV_LI_DI_TABLES, start=1):

    PI_STREAMLIT.markdown(f"### {ZV_OB_TABLE['title']}")

    ZV_BY_EXCEL_DATA = FC_GET_EXCEL_BYTES(
        ZVFCI_DF=ZV_OB_TABLE['dataframe']
    )

    FC_BTN_DOWNLOAD(
        ZVFCI_BY_DATA=ZV_BY_EXCEL_DATA,
        ZVFCI_ST_FILENAME=ZV_OB_TABLE['filename'],
        ZVFCI_ST_LABEL='Download Excel',
        ZVFCI_ST_KEY=f"download_button_{i}"
    )

    PI_STREAMLIT.dataframe(
        ZV_OB_TABLE['dataframe'],
        width='stretch',
        hide_index=True
    )