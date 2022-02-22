from argparse import ArgumentError

class subdocument_mutation:
    ADD_STATEMENT_KEY= "$add"
    UPDATE_STATEMENT_KEY = "$update"
    REMOVE_STATEMENT_KEY = "$remove"

    REMOVE_MUTATION_KEY = "_delete"
    ID_MUTATION_KEY = "_id"
    def __mutation_to_update_statement(self, document: dict, mutation: dict, path: str, next_path_element: str):
        """
        Navigate through the document based on the path specified in the mutation, and generate the appropriate update statement.
        This could be through one or many levels, so this will be done recursively.

        Parameters
        ----------
        document
            The complete dict that `mutation` needs to modify
        mutation
            A dict containing all the information needed to update `document`
            Examples:
                { "posts": [ { "_id": 2, "value": "too" } ] } ( this is an update )
                {
                    "posts": [
                        { "_id": 2, "value": "too" }, ( this is an update )
                        { "value": "four"},          ( this is an add )
                        { "_id": 4, "_delete": True } ( this is a remove )
                    ]
                }
        path
            The path through `document` that this function has generated so far. This will use indexes for sub elements
            instead of the id values provided in `mutation`
        next_path_element
            When recursion is needed, this will be the next value in the path to process.
            This should be an empty string for the first call to this function
        
        Returns
        -------
        A dict which contains all information needed in the update statement.
        """

        # If there is a next element specified, then add it to the path
        path += f".{next_path_element}" if next_path_element != "" else ""

        # If this is the first time this method is called, then set next_path_element equal to path
        # We need next_path_element set to the key of whatever element is going to be processed next
        next_path_element = next_path_element if next_path_element != "" else path
        current_element = document[next_path_element]

        # The current element might be an array of elements which we'll need to dig into recursively,
        #   or it'll be a singular dict meaning we're at the final stop and ready to generate an update
        #   statement
        if not isinstance(current_element, list):
            return { self.UPDATE_STATEMENT_KEY: { path: mutation } }
        else:
            try:
                id_value = mutation.pop(self.ID_MUTATION_KEY) # Get the id value to help find the index
            except KeyError:
                # The element has no id key, which means we are adding a new element (which will have
                #   it's id created automatically)
                return { self.ADD_STATEMENT_KEY: { path: [mutation] } }
            for index in range(0, len(current_element)):
                sub_element = current_element[index]
                if sub_element[self.ID_MUTATION_KEY] == id_value: # Loop through sub elements until we find the one we want
                    for mutated_key in mutation.keys():
                        if mutated_key == self.REMOVE_MUTATION_KEY:
                            return {self.REMOVE_STATEMENT_KEY: { f"{path}.{index}": True } }
                        if not isinstance(mutation[mutated_key], list):
                            new_mutation = mutation[mutated_key]
                        else:
                            new_mutation = mutation[mutated_key][0]
                        return self.__mutation_to_update_statement(sub_element, new_mutation, f"{path}.{index}", f"{mutated_key}")


    def generate_update_statement(self, document: dict, mutation: dict) -> dict:
        """
        The entry point for this class.
        It takes the information for all mutations needed on a specified document and generates all necessary update statements.

        Parameters
        ----------
        document
            The complete document, in dict form, which needs to be modified by `mutation`
        mutation
            A dict describing all the updates which need to be performed on `document`

        Returns
        -------
        A dict with all necessary output statements to update `document` based on `mutation`
        """

        if document is None or document == {}: raise ArgumentError(document, "You must provide a document with data.")
        if mutation is None or mutation == {}: raise ArgumentError(mutation, "You must provide at least one mutation.")

        output = {}
        for mutation_key in mutation.keys():
            mutation_item = mutation[mutation_key]
            for item in mutation_item:
                update_statement = self.__mutation_to_update_statement(document, item, mutation_key, "")
                for key in update_statement.keys():
                    output[key] = update_statement[key]

        return output
