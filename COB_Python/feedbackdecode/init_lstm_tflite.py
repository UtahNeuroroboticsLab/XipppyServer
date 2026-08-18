import numpy as np

try:
    # Lightweight runtime normally used on the portable controller
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    # Development-computer fallback
    from tensorflow.lite import Interpreter


def init_lstm_tflite(SS, model_path, num_threads=2):
    """
    Load and initialize the TFLite model.

    Call this exactly once before entering the real-time loop.
    """

import os


def init_lstm_tflite(SS, model_path, num_threads=2):

    if not isinstance(model_path, (str, bytes, os.PathLike)):
        raise TypeError(
            "model_path must be a path string, not "
            + str(type(model_path))
        )

    model_path = os.path.abspath(
        os.path.expanduser(model_path)
    )

    print("TFLite model path:", model_path)

    if not os.path.isfile(model_path):
        raise FileNotFoundError(
            "TFLite model was not found: " + model_path
        )

    model_size = os.path.getsize(model_path)

    print("TFLite model size:", model_size, "bytes")

    if model_size == 0:
        raise ValueError(
            "TFLite model file is empty: " + model_path
        )

    # Read the model into ordinary RAM instead of asking TFLite
    # to mmap the model directly from the filesystem.
    with open(model_path, "rb") as model_file:
        model_content = model_file.read()

    # Standard TFLite files generally contain the TFL3 identifier
    # at bytes 4 through 7.
    if len(model_content) < 8:
        raise ValueError("Model file is too small to be a TFLite model")

    print("Model header:", model_content[:8])

    if model_content[4:8] != b"TFL3":
        raise ValueError(
            "The selected file does not appear to be a valid "
            "TFLite FlatBuffer. Header was: "
            + repr(model_content[:8])
        )

    interpreter = Interpreter(
        model_content=model_content,
        num_threads=num_threads
    )

    interpreter.allocate_tensors()

    # Keep an explicit reference to the bytes for the lifetime
    # of the interpreter.
    SS["lstm_model_content"] = model_content
    SS["lstm_interpreter"] = interpreter

    input_info = interpreter.get_input_details()[0]
    output_info = interpreter.get_output_details()[0]

    print("TFLite input details:", input_info)
    print("TFLite output details:", output_info)

    
    interpreter.allocate_tensors()

    input_info = interpreter.get_input_details()[0]
    output_info = interpreter.get_output_details()[0]

    input_shape = tuple(int(x) for x in input_info["shape"])
    output_shape = tuple(int(x) for x in output_info["shape"])
    batch_size, window_size, model_feature_count = input_shape
    SS['num_features'] = model_feature_count
    SS['sel_feat_idx'] = np.arange(SS['num_features'], dtype=int)
    print("TFLite input shape:", input_shape)
    print("TFLite input dtype:", input_info["dtype"])
    print("TFLite output shape:", output_shape)
    print("Selected feature count:", len(SS["sel_feat_idx"]))

    # This implementation assumes:
    # [batch, time, features]
    if len(input_shape) != 3:
        raise ValueError(
            f"Expected a 3-D LSTM input [batch, time, features], "
            f"but model input is {input_shape}"
        )

    

    if batch_size != 1:
        raise ValueError(
            f"Expected model batch size 1, but model uses {batch_size}"
        )

    selected_feature_count = len(SS["sel_feat_idx"])

    if selected_feature_count != model_feature_count:
        raise ValueError(
            "Feature dimension mismatch:\n"
            f"  Model expects: {model_feature_count}\n"
            f"  sel_feat_idx provides: {selected_feature_count}"
        )

    if input_info["dtype"] != np.float32:
        raise TypeError(
            f"This code expects a float32 model, but the model input "
            f"dtype is {input_info['dtype']}."
        )

    SS["lstm_interpreter"] = interpreter
    SS["lstm_input_info"] = input_info
    SS["lstm_output_info"] = output_info

    SS["lstm_window_size"] = window_size
    SS["lstm_feature_count"] = model_feature_count
  
    SS["lstm_samples_seen"] = 0

    # Rows are time samples; columns are features.
    SS["lstm_z_window"] = np.zeros(
        (window_size, model_feature_count),
        dtype=np.float32
    )

    # The final output dimension is normally the number of kinematic DOFs.
    SS["lstm_num_outputs"] = output_shape[-1]

    return SS