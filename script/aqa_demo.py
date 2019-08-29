import argparse
import importlib
import os
import sys

root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, os.path.join(root_path, 'active-qa'))

reformulator = importlib.import_module('px.nmt.reformulator')
reformulator_pb2 = importlib.import_module('px.proto.reformulator_pb2')


def main(config_path, model_path):
    reformulator_instance = reformulator.Reformulator(
        hparams_path=config_path,
        source_prefix='<en> <2en> ',
        out_dir=model_path,
        environment_server_address='')

    while True:
        question = input("Input a question: ")
        responses = reformulator_instance.reformulate(questions=[question],
                                                      inference_mode=reformulator_pb2.ReformulatorRequest.BEAM_SEARCH)

        print("\nTop 20 rewrites:")
        for j, rewrite in enumerate(responses[0]):
            print(f"{j + 1}. {rewrite.reformulation}")
        print()
        print('=' * 100)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path")
    parser.add_argument("--model_path")

    args = parser.parse_args()

    main(args.config_path, args.model_path)
