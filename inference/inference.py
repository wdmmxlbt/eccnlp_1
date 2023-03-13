import os
import config
args = config.get_arguments()

if args.device[-1].isdigit():
    os.environ['CUDA_VISIBLE_DEVICES'] = args.device[-1]
else:
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import sys
# sys.path.append('/data/pzy2022/project/eccnlp')
sys.path.append('/data/fkj2023/Project/eccnlp')
# sys.path.append('/data/fkj2023/Project/eccnlp/inference')
# sys.path.append('../')
from config import re_filter
from utils import read_list_file, split_dataset, evaluate_sentence, read_word, print_list, check_log_dir, get_res_logger
from data_process.dataprocess import train_dataset, split_dataset, classification_dataset, dict_to_list

import logging

from item_classification.bert_inference import bertForSequenceClassification

from item_classification.classification_model_predict import classification_models_predict

from info_extraction.inference import extraction_inference

# from data_process.info_extraction import dataset_generate_train

from phrase_rerank.rank_data_process import get_logger1,  form_predict_input_list, add_embedding, get_text_list, merge_reasons
from phrase_rerank.lambdarank import LambdaRank, add_rerank, predict
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(module)s[line:%(lineno)d]: >> %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def bertFilter(args, dataset):
    filtedDataset = bertForSequenceClassification(args, dataset)

    return filtedDataset

def classification(args, dataset):
    predict_list = dict_to_list(dataset)
    predict_all = classification_models_predict(predict_list, args)
    logging.info(f'all predict dict nums:{len(predict_all)}')

    for i in range(len(predict_all)):
        dataset[i]['label'] = predict_all[i]


    # with open("./data/result_data/3.1_result_dict_DoubleEnsemble0309.txt", 'w', encoding='utf8') as f:
    #     for i in range(len(dataset)):
    #         f.write(str(dataset[i]) + '\n')

    return dataset

def extraction(args, dataset):
    _, _, result = extraction_inference(args, None, None, dataset)
    return result

def rerank_predict(args, uie_list, log):

    word = read_word(args.word_path)
    after_embedding_list = add_embedding(args, uie_list)
    text_list, num_list = get_text_list(uie_list)
    merged_list = merge_reasons(args, text_list, num_list, after_embedding_list)
    predict_list, reasons = form_predict_input_list(args, merged_list, word)
    predict_data = np.array(predict_list)
    predicted_list, rerank_reasons, rerank_scores = predict(args, predict_data, reasons)
    res = add_rerank(args, rerank_reasons,rerank_scores, merged_list, log)
    return res



if __name__ == '__main__':
    args = config.get_arguments()

    log_path = check_log_dir(args.time) 
    # print(log_path)
    # exit(0)

    inference_logger = get_res_logger('inference_logger', log_path + '/inference.log')    
    # read predict data...
    # predict_dataset = read_list_file(args.predict_data)
    # logging.info(f'length of raw dataset: {len(predict_dataset)}')

    # # waiting for re filter...
    # dataset = re_filter(predict_dataset)
    # logging.info(f'{len(predict_dataset) - len(dataset)} samples are filted by re_filter')
    # logging.info(f'all dataset dict nums:{len(dataset)}')
    
    # dataset = classification(args, dataset)
    # logging.info('double ensemble predict completed.')


    dataset = read_list_file(args.data)
    # dataset = read_list_file('/data/xf2022/Projects/eccnlp_local/data/result_data/3.1_result_dict_predict20.46.txt')

    logging.info(f'length of raw dataset: {len(dataset)}')

    # dataset = re_filter(dataset)

    filtedDataset = bertFilter(args, dataset)
    filtedDataset_logger = get_res_logger('filtedDataset', log_path + '/filtedDataset.log')
    print_list(filtedDataset, filtedDataset_logger)
    
    # train_data, dev_data, test_data = dataset_generate_train(args, dataset)
    # logging.info(f'{len(dataset)} samples left after re_filter')
    
    result = extraction(args, filtedDataset)
    # with open("./after_extraction_data3.1DoubleEnsemble.txt", 'w') as f:
    #     [f.write(str(data) + '\n') for data in result]
    # # evaluate_sentence(result, clf)


    # phrase_rerank

    # filepath = '/data/fkj2023/Project/eccnlp_local/phrase_rerank/info_extraction_result_1222.txt'
    # uie_list = read_list_file(filepath)
    # rerank_res = rerank_predict(args, uie_list)
    rerank_res = rerank_predict(args, result, inference_logger)


