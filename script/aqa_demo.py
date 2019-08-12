from px.nmt import reformulator
from px.proto import reformulator_pb2

# questions = ['Is there a validity period to be a Baby Bonus Approved Institution?',
#              'Who can apply to be a Baby Bonus Approved Institution?']

reformulator_instance = reformulator.Reformulator(
    hparams_path='config/aqa.json',
    source_prefix='<en> <2en> ',
    out_dir='model/pretrained/active-qa/translate.ckpt-1460356',
    environment_server_address='')

while True:
    question = input("Input a question: ")
    responses = reformulator_instance.reformulate(questions=[question],
                                                  inference_mode=reformulator_pb2.ReformulatorRequest.BEAM_SEARCH)

    print(f"Rewrites of \"{question}\":\n")
    for j, rewrite in enumerate(responses[0]):
        print(f"{j + 1}. {rewrite.reformulation}")
    print()
    print('=' * 100)
