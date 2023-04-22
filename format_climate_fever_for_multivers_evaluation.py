from datasets import load_dataset
import pandas as pd
import jsonlines

ds_orig = load_dataset("climate_fever", split='test')
df = ds_orig.to_pandas()

mv_label_dict = {0: 'SUPPORT', 1: 'CONTRADICT'}

docs = {}
doc_id = 0
indexed_evidence_sents = set()

with jsonlines.open('claims_comb.jsonl', 'w') as claims_writer:
    for claim_row in df.to_dict('records'):
        evidences = claim_row['evidences']
        cur_evidence_dict = {}
        cur_claim_doc_ids = set()
        for evidence in evidences:
            evidence_label = evidence['evidence_label']
            # add only sentences to the documents that are not NEI
            if evidence_label != 2:
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
                if not evidence_sent in indexed_evidence_sents:
                    abstract.append(evidence_sent)
                    indexed_evidence_sents.add(evidence_sent)
                    sent_ind = len(abstract) - 1
                else:
                    sent_ind = abstract.index(evidence_sent)


                curr_sent = {
                    "sentences": [sent_ind],
                    "label": mv_label_dict[evidence_label]
                }
                if f"{cur_doc_id}" in cur_evidence_dict:
                    exist_sents = cur_evidence_dict[f"{cur_doc_id}"]
                    appended = False
                    for s in exist_sents:
                        if s['label'] == curr_sent['label']:
                            s['sentences'].append(sent_ind)
                            appended = True
                    if not appended:
                        exist_sents.append(curr_sent)                    
                else:
                    cur_evidence_dict[f"{cur_doc_id}"] = [curr_sent]

        claim_doc = {
            'id': int(claim_row['claim_id']),
            'claim': claim_row['claim'],
            'doc_ids': list(cur_claim_doc_ids),
            'evidence': cur_evidence_dict
        }
        claims_writer.write(claim_doc)


with jsonlines.open('corpus_comb.jsonl', 'w') as corpus_writer:
    for doc in docs.values():
        if doc["abstract"]:
            corpus_writer.write(doc)
