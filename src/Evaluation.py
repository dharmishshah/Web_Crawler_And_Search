import os
import matplotlib.pyplot as plt


baseline_dirs = ['bm_25', 'jm_query_likelihood', 'tf_idf', 'prf', 'lucene']
subdirs = ['', 'stemmed', 'stopped']

pr_dir = 'precision_and_recall'

relevant_docs_dic = {}



def get_relevant_docs():
    
    global relevant_docs_dic
    
    with open('./test_collection/cacm.rel.txt', 'r+') as rel_file:
        line_data = rel_file.read().split('\n') 
        
        for line in line_data:
            if(len(line) == 0):
                continue
            parts = line.split(' ')
            query_id = parts[0]
            
            rel_doc_name = parts[2]
            
            if query_id not in relevant_docs_dic.keys():
                relevant_docs_dic[query_id] = [rel_doc_name]
            else:
                doc_list = relevant_docs_dic[query_id]
                doc_list.append(rel_doc_name)
                relevant_docs_dic.update({query_id : doc_list})
    
    

def evaluate_docs():
    
    get_relevant_docs()
    
    dirs_to_traverse = []
    for d in baseline_dirs:
        if d == 'prf' or d == 'lucene':
            dirs_to_traverse.append(d + '/')
        else:
            for s in subdirs:
                if s == '':
                    dirs_to_traverse.append(d + '/')
                else:
                    dirs_to_traverse.append(d + '_' + s + '/')
    
    for d in dirs_to_traverse:
        
        print(d)
        
        avg_precision_points = []
        avg_recall_points = []
        
        precision_dict = {}
        recall_dict = {} 
        mrr = {}
        
        for query_id in relevant_docs_dic.keys():
            
            rel_docs = relevant_docs_dic[query_id] 
            
            for direc in os.walk(os.getcwd() + '/results/' +d):
                for files in direc:
                    file_total = files
                    
            # /2 because 1.txt and 1_snippet.txt
            if(int(query_id) > (len(file_total)) / 2) and 'prf' not in d:
                break
            
            with open(os.getcwd() + '/results/' +d + str(query_id) + '.txt', 'r+', encoding='UTF-8') as f:
                
                lines = f.read().split('\n')
                
                relevant = len(rel_docs)
                retrieved = 0
                relevant_and_retrieved = 0
                
                doc_precision = {}
                doc_recall = {}
                
                # will traverse through top 100 records
                for l in lines:
                    
                    if(len(l) == 0):
                        continue
                    
                    doc_name = l.split(' ')[2]
                    
                    retrieved += 1
                    if doc_name in rel_docs:
                        # first discovered document
                        if query_id not in mrr:
                            mrr[query_id] = 1 / retrieved
                        relevant_and_retrieved += 1
                        
                    doc_precision[doc_name] = round((relevant_and_retrieved / retrieved), 3) 
                    doc_recall[doc_name] = round((relevant_and_retrieved / relevant), 3)
        
                precision_dict[query_id] = doc_precision
                recall_dict[query_id] = doc_recall
    
        write_precision_and_recall_values(precision_dict, recall_dict, d)
            
        p_at_5 = {}
        p_at_20 = {}
        
        for q_id in precision_dict.keys():
            doc_count = 0
            for doc_name in precision_dict[q_id]:
                doc_count += 1
                
                if doc_count == 5:
                    p_at_5[q_id] = precision_dict[q_id][doc_name]
                elif doc_count == 20:
                    p_at_20[q_id] = precision_dict[q_id][doc_name]
        
        write_p_at_k(p_at_5, p_at_20, d)
        
        prec_sum = 0.0
        for query_id in precision_dict:
            num = 0.0
            doc_prec_dic = precision_dict[query_id]
            for doc_id in doc_prec_dic:
                num += doc_prec_dic[doc_id]
                
            avg_precision = 0.0
            if len(doc_prec_dic) > 0:
                avg_precision = num / len(doc_prec_dic)
            
            avg_precision_points.append(avg_precision)
                
            prec_sum += avg_precision
        
            
        map_val = prec_sum / len(precision_dict)


        for query_id in recall_dict:
            num = 0.0
            doc_prec_dic = recall_dict[query_id]
            for doc_id in doc_prec_dic:
                num += doc_prec_dic[doc_id]
                
            avg_recall = 0.0
            if len(doc_prec_dic) > 0:
                avg_recall = num / len(doc_prec_dic)
            
            avg_recall_points.append(avg_recall)
                
            prec_sum += avg_precision


        x = d.split('/')
        plt.plot(avg_recall_points,avg_precision_points, label = x[0])

        prec_sum = 0.0
        # calculate mrr
        for rank in mrr:
            prec_sum += mrr[rank]

        mrr_val = prec_sum / len(precision_dict)
        
        MAP_MRR_str = "MAP : " + str(map_val) + "\n"
        MAP_MRR_str += "MRR : " + str(mrr_val) + "\n"
        
        with open(os.getcwd() + '/evaluation/' + d + 'map_mrr.txt', 'w+') as f:
            f.write(MAP_MRR_str)
    
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    
    plt.legend()
    plt.show()
        
def write_precision_and_recall_values(precision_dict, recall_dict, run_type):
    # recall_and_precison have same number of keys
    for q_id in recall_dict.keys():
        
        # get all docs
        doc_list = recall_dict[q_id].keys()    
        
        
        x = os.getcwd() + '/evaluation' + '/' + run_type+ pr_dir
        if not os.path.exists(x):
            os.makedirs(x)
                
        with open( x+'/' + str(q_id) + '.txt', 'w+') as f:
            
            f.write('Doc_name\tPrecision\tRecall\n')
            for doc_name in doc_list:
                f.write(doc_name + '\t')
                f.write(str(precision_dict[q_id][doc_name]) + '\t\t')
                f.write(str(recall_dict[q_id][doc_name]) + '\n')
                        

def write_p_at_k(p_at_5, p_at_20, run_type):
    
    x = os.getcwd() + '/evaluation' + '/' + run_type
    
    with open(x +'p_at_5.txt', 'w+') as f:
        f.write('query' + '\t' + 'p@5' + '\n')
        for q_id in p_at_5.keys():
            f.write(q_id + '\t' + str(p_at_5[q_id]) + '\n')
            
    with open(x +'p_at_20.txt', 'w+') as f:
        f.write('query' + '\t' + 'p@5' + '\n')
        for q_id in p_at_20.keys():
            f.write(q_id + '\t' + str(p_at_20[q_id]) + '\n')
            