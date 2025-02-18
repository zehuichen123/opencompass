from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import ZeroRetriever
from opencompass.openicl.icl_inferencer import GenInferencer
from opencompass.openicl.icl_evaluator import LMEvaluator
from opencompass.datasets import AlignmentBenchDataset
from mmengine.config import read_base

subjective_reader_cfg = dict(
    input_columns=['question', 'capability', 'prefix', 'suffix'],
    output_column='judge',
    )

subjective_all_sets = [
    "alignment_bench",
]
data_path ="data/subjective/alignment_bench"

alignment_bench_config_path = "data/subjective/alignment_bench/"
alignment_bench_config_name = 'config/multi-dimension'

subjective_datasets = []

for _name in subjective_all_sets:
    subjective_infer_cfg = dict(
            prompt_template=dict(
                type=PromptTemplate,
                template=dict(round=[
                    dict(
                        role='HUMAN',
                        prompt="{question}"
                    ),
                ]),
            ),
            retriever=dict(type=ZeroRetriever),
            inferencer=dict(type=GenInferencer, max_out_len=1024),
        )

    subjective_eval_cfg = dict(
        evaluator=dict(
            type=LMEvaluator,
            prompt_template=dict(
                type=PromptTemplate,
                template=dict(round=[
                    dict(
                        role='HUMAN',
                        prompt = "{prefix}[助手的答案开始]\n{prediction}\n[助手的答案结束]\n"
                    ),
                ]),
            ),
        ),
        pred_role="BOT",
    )

    subjective_datasets.append(
        dict(
            abbr=f"{_name}",
            type=AlignmentBenchDataset,
            path=data_path,
            name=_name,
            alignment_bench_config_path=alignment_bench_config_path,
            alignment_bench_config_name=alignment_bench_config_name,
            reader_cfg=subjective_reader_cfg,
            infer_cfg=subjective_infer_cfg,
            eval_cfg=subjective_eval_cfg
        ))
