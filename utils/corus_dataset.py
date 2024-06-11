from torch.utils.data import IterableDataset, DataLoader
import subprocess
import os
import nltk
nltk.download('punkt')


class CorusDataset(IterableDataset):
    def __init__(self, load_func, corpus_url, segments_per_doc,
                 ret_titles=False, max_docs_count=None):
        # save args
        self.__dict__.update(locals())
        del self.__dict__["self"]

        self.corpus_path = os.path.basename(
            corpus_url)  # wget saves to current dir
        self.sentence_tokenizer = nltk.data.load(
            'tokenizers/punkt/russian.pickle')

        # cmd = ['wget', '-nc', '-nv', corpus_url]
        cmd = ['curl', '-O', corpus_url]
        out = subprocess.run(
            cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if out.returncode != 0:
            print("Error while loading file:")
            print(out.stdout)
        # else:
        #     print(f"Sucessfully loaded corus dataset: '{self.corpus_path}'")

    def generate_doc(self):
        records = self.load_func(self.corpus_path)

        # corpus = ''
        true_seg_bounds = []
        doc_sentences = []
        titles = []

        total_records = self.segments_per_doc

        docs_count = 0
        is_last_record = False
        while not is_last_record:
            rec = next(records)
            segment_count = 1
            while True:
                segment_sentences = self.sentence_tokenizer.tokenize(rec.text)
                doc_sentences.extend(segment_sentences)
                if self.ret_titles:
                    titles.append(rec.title)

                # update true segment bounds
                for _ in range(len(segment_sentences)-1):
                    true_seg_bounds.append(0)

                segment_count += 1
                # if current record is not last
                try:
                    rec = next(records)
                    if (segment_count + 1) % self.segments_per_doc == 0:
                        true_seg_bounds.append(0)
                        output = [
                            doc_sentences,
                            true_seg_bounds,
                            docs_count  # as id
                        ]

                        # if self.ret_titles:
                        #     output.append(titles)

                        docs_count += 1

                        if docs_count is not None and docs_count == self.max_docs_count:
                            is_last_record = True

                        true_seg_bounds = []
                        doc_sentences = []
                        # titles = []
                        break
                    else:
                        # corpus += '\n\n'
                        true_seg_bounds.append(1)
                except StopIteration:
                    is_last_record = True
                    break

            yield output

    def configure_iterator(self, ret_titles):
        self.ret_titles = ret_titles

    def __iter__(self):
        doc_generator = self.generate_doc()
        return iter(doc_generator)
