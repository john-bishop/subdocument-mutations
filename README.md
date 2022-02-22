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
  
# Additional Notes
* Approximately 3.5 hrs was spent on this
* If I spent more time on this I would:
*   Add more unit tests for the class, especially the private methods
*   Add more exception handling around edge cases, so that I could provide clear error messages around
*       Updates to sub elements where the specified id doesn't exist
*       More validation around paths to ensure the path specified in the mutations actually exists. Would work to find a way to fail fast here.
*       Validate the format of provided mutations to ensure they are in the appropriate format
*   Look for ways to break up the code into smaller methods to help facilitate better, more focused, unit tests
