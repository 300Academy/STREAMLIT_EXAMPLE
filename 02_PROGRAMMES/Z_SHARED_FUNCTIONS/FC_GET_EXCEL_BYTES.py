from io import BytesIO
import polars as PI_POLARS

def FC_GET_EXCEL_BYTES(ZVFCI_DF: PI_POLARS.DataFrame) -> bytes:
    ZV_OB_EXCEL_BUF = BytesIO()

    ZVFCI_DF.write_excel(
        workbook=ZV_OB_EXCEL_BUF,
        worksheet='Results'
    )

    return ZV_OB_EXCEL_BUF.getvalue()