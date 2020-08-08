class DataHandler:
    '''
    An example template for creating a custom DataHandler.


    A tuple of arrays should be returned (in this order) containing the following:

    sent:
        The full text of the problem description
    shortest_path:
        The words comprising the shortest path between the source and target entities
    src_txt
        The text of the source entity
    tgt_txt:
        The text of the target entity
    src_vec
        The cui2vec vector for the source entity
    tgt_vec,
        The cui2vec vector for the target entity
    src_sem_type,
        The semantic type of the source entity
    tgt_sem_type,
        The semantic type of the target entity
    src_sem_type_group:
        The semantic type group of the source entity
    tgt_sem_type_group
        The semantic type group of the target entity
    y:
        Class labels

    Note only `get_data_data` and `get_validation_data` should return the class labels.
    'get_training_data' does not require labels, allowing users to use unlabled data for training.

    see 'umls/SemGroups_2018.txt' for semantic type/group names

    '''
    def get_test_data(self):
        pass

    def get_validation_data(self):
        pass

    def get_training_data(self):
        pass