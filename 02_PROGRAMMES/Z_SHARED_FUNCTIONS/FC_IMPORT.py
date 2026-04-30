import io as PI_IO
import polars as PI_POLARS

def FC_IMPORT_TEXT(
  ZVFCI_OB_FILE,
  ZVFCI_ST_DELIMITER=None,
  ZVFCI_LI_ENCODINGS=None
):
    ZV_DF = None
    ZV_ER_LAST = None

    if ZVFCI_ST_DELIMITER == None:
        ZVFCI_ST_DELIMITER = '\t'

    if ZVFCI_LI_ENCODINGS == None:
        ZVFCI_LI_ENCODINGS =[
            'utf8',
            'utf-8-sig',
            'utf8-lossy',
            'windows-1252',
            'latin1',
            'iso-8859-1',
            'iso-8859-15',
            'utf-16',
            'utf-16-le',
            'utf-16-be',
            'cp1250',
            'cp1251',
            'cp1253',
            'cp1254',
            'cp1257'    
        ]

    for ZV_ST_ENCODING in ZVFCI_LI_ENCODINGS:

        try:
            if hasattr(ZVFCI_OB_FILE, 'getvalue'):
                ZV_OB_SOURCE = PI_IO.BytesIO(ZVFCI_OB_FILE.getvalue())
            else:
                ZV_OB_SOURCE = ZVFCI_OB_FILE

            ZV_DF = (
                PI_POLARS.read_csv(
                    ZV_OB_SOURCE,
                    separator=ZVFCI_ST_DELIMITER,
                    encoding=ZV_ST_ENCODING,
                    ignore_errors=True,
                    has_header=True,
                    infer_schema_length=0,
                    null_values=[''],
                    quote_char=None,
                    truncate_ragged_lines=True   
                )
                .fill_null('')
            )

            break

        except Exception as ZV_ER:
            ZV_ER_LAST = ZV_ER

    if ZV_DF is None:
        print(f'Last error: {ZV_ER_LAST}')
    
    return ZV_DF
