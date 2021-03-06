# coding=utf-8
# Copyright 2018 The HuggingFace Inc. team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Convert BERT checkpoint."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import torch
from model.modeling_electra import ElectraConfig, ElectraForPreTraining
from model.modeling_electra import load_tf_weights_in_electra
import logging
logging.basicConfig(level=logging.INFO)

def convert_tf_checkpoint_to_pytorch(tf_checkpoint_path, electra_config_file, pytorch_dump_path):
    # Initialise PyTorch model
    config = ElectraConfig.from_pretrained(electra_config_file)
    # print("Building PyTorch model from configuration: {}".format(str(config)))
    model = ElectraForPreTraining(config)
    # Load weights from tf checkpoint
    load_tf_weights_in_electra(model, config, tf_checkpoint_path)

    # Save pytorch-model
    print("Save PyTorch model to {}".format(pytorch_dump_path))
    torch.save(model.state_dict(), pytorch_dump_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    ## Required parameters
    parser.add_argument("--tf_checkpoint_path",
                        default = "prev_trained_model/electra_small_tf",
                        type = str,
                        help = "Path to the TensorFlow checkpoint path.")
    parser.add_argument("--electra_config_file",
                        default = "prev_trained_model/electra_small_tf/config.json",
                        type = str,
                        help = "The config json file corresponding to the pre-trained BERT model. \n"
                            "This specifies the model architecture.")
    parser.add_argument("--pytorch_dump_path",
                        default = "prev_trained_model/electra_small/pytorch_model.bin",
                        type = str,
                        help = "Path to the output PyTorch model.")
    args = parser.parse_args()
    convert_tf_checkpoint_to_pytorch(args.tf_checkpoint_path,args.electra_config_file,
                                     args.pytorch_dump_path)

'''
python convert_electra_tf_checkpoint_to_pytorch.py \
    --tf_checkpoint_path=./prev_trained_model/electra_base_zh \
    --electra_config_file=./prev_trained_model/electra_base_zh/config.json \
    --pytorch_dump_path=./prev_trained_model/electra_base_zh/pytorch_model.bin
'''