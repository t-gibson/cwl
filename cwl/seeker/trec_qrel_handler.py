from cwl.seeker.common_helpers import file_exists
from cwl.seeker.common_helpers import AutoVivification
from cwl.seeker.topic_document_file_handler import TopicDocumentFileHandler


class TrecQrelHandler(TopicDocumentFileHandler):

    def __init__(self, filename=None):
        super(TrecQrelHandler, self).__init__(filename)

    def _put_in_line(self, line):
        """
        For TREC QREL the Format is:
            Topic Iteration Document Judgement
            Iteration is not used.
        """
        parts = line.split()
        topic = parts[0]
        doc = parts[2].strip()
        judgement = parts[3].strip()
        self.put_value(topic, doc, judgement)

    def _get_out_line(self, topic, doc):
        # outputs the topic document and value as the TREC QREL Format with iteration default to zero
        return "%s 0 %s %d\n" % (topic, doc, self.data[topic][doc])

    def validate_gains(self, min_gain=0.0, max_gain=1.0):
        """
        Iterates all gains and checks to ensure they are below the value of
        max_gain. 
        """
        all_gains = self.get_topic_doc_dict()
        for topic_id in all_gains:
            for gain in all_gains[topic_id].values():
                if gain > max_gain:
                    raise ValueError(f"Detected a gain value ({gain})  greater than the maximum ({max_gain}).\n"
                                     "Please check your input gain file")
                if gain < min_gain:
                    raise ValueError(f"Detected a gain value ({gain}) less than minimum ({min_gain}).\n "
                                     "Please check your input gain file.")
 
    def get_total_gains(self, topic):

        doc_list = self.get_doc_list(topic)
        gain = 0.0
        for doc in doc_list:
            gain += self.get_value(topic, doc)
        return gain

    def get_total_rels(self, topic):
        doc_list = self.get_doc_list(topic)
        rels = 0.0
        for doc in doc_list:
            if self.get_value(topic, doc) > 0.0:
                rels += 1.0
        return rels
