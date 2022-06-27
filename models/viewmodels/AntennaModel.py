
class AntennaModel:
    def __init__(self,
                ONAIR_SITE_TABLE_ID : int = None,
                SITE_IS_OIS : int = None,
                SITE_ENVIRONMENT_TYPE_ID : int = None,
                SITE_SITE_TYPE_ID : int = None,
                SITE_MONTAGE_TYPE_ID : int = None,
                SITE_RN_SUBREGION_ID : int = None,
                SITE_RN_REGION_ID : int = None,
                SITE_RN_MAIN_REGION_ID : int = None,
                SITE_COUNTY_ID : int = None,
                SITE_CITY_ID : int = None,
                SIR_CREATED_BY_USER_ID : int = None,
                SIR_MONTH_ID : int = None,
                SIR_YEAR_ID : int = None,
                SIR_REASON_ID : int = None,
                IR_TYPE_ID : int = None,
                 ):
        self.ONAIR_SITE_TABLE_ID : int = ONAIR_SITE_TABLE_ID
        self.SITE_IS_OIS : int = SITE_IS_OIS
        self.SITE_ENVIRONMENT_TYPE_ID : int = SITE_ENVIRONMENT_TYPE_ID
        self.SITE_SITE_TYPE_ID : int = SITE_SITE_TYPE_ID
        self.SITE_MONTAGE_TYPE_ID : int = SITE_MONTAGE_TYPE_ID
        self.SITE_RN_SUBREGION_ID : int = SITE_RN_SUBREGION_ID
        self.SITE_RN_REGION_ID : int = SITE_RN_REGION_ID
        self.SITE_RN_MAIN_REGION_ID : int = SITE_RN_MAIN_REGION_ID
        self.SITE_COUNTY_ID : int = SITE_COUNTY_ID
        self.SITE_CITY_ID : int = SITE_CITY_ID
        self.SIR_CREATED_BY_USER_ID : int = SIR_CREATED_BY_USER_ID
        self.SIR_MONTH_ID : int = SIR_MONTH_ID
        self.SIR_YEAR_ID : int = SIR_YEAR_ID
        self.SIR_REASON_ID : int = SIR_REASON_ID
        self.IR_TYPE_ID : int = IR_TYPE_ID