import json
from typing import List
from flask_restplus import fields

from controllers.common.models.CommonModels import CommonModels
from infrastructor.IocManager import IocManager

class AntennaModels:
    ns = IocManager.api.namespace('Antenna', description='Antenna endpoints',
                                  path='/api/ai/Antenna')

    antenna_info = IocManager.api.model('AntennaInfo', {
        'ONAIR_SITE_TABLE_ID': fields.Float(description='ONAIR_SITE_TABLE_ID', required=False, max=10000000000),
        'SITE_IS_OIS': fields.Float(description='SITE_IS_OIS', required=False,max=10000000000),
        'SITE_ENVIRONMENT_TYPE_ID': fields.Float(description='SITE_ENVIRONMENT_TYPE_ID', required=False, max=10000000000),
        'SITE_SITE_TYPE_ID': fields.Float(description='SITE_SITE_TYPE_ID', required=False, max=10000000000),
        'SITE_MONTAGE_TYPE_ID': fields.Float(description='SITE_MONTAGE_TYPE_ID', required=False, max=10000000000),
        'SITE_RN_SUBREGION_ID': fields.Float(description='SITE_RN_SUBREGION_ID', required=False, max=10000000000),
        'SITE_RN_REGION_ID': fields.Float(description='SITE_RN_REGION_ID', required=False, max=10000000000),
        'SITE_RN_MAIN_REGION_ID': fields.Float(description='SITE_RN_MAIN_REGION_ID', required=False, max=10000000000),
        'SITE_COUNTY_ID': fields.Float(description='SITE_COUNTY_ID', required=False, max=10000000000),
        'SITE_CITYAC_ID': fields.Float(description='SITE_CITYAC_ID', required=False, max=10000000000),
        'SIR_CREATED_BY_USER_ID': fields.Float(description='SIR_CREATED_BY_USER_ID', required=False, max=10000000000),
        'SIR_MONTH_ID': fields.Float(description='SIR_MONTH_ID', required=False, max=10000000000),
        'SIR_YEAR_ID': fields.Float(description='SIR_YEAR_ID', required=False, max=10000000000),
        'SIR_REASON_ID': fields.Float(description='SIR_REASON_ID', required=False, max=10000000000),
        'IR_TYPE_ID': fields.Float(description='IR_TYPE_ID', required=False, max=10000000000),
    })

    make_calcualation_model = IocManager.api.model('AntennaMakeCalculationModel', {
        'AntennaInfo': fields.Nested(antenna_info, description='Antenna Info list',
                                required=False),
    })

    @staticmethod
    def get_data_operation_contact_model(data_operation_contact: any) -> any:

        entity_model = any(
            Email=data_operation_contact.Email,
        )
        result_model = json.loads(json.dumps(entity_model.__dict__, default=CommonModels.date_converter))
        return result_model

    @staticmethod
    def get_data_operation_contact_models(data_operation_contacts: List[any]) -> List[
        any]:
        entities = []
        for data_operation_contact in data_operation_contacts:
            entity = AntennaModels.get_data_operation_contact_model(data_operation_contact)
            entities.append(entity)
        return entities
