import argparse

from transformers import (
    MODEL_MAPPING,
    SchedulerType,
)

# You should update this to your particular problem to have better documentation of `model_type`
MODEL_CONFIG_CLASSES = list(MODEL_MAPPING.keys())
MODEL_TYPES = tuple(conf.model_type for conf in MODEL_CONFIG_CLASSES)


def parse_args():
    '''
        config arguments for training
    '''
    arg_parser = argparse.ArgumentParser(description="BART")
    arg_parser.add_argument("--len_input", dest="len_input", type=str, default=None, help="set up prefix input",
                            choices=('no', 'topic', 'length', 'topic-length', 'length-topic', 'simple', 'simple-topic', 'topic-word', 'topic-simple', 'topic-last-length'))
    arg_parser.add_argument("--len_output", dest="len_output", default=None, help="set up prefix output", 
                            choices=('no', 'topic', 'length', 'topic-length', 'length-topic'))
    arg_parser.add_argument("--output_dir", dest="output_dir",
                            type=str, default="./output/1", help="default")
    arg_parser.add_argument("--train_file", dest="train_file", type=str,
                            default=None, help="A csv or a json file containing the training data.")
    arg_parser.add_argument("--validation_file", dest="validation_file", type=str,
                            default=None, help="A csv or a json file containing the validation data.")
    arg_parser.add_argument("--test_file", dest="test_file", type=str,
                            default=None, help="A csv or a json file containing the test data.")
    arg_parser.add_argument("--ignore_pad_token_for_loss", dest="ignore_pad_token_for_loss", type=bool, default=True,
                            help="Whether to ignore the tokens corresponding to " "padded labels in the loss computation or not.",)
    arg_parser.add_argument("--text_column", dest="text_column", type=str, default="dialogue",
                            help="The name of the column in the datasets containing the full texts (for summarization).")
    arg_parser.add_argument("--summary_column", dest="summary_column", type=str, default="summary",
                            help="The name of the column in the datasets containing the summaries (for summarization).")
    arg_parser.add_argument("--model_name_or_path", dest="model_name_or_path", type=str, default="facebook/bart-large",
                            help="Path to pretrained model or model identifier from huggingface.co/models.")
    arg_parser.add_argument("--model_type", dest="model_type", type=str, default="bart",
                            help="Model type to use if training from scratch.", choices=MODEL_TYPES)
    arg_parser.add_argument("--max_source_length", dest="max_source_length", 
                            type=int, default=1024, help="default")
    arg_parser.add_argument("--source_prefix", dest="source_prefix", type=str, default=None,
                            help="A prefix to add before every source text " "(useful for T5 models).")
    arg_parser.add_argument("--preprocessing_num_workers", type=int, default=None,
                            help="The number of processes to use for the preprocessing.")
    arg_parser.add_argument("--overwrite_cache", dest="overwrite_cache", type=bool,
                            default=None, help="Overwrite the cached training and evaluation sets")
    arg_parser.add_argument("--min_target_length", dest="min_target_length", type=int,
                            default=1, help="The minimal total sequence length for target text")
    arg_parser.add_argument("--max_target_length", dest="max_target_length", type=int, default=128, help="The maximum total sequence length for target text after "
                            "tokenization. Sequences longer than this will be truncated, sequences shorter will be padded."
                            "during ``evaluate`` and ``predict``.")
    arg_parser.add_argument("--num_beams", dest="num_beams", type=int, default=4, help="Number of beams to use for evaluation. This argument will be "
                            "passed to ``model.generate``, which is used during ``evaluate`` and ``predict``.")
    arg_parser.add_argument("--learning_rate", dest="learning_rate", type=float, default=5e-5,
                            help="Initial learning rate (after the potential warmup period) to use.")
    arg_parser.add_argument("--pad_to_max_length", action="store_true",
                            help="If passed, pad all samples to `max_length`. Otherwise, dynamic padding is used.",)
    arg_parser.add_argument("--weight_decay", dest="weight_decay",
                            type=float, default=1e-3, help="Weight decay to use.")
    arg_parser.add_argument("--label_smoothing", dest="label_smoothing",
                            type=float, default=0.1, help="hyperparameter for label smoothing.")
    arg_parser.add_argument("--length_penalty", dest="length_penalty", type=float,
                            default=1.0, help="large - longer sequence, small - shorter sequence")
    arg_parser.add_argument("--num_train_epochs", dest="num_train_epochs",
                            type=int, default=15, help="Total number of training epochs to perform.")
    arg_parser.add_argument("--per_device_train_batch_size", dest="per_device_train_batch_size",
                            type=int, default=8, help="Batch size (per device) for the training dataloader.")
    arg_parser.add_argument("--gradient_accumulation_steps", dest="gradient_accumulation_steps", type=int,
                            default=64, help="Number of updates steps to accumulate before performing a backward/update pass.")
    arg_parser.add_argument("--per_device_eval_batch_size", dest="per_device_eval_batch_size",
                            type=int, default=8, help="Batch size (per device) for the evaluation dataloader.")
    arg_parser.add_argument("--per_device_test_batch_size", dest="per_device_test_batch_size",
                            type=int, default=8, help="Batch size (per device) for the evaluation dataloader.")
    arg_parser.add_argument("--num_warmup_steps", dest="num_warmup_steps", type=int,
                            default=0, help="Number of steps for the warmup in the lr scheduler.")
    arg_parser.add_argument("--cache_dir", dest="cache_dir",
                            type=str, default="./output/cache", help="default")
    arg_parser.add_argument("--seed", dest="seed",
                            type=int, default=12345, help="default")
    arg_parser.add_argument("--config_name", type=str, default=None,
                            help="Pretrained config name or path if not the same as model_name")
    arg_parser.add_argument("--ctrlen_model", action='store_true', default=False, 
                            help="Use the ctrlen model or not",)
    arg_parser.add_argument("--tokenizer_name", type=str, default=None,
                            help="Pretrained tokenizer name or path if not the same as model_name")
    arg_parser.add_argument("--use_slow_tokenizer", dest="use_slow_tokenizer", action="store_true",
                            help="If passed, will use a slow tokenizer (not backed by the 🤗 Tokenizers library).")
    arg_parser.add_argument("--max_train_steps", type=int, default=None,
                            help="Total number of training steps to perform. If provided, overrides num_train_epochs.")
    arg_parser.add_argument("--lr_scheduler_type", type=SchedulerType, default="linear", help="The scheduler type to use.",
                            choices=["linear", "cosine", "cosine_with_restarts", "polynomial", "constant", "constant_with_warmup"])
    arg_parser.add_argument("--special_len_token_init", type=str, default=None,
                            help="ways to initialize special token for length (random, zero, token_embs)")
    arg_parser.add_argument("--embedding_lr", type=float, default=5e-5,
                            help="Initial learning rate for embedding layers.")
    arg_parser.add_argument("--len_start", type=int,
                            default=1, help="start length.")
    arg_parser.add_argument("--len_end", type=int,
                            default=100, help="end length.")
    arg_parser.add_argument("--data_aug", action='store_true', default=False,
                            help="whether to perform data augmentation or not")
    arg_parser.add_argument("--pred_len", action='store_true', default=False,
                            help="whether to use the golden length or predicted length")
    arg_parser.add_argument("--shuffle", action='store_true', default=False,
                            help="whether to shuffle the dataset to balance train/validation/test")
    arg_parser.add_argument("--topic_tagger", dest="topic_tagger", type=bool,
                            default=None, help="Use topic tag [TAG] or not")
    arg_parser.add_argument("--debug", action='store_true',
                            default=False, help="Use the debug mode or not")
    args = arg_parser.parse_args()

    # Sanity checks
    if args.train_file is None and args.validation_file is None:
        raise ValueError(
            "Need either a dataset name or a training/validation file.")
    else:
        if args.train_file is not None:
            extension = args.train_file.split(".")[-1]
            assert extension in [
                "csv", "json", "jsonl"], "`train_file` should be a csv or a json file."
        if args.validation_file is not None:
            extension = args.validation_file.split(".")[-1]
            assert extension in [
                "csv", "json", "jsonl"], "`validation_file` should be a csv or a json file."

    return args
