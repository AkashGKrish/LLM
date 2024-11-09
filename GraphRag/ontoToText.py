def get_ontology_data(ontology_graph):

    """
    Retrieves and organizes data from an ontology graph.

    This function takes an ontology graph as input, extracts its unique subjects, 
    and then retrieves the predicates and objects associated with each subject. 
    The data is then organized into a list of string chunks, where each chunk 
    represents a subject and its corresponding objects and predicates.

    Args:
        ontology_graph: The input ontology graph.

    Returns:
        A list of string chunks, where each chunk represents a subject and its 
        corresponding objects and predicates.
    """

    # Get unique subjects
    unique_subjects = set(ontology_graph.subjects(unique=True))

    # Initialize empty dictionary to store subjects, predicates, and objects
    subjects_with_predicates_objects = {}

    # Iterate through each unique subject
    for subject in unique_subjects:
        # Get all predicates and objects for the current subject
        predicates_objects = list(ontology_graph.triples((subject, None, None)))

        # Store the subject, predicates, and objects
        subjects_with_predicates_objects[subject] = predicates_objects

    # Create a list to store the output strings
    concept_chunks = []

    # Write each subject's data
    for subject in sorted(unique_subjects):
        concept_chunk = f"\nSubject: {subject}\nObjects and Predicates:\n"
        for predicate_object in sorted(subjects_with_predicates_objects[subject]):
            s, p, o = predicate_object
            concept_chunk += f"- Predicate: {p}, Object: {o}\n"
            
        # Add description of the knowledge chunk in simple language
        concept_chunk+="Description:\n"+get_description(concept_chunk)

        concept_chunks.append(concept_chunk)
    return concept_chunks





def get_description(concept_chunk):
    """
    This function generates a description string based on a given subject and a list of 
    object-predicate pairs. It extracts the real subject, real predicates, and real objects 
    from the input, which are provided in a specific format, and formats them into readable 
    sentences.

    Parameters:
    concept_chunk(list): A list containing a chunk of knowledge graph.

    Returns:
    str: A string that contains the description of the subject performing actions (predicates) on objects.
    """
    subject_and_OP = concept_chunk.split('\nObjects and Predicates:\n')
    # Step 1: Extract and clean up the subject.
    real_subject = subject_and_OP[0]           # Get the subject from the first part of input.
    subject_split = real_subject.split("/")    # Split by "/" to isolate the real subject.
    subject = subject_split[-1]                # Use the last part as the actual subject.

    # Step 2: Clean and process the predicate-object part of the input.
    subject_and_OP[1] = subject_and_OP[1][2:]  # Remove the first two characters (usually '- ').
    subject_and_OP[1] = subject_and_OP[1].replace("\n", "")  # Remove any newline characters.
    objects_and_predicates = subject_and_OP[1].split('- ')   # Split predicates and objects by '- '.

    objects = []   # To store the objects.
    predicates = []   # To store the predicates.

    # Step 3: Loop through the predicates and objects and process each pair.
    for i in objects_and_predicates:
        split_predicate_and_object = i.split(',')   # Split each pair by ',' (first part is predicate, second is object).
        
        predicate = split_predicate_and_object[0]   # Get the predicate (action).
        predicate_split = predicate.split("/")      # Split the predicate by "/" to get the real predicate.
        real_predicate = predicate_split[-1]        # Use the last part as the actual predicate.
        real_predicate = real_predicate.replace('#', ' ')
        real_predicate = ' '.join(word.capitalize() for word in real_predicate.split())

        object = split_predicate_and_object[1]      # Get the object (target of the action).
        object_split = object.split("/")            # Split the object by "/" to get the real object.
        real_object = object_split[-1]              # Use the last part as the actual object.
        
        predicates.append(real_predicate)           # Add the real predicate to the list.
        objects.append(real_object)                 # Add the real object to the list.

    # Step 4: Generate the description.
    length = len(objects)    # Get the number of objects (equal to the number of predicates).
    description = ''         # Initialize an empty string to store the final description.

    # Combine subject, predicate, and object into readable sentences.
    for i in range(0, length):
        description += f"{subject} {predicates[i]} {objects[i]}\n"   # Format: "subject predicate object".
    
    return description    # Return the formatted description.





