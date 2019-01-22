from __future__ import print_function

import argparse, os
from datetime import datetime
from keras.models import Sequential, load_model
from keras.layers import Dense, Flatten
from tensorflow.python.lib.io import file_io


#export
from tensorflow import saved_model
from keras import backend as K

from data_loader import get_games, save_last_training


def get_model(model_path):
    if file_io.file_exists(model_path):
        with file_io.FileIO(model_path, mode='r') as input_f:
            with file_io.FileIO("model.h5", mode='w+') as output_f:
                output_f.write(input_f.read())

        return load_model("model.h5")
    else:
        print("Building new model")
        model = Sequential([
            Dense(9, activation='relu',input_shape=(9,)),
            Dense(64, activation='relu'),
            Dense(64, activation='relu'),
            Dense(9, activation='softmax')
        ])

        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])

        return model


def get_ds_identity(identity_path):
    if file_io.file_exists(identity_path):
        with file_io.FileIO(identity_path, mode='r') as input_f:
            with file_io.FileIO("ds_identity.json", mode='w+') as output_f:
                output_f.write(input_f.read())


def train_model(job_dir=".", model_path="./model.h5", identity_path="identity.json", **args):
    logs_path = job_dir + '/logs/' + datetime.now().isoformat()
    print('Using logs_path located at {}'.format(logs_path))

    get_ds_identity(identity_path)

    x_train, y_train, x_test, y_test = get_games()

    print("X TRAIN: {}".format(x_train[2]))
    print("Y TRAIN: {}".format(y_train[2]))
    print("X TEST: {}".format(x_test[2]))
    print("Y TEST: {}".format(y_test[2]))

    if len(x_train) == 0 or len(y_train) == 0:
        print("No new data to train on")
        exit(0)

    print("Initializing model...")
    model = get_model(model_path)

    model.fit(x_train, y_train, epochs=20)

    test_loss, test_acc = model.evaluate(x_test, y_test)
    print("ACC: {} LOSS: {}".format(test_acc, test_loss))

    model.save("model.h5")

    # Save the model to the Cloud Storage bucket's jobs directory
    with file_io.FileIO("model.h5", mode='r') as input_f:
        with file_io.FileIO(model_path, mode='w+') as output_f:
            output_f.write(input_f.read())

    #export model
    model_builder = saved_model.builder.SavedModelBuilder("exported_model")
    inputs = {
        'input': saved_model.utils.build_tensor_info(model.input)
    }
    outputs = {
        'output': saved_model.utils.build_tensor_info(model.output)
    }
    signature_def = saved_model.signature_def_utils.build_signature_def(
        inputs=inputs,
        outputs=outputs,
        method_name=saved_model.signature_constants.PREDICT_METHOD_NAME
    )
    model_builder.add_meta_graph_and_variables(
        K.get_session(),
        tags=[saved_model.tag_constants.SERVING],
        signature_def_map={saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY: signature_def
                           })
    model_builder.save()

    #exported model upload
    model_files = os.listdir("./exported_model/variables")

    # Save the model to the Cloud Storage bucket's jobs directory
    with file_io.FileIO('exported_model/saved_model.pb', mode='r') as input_f:
        with file_io.FileIO(job_dir + '/saved_model.pb', mode='w+') as output_f:
            output_f.write(input_f.read())

    for mf in model_files:
        with file_io.FileIO('exported_model/variables/' + mf, mode='r') as input_f:
            with file_io.FileIO(job_dir + '/variables/' + mf, mode='w+') as output_f:
                output_f.write(input_f.read())

    save_last_training()


if __name__ == '__main__':
    # Parse the input arguments for common Cloud ML Engine options
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--job-dir',
        help='Location of the result of the training')
    parser.add_argument(
        '--model_path',
        help='Location of the current model')
    parser.add_argument(
        '--identity_path',
        help='Location of service account json to access DataStore')
    args = parser.parse_args()
    arguments = args.__dict__
    print("Arguments: {}".format(arguments))
    train_model(**arguments)
