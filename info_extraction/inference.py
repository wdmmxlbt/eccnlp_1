import sys
sys.path.append('/data/pzy2022/project/eccnlp')


def extraction_inference(args, train_data, dev_data, test_data):
    from paddlenlp import Taskflow

    schema = ['业绩归因']
    my_ie = Taskflow("information_extraction", schema=schema, task_path = args.save_dir + '/model_best', position_prob = 0.2)

    if train_data is not None:    
        for data in train_data:
            result = my_ie(data['raw_text'])
            data['output'] = result

    if dev_data is not None:
        for data in dev_data:
            result = my_ie(data['raw_text'])
            data['output'] = result

    if test_data is not None:
        for data in test_data:
            result = my_ie(data['raw_text'])
            data['output'] = result
    
    return train_data, dev_data, test_data