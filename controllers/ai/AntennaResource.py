import json
from flask_cors import cross_origin
from models.viewmodels.AntennaModel import AntennaModel
from injector import inject
from controllers.common.models.CommonModels import CommonModels
from controllers.ai.models.AntennaModels import AntennaModels
from domain.ai.services.NeuralNetworkModelService import NeuralNetworkModelService
from infrastructor.IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.exception.OperationalException import OperationalException

@AntennaModels.ns.route("")
class AntennaResource(ResourceBase):
    @inject
    def __init__(self, neural_network_model_service: NeuralNetworkModelService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.neural_network_model_service = neural_network_model_service


    @AntennaModels.ns.expect(AntennaModels.make_calcualation_model, validate=True)
    @AntennaModels.ns.marshal_with(CommonModels.SuccessModel)
    @IocManager.oauth.protect(["LocationShare.WebApi"])
    def post(self):
        """
        Data Operation definition
        """
        if 'AntennaInfo'  in IocManager.api.payload:
            data = json.loads(json.dumps(IocManager.api.payload["AntennaInfo"]),
                                           object_hook=lambda d: AntennaModel(**d))
        else:
            raise OperationalException("AntennaInfo required")
        result = self.neural_network_model_service.make_calculation(IocManager.api.payload)
        return CommonModels.get_response(result=result)

