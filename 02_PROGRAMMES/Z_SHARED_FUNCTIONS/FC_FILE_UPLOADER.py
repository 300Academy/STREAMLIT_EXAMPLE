import streamlit as PI_STREAMLIT

def FC_FILE_UPLOADER(
    ZVFCI_LI_ALLOWED_TYPES: list = ['csv', 'txt', 'xlsx'],
    ZVFCI_BO_ACCEPT_MUL_FILES: bool = True,
    ZVFCI_ST_KEY: str = 'file_uploader',
    ZVFCI_BO_USE_WIDTH: bool = False
):
    
    ZV_ST_ALLOWED_TYPES = ', '.join(ZVFCI_LI_ALLOWED_TYPES)
    ZV_ST_LABEL = f'Allowed file type(s): {ZV_ST_ALLOWED_TYPES}'

    ZV_OB_KWARGS = {}

    if ZVFCI_BO_USE_WIDTH:
        ZV_OB_KWARGS['width'] = 'stretch'

    return PI_STREAMLIT.file_uploader(
        label=ZV_ST_LABEL,
        type=ZVFCI_LI_ALLOWED_TYPES,
        accept_multiple_files=ZVFCI_BO_ACCEPT_MUL_FILES,
        key=ZVFCI_ST_KEY,
        label_visibility='visible',
        **ZV_OB_KWARGS
    )