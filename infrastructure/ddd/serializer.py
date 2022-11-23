import json
import importlib
from infrastructure.ddd.serializable import Serializable


class Serializer():
    # debe usar el toMap y fromMap para generar un json desde un dict y viceversa
    @staticmethod
    def serialize(payload: Serializable):
        payloadMap = payload.toMap()
        if "params" in payloadMap:
            paramsToDict = []
            for rule in payloadMap['params']:
                paramsToDict.append(rule.toMap())
            payloadMap['params'] = paramsToDict
        return json.dumps(payloadMap)

    @staticmethod
    def unserialize(jsonObject, event_type: str, event_module: str) -> Serializable:
        myDict = json.loads(jsonObject)
        my_module = importlib.import_module(event_module)
        MyClass = getattr(my_module, event_type)
        newAlert = MyClass.fromMap(myDict)
        return newAlert



