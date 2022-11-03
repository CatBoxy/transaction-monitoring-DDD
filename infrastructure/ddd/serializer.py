import json

from infrastructure.ddd.serializable import Serializable


class Serializer():
    # debe usar el toMap y fromMap para generar un json desde un dict y viceversa
    @staticmethod
    def serialize(payload: Serializable):
        payloadMap = payload.toMap()
        return json.dumps(payloadMap)

    @staticmethod
    def unserialize(jsonObject) -> dict:
        pass



