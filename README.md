# subdocument-mutations
A sample project showing how to generate update statement based on mutations of elements in a json document.

It receives one or more dicts which describe updates needed for the json document, which can be in the following formats:  
```
    {  
    
        "posts": [  
        
            { "_id": 2, "value": "too" }, ( this is an update )  
            
            { "value": "four"},          ( this is an add )  
            
            { "_id": 4, "_delete": True } ( this is a remove )  
            
        ]  
        
    }  
```

It outputs one or more update statements which can then be performed on the json document.  
```
{  
  "$update": { "posts.0.value": "too" },  
  "$add": { "posts": [ { "value": "four" } ] },  
  "$remove" : { "posts.2" : True }  
}
```

# Usage
The code is contained as a class in `subdocument_mutations.py`. You can import this file into your python code and call the class as shown:  

```
  import subdocument_mutations as sdm
  
  document = {
    "name": "my document",
    "items": [
      {
        "_id": 0,
        "value": "my value"
    ]
  }
  
  mutation = { "items": [ { "_id": 0, "value": "too" } ] }
  
  mutator = sdm.subdocument_mutation()
  
  update_statement = mutator.generate_update_statement(document, mutations)
```
