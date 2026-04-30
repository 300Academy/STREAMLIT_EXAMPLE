import streamlit as PI_STREAMLIT
from datetime import datetime as PI_DATETIME

def FC_BTN_DOWNLOAD(
    ZVFCI_BY_DATA: bytes,
    ZVFCI_ST_FILENAME: str,
    ZVFCI_ST_LABEL: str = 'Download',
    ZVFCI_ST_KEY: str = 'download_button'
):
    ZV_ST_TIMESTAMP = PI_DATETIME.now().strftime('%Y%m%d_%H%M%S')

    return PI_STREAMLIT.download_button(
        label=ZVFCI_ST_LABEL,
        data=ZVFCI_BY_DATA,
        file_name=f'{ZVFCI_ST_FILENAME}_{ZV_ST_TIMESTAMP}.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        key=ZVFCI_ST_KEY,
        width='stretch'
    )