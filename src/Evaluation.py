
baseline_dirs = []
subdirs = []


relevant_docs_dic = {}

def get_relevant_docs():
    
    global relevant_docs_dic
    
    with open('./test_collection/cacm.rel.txt', 'r+') as rel_file:
        line_data = rel_file.read().split('\n') 
        
        for line in line_data:
            parts = line.split(' ')
            query_id = parts[0]
            rel_doc_name = parts[1]
            
            if query_id not in relevant_docs_dic.keys():
                relevant_docs_dic[query_id] = [rel_doc_name]
            else:
                doc_list = relevant_docs_dic[query_id]
                doc_list.append(rel_doc_name)
                relevant_docs_dic.update(doc_list)
    
    
    print(relevant_docs_dic)
    
get_relevant_docs()