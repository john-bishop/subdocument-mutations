from argparse import ArgumentError
from urllib import request
import subdocument_mutations as sdm
import pytest

document = {
    "_id": 1,
    "name": "Johnny Content Creator",
    "posts": [
        {
            "_id": 2,
            "value": "one",
            "mentions": []
        },
        {
            "_id": 3,
            "value": "two",
            "mentions": [
                {
                    "_id": 5,
                    "text": "apple"
                },
                {
                    "_id": 6,
                    "text": "orange"
                }
            ]
        },
        {
        "_id": 4,
        "value": "three",
        "mentions": []
        }
    ]
}

def test_generate_update_statement_fail():
    mutator = sdm.subdocument_mutation()

    with pytest.raises(ArgumentError) as e:
        mutator.generate_update_statement(None, { "posts": [ { "_id": 2, "value": "too" } ] })

    with pytest.raises(ArgumentError) as e:
        mutator.generate_update_statement({ "posts": [ { "_id": 2, "value": "too" } ] }, None)
        
def test_generate_update_statement_succeed():
    mutations = [
        { "posts": [ { "_id": 2, "value": "too" } ] },
        { "posts": [ { "_id": 3, "mentions": [ { "_id": 5, "text": "pear" } ] } ] },
        { "posts": [ { "value": "four" } ] },
        { "posts": [ { "_id": 3, "mentions": [ { "text": "banana" } ] } ] },
        { "posts": [ { "_id": 2, "_delete": True } ] },
        {
            "posts": [
                { "_id": 2, "value": "too" },
                { "value": "four" },
                { "_id": 4, "_delete": True }
            ]
        }
    ]

    expected_outputs = [
        { "$update": { "posts.0.value": "too" } },
        { "$update": { "posts.1.mentions.0.text": "pear" } },
        { "$add": { "posts": [ { "value": "four" } ] } },
        { "$add": { "posts.1.mentions": [ { "text": "banana" } ] } },
        { "$remove" : { "posts.0" : True } },
        {
            "$update": { "posts.0.value": "too" },
            "$add": { "posts": [ { "value": "four" } ] },
            "$remove" : { "posts.2" : True }
        }
    ]

    mutator = sdm.subdocument_mutation()

    for i in range(0, len(mutations)):
        assert mutator.generate_update_statement(document, mutations[i]) == expected_outputs[i]
