from datasets import load_dataset
import pandas as pd
import jsonlines

ds_orig = load_dataset("climate_fever", split='test')
df = ds_orig.to_pandas()

mv_label_dict = {0: 'SUPPORT', 1: 'CONTRADICT'}

docs = {}
doc_id = 0
indexed_evidence_sents = set()

counter = 0

with jsonlines.open('claims_comb_train.jsonl', 'w') as claims_train_writer, \
    jsonlines.open('claims_comb_test.jsonl', 'w') as claims_test_writer:
    for claim_row in df.to_dict('records'):
        counter += 1
        evidences = claim_row['evidences']
        cur_evidence_dict = {}
        cur_claim_doc_ids = set()
        for evidence in evidences:
            evidence_label = evidence['evidence_label']
            evidence_article = evidence['article']
            evidence_sent = evidence['evidence']
            if evidence_article in docs:
                doc = docs.get(evidence_article)
            else:
                doc = {"doc_id": doc_id,
                       "title": evidence_article,
                       "abstract": []}
                docs[evidence_article] = doc
                doc_id += 1
            cur_doc_id = doc["doc_id"]
            cur_claim_doc_ids.add(cur_doc_id)
            abstract = doc["abstract"]
            # Don't allow abstracts longer than 4096 otherwise longformer won't work
            # actually, somewhere down the line when training the abstracts get concatentated
            # so this number need to be lower no to cause errors
            if len(''.join(abstract).split()) > 2900:
                continue
            if not evidence_sent in indexed_evidence_sents:
                abstract.append(evidence_sent)
                indexed_evidence_sents.add(evidence_sent)
                sent_ind = len(abstract) - 1
            else:
                sent_ind = abstract.index(evidence_sent)

            # add only evidences to the documents that are not NEI
            if evidence_label != 2:
                curr_sent = {
                    "sentences": [sent_ind],
                    "label": mv_label_dict[evidence_label]
                }
                if f"{cur_doc_id}" in cur_evidence_dict:
                    exist_sents = cur_evidence_dict[f"{cur_doc_id}"]
                    for s in exist_sents:
                        if s['label'] == curr_sent['label']:
                            s['sentences'].append(sent_ind)
                else:
                    cur_evidence_dict[f"{cur_doc_id}"] = [curr_sent]

        claim_doc = {
            'id': int(claim_row['claim_id']),
            'claim': claim_row['claim'],
            'cited_doc_ids': list(cur_claim_doc_ids),
            'evidence': cur_evidence_dict
        }
        if counter % 4 == 0:
            claims_test_writer.write(claim_doc)
        else:
            claims_train_writer.write(claim_doc)


with jsonlines.open('corpus_comb_for_training.jsonl', 'w') as corpus_writer:
    for doc in docs.values():
        if doc["abstract"]:
            corpus_writer.write(doc)
