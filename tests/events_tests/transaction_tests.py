import importlib
import json

from domain.events.transaction_created import TransactionCreated
from tests.validate_json import validateJSON


def test_transaction_created():
    """
    GIVEN TransactionCreated class instantiated
    WHEN the toMap and fromMap methods are called
    THEN toMap must return a json and fromMap must return an instantiated event from a dict
    """

    transaction = TransactionCreated(
        'id',
        'accNumber',
        'date',
        'loadedDate',
        'type',
        'method',
        '500',
        'ARS',
        'externalRef'
    )

    dtoString = transaction.toMap()
    isJson = validateJSON(dtoString)

    assert isJson is True

    myDict = json.JSONDecoder().decode(s=dtoString)

    assert type(myDict) == dict

    className = 'TransactionCreated'
    my_module = importlib.import_module("domain.events.transaction_created")
    MyClass = getattr(my_module, className)
    fromMap = getattr(MyClass, "fromMap")
    instance = fromMap(myDict)

    assert type(instance) == TransactionCreated
    assert instance.transactionId == 'id'
    assert instance.accountNumber == 'accNumber'
    assert instance.dateTime == 'date'
    assert instance.loadedDateTime == 'loadedDate'
    assert instance.type == 'type'
    assert instance.method == 'method'
    assert instance.amount == '500'
    assert instance.currency == 'ARS'
    assert instance.externalReference == 'externalRef'

